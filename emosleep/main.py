from emosleep.montage import compute_montage
from emosleep.events import create_events
from emosleep.epochs import create_epochs, create_baseline_epochs


datapath = '/Disk2/EmoSleep/derivativesNEW3/'
subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 
            'sub-06', 'sub-07', 'sub-10', 'sub-11', 'sub-12', 
            'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-19', 
            'sub-22', 'sub-23', 'sub-24', 'sub-25', 'sub-26', 
            'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-32']
ses = '01'

mat_fname = '{0}_ses-{1}_task-sleep_eeg_swaves.mat'

for subj in subjects:
    mfname = mat_fname.format(subj,ses)
