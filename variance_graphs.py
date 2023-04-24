from code_gen import EigenData
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import h5py
import math

data = EigenData() #creates instance of class
eigenworms = data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms()
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms

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
            frac_var.append(cumulative_sum/total_var)
        sorted_var = sorted(frac_var)
        # plot the fraction of variance explained
        x = [1,2,3,4,5]
        plt.plot(x, sorted_var,'.',markersize=14)
        plt.xticks(range(1, 6))
        plt.axhline(y=1, color='r', linestyle='-')
        plt.xlabel('K',fontsize=13)
        plt.ylabel(r'$\sigma^2_K$',fontsize=16)
        plt.show()
    def variance_percentages(self,k):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[wormfootage]
                worm = worm.transpose()
                firstrow = worm[k]
            count += 1
        
        print(firstrow)
        total_sum_firstworm = np.sum(firstrow)
        print("Total sum:" ,total_sum_firstworm)
        total_sum_squares = np.sum(np.square(firstrow))
        print("Total sum of squares:",total_sum_squares)
        eigen_square= np.square(firstrow)
        print("Eigenvalues squared:",eigen_square)
        count2=0
        sumv=0
        for value in eigen_square:
            percentage_of_variance = (value / total_sum_squares) * 100
            print("Variance percentage in 2dp: {:.2f}%".format(percentage_of_variance))
            if count2<4:
                sumv = sumv + percentage_of_variance
            count2+=1
        print(sumv)
    def find_sum(self,array):
        total = 0
        for i in array:
            total += i
        print(total)
    
        return total/33600

    def total_variance_percentages(self,s1,s2):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[wormfootage]
                worm = worm.transpose()
            count += 1
        k1 = []
        k2 = []
        k3 = []
        k4 = []
        k5 = []
        sum4 = []
        worm = worm[s1:s2]
        for row in worm:
            total_sum_firstworm = np.sum(row)
            #print("Total sum:" ,total_sum_firstworm)
            total_sum_squares = np.sum(np.square(row))
            #print("Total sum of squares:",total_sum_squares)
            eigen_square= np.square(row)
            #print("Eigenvalues squared:",eigen_square)
            count1=0
            count2=0

            sumv=0
            for value in eigen_square:
                percentage_of_variance = (value / total_sum_squares) * 100
                if count1 == 0:
                    k1.append(percentage_of_variance)
                elif count1 == 1:
                    k2.append(percentage_of_variance)
                elif count1 == 2:
                    k3.append(percentage_of_variance)
                elif count1 == 3:
                    k4.append(percentage_of_variance)
                elif count1 == 4:
                    k5.append(percentage_of_variance)
                    sum4.append(sumv)
                if count2<4:
                    sumv = sumv + percentage_of_variance
                count2+=1
                count1+=1
        k1_sum = sum(k1)/100
        #print("Average value of k1:",k1_sum/1000)
        k2_sum = np.sum(k2)/100
        #print("Average value of k2:",k2_sum/1000)
        k3_sum = np.sum(k3)/100
        #print("Average value of k3:",k3_sum/1000)
        k4_sum = np.sum(k4)/100
        #print("Average value of k4:",k4_sum/1000)
        k5_sum = np.sum(k5)/100
        #print("Average value of k5:",k5_sum/1000)
        Ssum4 = np.sum(sum4)/100
        #print("Average value of sum4:",Ssum4/33600)
        return k1_sum,k2_sum,k3_sum,k4_sum,k5_sum,Ssum4


k=0
#Initial_graphs().variance_modes_function()
#Initial_graphs().variance_percentages(k)
i=0
s1=0
s2=100
array1 = []
array2 = []
array3 = []
array4 = []
array5 = []
array_sum4 = []
for i in range(0,336):
    v1,v2,v3,v4,v5,avg4 = Initial_graphs().total_variance_percentages(s1,s2)
    s1+=100
    s2+=100
    array1.append(v1)
    array2.append(v2)
    array3.append(v3)
    array4.append(v4)
    array5.append(v5)
    array_sum4.append(avg4)
print(array_sum4)
