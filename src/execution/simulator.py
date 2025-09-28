# Additional simulator helpers (kept minimal)
from qiskit import Aer, transpile
from qiskit.providers.aer.noise import NoiseModel

def simulate_with_noise(qc, noise_model=None, shots=1024):
    backend = Aer.get_backend("qasm_simulator")
    basis_gates = None
    if noise_model:
        basis_gates = noise_model.basis_gates
    t_qc = transpile(qc, backend=backend)
    job = backend.run(t_qc, shots=shots, noise_model=noise_model)
    return job.result()
