from qiskit import QuantumCircuit
from src.execution.hybrid_executor import HybridExecutor

def test_hybrid_run():
    qc = QuantumCircuit(1,1)
    qc.h(0)
    qc.measure(0,0)
    exec = HybridExecutor(shots=64)
    res = exec.run(qc)
    assert 'counts' in res
    assert res['shots'] == 64
