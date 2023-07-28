import numpy as np
import xarray as xr


def compute_amplitude(data, tmin=None, tmax=None,
                      sfreq=None, fmin=None, fmax=None):
    """Compute the amplitude of a given signal.

    Args:
        data (instance of numpy.ndarray|xarray.DataArray): The array
            containing the data, it should be of shape (trials, roi, times)
            (and include the conditions on the trials dim if DataArray).
        tmin (float|None, optional): Starting time point in seconds.
            If None and data is a DataArray it will be inferred on time dim.
            Defaults to None.
        tmax (float|None, optional): Ending time point in seconds. If None and
            data is a DataArray it will be inferred on time dim.
            Defaults to None.
        sfreq (float|None, optional): Sampling frequency. If None it will be
            inferred using tmin and tmax. Defaults to None.
        fmin (float|None, optional): Minimal frequency to consider to
            compute the amplitude. If None fmin=0. Defaults to None.
        fmax (float|None, optional): Maximal frequency to consider to compute
            the ampitude. If None fmax=sfreq/2. Defaults to None.

    Returns:
        amplitudes (instancee of xarray.DataArray): DataArray of shape 
            (roi, frequencies, trials)
    """
    
    # data are in (roi, times, trials)
    
    if tmin is None:
        tmin = data.time.min().values
    if tmax is None:
        tmax = data.time.max().values
    if sfreq is None:
        sfreq = len(data.time) // (tmax - tmin)
    
    samples = int(((tmax - tmin) * sfreq).round())
    f_trans = np.fft.fft(data.values, axis=1)
    amplitudes = 2 / samples * np.absolute(f_trans)
    frequencies = np.fft.fftfreq(samples) * samples * 1 / (tmax - tmin)
    
    amplitudes = amplitudes[:, :amplitudes.shape[1] // 2, :]
    frequencies = frequencies[:len(frequencies) // 2]
    
    amplitudes = xr.DataArray(amplitudes,
                              coords=[data.roi, frequencies, data.trials],
                              dims=['roi', 'freq', 'trials'])
    
    if isinstance(data, xr.DataArray):
        amplitudes = amplitudes.assign_coords(condition=('trials',
                                                         data.condition.data))
    
    if fmin is None:
        fmin = frequencies[0]
    if fmax is None:
        fmax = frequencies[-1]
        
    amplitudes = amplitudes.sel({'freq': slice(fmin, fmax)})
    
    return amplitudes


if __name__ == '__main__':

    data_fname = '/media/jerry/ruggero/EmoSleep/mne/ltc/label_tc.nc'
    
    data = xr.load_dataarray(data_fname)

    compute_amplitude(data, fmin=.5, fmax=4.)