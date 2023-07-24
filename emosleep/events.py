import numpy as np
import mne
from emosleep.io import open_matfile


def create_events(mat_fname, eve_fname=False):
    """This function creates a MNE-fromat event matrix of shape (trials, 3).
       The firs column corresponds to trial number, the second is full of
       zeros, the third is organized as follows:
            - 0: rejected trial
            - 1: negative stimulus
            - 2: neutral stimulus
            - 3: positive stimulus

    Args:
        mat_fname (path-like): path to the .mat file
        eve_fname (path-like | False): if False, the event matrix will be just
            returned, otherwise it will be saved in the given path.
            Defaults to False.

    Raises:
        ValueError: raise VaueError if eve_fname is not False or path-like 

    Returns:
        numpy.ndarray: array of shape (trials, 3) containing the events
    """
    mat = open_matfile(mat_fname)
    neg_eve = (mat['idx_neg'].squeeze() - 1)
    ntr_eve = (mat['idx_ntr'].squeeze() - 1)
    pos_eve = (mat['idx_pos'].squeeze() - 1)
    
    events = np.zeros((192, 3))
    events[:, 0] = np.arange(192, dtype=int)
    
    for i, ev in enumerate([neg_eve, ntr_eve, pos_eve]):
        for t in ev:
            events[t, -1] = i + 1
    # verify the number of rejected trials
    rej = mat['rejjp'].squeeze()
    zeros = np.where(events[:, -1] == 0)[0]
    assert len(rej) == len(zeros)
    
    events = events.astype(int)
    
    if eve_fname is not False:
        if isinstance(eve_fname, str):
            mne.write_events(eve_fname, events, overwrite=True)
        else:
            raise ValueError('eve_fname should be False or path-like object')
        
    return events


if __name__ == '__main__':
    mat_fname = '/media/jerry/ruggero/EmoSleep/sub-07_ses-01_task-sleep_eeg_swaves.mat'
    eve_fname = '/media/jerry/ruggero/EmoSleep/mne/eve/events-eve.fif'
    
    create_events(mat_fname, eve_fname)
