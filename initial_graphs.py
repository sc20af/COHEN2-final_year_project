from code_generation import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
eigenworms, footage = ed.get_data()

class Initial_graphs(object):
    #generates the first 6 worms 
    def generate_first_eigenworms(self):
        s = []
        for i in range(1,101):
            a = i/100
            s.append(a)
        count = 1
        for ew in eigenworms[:6]:
            plt.plot(s, ew, '-')
            message = ('Eigenworm: '+ str(count))
            plt.title(message)
            plt.xlabel("s")
            plt.ylabel("θ(rad)")
            plt.show()
            count+=1
    def generate_a1a2(self):
        a1 = []
        a2 = []
        for wormfootage in footage:
            worm = footage[wormfootage]
            wmrow_cnt = 0
            a1 = worm[0]
            a1 = a1[:100]
            a2 = worm[1]
            a2 = a2[:100]
            plt.plot(a1, a2, '--.')
            plt.title("probability density for the two PCA modes")
            plt.xlabel("a1")
            plt.ylabel("a2")
            plt.show()
ig = Initial_graphs().generate_a1a2()
#ig = Initial_graphs().generate_first_eigenworms()

#need to sort eigenworms 