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
def choose_k_eigenvectors(k,eigenvalues,eigenvectors):
    eigenvalues_selected = eigenvalues[:k]
    eigenvectors_selected = eigenvectors[:, :k]
    return eigenvalues_selected,
def reconstructed_matrix(k, eigenvalues,eigenvectors,matrix):
    reconstructed_matrix = np.zeros_like(matrix, dtype=np.complex128)
    for i in range(k):
        reconstructed_matrix += eigenvalues[i] * np.outer(eigenvectors[:, i], np.conj(eigenvectors[:, i]))
    reconstructed_matrix = np.real(reconstructed_matrix)
    return reconstructed_matrix
def plot_matrix_vs_reconstructed_matrix(reconstructed_matrix,angles):
    figure, axis = plt.subplots(1, 2,figsize=(10, 5))
    amplitude = 1
    f=1
    T=1/f
    x_recon = amplitude*np.sin(reconstructed_matrix/T)
    x = amplitude*np.sin(angles/T)
    axis[0].plot(angles, x, label='Original Matrix')
    axis[0].set_title("Original Matrix")
    axis[1].plot(angles, x_recon[:, 0], label='Reconstructed Matrix')
    axis[1].set_title("Reconstructed Matrix")
    plt.show()

def plot_histograms(reconstructed_matrix,cov_matrix):
    fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5))
    im1 = ax1.imshow(cov_matrix)
    ax1.set_title('Original Matrix')
    im2 = ax2.imshow(reconstructed_matrix)
    ax2.set_title('Reconstructed Matrix')
    fig.colorbar(im1, ax=ax1)
    fig.colorbar(im2, ax=ax2)
    plt.show()
def main():
    angles,covariance_matrix = generate_matrix()
    eigenvalues, eigenvectors = eigen_decomposition(covariance_matrix)
    eigenvalues, eigenvectors = sort_eigen(eigenvalues, eigenvectors)
    k = 90
    eigenvalues_selected,eigenvectors_selected=choose_k_eigenvectors(k,eigenvalues,eigenvectors)
    recon_matrix = reconstructed_matrix(k,eigenvalues_selected,eigenvectors_selected,covariance_matrix)
    plot_matrix_vs_reconstructed_matrix(recon_matrix,angles)
    plot_histograms(recon_matrix,covariance_matrix)
if __name__ == "__main__":
    main()