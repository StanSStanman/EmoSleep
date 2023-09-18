import os
import os.path as op
import mne
# from emosleep.montage import compute_montage
# from emosleep.events import create_events
# from emosleep.epochs import create_baseline_epochs
from emosleep.epochs_pre import create_epochs
# from emosleep.bem import compute_bem
# from emosleep.source_space import compute_source_space
# from emosleep.forward_solution import compute_forward_model
from emosleep.signal_se import (compute_lcmv_sources,
                                compute_inverse_sources,
                                labeling)


datapath = '/Disk2/EmoSleep/derivatives/'
subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05',
            'sub-06', 'sub-07', 'sub-10', 'sub-11', 'sub-12',
            'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-19',
            'sub-22', 'sub-23', 'sub-24', 'sub-25', 'sub-26',
            'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-32']
# subjects = ['sub-01']
ses = '01'

mat_fname = '{0}_ses-{1}_task-sleep_eeg_swaves.mat'
montage_filename = '{0}_ses-{1}-mont.fif'
events_filename = '{0}_ses-{1}-eve.fif'
epo_filename = '{0}_ses-{1}_pre-epo.fif'
bln_filename = '{0}_ses-{1}_bln-epo.fif'
trans_filename = 'common-trans.fif'
bem_filename = 'common-bem-sol.fif'
src_filename = 'common-src.fif'
fwd_filename = 'common-fwd.fif'
ltc_filename = '{0}_ses-{1}_pre_ltc.nc'

for subj in subjects:
    # define folder names and create them
    mne_dir = op.join(datapath, subj, 'mne')
    if not op.exists(mne_dir):
        os.mkdir(mne_dir)
    mfname = op.join(datapath, subj, mat_fname.format(subj, ses))
    
    mont_dir = op.join(mne_dir, 'mont')
    if not op.exists(mont_dir):
        os.mkdir(mont_dir)
    mont_fname = op.join(mont_dir, montage_filename.format(subj, ses))

    # digimontage = compute_montage(mfname, mont_fname)
    digimontage = mne.channels.read_dig_fif(mont_fname)

    eve_dir = op.join(mne_dir, 'eve')
    if not op.exists(eve_dir):
        os.mkdir(eve_dir)
    eve_fname = op.join(eve_dir, events_filename.format(subj, ses))

    # events = create_events(mfname, eve_fname)
    events = mne.read_events(eve_fname)

    epo_dir = op.join(mne_dir, 'epo')
    if not op.exists(epo_dir):
        os.mkdir(epo_dir)
    epo_fname = op.join(epo_dir, epo_filename.format(subj, ses))
    ev_id = {'no_kc': 0, 'kc': 1}
    epochs = create_epochs(mfname, mont_fname, eve_fname, epo_fname,
                           ev_id=ev_id)

    bln_fname = op.join(epo_dir, bln_filename.format(subj, ses))

    # baseline = create_baseline_epochs(mfname, mont_fname, eve_fname,
    #                                   bln_fname, ev_id=ev_id)
    # baseline = mne.read_epochs(bln_fname)

fs_dir = op.join(datapath, 'freesurfer')
mne.datasets.fetch_fsaverage(subjects_dir=fs_dir, verbose=True)

trans_dir = op.join(fs_dir, 'trans')
if not op.exists(trans_dir):
    os.mkdir(trans_dir)
trans_fname = op.join(trans_dir, trans_filename)
    
# mne.gui.coregistration(subjects_dir=datapath, subject='fsaverage',
#                        head_high_res=False, show=True, block=True)
    
bem_dir = op.join(fs_dir, 'bem')
if not op.exists(bem_dir):
    os.mkdir(bem_dir)
bem_fname = op.join(bem_dir, bem_filename)

# compute_bem('fsaverage', fs_dir, bem_fname)

src_dir = op.join(fs_dir, 'src')
if not op.exists(src_dir):
    os.mkdir(src_dir)
src_fname = op.join(src_dir, src_filename)

# compute_source_space('fsaverage', fs_dir, src_fname, spacing='oct6')

fwd_dir = op.join(fs_dir, 'fwd')
if not op.exists(fwd_dir):
    os.mkdir(fwd_dir)
fwd_fname = op.join(fwd_dir, fwd_filename)

# compute_forward_model(epo_fname, trans_fname, src_fname, bem_fname, fwd_fname)

for subj in subjects:
    mne_dir = op.join(datapath, subj, 'mne')
    
    ltc_dir = op.join(mne_dir, 'ltc')
    if not op.exists(ltc_dir):
        os.mkdir(ltc_dir)
    ltc_fname = op.join(ltc_dir, ltc_filename.format(subj, ses))
    
    epo_dir = op.join(mne_dir, 'epo')
    epo_fname = op.join(epo_dir, epo_filename.format(subj, ses))
    bln_fname = op.join(epo_dir, bln_filename.format(subj, ses))
    events = mne.read_epochs(epo_fname).events[:, -1]
    
    # stc = compute_lcmv_sources(epo_fname, bln_fname, fwd_fname, events=None)
    stc = compute_inverse_sources(epo_fname, bln_fname, fwd_fname)
    
    labeling('fsaverage', fs_dir, stc, src_fname, ltc_fname, events)
