"""
Hardware profile example.
"""
DEFAULT_HW_PROFILE = {
    "num_qubits": 5,
    "error_rates": {0: 0.002, 1: 0.003, 2: 0.005, 3: 0.007, 4: 0.004},
    "topology": [(0,1), (1,2), (2,3), (3,4), (0,2)]
}
