from code_generation import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

ed = EigenData("EigenWorms.mat", "20150814-All-PNAS2011-DataStitched .mat")
eigenworms, footage = ed.get_data()

class Initial_graphs(object):

    def variance_modes_function(self):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[ wormfootage ]
                worm = worm.transpose()
                firstrow = worm[0]
            count += 1
        # sort the eigenvalues in descending order
        idx = np.argsort( firstrow )[::-1]
        firstrow = firstrow[idx]
        firstrow = firstrow[::-1]
        # compute the total sum of all eigenvalues
        total_var = np.sum(firstrow)
        #print(total_var)
        frac_var = []
        cumulative_sum = 0
        for k in range(1, len(firstrow)+1):
            cumulative_sum += firstrow[k-1]
            frac_var.append(cumulative_sum/10)
        for i in range(0,3):
            frac_var.append(1)
        # plot the fraction of variance explained
        plt.plot(range(1, len(firstrow)+4), frac_var,'.',markersize=14)
        plt.axhline(y=1, color='r', linestyle='-')
        plt.xlabel('Number of eigenvalues')
        plt.ylabel('Fraction of variance explained')
        plt.show()


    def variance_with_s(self):
        count =0
        for wormfootage in footage:
            if count == 0:
                worm = footage[wormfootage]
                worm = worm.transpose()
                #print(worm)
            count+=1
        first_row = worm[0]/10   
        count =0
        w = []
        a=0
        s=[]
        for i in range(1,101):
            s.append(i/100)
        #print(eigenworms[0])
        array_w = []
        for item in first_row:
            w = item*eigenworms[count]
            a+=w
            array_w.append(a)
        for i in range(0,5):
             plt.plot(s,array_w[i]*(i+1) ,label='Curve {}'.format(i+1))
        plt.axhline(y=1, linestyle='--', color='black')
        # add a legend, x-label, and y-label
        plt.legend()
        plt.xlabel('X-axis Label')
        plt.ylabel('Y-axis Label')
        # show the plot
        plt.show()
        # count =0
        # for wormfootage in footage:
        #     if count == 0:
        #         worm = footage[wormfootage]
        #         worm = worm.transpose()
        #         #print(worm)
        #         firstrow=worm[0]
        #     count+=1
        # ew = eigenworms[:5]
        # idx = np.argsort( firstrow )[::-1]
        # firstrow = firstrow[idx]
        # firstrow = firstrow[::-1]
        # ew = ew[idx]
        # ew = ew[::-1]
        # # compute the total sum of all eigenvalues
        # total_var = np.sum(firstrow)
        # #print(total_var)
        # frac_var = []
        # cumulative_sum = 0
        # for k in range(1, len(firstrow)+1):
        #     cumulative_sum += firstrow[k-1]
        #     frac_var.append(cumulative_sum/10)
        # print(frac_var)
        # # eigenvalues = worm[0]
        # # sum_of_eigenvalues = eigenvalues[0]+eigenvalues[1]+eigenvalues[2]+eigenvalues[3]+eigenvalues[4]
        # # print(eigenvalues)
        # s=[]
        # for i in range(1,101):
        #     s.append(i/100)
        
        # # final_array = []
        # # final_array.append(ew[0]*eigenvalues[0]/sum_of_eigenvalues)
        # # final_array.append(final_array[0] +ew[1]*eigenvalues[1]/sum_of_eigenvalues)
        # # final_array.append(final_array[1] + ew[2]*eigenvalues[2]/sum_of_eigenvalues)
        # # final_array.append(final_array[2] + ew[3]*eigenvalues[3]/sum_of_eigenvalues)
        # # final_array.append(final_array[3] + ew[4]*eigenvalues[4]/sum_of_eigenvalues)
        # for i in range(0,5):
        #     #plt.plot(s,final_array[i]*(i+1) ,label='Eigenworm {}'.format(i+1))
        #     plt.plot(s,frac_var[i]*ew[i]*(i+1) ,label='Eigenworm {}'.format(i+1))
        # plt.axhline(y=1, linestyle='--', color='black')

        # # add a legend, x-label, and y-label
        # plt.legend()
        # plt.xlabel('X-axis Label')
        # plt.ylabel('Y-axis Label')
        # # show the plot
        # plt.show()





    
Initial_graphs().variance_modes_function()
#Initial_graphs().variance_with_s()