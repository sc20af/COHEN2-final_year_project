# Initial code taken from stephens-2d-eigenworm-data gitlab repository


import numpy as np
import scipy.io
import h5py

class EigenData(object):
    '''Represents the original experiment data.'''
    #EigenData Class:uses the original experiment data in the EigenWorms.mat and 20150814-All-PNAS2011-DataStitched .mat MATLAB files
    
    def __init__(self, eigen_path ="", footage_path=""):
        self._eigen_path = eigen_path
        self._footage_path = footage_path

    def get_data(self):
        '''
        Loads the matlab files from the original experiment and parses them into
        expected numpy formats
        '''
        #Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(self._eigen_path)
        eigenworms = eigenworms["EigenWorms"].transpose()
        footage = {}
        f = h5py.File(self._footage_path)
        i = 0
        for k, v in f.items():
            if k != "tr":
                for k2, v2 in v.items():
                    if v2.shape == (5, 33600) or v2.shape == (6, 33600):
                        footage[i] = np.array(v2)
                        i+=1
        return eigenworms, footage
