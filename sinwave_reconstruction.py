#libraries needed to generate and reconstruct using eigenvectors and eigenvalues the sin wave
import numpy as np
from scipy.linalg import toeplitz
import matplotlib.pyplot as plt
# class SineWave that has a purpose to use PCA and reconstruct a sin wave
class SineWave(object):
    #function generates initial angles and covariance matrix that will be used in reconstruction
    def generate_matrix(self):
        number = 100 # number of points
        frequency = 1   # Frequency
        amplitude = 1   # Amplitude
        angles = np.linspace(0, 2 * np.pi, num=number, endpoint=False)
        time = np.linspace(0, number/frequency, number)  # Time 
        angles_c = amplitude * np.sin(2 * np.pi * frequency * time) #angles
        #This will create an array called angles with 100 equally spaced angles between 0 and 2π,
        #where the endpoint=False argument means that the end point 2π is not included in the angles
        #construct covariance matrix
        #finds the mean 
        mean_angles = np.mean(angles_c)
        length = len(angles_c) 
        #fills new matrix of same size with zeros
        temp_covariance = np.zeros((length,))
        #calculates (xi-mean) and (xi-mean)^T(transpose)
        #multiplies these two values and divides with their total value
        for value in range(length):
            current = length - value
            s =(angles_c[:current] - mean_angles)
            m = s.transpose()
            temp_covariance[value] = np.sum(s*m) / length
        #calculates covariance matrix with absolute value of each element
        cov_matrix = np.zeros((length, length))
        for x in range(length):
            for y in range(length):
                cov_matrix[x,y] = temp_covariance[np.abs(x-y)]

        cov_matrix = angles[np.arange(number)[:, None] - np.arange(number)]
        #returns angles and covariance matrix
        return angles,cov_matrix
    #calculates eigenvalues and eigenvectors from covariance matrix
    def eigen_decomposition(self,cov_matrix):
        #get the eigenvalues and eigenvectors from the covariance matrix
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        return eigenvalues, eigenvectors
    #sorting in desc order function
    def sort_eigen(self,eigenvalues, eigenvectors):
        # Sort eigenvalues and eigenvectors in descending order based on the eigenvalues
        sort_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[sort_indices]
        sorted_eigenvectors = eigenvectors[:, sort_indices]
        return sorted_eigenvalues,sorted_eigenvectors
    #function that takes the number of eigenvectors needed for reconstruction, eigenvalues, eigenvectors and covariance matrix
    def reconstructed_matrix(self,k, eigenvalues,eigenvectors,covariance_matrix):
        #creates an array of zeros with the same shape as the covariance matrix
        reconstructed_matrix = np.zeros_like(covariance_matrix, dtype=np.complex128)
        #loop up to 'k' eigenvalues and eigenvectors
        abs_eigenvalues = np.abs(eigenvalues)
        current_sum_eigenvalues = np.sum(abs_eigenvalues)
        for i in range(k):
            eigenvector_value = eigenvectors[:,i] #eigenvector
            eigenvector_value_conjugate = np.conj(eigenvectors[:, i]) #eigenvector conjugate
            final_eigenvector = np.outer(eigenvector_value,eigenvector_value_conjugate) #final eigenvector
            element = eigenvalues[i] * final_eigenvector  # element to be added in reconstructed matrix
            reconstructed_matrix += element
        reconstructed_matrix = np.real(reconstructed_matrix) # takes only the real part of the array

        return reconstructed_matrix,current_sum_eigenvalues
    #function plots the original matrix next to the final reconstructed
    def plot_matrix_vs_reconstructed_matrix(self,reconstructed_matrix,angles):
        figure, axis = plt.subplots(1, 2,figsize=(10, 5))
        amplitude = 1
        f=1
        T=1/f
        x_recon = amplitude*np.sin(reconstructed_matrix/T)
        x = amplitude*np.sin(angles/T)
        axis[0].set_title("Original Matrix")
        axis[0].plot(angles, x, label='Original Matrix')
        axis[0].set_title("Original Matrix")
        axis[1].plot(angles, x_recon[:, 0], label='Reconstructed Matrix')
        axis[1].set_title("Reconstructed Matrix")
        plt.show()
    #function plots initial sine wave
    def plot_sine_wave(self,angles):
        amplitude = 1
        f=1
        T=1/f
        x = amplitude*np.sin(angles/T)
        plt.plot(angles, x, label='Original Matrix')
        plt.title("Original Sine Wave")
        plt.show()
    #function plots the reconstructed wave
    def plot_reconstructed(self,reconstructed_matrix,angles):
        amplitude = 1
        f=1
        T=1/f
        x_recon = amplitude*np.sin(reconstructed_matrix/T)
        plt.plot(angles, x_recon[:, 0], label='Reconstructed Matrix')
        plt.title("Reconstructed Matrix")
        plt.show()
    #function plots heatmap of covariance matrix next to the heatmap of the reconstructed matrix
    def plot_heatmaps(self,reconstructed_matrix,cov_matrix):
        fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5))
        im1 = ax1.imshow(cov_matrix)
        ax1.set_title('Original Matrix')
        im2 = ax2.imshow(reconstructed_matrix)
        ax2.set_title('Reconstructed Matrix')
        fig.colorbar(im1, ax=ax1)
        fig.colorbar(im2, ax=ax2)
        plt.show()
    #function plots only the original covariance matrix heatmap
    def sine_wave_heatmap(self,cov_matrix):
        plt.imshow(cov_matrix)
        plt.title('Sine Wave Heatmap')
        plt.colorbar()
        plt.show()
    #function plots the heatmap of the reconstructed wave
    def reconstructed_wave_heatmap(self,reconstructed_matrix):
        plt.imshow(reconstructed_matrix)
        plt.title('Reconstructed Wave Heatmap')
        plt.colorbar()
        plt.show()
    #function plots a heatmap showing the error between the original and reconstructed matrices
    def plot_error_heatmap(self,reconstructed_matrix,cov_matrix):
        difference = np.abs(cov_matrix - reconstructed_matrix)
        mean_difference = np.mean(difference)
        error_percentage = mean_difference/np.mean(cov_matrix)
        print("Error in reconstruction" ,np.real(error_percentage)*100,"%")
        # Plot the heatmap
        plt.imshow(difference, cmap='viridis', interpolation='nearest')
        # Add colorbar
        plt.colorbar()
        # Show the plot
        plt.show()
    #main function in class
    def main(self):
        angles,covariance_matrix = self.generate_matrix() # gets angles and resulted covariance matrix
        eigenvalues, eigenvectors = self.eigen_decomposition(covariance_matrix) #eigenvalues and eigenvectors from cov matrix
        eigenvalues, eigenvectors = self.sort_eigen(eigenvalues, eigenvectors) #sorts eigenvalues with corresponding eigenvectprs
        k = 100
        print("Number of components used:" ,k)
        current_eigenvalues = eigenvalues[:k] #takes needed eigenvalues specified by k
        current_eigenvectors = eigenvectors[:, :k] #takes needed eigenvectors specified by k
        #finds the reconstructed matrix and the current sum of eigenvalues
        recon_matrix,current_sum_eigenvalues = self.reconstructed_matrix(k,current_eigenvalues,current_eigenvectors,covariance_matrix)
        #finds the reconstructed matrix and sum of all 100 eigenvalues
        recon_full_matrix,total_sum_eigenvalues = self.reconstructed_matrix(100,eigenvalues[:100],eigenvectors[:, :100],covariance_matrix)
        #variance calculations 
        variance_percentage = current_sum_eigenvalues/total_sum_eigenvalues * 100
        print("Current sum of eigenvalues", np.real(current_sum_eigenvalues))
        print("Total sum of eigenvalues", np.real(total_sum_eigenvalues))
        print("Percentage of variance", np.real(variance_percentage),"%")
        #plots sinewave
        self.plot_sine_wave(angles)
        #plots reconstructed wave
        self.plot_reconstructed(recon_matrix,angles)
        #self.plot_matrix_vs_reconstructed_matrix(recon_matrix,angles)
        #plots sine wave heatmap
        self.sine_wave_heatmap(covariance_matrix)
        #plots sine wave reconstructed heatmap
        self.reconstructed_wave_heatmap(recon_matrix)
        #self.plot_heatmaps(recon_matrix,covariance_matrix)
        #plots error heatmap of difference of actual with reconstructed values
        self.plot_error_heatmap(recon_matrix,covariance_matrix)

#the main function is called first in the Sine Wave class
if __name__ == "__main__":
    SineWave().main()