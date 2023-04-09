#libraries needed to generate and reconstruct using eigenvectors and eigenvalues the sin wave
import numpy as np
from scipy.linalg import toeplitz
import matplotlib.pyplot as plt

class SinWave(object):
    def generate_matrix(self):
        number = 100 # number of points
        frequency = 10   # Frequency
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
        print(cov_matrix)

        cov_matrix = angles[np.arange(number)[:, None] - np.arange(number)]
        return angles,cov_matrix

    def eigen_decomposition(self,cov_matrix):
        #get the eigenvalues and eigenvectors from the covariance matrix
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        return eigenvalues, eigenvectors

    def sort_eigen(self,eigenvalues, eigenvectors):
        # Sort eigenvalues and eigenvectors
        sort_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvalues = eigenvalues[sort_indices]
        sorted_eigenvectors = eigenvectors[:, sort_indices]
        return sorted_eigenvalues,sorted_eigenvectors
    
    def reconstructed_matrix(self,k, eigenvalues,eigenvectors,matrix):
        eigenvalues_selected = eigenvalues[:k]
        eigenvectors_selected = eigenvectors[:, :k]
        reconstructed_matrix = np.zeros_like(matrix, dtype=np.complex128)
        for i in range(k):
            reconstructed_matrix += eigenvalues_selected[i] * np.outer(eigenvectors_selected[:, i], np.conj(eigenvectors_selected[:, i]))
        reconstructed_matrix = np.real(reconstructed_matrix)
        return reconstructed_matrix
    
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

    def plot_sine_wave(self,angles):
        amplitude = 1
        f=1
        T=1/f
        x = amplitude*np.sin(angles/T)
        plt.plot(angles, x, label='Original Matrix')
        plt.title("Original Sine Wave")
        plt.show()

    def plot_heatmaps(self,reconstructed_matrix,cov_matrix):
        fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5))
        im1 = ax1.imshow(cov_matrix)
        ax1.set_title('Original Matrix')
        im2 = ax2.imshow(reconstructed_matrix)
        ax2.set_title('Reconstructed Matrix')
        fig.colorbar(im1, ax=ax1)
        fig.colorbar(im2, ax=ax2)
        plt.show()

    def sine_wave_heatmap(self,cov_matrix):
        plt.imshow(cov_matrix)
        plt.title('Sine Wave Heatmap')
        plt.colorbar()
        plt.show()

    def plot_error_heatmap(self,reconstructed_matrix,cov_matrix):
        error = cov_matrix - reconstructed_matrix
        #print(error)
        # Plot the heatmap
        plt.imshow(error, cmap='viridis', interpolation='nearest')
        # Add colorbar
        plt.colorbar()
        # Show the plot
        plt.show()

    def main(self):
    
        angles,covariance_matrix = self.generate_matrix()
        eigenvalues, eigenvectors = self.eigen_decomposition(covariance_matrix)
        eigenvalues, eigenvectors = self.sort_eigen(eigenvalues, eigenvectors)
        k = 100
        recon_matrix = self.reconstructed_matrix(k,eigenvalues,eigenvectors,covariance_matrix)
        self.plot_sine_wave(angles)
        self.plot_matrix_vs_reconstructed_matrix(recon_matrix,angles)
        self.sine_wave_heatmap(covariance_matrix)
        self.plot_heatmaps(recon_matrix,covariance_matrix)
        self.plot_error_heatmap(recon_matrix,covariance_matrix)


if __name__ == "__main__":
    SinWave().main()