# Initial code taken from stephens-2d-eigenworm-data gitlab repository

import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py

class EigenData(object):
    '''Represents the original experiment data.'''
    #EigenData Class:uses the original experiment data in the EigenWorms.mat and 20150814-All-PNAS2011-DataStitched .mat MATLAB files
    
    def __init__(self, eigen_path ="", footage_path=""):
        self._eigen_path = eigen_path
        self._footage_path = footage_path
    
    def generate_postures(self, array1, array2):
        plt.plot(array1, array2, '.')
        plt.title("Worm Shape")
        plt.xlabel("s")
        plt.ylabel("θ")
        plt.show()

    def get_data(self):
        '''
        Loads the matlab files from the original experiment and parses them into
        expected numpy formats
        '''
        #Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(self._eigen_path)
        eigenworms = eigenworms["EigenWorms"]
        footage = {}
        f = h5py.File(self._footage_path, "r+")
        eigenworms = eigenworms[:, :6]
        i = 0
        for k, v in f.items():
            if k != "tr":
                for k2, v2 in v.items():
                    if v2.shape == (5, 33600) or v2.shape == (6, 33600):
                        footage[i] = np.array(v2)
                        i+=1
    #multiplication of the eigenvalues with the eigenvectors for each worm to get tje arc length θ(s)
    #worm_array is a list that contatins the arc length for the points of one worm
    #big_array is a list that contains 12 lists (one for each worm used) that contain the arc length of the first 100 points
        wm = 0
        worm_array = []
        big_array = []
        for wormfootage in footage:
            worm = footage[wormfootage]
            worm = worm.transpose()
            # print(worm)
            wmrow_cnt = 0
            for wormRow in worm[:100]:
                # print(wormRow)
                # print(wmrow_cnt)
                value_cnt = 0
                for wormValue in wormRow:
                    wm += wormValue*eigenworms[wmrow_cnt][value_cnt]
                    value_cnt += 1
                worm_array.append(wm)
                wmrow_cnt += 1
                wm = 0
            big_array.append(worm_array)
            worm_array = []
        # print(big_array)
        numbers_array = []

        for num in range(1, 101):
            numbers_array.append(num/100)
            
            
        for i in range(0, 12):
            self.generate_postures(numbers_array, big_array[i])
            
            
            
        return eigenworms, footage

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
d1, d2 = ed.get_data()