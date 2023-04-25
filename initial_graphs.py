#imported libraries
from code_gen import EigenData
import matplotlib.pyplot as plt

data = EigenData() #creates instance of class
eigenworms = data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms()
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms
count =0 #counter to get information about the first worm
#class named Initial_graphs
class Initial_graphs(object):
    #generates the first 6 worms graphs
    def generate_first_eigenworms(self):
        s = [] # array of 100 equidistant points
        for i in range(1,101):
            a = i/100
            s.append(a)
        count = 1
        #each eigenworm columns represents a Principal Component
        for ew in eigenworms[:6]:
            plt.plot(s, ew, '-') #plots graph
            message = ('Eigenworm: '+ str(count)) #title
            plt.title(message)
            plt.xlabel("s") #x label
            plt.ylabel("θ(rad)") #y label
            plt.show()
            count+=1

ig = Initial_graphs().generate_first_eigenworms()

