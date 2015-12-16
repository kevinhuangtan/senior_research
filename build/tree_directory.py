import h5py
import numpy as np
from dtype import dt
import os


def header_len(fname):
    """ Get number of header lines."""
    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return

def tree_gen(f):
    """
    Generator that yields rows of each tree.
    
    """
    
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield first_row
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        parsed_line = line.strip().split()
        yield np.array(tuple(parsed_line), dtype = dt)
        row += 1 

def create(subvolume):
    """
    Adds tree metadata for each tree in the subvolume to tree directory. Each subvolume has a tree_directory.

    User can retrieve data like:
    tree_directory['treeID'] --> [length, offset, haloid_depth_first, haloid_last_mainleaf_depthfirst]

    length: number of rows in the tree
    offset: offset points to location in memmapped binary file
    haloid_depth_first: indicates root of tree (also the root of the trunk)
    haloid_last_mainleaf_depthfirst: last leaf of the trunk


    Parameters
    ----------
    subvolume : string
        Name of subvolume

    Examples
    --------

    >>> create('0_0_0')
    >>> #now you can retrieve the metadata from 
    >>> treeID = '3060286872'
    >>> with h5py.File('tree_directory.hdf5', 'r') as tree_directory:
    >>>     metadata = tree_directory[treeID][...]
    >>> print metadata
    >>> [    22173   1496684 109528093 109528271]
    
    """
    subvolume_file = 'tree_ascii_data/tree_'+ subvolume + '.dat' 
    subvolume_folder = './trees/'+subvolume
    if not os.path.exists(subvolume_folder):
        os.makedirs(subvolume_folder)

    tree_directory_fname = 'trees/' + subvolume + '/tree_directory.hdf5'


    print 'creating tree directory at', tree_directory_fname

    h = header_len(subvolume_file)
    with h5py.File(tree_directory_fname,"w") as hf: 
        with open(subvolume_file, 'r') as f:
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            tree_data = [0,0]
            while(tree_index < num_trees):
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                print '#tree', str(tree_index) + '/' + str(num_trees)
                tree = tree_gen(f)
                tree = np.array(list(tree))
                len_arr = len(tree)

                root = tree['haloid_depth_first'].argmin()

                hf[tree_id] = np.array([
                    len_arr, 
                    offset_sum, 
                    tree[root]['haloid_depth_first'], 
                    tree[root]['haloid_last_mainleaf_depthfirst']
                ])  
                tree_index += 1
                offset_sum += len_arr
    return 

