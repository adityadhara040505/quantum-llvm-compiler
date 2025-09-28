def estimate_fidelity_simple(qc, error_rates):
    # Very simple estimate: 1 - sum(error_rates for qubits used) scaled by count
    used_qubits = set(range(qc.num_qubits))
    total_error = sum(error_rates.get(q, 0.001) for q in used_qubits)
    est = max(0.0, 1.0 - total_error)
    return est
