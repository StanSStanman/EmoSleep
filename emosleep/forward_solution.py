import mne


def compute_forward_model(info_fname, trans_fname, src_fname,
                          bem_fname, fwd_fname):
    """_summary_

    Args:
        info_fname (str): path of the file containg info, 
            can be a mne raw or epochs file
        trans_fname (str): path to the transformation matrix file
        src_fname (str): path to the source space file
        bem_fname (str): path to the BEM model file
        fwd_fname (str): name of the path were the forward solution 
            will be saved
    """
    if '-raw' in info_fname:
        info = mne.io.read_raw_fif(info_fname).info
    elif '-epo' in info_fname:
        info = mne.read_epochs(info_fname).info
    trans = mne.read_trans(trans_fname)
    src = mne.read_source_spaces(src_fname)
    bem = mne.read_bem_solution(bem_fname)

    fwd = mne.make_forward_solution(info=info, trans=trans,
                                    src=src, bem=bem,
                                    meg=False, eeg=True,
                                    mindist=5.0, n_jobs=-1, verbose=False)

    mne.write_forward_solution(fwd_fname, fwd, overwrite=True)

    return


if __name__ == '__main__':
    info_fname = '/media/jerry/ruggero/EmoSleep/mne/epo/epochs-epo.fif'
    trans_fname = '/media/jerry/ruggero/EmoSleep/mne/trans/transform-trans.fif'
    bem_fname = '/media/jerry/ruggero/EmoSleep/mne/bem/bem-bem-sol.fif'
    src_fname = '/media/jerry/ruggero/EmoSleep/mne/src/sources-src.fif'
    fwd_fname = '/media/jerry/ruggero/EmoSleep/mne/fwd/forward-fwd.fif'
    
    compute_forward_model(info_fname, trans_fname, src_fname,
                          bem_fname, fwd_fname)
    
