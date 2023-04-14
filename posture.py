#libraries used
import numpy as np
import scipy.io
import h5py
import math
import matplotlib.pyplot as plt
#class EigenData was taken from stephens-2d-eigenworm-data gitlab repository from test.py in order to generate the data
#functions __init__(), get_eigenworms(),get_footage() and reconstruct() were taken from that python script
#https://gitlab.com/tom-ranner/stephens-2d-eigenworm-data/-/blob/master/stephens-2011-data/test.py
class EigenData(object):
    '''Represents the original experiment data.'''
    #RECONSTRUCTS USING ALL PCs
    #init function
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def __init__(self):
        self._eigenworms = None #sets variable to None
    #function returns eigenworms array that is an 100x100 array, where the columns are the eigenworms used and the rows correspond to each angle value of midline points
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def get_eigenworms(self, eigen_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Eigenworms are stored as 100 'angles' at equidistributed coordinates
        down the body.
        '''
        # Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(eigen_path)
        self._eigenworms = eigenworms["EigenWorms"].transpose() # transposes array ( changes columns with rows)
        return self._eigenworms
    
    #function returns footage dictionary that has the eigenvalues array for each of the 12 worms
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def get_footage(self, footage_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Footage is stored as coefficients with respect to the eigenworm basis.
        '''
        f = h5py.File(footage_path, 'r') # opens file in read mode
        footage = {} # creates empty dictionary
        for k, v in f.items(): # key, value in dictionary f
            if k != 'tr':
                for k2, v2 in v.items(): #key2, value2 in previous value
                    if v2.shape == (5, 33600) or v2.shape == (6, 33600): #checks shape of value2 
                        footage[k2] = np.array(v2) #takes array of eigenvalues
        return footage #returns array
    

    #function reconstructs the angles 
    #function was taken from stephens-2d-eigenworm-data gitlab repository from test.py
    def reconstruct(self, coefficients):
        '''
        Reconstruct multiple postures from basis coefficients to angles.
        '''
        n_basis_required = coefficients.shape[0] #takes the number of columns which is the number of PCs used
        return self._eigenworms[0:n_basis_required, :].transpose() @ \
            coefficients # multiplies eigenworms with corresponding eigenvalues to get the angles in order to reconstruct posture
    

    #function calculates the endpoint of the segment based on the start point and the angle
    def segment_endpoint(self,segment_start,angle):
        theta = angle # angles theta (θ) is measured in radians
        length = 0.01
        start_x = segment_start[0] # start of segment x point
        start_y = segment_start[1] # start of segment y point
        end_x = start_x + length * math.cos(theta) # end of segment x point
        end_y = start_y + length * math.sin(theta) # end pf segment y point
        end_point = (end_x, end_y) # final endpoint tuple ( x,y)
        return end_point # returns endpoint
    
    #function calculates array of segments, where each segment includes the x,y coordinates of the start point and the end point
    def line_of_segment(self,start_p,angles):
        segments_array = [] # creates array of segments
        segment_start = start_p #start point of segment
        for angle in angles:
            segment_end = self.segment_endpoint(segment_start, angle) 
            #calls the function to return the coordinates of the end point based on the start point and the angle
            segments_array.append((segment_start, segment_end)) # appends tuple of x,y coordinates of start point and end point
            #format of each point: (segment_start, segment_end) -> ((x_start,y_start),(x_end,y_end))
            segment_start = segment_end # start of new segment becomes the end of previous segment
        return segments_array # returns array of tuples of x,y coordinates of start point and end point
    
    #function plots graph showing the angles at each of the 100 points on the midline of the worm
    def plot_angles(self,angles,s):
        #angles: array of 100 angles measured in radians
        #s: coordinates of 100 equidistant points on the midline of the worm
        plt.plot(s, angles,'--.') # plots angles with s
        plt.axhline(y=0, color='r', linestyle='--') #plots a straight line at y=0
        plt.ylabel('θ(rad)',fontsize=13) # x label
        plt.xlabel('s',fontsize=16) #y label
        plt.show() # show the graph



if __name__ == "__main__":
    data = EigenData() #creates instance of class
    data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms()

    footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms
    s=[] #array of 100 equidistant points 
    #each point is distant 0.01 
    for i in range(1,101):
            s.append(i/100)
    count =0 #uses count to use the data only for the first worm
    for k in footage.keys():
        if count == 0: # first worm
            r = data.reconstruct(footage[k]) #calls function to reconstruct angles for the first worm
        count+=1
    r = r.transpose() # switches columns with rows using transpose built-in function
    f_angles =r[0] #first worm angles
    sum=0
    for a in f_angles:
        sum = sum+a #total sum of all angles for the first worm
    mean_angle = sum/100 #mean angle is nearly zero
    #for loop for each frame of the worm
    for frames in range(0,33600):
        angles = r[frames] # angles array
        angles = angles[::-1] 
        #reverse it so the s=0 which is the head should be at the right end
        #s=1 which is tail should be the first angle in the reversed array
        start_point = (0,0) #start point of the worm
        X = [] #array of X coordinates
        Y = [] #array of Y coordinates
        #the indexes match to points
        seg = data.line_of_segment(start_point,angles) #returns array of segments for that frame
        plt.clf() #clears figure to show next frame
        for element in seg: #for each segment where element is  (segment_start, segment_end) -> ((x_start,y_start),(x_end,y_end))
            maxx=-100 #uses maxx and maxy to find the coordinates of the head 
            maxy=-100
            if element[0][0]>=maxx:
                maxx= element[0][0]
            if element[1][0]>=maxx:
                maxx = element[1][0]
            if element[0][1]>=maxy:
                maxy = element[0][1]
            if element[1][1]>=maxy:
                maxy = element[1][1]
            X.append(element[0][0]) #appends X coordinates to X array
            X.append(element[1][0]) #appends X coordinates to X array
            Y.append(element[0][1]) # appends Y coordinates to Y array
            Y.append(element[1][1]) # appends Y coordinates to Y array
        plt.plot(X, Y, '-')     #plots the points using - to create segments
        plt.plot(maxx,maxy,'.',color='red') #the head is indicated with a red dot
        plt.pause(0.04) #each frame has a pause of 0.04s which is equal to 40ms like the actual time value

           
    plt.show() #shows plot 
  