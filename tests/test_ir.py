from src.ir.qir_builder import QIRBuilder
def test_qir_builder_alloc():
    b = QIRBuilder()
    n1 = b.allocate_qubit("q0")
    n2 = b.allocate_qubit("q1")
    assert n1 in b.qubits
    assert n2 in b.qubits
    irt = b.get_ir()
    assert "quantum_module" in irt
