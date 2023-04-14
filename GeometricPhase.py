#imported libraries to use in geometric phase
from code_gen import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

data = EigenData() #creates instance of class
data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms()
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms
count =0
for k in footage.keys():
    if count == 0: # first worm
        r = data.reconstruct(footage[k])
    count+=1
r = r.transpose()
#print(r[0])
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
        frequency = phase_velocity / (2*math.pi)
        #print(frequency)
        self.generate_phase_velocity(phase_velocity,times)
        times = times[:99]
        phase_acceleration = np.diff(phase_velocity) / np.diff(times)
        self.generate_phase_acceleration(phase_acceleration,times)
        #num=0
        for num in range(0,10):
             vel1 = self.find_velocity_way1(phase_velocity,r[0],num)
             print(vel1)


    def generate_phase_acceleration(self,ph_acc,t):
        plt.plot(t[:-1], ph_acc)
        plt.xlabel('Time (s)')
        plt.title("Phase acceleration in time")
        plt.ylabel('Phase acceleration (cycles/s)')
        plt.show()


    def generate_phase_velocity(self,ph_vel,t):
        plt.plot(t[:-1], ph_vel)
        plt.title("Phase velocity in time")
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
    
    def find_velocity_way1(self,phv,angles,num):
        current_phv = phv[num]
        Total_Sum = 0
        for i in range(1,100):
            s=0.01
            curvature = (angles[i]-angles[i-1])/s
            Radius = 1/curvature
            Total_Sum += Radius
        Radius_avg = Total_Sum/100
        velocity = Radius_avg*current_phv
        return velocity
    

        

ig = GeometricPhase().main_fun()
