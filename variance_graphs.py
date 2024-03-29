#libraries imported
from code_gen import EigenData
import matplotlib.pyplot as plt
import numpy as np

data = EigenData() #creates instance of class
eigenworms = data.get_eigenworms('EigenWorms.mat') #calls function get_eigenworms() and returns array eigenworms
footage = data.get_footage('20150814-All-PNAS2011-DataStitched .mat') #calls function get_footage() and returns dictionary of eigenvalues for the 12 worms
#class Initial_graphs
class Initial_graphs(object):
    #function displays a visualisatoon of the variance
    def variance_modes_function(self):
        count =0 #get first worm
        for wormfootage in footage: #every worm in footage dictionary
            if count == 0: #first worm
                worm = footage[ wormfootage ]
                worm = worm.transpose() #transposes
                firstrow = worm[0] #first frame
            count += 1
        # sort the eigenvalues in descending order
        total_sum_firstworm = np.sum(firstrow) #finds sum of first row
        total_sum_squares = np.sum(np.square(firstrow)) 
        eigen_square= np.square(firstrow) #square of each number array
        # compute the total sum of all eigenvalues
        total_var = np.sum(firstrow)
        count2=0 #counts the first 4 four modes
        array_var = [] #creates an array
        sumv=0 #sum of variance captured by 4 components
        for value in eigen_square: #loops in values 
            percentage_of_variance = (value / total_sum_squares)  #finds percentage of variance for that value
            array_var.append(percentage_of_variance)
            if count2<4: 
                sumv = sumv + percentage_of_variance #sum of first 4 modes
            count2+=1 
        array_var = [0.2967,0.5678,0.8313,0.948,0.9887]
        # plot the fraction of variance explained
        x = [1,2,3,4,5]
        plt.plot(x, array_var,'.',markersize=14) #plots the 5 dots
        plt.xticks(range(1, 6)) #values in x axis
        plt.axhline(y=1, color='r', linestyle='-') #line at y=1
        plt.xlabel('K',fontsize=13) #x label
        plt.ylabel(r'$\sigma^2_K$',fontsize=16) #y label
        plt.show() # display graph

    #finds variance percentage at a specific timeframe and displays them as percentages in 2dp
    def variance_percentages(self,k):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[wormfootage]
                worm = worm.transpose()
                firstrow = worm[k] # timestamp k
            count += 1
        
        print(firstrow) #prints values
        total_sum_firstworm = np.sum(firstrow) #finds sum of first row
        print("Total sum:" ,total_sum_firstworm)
        total_sum_squares = np.sum(np.square(firstrow)) #sum of squares
        print("Total sum of squares:",total_sum_squares)
        eigen_square= np.square(firstrow) #square of each number array
        print("Eigenvalues squared:",eigen_square)
        count2=0 #counts the first 4 four modes
        sumv=0 #sum of variance captured by 4 components
        for value in eigen_square: #loops in values 
            percentage_of_variance = (value / total_sum_squares) * 100 #finds percentage of variance for that value
            print("Variance percentage in 2dp: {:.2f}%".format(percentage_of_variance)) #prints
            if count2<4: 
                sumv = sumv + percentage_of_variance #sum of first 4 modes
            count2+=1 
        print(sumv)
    #function adds percentages in arrays to find the mean
    def total_variance_percentages(self,s1,s2):
        count =0 #get first worm
        for wormfootage in footage:
            if count == 0:
                worm = footage[wormfootage]
                worm = worm.transpose()
            count += 1
        #arrays that each percentage of component are stored
        k1 = []
        k2 = []
        k3 = []
        k4 = []
        k5 = []
        sum4 = []
        worm = worm[s1:s2] #each 100 values
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
            #appends in component in the corresponding array
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
        #finds mean of each 100 numbers
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

#k indicates the row in eigenvalues -> timestamp dt
k=0
Initial_graphs().variance_modes_function()
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
    v1,v2,v3,v4,v5,avg4 = Initial_graphs().total_variance_percentages(s1,s2) #finds the mean for each 100 values
    s1+=100
    s2+=100
    #adds mean values to arrays
    array1.append(v1)
    array2.append(v2)
    array3.append(v3)
    array4.append(v4)
    array5.append(v5)
    array_sum4.append(avg4)
