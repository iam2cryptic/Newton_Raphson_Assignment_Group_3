# Newton_Raphson_Assignment_Group_3
built by Lloyd, Nath, and the boys

# Load Flow Analysis using Newton-Raphson Method

This project implements a load flow analysis solver using the Newton-Raphson method in Python. The solver calculates the voltage magnitudes and angles at each bus in a power system network.

## Table of Contents
- Introduction
- Features
- Installation
- Usage
- Modules
- Contributing
- License
- Acknowledgements

## Introduction
Load flow analysis is a fundamental tool in power system engineering used to determine the steady-state operating conditions of a power system. This project uses the Newton-Raphson method, which is an iterative numerical technique, to solve the load flow problem.

## Features
- Calculates voltage magnitudes and angles at each bus.
- Handles different types of buses: PQ, PV, and Slack (Vθ).
- Uses an admittance matrix derived from the impedance matrix.
- Provides detailed error handling and convergence checks.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/load-flow-analysis.git
    cd load-flow-analysis
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script:
    ```bash
    python main.py
    ```

2. Follow the prompts to input the bus data and impedance matrix.

## Modules
- **bus_data_input.py**: Handles the input of bus data and determines the bus type.
- **calculated_power.py**: Calculates the power at each bus.
- **equation.py**: Generates power equations based on the bus data and admittance matrix.
- **jacobian.py**: Calculates the Jacobian matrix and its inverse.
- **y_matrix.py**: Calculates the admittance matrix from the impedance matrix.
- **y_matrix_gen.py**: Generates the admittance matrix and converts it to polar form.
- **main.py**: Implements the Newton-Raphson method for load flow analysis.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- Thanks to the open-source community for providing valuable resources and tools.
- Special thanks to Dr. Elvis Twumasi for inspiring the development of this project.


