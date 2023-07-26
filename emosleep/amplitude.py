import numpy as np
import xarray as xr


def compute_amplitude(data, tmin=None, tmax=None, 
                      sfreq=None, fmin=None, fmax=None):
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