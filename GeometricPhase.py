#imported libraries to use in geometric phase
from code_gen import EigenData
import matplotlib.pyplot as plt
import numpy as np
import math

data = EigenData() #creates instance of class
data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms() to get eigenworms array
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms
count =0 #counter for first worm
for k in footage.keys():
    if count == 0: # first worm
        r = data.reconstruct(footage[k])
    count+=1
r = r.transpose() # transposes data of first worm

#class GeometricPhase responsible for graphs of phase, phase velocity & acceleration
class GeometricPhase(object):
    #main class
    def main(self):
        a1 = [] # array of first component values
        a2 = [] #array of second component values
        count = 0
        for wormfootage in footage:
            if count ==0:
                worm = footage[wormfootage] #first worm data
            count+=1
        a1 = worm[0] # first column
        a1 = a1[:100] #100 first timestamps
        a2 = worm[1] #second column
        a2 = a2[:100] #100 first timestamps
        self.generate_a1a2(a1,a2) #graph generation using function
        phase_angles = np.arctan2(-a2, a1) #finds phase values
        min_phase = 0 #minimum phase value
        max_phase = 0 #maximum phase value
        for phase in phase_angles:
            if phase> max_phase:
                max_phase = phase
            if phase< min_phase:
                min_phase = phase
        #print("Max phase:", max_phase)
        #print("Min phase:", min_phase)
        #phase goes from -π to +π

        times = np.linspace(0, 4, 100)  #time values
        self.generate_phase_graph(phase_angles) #generate phase graph
        phase_velocity = np.diff(phase_angles) / np.diff(times) #phase velocity calculations
        frequency = phase_velocity / (2*math.pi) #frequency values
        #print(frequency)
        self.generate_phase_velocity(phase_velocity,times) #generate phase velocity graphs
        times = times[:99] #times
        phase_acceleration = np.diff(phase_velocity) / np.diff(times) #phase acceleration values
        for num in range(0,10): #velocity values of 10 timestamps
             vel1 = self.find_velocity(phase_velocity,r[0],num)
             print("Velocity for ",num ,"is:" ,vel1)
    #phase acceleration graphs showing values at different timestamps
    def generate_phase_acceleration(self,ph_acc,t):
        plt.plot(t[:-1], ph_acc) #plots values
        plt.xlabel('Time (s)') #x label
        plt.title("Phase acceleration in time") #title of graph
        plt.ylabel('Phase acceleration (cycles/s)') #y label
        plt.show() #display graph
    #phase velocity graphs showing values at different timestamps
    def generate_phase_velocity(self,ph_vel,t):
        plt.plot(t[:-1], ph_vel) #plot values
        plt.title("Phase velocity in time") #title
        plt.xlabel('Time (s)') #x label
        plt.ylabel('Phase velocity (rad/s)') #y label
        plt.show() #show graph
    #phase graphs showing values at different times
    def generate_phase_graph(self,angles):
        times = np.linspace(0, 4, 100)  #times array
        plt.plot(times,angles, '--.') #plots values
        plt.title("Phase in time") #title
        plt.xlabel("t") #x label
        plt.ylabel("phase") #y label
        plt.show() #show graph
    #graph showing first two mode values
    def generate_a1a2(self,a1,a2):   
        plt.plot(a1, a2, '--.') #plots values
        plt.title("First two PCA modes visual representation") #titles
        plt.xlabel("a1") #x label
        plt.ylabel("a2")#y label
        plt.show() # show graph
    #calculations in order to find velocity and make predictions
    def find_velocity(self,phv,angles,num):
        current_phv = phv[num] #find phase velocity value (ω) at that timestamp
        Total_Sum = 0 # sum = 0
        array = []
        for i in range(1,100): # first 100 values
            s=0.01 # segment length
            curvature = (angles[i]-angles[i-1])/s #curvature
            Radius = 1/curvature #radius
            array.append(Radius) #array of radius
        current_radius = array[num] #finds radius corresponding to that timestamp
        velocity = current_radius*current_phv #calculates velocity using formula u=ωR
        return velocity #returns velocity
    
#calls main function
ig = GeometricPhase().main()
