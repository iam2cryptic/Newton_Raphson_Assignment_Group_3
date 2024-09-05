import numpy as np

# Calculate the admittance matrix Y from the impedance matrix Z
def y_matrix(Z):
    n = len(Z)
    Y = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            if i == j:
                # Sum of the reciprocals of the impedances connected to the bus
                 Y[i, j] = sum(1 / Z[i, k] if np.abs(Z[i, k]) != 0 else 0 for k in range(n))
            else:
                # Negative reciprocal of the impedance between different buses
                if np.abs(Z[i, j]) != 0:
                    Y[i, j] = -1 / Z[i, j]
                else:
                    Y[i, j] = 0
    return np.round(Y, 2)
