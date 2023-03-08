
import numpy as np
import scipy.io
import h5py
import matplotlib.pyplot as plt
from matplotlib import animation
#optimisation-algorithms-analysis
class EigenData(object):
    '''Represents the original experiment data.'''

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
        print(self._eigenworms[0:n_basis_required, :].transpose().shape,
              coefficients.shape)
        return self._eigenworms[0:n_basis_required, :].transpose() @ \
            coefficients
    def data_r(self):
        s=[]
        for i in range(1,101):
            s.append(i/100)
        for k in footage.keys():
        #print(k, footage[k].shape)
            r = data.reconstruct(footage[k])
        r = r.transpose()
        return r
    
  

if __name__ == "__main__":
    data = EigenData()
    data.get_eigenworms('EigenWorms.mat')

    footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat')
    s=[]

    for i in range(1,101):
            s.append(i/100)

    for k in footage.keys():
        #print(k, footage[k].shape)
        r = data.reconstruct(footage[k])

    r = r.transpose()

    print('-->', r[0])

    for frame in range(0,33600):
        plt.clf()
        plt.scatter(s, r[frame],s=10,color='blue')
        plt.plot(s, r[frame], '.--')
        plt.pause(0.001)


       

        #plt.title("Curvature as a function of θ(s)") 
        #plt.xlabel("s")
        #plt.ylabel("θ(rad)")

    plt.show()
  