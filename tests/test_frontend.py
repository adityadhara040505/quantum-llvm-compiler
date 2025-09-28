import os
from src.frontend.parser import parse_qasm_file
from src.frontend.ast_nodes import QuantumAST

def test_parse_simple_qasm(tmp_path):
    qasm = """
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];
    measure q[0] -> c[0];
    """
    f = tmp_path / "test.qasm"
    f.write_text(qasm)
    ast = parse_qasm_file(str(f))
    assert isinstance(ast, QuantumAST)
    # at least 3 nodes
    assert len(ast.nodes) >= 3
