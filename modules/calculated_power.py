import numpy as np

def calculated_power(buses, Y, n):
    S = np.zeros((n, 1), dtype=complex)
    assumed_voltage = 1 #buses[0]['Vmag']
    assumed_angle = 0 #buses[0]['Vang']

    for bus in buses:
        if bus['type'] == "PQ" and bus['Vmag']== '' and bus['Vang'] == '':
            bus["Vmag"] = assumed_voltage
            bus["Vang"] = assumed_angle
        elif bus['type'] == "PV" and bus['Vang'] == '':
            bus["Vang"] = assumed_angle

    # Calculate the current at each bus
    voltage = []
    for bus in buses:
        try:
            Vmag = float(bus['Vmag'])  # Ensure Vmag is a float
            Vang = float(bus['Vang'])  # Ensure Vang is a float
            voltage.append(Vmag * np.exp(1j * Vang))
        except (ValueError, KeyError) as e:
            print(f"Error converting bus data to voltage: {e}")
            return None
    print(buses)
    voltage = np.array(voltage).reshape(-1, 1)
    print("Voltage:", voltage)

    # Calculate the current at each bus
    current = np.dot(Y, voltage)

    # Calculate the power at each bus
    for i in range(n):
        Vi_conj = np.conjugate(voltage[i])
        S[i] = np.round(Vi_conj * current[i], 4)


    # Deconstruct the power into real and reactive power
    deconstructed_power_list = []

    # Deconstruct the power into real and reactive power and flatten it into a column vector
    for i, bus in enumerate(buses):
        if bus['type'] == "Vθ":
            continue
        elif bus['type'] == "PQ":
            deconstructed_power_list.extend([S[i].real, -S[i].imag])  # Add both real and reactive power
        elif bus['type'] == 'PV':
            deconstructed_power_list.append(S[i].real)  # Add only real power for PV buses

    # Convert the list to a NumPy column vector (2D array with shape (n, 1))
    deconstructed_power = np.array(deconstructed_power_list, dtype=float).reshape(-1, 1)

    return deconstructed_power


# buses = [
#     {'Vmag': 1.0, 'Vang': 0.0, 'type': 'PQ'},
#     {'Vmag': 0.98, 'Vang': -5.0, 'type': 'PV'},
#     {'Vmag': 1.02, 'Vang': 3.0, 'type': 'PQ'}
# ]

# # Example admittance matrix Y for a 3-bus system
# Y = np.array([
#     [10-30j, -5+15j, -5+15j],
#     [-5+15j, 10-30j, -5+15j],
#     [-5+15j, -5+15j, 10-30j]
# ])

# n = 3  # Number of buses
