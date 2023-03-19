from code_generation import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
eigenworms, footage = ed.get_data()

class GeometricPhase(object):
    def main_fun(self):
        a1 = []
        a2 = []
        count = 0
        for wormfootage in footage:
            if count ==0:
                worm = footage[wormfootage]
            count+=1
        a1 = worm[0]
        a1 = a1[:100]
        a2 = worm[1]
        a2 = a2[:100]
        #self.generate_a1a2(a1,a2)
    



    def generate_a1a2(self,a1,a2):   
        plt.plot(a1, a2, '--.')
        plt.title("two PCA modes")
        plt.xlabel("a1")
        plt.ylabel("a2")
        plt.show()
    


ig = GeometricPhase().main_fun()
