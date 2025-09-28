"""
Unified Quantum-Classical Compiler Demo
Demonstrates both quantum circuit compilation and NASM assembly compilation
"""

import sys
import os
sys.path.append('src')

from frontend.nasm_parser import compile_nasm_to_llvm
from frontend.parser import parse_qasm_file
from ir.qir_builder import QIRBuilder

def demo_nasm_compilation():
    """Demo NASM assembly compilation"""
    print("=" * 60)
    print("NASM x86_64 Assembly to LLVM IR Compilation")
    print("=" * 60)
    
    # Check if our simple demo exists
    nasm_file = "examples/simple_demo.asm"
    
    if os.path.exists(nasm_file):
        try:
            llvm_ir = compile_nasm_to_llvm(nasm_file)
            
            # Save the output
            output_file = "output_nasm_demo.ll"
            with open(output_file, 'w') as f:
                f.write(llvm_ir)
            
            print(f"✅ Successfully compiled {nasm_file}")
            print(f"📄 LLVM IR saved to: {output_file}")
            print("\n🔍 Generated LLVM IR Preview:")
            print("-" * 40)
            print(llvm_ir[:500] + "..." if len(llvm_ir) > 500 else llvm_ir)
            
        except Exception as e:
            print(f"❌ Error compiling NASM: {e}")
    else:
        print(f"⚠️  NASM demo file not found: {nasm_file}")

def demo_quantum_compilation():
    """Demo quantum circuit compilation"""
    print("\n" + "=" * 60)
    print("Quantum Circuit to QIR Compilation")
    print("=" * 60)
    
    # Check if quantum examples exist
    quantum_files = ["examples/grover.qasm", "examples/teleport.qasm"]
    
    for qasm_file in quantum_files:
        if os.path.exists(qasm_file):
            try:
                with open(qasm_file, 'r') as f:
                    qasm_code = f.read()
                
                # Parse quantum circuit
                ast = parse_qasm_file(qasm_file)
                
                # Build QIR
                qir_builder = QIRBuilder()
                
                # Allocate qubits and generate gates from AST
                from frontend.ast_nodes import GateNode, MeasureNode
                
                # Track allocated qubits to avoid duplicates
                allocated_qubits = set()
                
                for node in ast.nodes:
                    if isinstance(node, GateNode):
                        # Allocate qubits if needed
                        for qubit in node.qubits:
                            if qubit not in allocated_qubits:
                                qir_builder.allocate_qubit(f"q{qubit}")
                                allocated_qubits.add(qubit)
                        # Add gate intrinsic
                        qir_builder.add_intrinsic_gate(node.name, node.qubits)
                    elif isinstance(node, MeasureNode):
                        if node.qubit not in allocated_qubits:
                            qir_builder.allocate_qubit(f"q{node.qubit}")
                            allocated_qubits.add(node.qubit)
                        qir_builder.add_intrinsic_gate("measure", [node.qubit])
                
                # Get the module
                module = qir_builder.get_ir()
                
                # Save output
                base_name = os.path.splitext(os.path.basename(qasm_file))[0]
                output_file = f"output_{base_name}_unified.ll"
                
                with open(output_file, 'w') as f:
                    f.write(str(module))
                
                print(f"✅ Successfully compiled {qasm_file}")
                print(f"📄 QIR saved to: {output_file}")
                
            except Exception as e:
                print(f"❌ Error compiling quantum circuit {qasm_file}: {e}")

def main():
    """Main demo function"""
    print("🚀 Unified Quantum-Classical Compiler Demo")
    print("This demo shows compilation of both:")
    print("  1. NASM x86_64 Assembly → LLVM IR")
    print("  2. Quantum Circuits → QIR (Quantum IR)")
    
    # Demo both compilation types
    demo_nasm_compilation()
    demo_quantum_compilation()
    
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("The quantum-llvm-compiler now supports both paradigms:")
    print("  • Quantum computing via QASM → QIR")
    print("  • Classical computing via NASM → LLVM IR")
    print("=" * 60)

if __name__ == "__main__":
    main()