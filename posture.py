
import numpy as np
import scipy.io
import h5py
import math
import matplotlib.pyplot as plt
#class EigenData was taken from stephens-2d-eigenworm-data gitlab repository from test.py in order to generate the data
#https://gitlab.com/tom-ranner/stephens-2d-eigenworm-data/-/blob/master/stephens-2011-data/test.py
class EigenData(object):
    '''Represents the original experiment data.'''
    #RECONSTRUCTS USING ALL PCs
    def __init__(self):
        self._eigenworms = None

    def get_eigenworms(self, eigen_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Eigenworms are stored as 100 'angles' at equidistributed coordinates
        down the body.
        '''
        # Load the matlab files into numpy arrays
        eigenworms = scipy.io.loadmat(eigen_path)
        self._eigenworms = eigenworms["EigenWorms"].transpose()
        return self._eigenworms

    def get_footage(self, footage_path):
        '''
        Loads the matlab files from the original experiment and parses them
        into expected numpy formats.

        Footage is stored as coefficients with respect to the eigenworm basis.
        '''
        f = h5py.File(footage_path, 'r')
        footage = {}
        for k, v in f.items():
            if k != 'tr':
                for k2, v2 in v.items():
                    if v2.shape == (5, 33600) or v2.shape == (6, 33600):
                        footage[k2] = np.array(v2)
        return footage

    def reconstruct(self, coefficients):
        '''
        Reconstruct multiple postures from basis coefficients to angles.
        '''
        n_basis_required = coefficients.shape[0]
        #print(self._eigenworms[0:n_basis_required, :].transpose().shape,
              #coefficients.shape)
        return self._eigenworms[0:n_basis_required, :].transpose() @ \
            coefficients
    #function calculates the endpoint of the segment based on the start point and the angle
    def segment_endpoint(self,segment_start,length,angle):
        theta = angle # angles theta (θ) is measured in radians
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
            length = 0.01 #length is fixed since we have 100 point and a total arc length s=1
            segment_end = self.segment_endpoint(segment_start, length, angle) 
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
    data = EigenData()
    data.get_eigenworms('EigenWorms.mat')

    footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat')
    s=[]
    for i in range(1,101):
            s.append(i/100)
    count =0
    for k in footage.keys():
        if count == 0: # first worm
            r = data.reconstruct(footage[k])
        count+=1
    print(r.shape)
    r = r.transpose()
    f_angles =r[0]
    sum=0
    for a in f_angles:
        sum = sum+a
    print("Mean angle:", sum/100)
    s = []
    for i in range(1,101):
        s.append(i/100)

    #data.plot_angles(f_angles,s)
    #count2 =0
    for frames in range(0,33600):
        angles = r[frames]
        angles = angles[::-1] 
        #we reverse it so the s=0 which is the head should be at the right end
        #s=1 which is tail should be the first angle in the reversed array
        start_point = (0,0)
        X = []
        Y = []
        seg = data.line_of_segment(start_point,angles)
        plt.clf()
        for element in seg:
            maxx=-100
            maxy=-100
            if element[0][0]>=maxx:
                maxx= element[0][0]
            if element[1][0]>=maxx:
                maxx = element[1][0]
            if element[0][1]>=maxy:
                maxy = element[0][1]
            if element[1][1]>=maxy:
                maxy = element[1][1]
            X.append(element[0][0])
            X.append(element[1][0])
            Y.append(element[0][1])
            Y.append(element[1][1])
        plt.scatter(X,Y,marker='')
        plt.plot(X, Y, '-')
        plt.plot(maxx,maxy,'.',color='red')
        plt.pause(0.04)
        #start_point = element(len(element))
        
           
    plt.show()
  