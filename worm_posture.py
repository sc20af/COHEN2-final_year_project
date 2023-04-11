
import numpy as np
import scipy.io
import h5py
import math
import matplotlib.pyplot as plt
#class EigenData was taken from stephens-2d-eigenworm-data gitlab repository from test.py in order to generate the data
class EigenData(object):
    '''Represents the original experiment data.'''
    #RECONSTRUCTS USING ONLY 2 PCs
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
        n_basis_required = 2
        coefficients = coefficients[:2]
        rec =self._eigenworms[0:n_basis_required, :].transpose() @ \
            coefficients
        return(rec)
    
    def segment_endpoint(self,start_p,ang,len):
        theta = ang 
        end_point = (start_p[0] + len * math.cos(theta), start_p[1] + len * math.sin(theta))
        return end_point
    
    def line_of_segment(self,start_p,angles):
        segments_array = []
        previous_end = start_p
        for angle in angles:
            len = 0.01
            segment_end = self.segment_endpoint(previous_end,angle,len)
            segments_array.append((previous_end, segment_end))
            previous_end = segment_end
        return segments_array


if __name__ == "__main__":
    data = EigenData()
    data.get_eigenworms('EigenWorms.mat')

    footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat')
    s=[]
    for i in range(1,101):
            s.append(i/100)
    count = 0
    for k in footage.keys():
        if count == 0: # first worm
            r = data.reconstruct(footage[k])
        count+=1
    r = r.transpose()
    
    for frames in range(0,33600):
        angles = r[frames]
        angles = angles[::-1]
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
        plt.plot(maxx,maxy,'.',color='red') #head
        plt.pause(0.04)
           
    plt.show()
  