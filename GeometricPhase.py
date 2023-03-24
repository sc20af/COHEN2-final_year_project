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
        self.generate_a1a2(a1,a2)
        phase_angles = np.arctan2(-a2, a1)
        min_phase = 0
        max_phase = 0
        for phase in phase_angles:
            if phase> max_phase:
                max_phase = phase
            if phase< min_phase:
                min_phase = phase
        #print("Max phase:", max_phase)
        #print("Min phase:", min_phase)
        #phase goes from -π to +π

        times = np.linspace(0, 4, 100) 
        self.generate_phase_graph(phase_angles)
        phase_velocity = np.diff(phase_angles) / np.diff(times)
        self.generate_phase_velocity(phase_velocity,times)
        times = times[:99]
        phase_acceleration = np.diff(phase_velocity) / np.diff(times)
        self.generate_phase_acceleration(phase_acceleration,times)

    def generate_phase_acceleration(self,ph_acc,t):
        plt.plot(t[:-1], ph_acc)
        plt.xlabel('Time (s)')
        plt.ylabel('Phase acceleration (cycles/s)')
        plt.show()
    def generate_phase_velocity(self,ph_vel,t):
        plt.plot(t[:-1], ph_vel)
        plt.xlabel('Time (s)')
        plt.ylabel('Phase velocity (rad/s)')
        plt.show()
    
    def generate_phase_graph(self,angles):
        times = np.linspace(0, 4, 100) 
        plt.plot(times,angles, '--.')
        plt.title("Phase in time")
        plt.xlabel("t")
        plt.ylabel("phase")
        plt.show()


    def generate_a1a2(self,a1,a2):   
        plt.plot(a1, a2, '--.')
        plt.title("two PCA modes")
        plt.xlabel("a1")
        plt.ylabel("a2")
        plt.show()
    


ig = GeometricPhase().main_fun()
