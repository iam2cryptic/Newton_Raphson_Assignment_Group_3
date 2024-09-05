import sympy as sp
import numpy as np

# Generate the unknowns
def generate_unknowns(bus_data):
    unknowns = []
    for bus in bus_data:
        if bus['type'] == 'PQ':
            unknowns.append(bus['Vmag_symbol'])
            unknowns.append(bus['Vang_symbol'])
        elif bus['type'] == 'PV':
            unknowns.append(bus['Vang_symbol'])
    #print(f"Unknowns: {unknowns}")
    return unknowns

def power_equations_generator(bus_data, admittance_matrix, n):
    power_equations = []
    admittance_matrix = np.round(admittance_matrix, 4)

    # Convert admittance matrix to complex numbers if it's not already

    for bus in bus_data:
        bus_number = bus['bus_number'] - 1
        V_k = bus['Vmag_symbol']
        δ_k = bus['Vang_symbol']

        P_k = 0
        Q_k = 0

        for n in range(len(bus_data)):
            V_n = bus_data[n]['Vmag_symbol']
            δ_n = bus_data[n]['Vang_symbol']

            # Get the admittance matrix element as a complex number
            Y_kn = admittance_matrix[bus_number, n]

            # Calculate power contributions
            θ_kn = np.round(np.angle(Y_kn),4)  # Angle in radians
            Y_kn_mag = np.round(np.abs(Y_kn),4)  # Magnitude

            # SymPy expressions for angle and magnitude
            cos_term = sp.cos(θ_kn + δ_n - δ_k)
            sin_term = sp.sin(θ_kn + δ_n - δ_k)

            P_k += V_k * V_n * Y_kn_mag * cos_term
            Q_k += V_k * V_n * Y_kn_mag * sin_term
            P_k = P_k.evalf(4)
            Q_k = Q_k.evalf(4)

        if bus['type'] == 'PQ':
            power_equations.append(P_k)
            power_equations.append(-Q_k)  # Reactive power should be negative
            # print(f"P_{bus_number + 1} = {P_k}")
            # print(f"Q_{bus_number + 1} = {Q_k}")
            # print("-------------------")
        elif bus['type'] == 'PV':
            power_equations.append(P_k)
            # print(f"P_{bus_number + 1} = {P_k}")
            # print("-------------------")

    return power_equations

# # Example data for a 2-bus system
# bus_data = [
#     {'type': 'PQ', 'Vmag_symbol': sp.symbols('V1'), 'Vang_symbol': sp.symbols('δ1'), 'bus_number': 1},
#     {'type': 'PV', 'Vmag_symbol': sp.symbols('V2'), 'Vang_symbol': sp.symbols('δ2'), 'bus_number': 2},
# ]

# # Admittance matrix in complex form (already complex)
# admittance_matrix = np.array([
#     [1.0 + 0j, 0.1 - 0.1j],
#     [0.1 - 0.1j, 1.0 + 0j]
# ])

# Number of buses
#n = 2

# Call the function
#power_equations = power_equations_generator(bus_data, admittance_matrix, n)

# Output the generated power equations
# for i, eq in enumerate(power_equations):
#     print(f"Equation {i+1}: {eq}")
