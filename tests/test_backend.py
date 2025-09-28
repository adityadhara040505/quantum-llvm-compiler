from src.frontend.parser import parse_qasm_file
from src.backend.transpiler import ast_to_qiskit_circuit
import tempfile

def test_transpile_example(tmp_path):
    qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[3];
    creg c[3];
    h q[0];
    cx q[0],q[1];
    cx q[1],q[2];
    measure q[2] -> c[2];
    """
    p = tmp_path / "ex.qasm"
    p.write_text(qasm)
    ast = parse_qasm_file(str(p))
    qc = ast_to_qiskit_circuit(ast)
    assert qc.num_qubits >= 1
