#libraries needed to generate and reconstruct using eigenvectors and eigenvalues the sin wave
import numpy as np
from scipy.linalg import toeplitz
import matplotlib.pyplot as plt

#this functions prints 2 graphs showing the original matrix and the reconstructed matrix using PCA
def plot_PCA(original_matrix,k,eigenvectors,eigenvalues):
    reconstructed_matrix = np.zeros_like(original_matrix)
    reconstructed_matrix = reconstructed_matrix.astype(np.complex128)
    for item in range(0,k):
        egvec = np.outer(eigenvectors[:, item], np.conj(eigenvectors[:, item]))
        # Multiply eigenvector by the corresponding eigenvalue
        final = eigenvalues[item] * egvec
        # Adds multiplication recursively to the reconstructed matrix
        reconstructed_matrix += final
    
    # Convert the reconstructed matrix to real numbers
    reconstructed_matrix = np.real(reconstructed_matrix)
    
    # Plot original and reconstructed matrix
    figure, axis = plt.subplots(1, 2,figsize=(10, 5))
    om = axis[0].imshow(original_matrix)
    axis[0].set_title('Original Matrix')
    rm = axis[1].imshow(reconstructed_matrix)
    axis[1].set_title('Reconstructed Matrix')
    plt.colorbar(om)
    plt.colorbar(rm)
    plt.show()

def plot_functions():
    # Generates 100 angles
    angles = np.linspace(0, 2 * np.pi, num=100, endpoint=False)
    #This will create an array called angles with 100 equally spaced angles between 0 and 2π,
    #where the endpoint=False argument means that the end point 2π is not included

    # Generate sine wave
    f = 1  # frequency 
    T = 1/f #period: time needed for a wave to pass from a specific point

    x = np.sin(angles/T) # finds x coordinates based on the angles 

    #  items of x moved by 1 position to the left
    matrix = toeplitz(x, np.roll(x, -1))

    # Finds eigenvectors and corresponding eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    #print(len(eigenvalues)) 100 eigenvalues and 100 corresponding eigenvectors
    # Choose the first k eigenvectors
    k = 100
    eigenvalues_selected = eigenvalues[:k]
    eigenvectors_selected = eigenvectors[:, :k]

    # Initialise the subplot function using number of rows and columns
    figure, axis = plt.subplots(1, 2,figsize=(10, 5))
    # Multiply eigenvectors and eigenvalues to get back original sine wave
    x_recon = eigenvectors_selected @ np.diag(eigenvalues_selected) 
    x_recon = x_recon @ np.linalg.inv(eigenvectors_selected)


    # Plot original and reconstructed wave
    axis[0].plot(angles, x, label='Original Matrix')
    axis[0].set_title("Original Matrix")
    axis[1].plot(angles, x_recon[:, 0], label='Reconstructed Matrix')
    axis[1].set_title("Reconstructed Matrix")
    #plt.legend()
    plot_PCA(matrix,k,eigenvectors_selected,eigenvalues_selected)
    plt.show()

plot_functions()