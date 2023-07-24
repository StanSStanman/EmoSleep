import os
import os.path as op
import json


def write_bad_trials(epo_fname, bad_trials):
    bad_t = [int(x) for x in bad_trials]
    epo_dir = op.abspath(op.join(epo_fname, os.pardir))
    with open(op.join(epo_dir, 'bad_trials.json'), 'w') as f:
        json.dump(list(bad_t), f)
    return
    
    
def read_bad_trials(epo_fname, bad_fname='bad_trials.json'):
    epo_dir = op.abspath(op.join(epo_fname, os.pardir))
    with open(op.join(epo_dir, 'bad_trials.json'), 'r') as f:
        bad_t = json.load(f)
    return bad_t
