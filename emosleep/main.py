import os
import os.path as op
from emosleep.montage import compute_montage
from emosleep.events import create_events
from emosleep.epochs import create_epochs, create_baseline_epochs


datapath = '/Disk2/EmoSleep/derivatives/'
subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 
            'sub-06', 'sub-07', 'sub-10', 'sub-11', 'sub-12', 
            'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-19', 
            'sub-22', 'sub-23', 'sub-24', 'sub-25', 'sub-26', 
            'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-32']
ses = '01'

mat_fname = '{0}_ses-{1}_task-sleep_eeg_swaves.mat'
montage_filename = '{0}_ses-{1}-mont.fif'
events_filename = '{0}_ses-{1}-eve.fif'
epo_filename = '{0}_ses-{1}-epo.fif'
bln_filename = '{0}_ses-{1}_bln-epo.fif'


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

    digimontage = compute_montage(mfname, mont_fname)

    eve_dir = op.join(mne_dir, 'eve')
    if not op.exists(eve_dir):
        os.mkdir(eve_dir)
    eve_fname = op.join(eve_dir, events_filename.format(subj, ses))

    events = create_events(mfname, eve_fname)

    epo_dir = op.join(mne_dir, 'epo')
    if not op.exists(epo_dir):
        os.mkdir(epo_dir)
    epo_fname = op.join(epo_dir, epo_filename.format(subj, ses))
    ev_id = {'reject': 0, 'negative': 1, 'neutral': 2, 'positive': 3}
    epochs = create_epochs(mfname, mont_fname, eve_fname, epo_fname,
                           ev_id=ev_id)

    bln_fname = op.join(epo_dir, bln_filename.format(subj, ses))

    baseline = create_baseline_epochs(mfname, mont_fname, eve_fname,
                                      bln_fname, ev_id=ev_id)
