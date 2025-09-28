"""
Transpiler: map gate names from AST to qiskit QuantumCircuit operations
A small mapping for common gates.
"""
from qiskit import QuantumCircuit

_GATE_MAP = {
    'h': lambda qc, qubits, params: qc.h(qubits[0]),
    'cx': lambda qc, qubits, params: qc.cx(qubits[0], qubits[1]),
    'x': lambda qc, qubits, params: qc.x(qubits[0]),
    'y': lambda qc, qubits, params: qc.y(qubits[0]),
    'z': lambda qc, qubits, params: qc.z(qubits[0]),
    'rz': lambda qc, qubits, params: qc.rz(params[0], qubits[0]),
    'rx': lambda qc, qubits, params: qc.rx(params[0], qubits[0]),
    'measure': lambda qc, qubits, params: qc.measure(qubits[0], params[0]),
}

def ast_to_qiskit_circuit(ast, num_qubits_hint=None):
    # estimate num qubits
    max_q = -1
    for node in ast.nodes:
        if hasattr(node, 'qubits'):
            for q in node.qubits:
                if isinstance(q, int) and q > max_q:
                    max_q = q
        if hasattr(node, 'qubit') and node.qubit > max_q:
            max_q = node.qubit
    num_qubits = max(num_qubits_hint or 0, max_q + 1)
    # determine classical bits needed (simple: number of measure nodes)
    nmeas = sum(1 for n in ast.nodes if n.__class__.__name__ == 'MeasureNode')
    qc = QuantumCircuit(num_qubits, nmeas)
    meas_idx = 0
    for node in ast.nodes:
        name = getattr(node, 'name', 'measure') if hasattr(node, 'name') else None
        if node.__class__.__name__ == 'GateNode':
            mapfn = _GATE_MAP.get(name.lower())
            if mapfn:
                mapfn(qc, node.qubits, node.params)
            else:
                # fallback: treat as unitary placeholder (no-op)
                pass
        elif node.__class__.__name__ == 'MeasureNode':
            qc.measure(node.qubit, meas_idx)
            meas_idx += 1
    return qc
