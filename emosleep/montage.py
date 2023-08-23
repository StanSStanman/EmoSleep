import numpy as np
import mne
import matplotlib.pyplot as plt
from emosleep.io import open_matfile


def compute_montage(mat_fname, mont_fname=False):
    """Exctract the digital montage of the electrodes from the mat file and
        put it in a MNE compatible form

    Args:
        mat_fname (path_like): Path to the matlab file.
        mont_fname (path_like|False, optional): Path where tha montage file 
            will be saved, if False the montage will not be saved. 
            Defaults to False.

    Returns:
        dig_mont (instance of mne.channels.DigMontage): MNE compatible montage
    """
    mat = open_matfile(mat_fname)
    ch_pos = {}
    for c in mat['chanlocs'][0, :]:
        ch_pos[c[0][0]] = np.array([c[1], c[2], c[3]]).squeeze() * .01
    dig_mont = mne.channels.make_dig_montage(ch_pos=ch_pos,
                                             coord_frame='unknown')
    if mont_fname is not False:
        if isinstance(mont_fname, str):
            dig_mont.save(mont_fname, overwrite=True)
        else:
            raise ValueError('mont_fname should be False or path-like object')
   # dig_mont.plot(show=False, kind='3d')
   # plt.show(block=True)
    return dig_mont


if __name__ == '__main__':
    mat_fname = '/media/jerry/ruggero/EmoSleep/sub-07_ses-01_task-sleep_eeg_swaves.mat'
    mont_fname = '/media/jerry/ruggero/EmoSleep/mne/mont/montage-mont.fif'
    
    compute_montage(mat_fname, mont_fname=mont_fname)
