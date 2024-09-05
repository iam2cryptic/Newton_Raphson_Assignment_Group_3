import numpy as np
import modules.y_matrix_gen as ymg
import modules.bus_data_input as bdi
import modules.calculated_power as cp
import modules.jacobian as jac

def main():
    #Obtain the admittance matrix
    admittance_matrix = ymg.admittance_matrix()

    # Example admittance matrix Y for a 3-bus system
    '''admittance_matrix = np.array([
    [0 - 7.5j, 0 + 2.5j, 0 + 5.0j],
    [0 + 2.5j, 0 - 6.5j, 0 + 4.0j],
    [0 + 5.0j, 0 + 4.0j, 0 - 9.0j]
    ])'''

    admittance_matrix = np.round(admittance_matrix, 4)
    #polar_matrix = ymg.admittance_to_polar(admittance_matrix)
    #print("Admittance Matrix in Polar Form:\n", polar_matrix)

    #Obtain the bus data
    bus_data = bdi.bus_data(len(admittance_matrix))
    #tolerance = float(input("Enter the mismatch tolerance value: "))  # Allow user to specify tolerance
    tolerance = 0.01
    # Initialize iteration count
    iteration_count = 0
    max_iterations = 100  # Maximum number of iterations to prevent infinite loops

    while True:
        # Calculate the power at each bus
        calculated_power = cp.calculated_power(bus_data, admittance_matrix, len(admittance_matrix))
        print("Calculated Power:\n", calculated_power)

        # Determine the number of entries needed
        num_pq_buses = sum(1 for bus in bus_data if bus["type"] == "PQ")
        num_pv_buses = sum(1 for bus in bus_data if bus["type"] == "PV")

        # Initialize the power mismatch array
        power_mismatch = np.zeros(((num_pq_buses * 2) + num_pv_buses, 1))

        # Index to fill in the power_mismatch array
        index = 0

        # Calculate power mismatch
        for bus in bus_data:
            bus_type = bus["type"]
            if bus_type == "PQ":
                # For PQ buses, both active and reactive power should be considered
                power_mismatch[index] = np.round(bus["P"] - calculated_power[index], 4)
                print("P: ", bus["P"])
                print("Calculated Power: ", calculated_power[index])
                power_mismatch[index + 1] = np.round(bus["Q"] - calculated_power[index + 1], 4)
                print("Q: ", bus["Q"])
                print("Calculated Reactive Power: ", calculated_power[index + 1])
                index += 2
            elif bus_type == "PV":
                # For PV buses, only active power mismatch is considered
                power_mismatch[index] = np.round(bus["P"] - calculated_power[index], 4)
                print("P: ", bus["P"])
                print("Calculated Power: ", calculated_power[index])
                index += 1
        print("Power Mismatch:\n", power_mismatch)

        # Check if the maximum mismatch is within the tolerance
        max_mismatch = np.max(np.abs(power_mismatch))
        if max_mismatch <= tolerance:
            print("Power mismatch is within tolerance.")
            print("Final Bus Data:\n", bus_data)
            print("Number of iterations: ", iteration_count)
            break

        # Calculate the Jacobian matrix and its inverse
        jacobian_matrix = jac.jacobian(bus_data, admittance_matrix, len(admittance_matrix))
        inverse_jacobian = jac.jacobian_inverse(jacobian_matrix)

        if inverse_jacobian is None:
            print("Jacobian matrix inversion failed. Terminating.")
            return

        print("Inverse Jacobian Matrix:\n", inverse_jacobian)

        # Calculate the change in voltage and angle
        change = np.dot(inverse_jacobian, power_mismatch)
        change = np.array(change).astype(np.float64)

        # Now apply np.round without errors
        change = np.round(change, 4)
        print("Change Vector:\n", change)

        num_buses = len(bus_data)

        # Create an index tracker for change vector
        change_index = 0

        for i in range(num_buses):
            bus_type = bus_data[i]["type"]

            if bus_type == "Vθ":
                # Skip updates for the slack bus
                continue

            if bus_type == "PQ":
                # PQ buses contribute two entries to the change vector
                if change_index + 2 > len(change):
                    print("Error: Change vector is too short for PQ bus updates.")
                    return

                bus_data[i]["Vmag"] += change[change_index]
                bus_data[i]["Vang"] += change[change_index + 1]
                change_index += 2

            elif bus_type == "PV":
                # PV buses contribute only one entry to the change vector
                if change_index + 1 > len(change):
                    print("Error: Change vector is too short for PV bus updates.")
                    return

                bus_data[i]["Vang"] += change[change_index]
                change_index += 1

        if change_index != len(change):
            print("Warning: Change vector contains unused elements.")

        print("Updated Bus Data:\n", bus_data)

        iteration_count += 1
        if iteration_count >= max_iterations:
            print("Maximum number of iterations reached. Terminating.")
            break
main()
