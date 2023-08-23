import mne
import numpy as np
from emosleep.io import open_matfile
from emosleep.utils import write_bad_trials, read_bad_trials


def create_epochs(mat_fname, mont_fname, eve_fname, epo_fname,
                  sfreq=500., tmin=-.5, ev_id=None):
    """Create epochs from the mat file (sw_prp/signal), it needs the events 
        file and the montage file to be generated first.

    Args:
        mat_fname (path_like): Path to the mat file.
        mont_fname (path_like): Path to the DigMont file.
        eve_fname (path_like): Path to the event file.
        epo_fname (path_like): Path were the Epochs file will be saved.
        sfreq (float, optional): Sampling frequency (in Hz). Defaults to 500..
        tmin (float, optional): Starting time point in seconds.
            Defaults to -.5.
        ev_id (dict|None, optional): Dictionary containing the description of
            the events contained in the events file. Defaults to None.

    Returns:
        epochs (instance of mne.Epochs): Epochs object containing all the 
            relative informations and the data in the form of a 3D matrix of 
            shape (trials, channels, times).
    """
    # Retrieving data
    mat = open_matfile(mat_fname)
    data = mat['sw_prp']['signal'][0, 0]  # (ch, tp, tr)
    data = np.transpose(data, axes=[2, 0, 1])
    
    # Retrieving montage
    digi_mont = mne.channels.read_dig_fif(mont_fname)
    # Retrieving events
    events = mne.read_events(eve_fname)
    # Building infos
    ch_names = digi_mont.ch_names
    info = mne.create_info(ch_names, sfreq, ch_types='eeg')
    # Building epochs
    epochs = mne.EpochsArray(data, info, events=events, 
                             tmin=tmin, event_id=ev_id)
    epochs.set_montage(digi_mont)
    # Detecting bad trials
    zeros = np.where(events[:, -1] == 0)[0]
    # Detecting nans
    nans = np.where(np.isnan(data).sum(-1).sum(-1) > 0.)[0]
    bad_trials = np.sort(np.hstack((zeros, nans)))
    # Dropping bads and nans
    epochs.drop(bad_trials, reason='bad or nans')
    # Save baseline epochs
    epochs.save(fname=epo_fname, overwrite=True)
    # Wanna plot?
    # epochs.plot(n_epochs=4, show=True, block=True, scalings={'eeg': 10})
    # Writing list of bad trials
    write_bad_trials(epo_fname, bad_trials)
    
    return epochs


def create_baseline_epochs(mat_fname, mont_fname, eve_fname, epo_fname,
                           sfreq=500., tmin=-2., ev_id=None):
    """Create epochs from the mat file (data_filt_ep), it needs the events 
        file and the montage file to be generated first.

    Args:
        mat_fname (path_like): Path to the mat file.
        mont_fname (path_like): Path to the DigMont file.
        eve_fname (path_like): Path to the event file.
        epo_fname (path_like): Path were the Epochs file will be saved.
        sfreq (float, optional): Sampling frequency (in Hz). Defaults to 500..
        tmin (float, optional): Starting time point in seconds.
            Defaults to -.2.
        ev_id (dict|None, optional): Dictionary containing the description of
            the events contained in the events file. Defaults to None.
    Returns:
        epochs (instance of mne.Epochs): Epochs object containing all the 
            relative informations and the data in the form of a 3D matrix of 
            shape (trials, channels, times).
    """
    mat = open_matfile(mat_fname)
    data = mat['data_filt_ep']
    data = np.transpose(data, axes=[2, 0, 1])
    print(data.shape)
    
    # Retrieving montage
    digi_mont = mne.channels.read_dig_fif(mont_fname)
    # Retrieving events
    events = mne.read_events(eve_fname)
    # Building infos
    ch_names = digi_mont.ch_names
    info = mne.create_info(ch_names, sfreq, ch_types='eeg')
    # Building epochs
    epochs = mne.EpochsArray(data, info, events=events,
                             tmin=tmin, event_id=ev_id)
    epochs.set_montage(digi_mont)
    # Reading bad trials from previous epoching
    bad_trials = read_bad_trials(epo_fname)
    # Dropping bad trials
    epochs.drop(bad_trials, reason='bad or nans')
    # Cropping data in the baseline period
    epochs = epochs.crop(-1.5, -.5)
    # Save baseline epochs
    epochs.save(fname=epo_fname, overwrite=True)
    # Wanna plot?
    # epochs.plot(n_epochs=4, show=True, block=True, scalings={'eeg': 10})
    
    return epochs


if __name__ == '__main__':
    mat_fname = '/media/jerry/ruggero/EmoSleep/sub-07_ses-01_task-sleep_eeg_swaves.mat'
    mont_fname = '/media/jerry/ruggero/EmoSleep/mne/mont/montage-mont.fif'
    eve_fname = '/media/jerry/ruggero/EmoSleep/mne/eve/events-eve.fif'
    epo_fname = '/media/jerry/ruggero/EmoSleep/mne/epo/epochs-epo.fif'
    bln_fname = '/media/jerry/ruggero/EmoSleep/mne/epo/baseline-epo.fif'
    
    ev_id = {'reject': 0, 'negative': 1, 'neutral': 2, 'positive': 3}
    # ev_id = {'negative': 1, 'neutral': 2, 'positive': 3}
    
    create_epochs(mat_fname, mont_fname, eve_fname, epo_fname, ev_id=ev_id)
    create_baseline_epochs(mat_fname, mont_fname, eve_fname, bln_fname,
                           ev_id=ev_id)
