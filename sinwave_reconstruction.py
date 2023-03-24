#libraries needed to generate and reconstruct using eigenvectors and eigenvalues the sin wave
import numpy as np
from scipy.linalg import toeplitz
import matplotlib.pyplot as plt

def generate_matrix():
    angles = np.linspace(0, 2 * np.pi, num=100, endpoint=False)
    #This will create an array called angles with 100 equally spaced angles between 0 and 2π,
    #where the endpoint=False argument means that the end point 2π is not included in the angles
    #construct covariance matrix
    cov_matrix = angles[np.arange(100)[:, None] - np.arange(100)]
    return angles,cov_matrix
def eigen_decomposition(matrix):
    #get the eigenvalues and eigenvectors from the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors
def sort_eigen(eigenvalues, eigenvectors):
    # Sort eigenvalues and eigenvectors
    sort_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sort_indices]
    sorted_eigenvectors = eigenvectors[:, sort_indices]
    return sorted_eigenvalues,sorted_eigenvectors
def main():
    angles,covariance_matrix = generate_matrix()
    eigenvalues, eigenvectors = eigen_decomposition(covariance_matrix)
    eigenvalues, eigenvectors = sort_eigen(eigenvalues, eigenvectors)

if __name__ == "__main__":
    main()