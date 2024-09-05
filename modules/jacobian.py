from . import equation as eq
import sympy as sp

def jacobian(bus_data, admittance_matrix, n):
    # Generate unknowns and power equations
    unknowns = eq.generate_unknowns(bus_data)
    power_equations = eq.power_equations_generator(bus_data, admittance_matrix, n)
    print("Power Equations:", power_equations)

    # Initialize Jacobian matrix with zeros
    jacobian_matrix = sp.zeros(len(power_equations), len(unknowns))

    # Create a substitution dictionary from bus data
    substitution_dictionary = {}
    for bus in bus_data:
        if 'Vmag_symbol' in bus and 'Vmag' in bus:
            substitution_dictionary[bus["Vmag_symbol"]] = sp.Float(bus["Vmag"])
        if 'Vang_symbol' in bus and 'Vang' in bus:
            substitution_dictionary[bus["Vang_symbol"]] = sp.Float(bus["Vang"])

    # Fill the Jacobian matrix
    for i, power_equation in enumerate(power_equations):
        for j, unknown in enumerate(unknowns):
            # Differentiate the equation with respect to the unknown
            differentiated_equation = sp.diff(power_equation, unknown)
            # Substitute the values and evaluate the result
            substituted_value = differentiated_equation.subs(substitution_dictionary)
            jacobian_matrix[i, j] = substituted_value.evalf(4)
    print("Jacobian Matrix:\n", jacobian_matrix)
    return jacobian_matrix

def jacobian_inverse(jacobian):
    try:
        # Compute the inverse of the Jacobian matrix
        inverse_matrix = jacobian.inv()
        return inverse_matrix
    except sp.NonSquareMatrixError:
        print("The Jacobian matrix must be square to compute its inverse.")
        return None
    except sp.NonInvertibleMatrixError:
        print("The Jacobian matrix is not invertible.")
        return None
