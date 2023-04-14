#libraries used
import numpy as np
import scipy.io
import h5py
import math
import matplotlib.pyplot as plt
#class EigenData was taken from stephens-2d-eigenworm-data gitlab repository from test.py in order to generate the data
#functions __init__(), get_eigenworms(),get_footage() and reconstruct() were taken from that python script
#https://gitlab.com/tom-ranner/stephens-2d-eigenworm-data/-/blob/master/stephens-2011-data/test.py
class EigenData(object):
    '''Represents the original experiment data.'''
    #RECONSTRUCTS USING ALL PCs
    #init function
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def __init__(self):
        self._eigenworms = None #sets variable to None
    #function returns eigenworms array that is an 100x100 array, where the columns are the eigenworms used and the rows correspond to each angle value of midline points
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def get_eigenworms(self, eigen_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Eigenworms are stored as 100 'angles' at equidistributed coordinates
        down the body.
        '''
        # Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(eigen_path)
        self._eigenworms = eigenworms["EigenWorms"].transpose() # transposes array ( changes columns with rows)
        return self._eigenworms
    
    #function returns footage dictionary that has the eigenvalues array for each of the 12 worms
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def get_footage(self, footage_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Footage is stored as coefficients with respect to the eigenworm basis.
        '''
        f = h5py.File(footage_path, 'r') # opens file in read mode
        footage = {} # creates empty dictionary
        for k, v in f.items(): # key, value in dictionary f
            if k != 'tr':
                for k2, v2 in v.items(): #key2, value2 in previous value
                    if v2.shape == (5, 33600) or v2.shape == (6, 33600): #checks shape of value2 
                        footage[k2] = np.array(v2) #takes array of eigenvalues
        return footage #returns array
    

    #function reconstructs the angles 
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def reconstruct(self, coefficients):
        '''
        Reconstruct multiple postures from basis coefficients to angles.
        '''
        n_basis_required = coefficients.shape[0] #takes the number of columns which is the number of PCs used
        return self._eigenworms[0:n_basis_required, :].transpose() @ \
            coefficients # multiplies eigenworms with corresponding eigenvalues to get the angles in order to reconstruct posture
    
