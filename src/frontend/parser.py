from .ast_nodes import QuantumAST, GateNode, MeasureNode
from qiskit import QuantumCircuit

# QASM3 loader
try:
    from qiskit_qasm3_import import qasm3
except ImportError:
    qasm3 = None


def parse_qasm_file(file_path: str) -> QuantumAST:
    """Parse a QASM2 or QASM3 file into QuantumAST."""

    # detect version - look for first non-empty line
    with open(file_path, "r") as f:
        first_line = ""
        for line in f:
            stripped = line.strip()
            if stripped:
                first_line = stripped
                break

    if first_line.startswith("OPENQASM 2"):
        circuit = QuantumCircuit.from_qasm_file(file_path)
    else:
        if qasm3 is None:
            raise ImportError("qiskit_qasm3_import is required for OpenQASM 3 files. Install with: pip install qiskit-qasm3-import")
        circuit = qasm3.load(file_path)

    ast = QuantumAST()
    for instr, qargs, cargs in circuit.data:
        name = instr.name
        # Fix for newer Qiskit versions - use circuit.find_bit() to get indices
        q_indices = [circuit.find_bit(q).index for q in qargs]
        if name.lower() == "measure":
            c_index = circuit.find_bit(cargs[0]).index if cargs else 0
            for qi, ci in zip(q_indices, [c_index] * len(q_indices)):
                ast.add_node(MeasureNode(qi, ci))
        else:
            params = list(getattr(instr, "params", []))
            ast.add_node(GateNode(name, q_indices, params))

    return ast
