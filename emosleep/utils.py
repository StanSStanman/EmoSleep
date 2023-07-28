import os
import os.path as op
import json


def write_bad_trials(epo_fname, bad_trials, bad_fname='bad_trials.json'):
    """Write down discarded trials (bad + nans) in a json file, saved in the 
    same directiory of the epo_fname file.

    Args:
        epo_fname (path_like): path to the epochs file
        bad_trials (list): list of positions of discarded trials
        bad_fname (str, optional): name of the bad trials json file.
            Default to 'bad_trials.json'
    """
    bad_t = [int(x) for x in bad_trials]
    epo_dir = op.abspath(op.join(epo_fname, os.pardir))
    with open(op.join(epo_dir, bad_fname), 'w') as f:
        json.dump(list(bad_t), f)
    return


def read_bad_trials(epo_fname, bad_fname='bad_trials.json'):
    """Read the json file containing the positions of discarded trials.

    Args:
        epo_fname (path_like): path to the epochs file
        bad_fname (str, optional): name of the bad trials json file.
            Defaults to 'bad_trials.json'.

    Returns:
        bad_t (list): list of discarded trials
    """
    epo_dir = op.abspath(op.join(epo_fname, os.pardir))
    with open(op.join(epo_dir, bad_fname), 'r') as f:
        bad_t = json.load(f)
    return bad_t
