import os
import os.path as op
import json
import numpy as np
import xarray as xr


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


def get_peaks(data, dim):
    maxs = data.max(dim).values
    mins = data.min(dim).values

    pks = np.zeros_like(maxs)

    pks[abs(mins)>maxs] = mins[abs(mins)>maxs]
    pks[abs(mins)<maxs] = maxs[abs(mins)<maxs]

    data = data.max(dim)
    data.values = pks

    return data


def z_score(data, twin=None):
    '''
    Perform z-score on the 3rd dimension of an array
    ( y = (x - mean(x)) / std(x) )
    :param data: np.ndarray | xr.DataArray
        Data on which perform the z-score, average e standard deviation
        are computed on the 3rd dimension
    :return: np.ndarray | xr.DataArray
        z-scored data
    '''
    isinstance(twin, (tuple, type(None)))
    if twin is None:
        if isinstance(data, xr.DataArray):
            data.data = ((data.data - data.data.mean(-1, keepdims=True)) /
                         data.data.std(-1, keepdims=True))
        elif isinstance(data, np.ndarray):
            data = ((data - data.mean(-1, keepdims=True)) /
                    data.std(-1, keepdims=True))
    else:
        if isinstance(data, xr.DataArray):
            bln = data.sel({'times': slice(*twin)})
            data.data = ((data.data - bln.data.mean(-1, keepdims=True)) /
                         bln.data.std(-1, keepdims=True))
        else:
            raise ValueError('If twin is specified, data should be an '
                             'xarray.DataArray with one dim called \'times\'')
    return data
