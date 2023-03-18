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
                worm = footage[wormfootage]
                worm = worm.transpose()
                firstrow = worm[0]
                print(firstrow)
            count += 1

Initial_graphs().variance_modes_function()