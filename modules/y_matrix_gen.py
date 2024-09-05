from . import y_matrix as ym
import numpy as np

def admittance_matrix():
    while True:  # Continue until the function succeeds
        try:
            n = int(input("How many buses are there in the system? \n"))
            Z = np.zeros((n, n), dtype=complex)

            for i in range(n):
                for j in range(i, n):  # Only loop for j >= i to ensure symmetry
                    if i == j:
                        Z[i, j] = complex(input(f"Enter the self impedance of bus {i+1}: "))
                    else:
                        Z[i, j] = complex(input(f"Enter the impedance between bus {i+1} and bus {j+1}: "))
                        Z[j, i] = Z[i, j]  # Symmetry: Z[j, i] is the same as Z[i, j]

            #print("The impedance matrix is: \n", Z)
            Y = ym.y_matrix(Z)
            print("The admittance matrix is: \n", Y)
            return Y

        except Exception as e:
            print(f"An error occurred: {e}. Please try again.\n")

def admittance_to_polar(Y):
    n = Y.shape[0]  # Assuming Y is a square matrix
    polar_matrix = np.zeros((n, n), dtype=object)  # Create a matrix to store the polar form

    for i in range(n):
        for j in range(n):
            magnitude = np.abs(Y[i, j])  # Magnitude of the complex number
            angle = np.angle(Y[i, j], deg=True)  # Angle in degrees
            polar_matrix[i, j] = (float(magnitude), float(angle))  # Store as a tuple (magnitude, angle)

    return polar_matrix
