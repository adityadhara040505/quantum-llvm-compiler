"""
HybridExecutor: runs a qiskit QuantumCircuit either in simulator or via provider.
For the prototype we use Aer qasm_simulator (if available).
"""
from qiskit_aer import AerSimulator
from qiskit import transpile

import time

# class HybridExecutor:
#     def __init__(self, backend_name="aer_simulator", shots=1024):
#         # Try to use AerSimulator; fallback to qasm_simulator via Aer.get_backend
#         try:
#             self.backend = AerSimulator()
#         except Exception:
#             self.backend = Aer.get_backend("qasm_simulator")
#         self.shots = shots

#     def run(self, qc):
#         start = time.time()
#         job = execute(qc, backend=self.backend, shots=self.shots)
#         result = job.result()
#         end = time.time()
#         counts = result.get_counts()
#         runtime = end - start
#         return {"counts": counts, "runtime": runtime, "shots": self.shots}
class HybridExecutor:
    def __init__(self, shots=1024):
        self.backend = AerSimulator()
        self.shots = shots

    def run(self, qc):
        start = time.time()
        tqc = transpile(qc, self.backend)
        result = self.backend.run(tqc, shots=self.shots).result()
        end = time.time()
        counts = result.get_counts()
        runtime = end - start
        return {"counts": counts, "runtime": runtime, "shots": self.shots}

