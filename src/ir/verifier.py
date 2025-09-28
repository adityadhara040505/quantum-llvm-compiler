"""
Lightweight verification: checks some simple invariants:
- measurements target existing qubits
- gate nodes reference valid qubit indices (non-negative)
"""

def verify_ast(ast):
    valid = True
    errors = []
    # find max qubit index referenced
    max_q = -1
    for node in ast.nodes:
        if hasattr(node, 'qubits'):
            for q in node.qubits:
                if q is None or q < 0:
                    valid = False
                    errors.append(f"Invalid qubit index: {q}")
                if q > max_q:
                    max_q = q
        if hasattr(node, 'qubit'):
            if node.qubit is None or node.qubit < 0:
                valid = False
                errors.append(f"Invalid measurement qubit: {node.qubit}")
            if node.qubit > max_q:
                max_q = node.qubit
    return valid, errors
