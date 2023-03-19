from code_generation import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
eigenworms, footage = ed.get_data()

class Initial_graphs(object):

    def variance_modes_function(self):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[ wormfootage ]
                worm = worm.transpose()
                firstrow = worm[0]
                #print(firstrow)
            count += 1
            # sort the eigenvalues in descending order
        idx = np.argsort( firstrow )[::-1]
        firstrow = firstrow[idx]
        firstrow = firstrow[::-1]
        print(firstrow)
        # compute the total sum of all eigenvalues
        total_var = np.sum(firstrow)
        print(total_var)
        frac_var = []
        cumulative_sum = 0
        for k in range(1, len(firstrow)+1):
            cumulative_sum += firstrow[k-1]
            frac_var.append(cumulative_sum/10)
        for i in range(0,3):
            frac_var.append(1)
        # plot the fraction of variance explained
        plt.plot(range(1, len(firstrow)+4), frac_var,'.',markersize=14)
        plt.axhline(y=1, color='r', linestyle='-')
        plt.xlabel('Number of eigenvalues')
        plt.ylabel('Fraction of variance explained')
        plt.show()

Initial_graphs().variance_modes_function()