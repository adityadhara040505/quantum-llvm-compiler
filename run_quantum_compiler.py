#!/usr/bin/env python3
"""
Simple runner script for the quantum-llvm-compiler project.
Usage: python run_quantum_compiler.py [qasm_file]
"""
import sys
import os
from src.frontend.parser import parse_qasm_file
from src.ir.passes import superposition_opt, entanglement_aware_pass
from src.ir.qir_builder import QIRBuilder
from src.ir.verifier import verify_ast
from src.backend.llvm_integration import qir_to_qiskit
from src.backend.emitter import emit_outputs
from src.execution.hybrid_executor import HybridExecutor
from src.utils.logger import get_logger

logger = get_logger("quantum_compiler")

def run_quantum_compiler(qasm_file):
    """Run the complete quantum compilation pipeline."""
    print(f"🚀 Running quantum compiler on: {qasm_file}")
    print("=" * 50)
    
    # 1. Parse QASM to AST
    print("1. Parsing QASM file...")
    ast = parse_qasm_file(qasm_file)
    print(f"   ✓ Parsed {len(ast.nodes)} AST nodes")
    
    # 2. Run optimization passes
    print("2. Running optimization passes...")
    original_nodes = len(ast.nodes)
    ast = superposition_opt(ast)
    optimized_nodes = len(ast.nodes)
    if optimized_nodes < original_nodes:
        print(f"   ✓ Superposition optimization: {original_nodes} → {optimized_nodes} nodes")
    else:
        print("   ✓ Superposition optimization: no changes")
    
    ent_map = entanglement_aware_pass(ast)
    if ent_map:
        print(f"   ✓ Entanglement analysis: {ent_map}")
    else:
        print("   ✓ Entanglement analysis: no entangled qubits")
    
    # 3. Verify AST
    print("3. Verifying AST...")
    ok, errors = verify_ast(ast)
    if not ok:
        print(f"   ❌ Verification failed: {errors}")
        return False
    print("   ✓ AST verification passed")
    
    # 4. Build QIR (Quantum IR)
    print("4. Building Quantum IR...")
    qir = QIRBuilder()
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
    print(f"   ✓ Generated IR with {len(used_qubits)} qubits")
    
    # 5. Convert to Qiskit circuit
    print("5. Converting to Qiskit circuit...")
    qc = qir_to_qiskit(ast, qir)
    print(f"   ✓ Circuit: {qc.num_qubits} qubits, {qc.num_clbits} classical bits, depth={qc.depth()}")
    
    # 6. Emit output files
    print("6. Emitting output files...")
    base_name = os.path.splitext(os.path.basename(qasm_file))[0]
    outfile_prefix = f"output_{base_name}"
    llf, qasmf, jsonf = emit_outputs(ir_text, qc, outfile_prefix=outfile_prefix)
    print(f"   ✓ Generated: {os.path.basename(llf)}, {os.path.basename(qasmf)}, {os.path.basename(jsonf)}")
    
    # 7. Execute on simulator
    print("7. Executing on quantum simulator...")
    executor = HybridExecutor(shots=1024)
    result = executor.run(qc)
    print(f"   ✓ Simulation complete: runtime={result['runtime']:.3f}s, shots={result['shots']}")
    print(f"   📊 Results: {result['counts']}")
    
    print("=" * 50)
    print("✅ Quantum compilation pipeline completed successfully!")
    return True

def main():
    if len(sys.argv) > 1:
        qasm_file = sys.argv[1]
    else:
        # Default to teleport example
        qasm_file = "examples/teleport.qasm"
    
    if not os.path.exists(qasm_file):
        print(f"❌ Error: QASM file '{qasm_file}' not found")
        print("Available examples:")
        examples_dir = "examples"
        if os.path.exists(examples_dir):
            for f in os.listdir(examples_dir):
                if f.endswith('.qasm'):
                    print(f"  - {os.path.join(examples_dir, f)}")
        return 1
    
    try:
        success = run_quantum_compiler(qasm_file)
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())