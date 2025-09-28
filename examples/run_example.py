"""
Run an end-to-end example:
- parse QASM -> AST
- run simple passes
- build a QIR module (textual)
- transpile to qiskit circuit
- emit outputs and run on simulator
"""
import os
from src.frontend.parser import parse_qasm_file
from src.ir.passes import superposition_opt, entanglement_aware_pass
from src.ir.qir_builder import QIRBuilder
from src.ir.verifier import verify_ast
from src.backend.llvm_integration import qir_to_qiskit
from src.backend.emitter import emit_outputs
from src.execution.hybrid_executor import HybridExecutor
from src.utils.config import DEFAULT_HW_PROFILE
from src.utils.logger import get_logger

logger = get_logger("run_example")

def main():
    cwd = os.path.dirname(__file__)
    qasm_path = os.path.join(cwd, "teleport.qasm")
    logger.info("Parsing QASM...")
    ast = parse_qasm_file(qasm_path)
    logger.info("AST nodes: %d", len(ast.nodes))

    # runs passes
    ast = superposition_opt(ast)
    ent_map = entanglement_aware_pass(ast)
    logger.info("Entanglement map: %s", ent_map)

    ok, errors = verify_ast(ast)
    if not ok:
        logger.error("Verification failed: %s", errors)
        return

    # build QIR (textual)
    qir = QIRBuilder()
    # simple allocate qubits based on AST
    used_qubits = set()
    for node in ast.nodes:
        if hasattr(node, 'qubits'):
            for q in node.qubits:
                used_qubits.add(q)
        if hasattr(node, 'qubit'):
            used_qubits.add(node.qubit)
    for q in sorted(used_qubits):
        qir.allocate_qubit(f"q{q}")

    ir_text = qir.get_ir()
    logger.info("Generated IR text (short):\n%s", ir_text.splitlines()[:10])

    # convert to qiskit circuit
    qc = qir_to_qiskit(ast, qir)
    logger.info("Circuit: qubits=%d, clbits=%d, depth=%d", qc.num_qubits, qc.num_clbits, qc.depth())

    # emit files
    llf, qasmf, jsonf = emit_outputs(ir_text, qc, outfile_prefix=os.path.join(cwd, "teleport_out"))
    logger.info("Emitted files: %s, %s, %s", llf, qasmf, jsonf)

    # run on simulator
    execr = HybridExecutor(shots=512)
    res = execr.run(qc)
    logger.info("Execution results: counts=%s, runtime=%.3fs", res['counts'], res['runtime'])

if __name__ == "__main__":
    main()
