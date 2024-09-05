import sympy as sp
import numpy as np

def bus_data(n):
    while True:
        try:
            buses = []
            slack_bus_defined = False
            for i in range(n):
                bus = {}
                # Bus number
                bus['bus_number'] = i + 1

                # Input voltage in pu
                voltage_input = input(f"Enter the voltage at bus {i+1} in pu: ")
                if voltage_input:
                    voltage = complex(voltage_input)
                    bus['Vmag'] = abs(voltage)
                    bus['Vang'] = sp.arg(voltage).evalf()

                else:
                    bus['Vmag'] = ""
                    bus['Vang'] = ""

                # Define the voltage and angle as symbols
                bus['Vmag_symbol'] = sp.symbols(f"V_{i+1}")
                bus['Vang_symbol'] = sp.symbols(f"theta_{i+1}")

                # Input active power in pu
                bus['P'] = input(f"Enter the active injected power of bus {i+1} in pu: ")
                if bus['P']:
                    bus['P'] = float(bus['P'])
                else:
                    bus['P'] = ""

                # Input reactive power in pu
                bus['Q'] = input(f"Enter the reactive injected power of bus {i+1} in pu: ")
                if bus['Q']:
                    bus['Q'] = float(bus['Q'])
                else:
                    bus['Q'] = ""

                # Determine bus type
                if bus['Q'] != "" and bus['P'] != "" and bus['Vmag'] == "":
                    bus['type'] = 'PQ'
                elif bus['Q'] == "" and bus['P'] != "" and bus['Vmag'] != "":
                    bus['type'] = 'PV'
                elif bus['Q'] == "" and bus['P'] == "" and bus['Vmag'] != "" and bus['Vang'] != "":
                    if not slack_bus_defined:
                        bus['type'] = 'Vθ'
                        slack_bus_defined = True
                    else:
                        print("Only one slack bus is allowed")
                        break  # Skip this bus and continue with the next
                else:
                    print(f"Bus {i+1} type could not be determined based on provided data.")
                    break  # If bus type can't be determined, skip this bus

                buses.append(bus)

            # Check if a slack bus was defined
            if not slack_bus_defined:
                print("No slack bus was defined. Please start over.")
                continue  # Restart the whole process it no slack bus was defined
            else:
                print(buses)
                return buses
        # Error handling
        except ValueError as e:
            print(f"Input error: {e}. Please enter the correct data format.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
