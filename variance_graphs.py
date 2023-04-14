from code_gen import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

data = EigenData() #creates instance of class
eigenworms = data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms()
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms

class Initial_graphs(object):

    def variance_modes_function(self):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[ wormfootage ]
                worm = worm.transpose()
                firstrow = worm[0]
            count += 1
        # sort the eigenvalues in descending order
        idx = np.argsort( firstrow )[::-1]
        firstrow = firstrow[idx]
        firstrow = firstrow[::-1]
        # compute the total sum of all eigenvalues
        total_var = np.sum(firstrow)
        #print(total_var)
        frac_var = []
        cumulative_sum = 0
        for k in range(1, len(firstrow)+1):
            cumulative_sum += firstrow[k-1]
            frac_var.append(cumulative_sum/total_var)
        sorted_var = sorted(frac_var)
        # plot the fraction of variance explained
        x = [1,2,3,4,5]
        plt.plot(x, sorted_var,'.',markersize=14)
        plt.xticks(range(1, 6))
        plt.axhline(y=1, color='r', linestyle='-')
        plt.xlabel('K',fontsize=13)
        plt.ylabel(r'$\sigma^2_K$',fontsize=16)
        plt.show()


    
Initial_graphs().variance_modes_function()
