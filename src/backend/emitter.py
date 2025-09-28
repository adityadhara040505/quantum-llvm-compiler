"""
Emitter: write output artifacts: textual IR, QASM, and optional JSON profile.
"""
import json

def emit_outputs(ir_text: str, qiskit_circuit, outfile_prefix="output"):
    # Fix for newer Qiskit versions - use qasm() method from qiskit.qasm2
    from qiskit import qasm2
    qasm = qasm2.dumps(qiskit_circuit)
    with open(f"{outfile_prefix}.ll", "w") as f:
        f.write(ir_text)
    with open(f"{outfile_prefix}.qasm", "w") as f:
        f.write(qasm)
    # simple metrics file
    meta = {
        "num_qubits": qiskit_circuit.num_qubits,
        "num_clbits": qiskit_circuit.num_clbits,
        "depth": qiskit_circuit.depth()
    }
    with open(f"{outfile_prefix}.json", "w") as f:
        json.dump(meta, f, indent=2)
    return f"{outfile_prefix}.ll", f"{outfile_prefix}.qasm", f"{outfile_prefix}.json"
