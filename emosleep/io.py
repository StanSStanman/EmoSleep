import h5py
from scipy.io import loadmat


def open_matfile(mat_fname):
    """Simple function to open mat files, if the file version is <=7.3 uses 
        scipy.io.loadmat, otherwise h5py.

    Args:
        mat_fname (path_like): _description_

    Returns:
        mat (dict| instance of h5py.Group): Content of the mat file.
    """
    try:
        mat = loadmat(mat_fname)
        print('Loaded mat file <= v7.3...\n')
    except:
        mat = h5py.File(mat_fname)
        print('Loaded mat file >= v7.3...\n')
    return mat


def read_h5ref(ref, h5_file):
    # Chech if ref belongs to Reference class, 
    # otherwise return without modifications
    if isinstance(ref, h5py.h5r.Reference):
        # Extract the reference from file
        obj = h5_file[ref]
        # Append all the objects in a list
        objs = []
        for o in obj:
            objs.append(o)
        return objs
    else:
        return ref
