#from code_generation import EigenData
from init import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

ed = EigenData()
eigenworms = ed.get_eigenworms("EigenWorms.mat")
footage = ed.get_footage("20150814-All-PNAS2011-DataStitched .mat")
count =0
for k in footage.keys():
    if count == 0: # first worm
        r = ed.reconstruct(footage[k])
    count+=1
r = r.transpose()
print(r[0])
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
        num=0
        a11 = a1[0]
        a12 = a2[0]
        #velocity = self.find_velocity_way1(a11,a12,phase_velocity,num)
        #print(velocity)
        for num in range(0,10):
            vel = self.find_velocity_way2(phase_velocity,r[0],num)
            print(vel)

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
    
    def find_velocity_way1(self,a1,a2,phv,num):
        #s -> position
        #n -> number of waves
        #L -> body length
        n=1
        L=1
        TotalCurvature=0
        for i in range(1,101):
            s = i/100
            v1 = math.sin(2*math.pi*n*s/L)
            v2 = math.cos(2*math.pi*n*s/L)
            curvature = a1*v1+a2*v2
            TotalCurvature += curvature
            #print("TotalCurvature = " ,TotalCurvature )
        AveragingCurvature = TotalCurvature/100
        #print("Averaging Curvature = " ,AveragingCurvature)
        Radius = 1/AveragingCurvature
        #print(phv[0])
        velocity = phv[num]*Radius
        return velocity
    
    def find_velocity_way2(self,phv,angles,num):
        current_phv = phv[num]
        Total_Sum = 0
        for i in range(1,101):
            s = i/100
            Radius = s/angles[i-1]
            Total_Sum += Radius
        Radius_avg = Total_Sum/100

        velocity = Radius_avg*current_phv/10
        return velocity

        

ig = GeometricPhase().main_fun()
