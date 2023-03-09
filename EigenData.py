# Initial code taken from stephens-2d-eigenworm-data gitlab repository

import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

class EigenData(object):
    '''Represents the original experiment data.'''
    #EigenData Class:uses the original experiment data in the EigenWorms.mat and 20150814-All-PNAS2011-DataStitched .mat MATLAB files
    
    def __init__(self, eigen_path ="", footage_path=""):
        self._eigen_path = eigen_path
        self._footage_path = footage_path
        
    def generate_postures(self,array):
        dt = []
        for i in range(1,100):
            dt.append(i/100)
        plt.plot(dt,array,'.--')
        plt.title("Worm posture")
        plt.xlabel("t")
        plt.ylabel("s")
        plt.show()
        
    def generate_stdev_eigenworms(self,array):
        s = []
        for i in range(1,101):
            a = i/100
            s.append(a)
        for i in array:
            plt.plot(s,i)
        plt.title("Fraction of variance")
        plt.xlabel("s")
        plt.ylabel("sk")
        plt.show()
        
    
    def generate_shapes(self, array1, array2):
        #provides a description of the worm's shape 
        #mean value of θ  is always zero
        plt.plot(array1, array2, '.')
        plt.title("Curvature as a function of θ(s)")
        plt.xlabel("s")
        plt.ylabel("θ(rad)")
        plt.show()

    def generate_a1a2(self, a1, a2):
        plt.plot(a1, a2, '--.')
        plt.title("probability density for the two PCA modes")
        plt.xlabel("a1")
        plt.ylabel("a2")
        plt.show()
        
    def integrate_posture(self, angle1 ,angle2):
        out = math.sin(angle2) -math.cos(angle2) +angle2 -math.sin(angle1) + math.cos(angle1) -angle1
        return out
        
    def get_data(self):
        '''
        Loads the matlab files from the original experiment and parses them into
        expected numpy formats
        '''
        #Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(self._eigen_path)
        eigenworms = eigenworms["EigenWorms"]
        print(eigenworms)
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
        worm_array = [] #worm array for each worm
        big_array = [] # big array contains all 12 worms
        for wormfootage in footage:
            worm = footage[wormfootage] # each worm
            worm = worm.transpose() # transpose 
            #print(eigenworms)
            wmrow_cnt = 0
            for wormRow in worm[:100]: # take the first 100 points ( 1 full body)
                #print(wormRow)
                #print(wmrow_cnt)
                value_cnt = 0
                for wormValue in wormRow:
                    #print(value_cnt)
                    wm += wormValue*eigenworms[wmrow_cnt][value_cnt]
                    value_cnt += 1
                worm_array.append(wm)
                wmrow_cnt += 1
                wm = 0
            big_array.append(worm_array)
            worm_array = []
        #print(big_array)
        numbers_array = []

        for num in range(1, 101):
            numbers_array.append(num/100)
        a1 = []
        a2 = []
        for wormfootage in footage:
            worm = footage[wormfootage]
            wmrow_cnt = 0
            a1 = worm[0]
            a1 = a1[:100]
            a2 = worm[1]
            a2 = a2[:100]
            self.generate_a1a2(a1, a2)
            
        
        for i in range(0, 12):
           self.generate_shapes(numbers_array, big_array[i])

# np.set_printoptions(threshold=sys.maxsize)


#first worm 
        first_worm = []
        post_array_worm = []
        post_array_big = []
        for i in range(0,12):
            worm = big_array[i]
            #print(worm) #arclength along the body
            
            for j in range(0,99):
               pos = self.integrate_posture(worm[j],worm[j+1])
               post_array_worm.append(pos)
               #print(j)
            post_array_big.append(post_array_worm)
            post_array_worm = []
        #print(post_array_big)

        for i in range(0,12):
            worm = post_array_big[i]
            fr = worm[::-1]
            #print(fr)
            self.generate_postures(fr)
            
            
            
            egnw = eigenworms.transpose()
           
#standard deviaton graphs for eigenvectors
        wm=0
        small_array = []
        big_worm_array = []
        worm_array=[]
        for wormfootage in footage:
                worm = footage[wormfootage]
                worm_column_cnt =0
                for column in worm:
                    #print (new_clmn)
                    new_clmn = column[:100]
                    wmrow_cnt=0
                    for value in new_clmn:
                        wm = value*egnw[worm_column_cnt][wmrow_cnt]
                        #print(wm)
                        small_array.append(wm)
                        wmrow_cnt+=1
                    worm_array.append(small_array)
                    small_array = []
                    worm_column_cnt+=1
                worm_column_cnt =0
                big_worm_array.append(worm_array)
                worm_array = []

        #print(big_worm_array)
        worm_cnt=0
        #for worm in big_worm_array:
            #self.generate_stdev_eigenworms(worm)
                   #worm_column_cnt -> which column we are
                   
              
              
                   

        return eigenworms, footage

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
d1, d2 = ed.get_data()