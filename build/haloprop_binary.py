import h5py
import numpy as np
from dtype import dt
import os

def header_len(fname):
    """ 
    Returns number of header lines of subvolume ascii file.

    """

    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return

def tree_gen(f, haloprop_key):
    """
    Generator that yields rows of each tree.
    
    """

    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield first_row[haloprop_key]
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first'])+1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        parsed_line = line.strip().split()
        yield parsed_line[dt.names.index(haloprop_key)]
        row += 1 

def create(subvolume, haloprop_key):
    """
    Creates memory mapped binary file for a given haloprop for a given subvolume.
    
    Parameters
    ----------
    subvolume : string
        Name of subvolume

    haloprop_key : string
        Name of haloprop_key

    Examples
    --------
    
    >>> create('0_0_0', 'scale')
    
    """

    subvolume_file = 'tree_ascii_data/tree_'+subvolume+'.dat'
    tree_directory = 'trees/'+subvolume+'/tree_directory.hdf5'
    ouput_binary = 'trees/'+subvolume+'/'+haloprop_key+'.'+str(dt[haloprop_key])+'/'+haloprop_key+'.data'
    print 'creating haloprop binary at', ouput_binary, 'for haloprop_key:', haloprop_key

    haloprop_folder = './trees/'+subvolume+'/'+haloprop_key+'.'+str(dt[haloprop_key])
    if not os.path.exists(haloprop_folder):
        os.makedirs(haloprop_folder)
    h = header_len(subvolume_file)
    with open(subvolume_file, 'r') as f:
        with h5py.File(tree_directory,"r") as hf: 
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            binaryarr = []
            while(tree_index < num_trees):
                print '#tree', str(tree_index) + '/' + str(num_trees)
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                binaryarr += (list(tree_gen(f, haloprop_key)))
                tree_index += 1
            mm = np.memmap(filename = ouput_binary, 
            dtype=dt[haloprop_key], mode='w+', shape=(1, len(binaryarr)))
            mm[:] = np.array(binaryarr)
            del mm
    return 



