#!/bin/bash

# Quantum LLVM Compiler Demo Script
# This script demonstrates all capabilities of the quantum-llvm-compiler project

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored headers
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_step() {
    echo -e "${GREEN}➤ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check if virtual environment is activated
check_environment() {
    print_step "Checking environment setup..."
    
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment not activated. Activating now..."
        source .venv/bin/activate || {
            print_error "Failed to activate virtual environment. Run ./setup.sh first."
            exit 1
        }
    fi
    
    # Check if required packages are installed
    python -c "import qiskit, llvmlite, numpy" 2>/dev/null || {
        print_error "Required packages not installed. Run ./setup.sh first."
        exit 1
    }
    
    print_success "Environment check passed"
}

# Run tests to verify everything works
run_tests() {
    print_header "RUNNING COMPREHENSIVE TESTS"
    print_step "Executing test suite..."
    
    PYTHONPATH=. python -m pytest tests/ -v || {
        print_error "Tests failed. Please check the installation."
        exit 1
    }
    
    print_success "All tests passed!"
}

# Demonstrate basic quantum circuit compilation
demo_basic_compilation() {
    print_header "BASIC QUANTUM IR COMPILATION DEMO"
    
    print_step "Compiling Quantum Teleportation Circuit..."
    PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm
    
    echo ""
    print_step "Generated files:"
    ls -la output_teleport.* 2>/dev/null || echo "Output files not found"
    
    echo ""
    print_step "Compiling Grover's Algorithm Circuit..."
    PYTHONPATH=. python run_quantum_compiler.py examples/grover.qasm
    
    echo ""
    print_step "Generated files:"
    ls -la output_grover.* 2>/dev/null || echo "Output files not found"
}

# Show IR generation capabilities
demo_ir_generation() {
    print_header "QUANTUM IR GENERATION CAPABILITIES"
    
    print_step "Demonstrating Quantum IR structure..."
    
    PYTHONPATH=. python -c "
from src.ir.qir_builder import QIRBuilder
from src.frontend.parser import parse_qasm_file

print('🔧 Creating Quantum IR Builder...')
qir = QIRBuilder('demo_module')

print('📝 Allocating qubits...')
for i in range(3):
    qir.allocate_qubit(f'q{i}')

print('⚡ Adding quantum gate intrinsics...')
qir.add_intrinsic_gate('h', ['q0'])
qir.add_intrinsic_gate('cx', ['q0', 'q1'])
qir.add_intrinsic_gate('rz', ['q2'])
qir.add_intrinsic_gate('measure', ['q0'])

print('\n📄 Generated Quantum IR:')
print(qir.get_ir())

print('\n🔍 Parsing real circuit for comparison...')
ast = parse_qasm_file('examples/teleport.qasm')
print(f'AST nodes: {len(ast.nodes)}')
for i, node in enumerate(ast.nodes):
    print(f'  {i}: {node}')
"
}

# Demonstrate optimization passes
demo_optimization() {
    print_header "QUANTUM OPTIMIZATION PASSES DEMO"
    
    print_step "Creating circuit with redundant operations..."
    
    # Create a test circuit with redundant gates
    cat > demo_redundant.qasm << 'EOF'
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
h q[0];
x q[1];
x q[1];
h q[2];
cx q[0],q[1];
cx q[1],q[2];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
EOF
    
    print_step "Demonstrating optimization effectiveness..."
    
    PYTHONPATH=. python -c "
from src.frontend.parser import parse_qasm_file
from src.ir.passes import superposition_opt, entanglement_aware_pass
import time

print('🔄 Parsing circuit with redundant operations...')
ast = parse_qasm_file('demo_redundant.qasm')
original_gates = [node for node in ast.nodes if hasattr(node, 'name')]
print(f'Original gates: {len(original_gates)}')

print('⚡ Applying superposition optimization...')
start_time = time.time()
optimized_ast = superposition_opt(ast)
opt_time = time.time() - start_time

optimized_gates = [node for node in optimized_ast.nodes if hasattr(node, 'name')]
reduction = len(original_gates) - len(optimized_gates)
percentage = (reduction / len(original_gates)) * 100

print(f'Optimized gates: {len(optimized_gates)}')
print(f'Reduction: {reduction} gates ({percentage:.1f}%)')
print(f'Optimization time: {opt_time:.6f}s')

print('🔗 Analyzing entanglement...')
ent_map = entanglement_aware_pass(optimized_ast)
print(f'Entanglement map: {ent_map}')
print(f'Entangled qubit pairs: {len(ent_map)}')
"
    
    # Clean up
    rm -f demo_redundant.qasm
}

# Demonstrate quantum simulation
demo_simulation() {
    print_header "QUANTUM CIRCUIT SIMULATION DEMO"
    
    print_step "Running quantum simulations with different shot counts..."
    
    PYTHONPATH=. python -c "
from src.frontend.parser import parse_qasm_file
from src.backend.transpiler import ast_to_qiskit_circuit
from src.execution.hybrid_executor import HybridExecutor
import time

print('🔬 Setting up quantum circuits...')
teleport_ast = parse_qasm_file('examples/teleport.qasm')
grover_ast = parse_qasm_file('examples/grover.qasm')

teleport_qc = ast_to_qiskit_circuit(teleport_ast)
grover_qc = ast_to_qiskit_circuit(grover_ast)

shot_counts = [100, 500, 1000]

print('\n📊 Teleportation Circuit Results:')
for shots in shot_counts:
    executor = HybridExecutor(shots=shots)
    start_time = time.time()
    result = executor.run(teleport_qc)
    runtime = time.time() - start_time
    
    print(f'  Shots: {shots:4d} | Results: {result[\"counts\"]} | Time: {runtime:.3f}s')

print('\n📊 Grover Circuit Results:')
for shots in shot_counts:
    executor = HybridExecutor(shots=shots)
    start_time = time.time()
    result = executor.run(grover_qc)
    runtime = time.time() - start_time
    
    print(f'  Shots: {shots:4d} | Results: {result[\"counts\"]} | Time: {runtime:.3f}s')
"
}

# Show file outputs and analysis
demo_output_analysis() {
    print_header "OUTPUT FILE ANALYSIS"
    
    print_step "Analyzing generated output files..."
    
    if [ -f "output_teleport.ll" ]; then
        print_info "LLVM IR Structure (teleport.ll):"
        echo "----------------------------------------"
        cat output_teleport.ll
        echo "----------------------------------------"
        echo ""
    fi
    
    if [ -f "output_teleport.qasm" ]; then
        print_info "Optimized QASM Output (teleport.qasm):"
        echo "----------------------------------------"
        cat output_teleport.qasm
        echo "----------------------------------------"
        echo ""
    fi
    
    if [ -f "output_teleport.json" ]; then
        print_info "Circuit Metadata (teleport.json):"
        echo "----------------------------------------"
        cat output_teleport.json
        echo "----------------------------------------"
        echo ""
    fi
    
    print_step "File size comparison:"
    ls -lh output_* 2>/dev/null || echo "No output files found"
}

# Performance benchmarking
demo_performance() {
    print_header "PERFORMANCE BENCHMARKING"
    
    print_step "Running performance benchmarks..."
    
    PYTHONPATH=. python -c "
import time
from src.frontend.parser import parse_qasm_file
from src.ir.passes import superposition_opt, entanglement_aware_pass
from src.ir.qir_builder import QIRBuilder
from src.backend.transpiler import ast_to_qiskit_circuit
from src.execution.hybrid_executor import HybridExecutor

print('⏱️  Benchmarking quantum compilation pipeline...')

# Create different sized circuits for testing
circuits = {
    'Small (3 qubits)': 'examples/teleport.qasm',
    'Medium (3 qubits)': 'examples/grover.qasm'
}

for name, file in circuits.items():
    print(f'\n🔍 Testing {name}:')
    
    # Parse
    start = time.time()
    ast = parse_qasm_file(file)
    parse_time = time.time() - start
    
    # Optimize
    start = time.time()
    opt_ast = superposition_opt(ast)
    ent_map = entanglement_aware_pass(opt_ast)
    opt_time = time.time() - start
    
    # Generate IR
    start = time.time()
    qir = QIRBuilder()
    qir_text = qir.get_ir()
    ir_time = time.time() - start
    
    # Convert to circuit
    start = time.time()
    qc = ast_to_qiskit_circuit(opt_ast)
    circuit_time = time.time() - start
    
    # Simulate
    start = time.time()
    executor = HybridExecutor(shots=100)
    result = executor.run(qc)
    sim_time = time.time() - start
    
    total_time = parse_time + opt_time + ir_time + circuit_time + sim_time
    
    print(f'  Parse time:    {parse_time:.6f}s ({parse_time/total_time*100:.1f}%)')
    print(f'  Optimize time: {opt_time:.6f}s ({opt_time/total_time*100:.1f}%)')
    print(f'  IR gen time:   {ir_time:.6f}s ({ir_time/total_time*100:.1f}%)')
    print(f'  Circuit time:  {circuit_time:.6f}s ({circuit_time/total_time*100:.1f}%)')
    print(f'  Simulation:    {sim_time:.6f}s ({sim_time/total_time*100:.1f}%)')
    print(f'  TOTAL:         {total_time:.6f}s')
    print(f'  Gates:         {len([n for n in ast.nodes if hasattr(n, \"name\")])}')
    print(f'  Qubits:        {qc.num_qubits}')
    print(f'  Depth:         {qc.depth()}')
"
}

# Show project capabilities summary
demo_capabilities() {
    print_header "PROJECT CAPABILITIES SUMMARY"
    
    print_info "✅ Supported Features:"
    echo "   • QASM 2.0 parsing and AST generation"
    echo "   • Quantum-specific optimization passes"
    echo "   • LLVM-compatible IR generation"
    echo "   • Entanglement analysis and tracking"
    echo "   • Noise-aware qubit scheduling"
    echo "   • Qiskit circuit transpilation"
    echo "   • Quantum simulation execution"
    echo "   • Multi-format output (LLVM IR, QASM, JSON)"
    
    echo ""
    print_info "📋 Supported Quantum Gates:"
    echo "   • Hadamard (H), Pauli gates (X, Y, Z)"
    echo "   • CNOT (CX), Rotation gates (RX, RY, RZ)"
    echo "   • Measurement operations"
    
    echo ""
    print_info "🔧 Optimization Passes:"
    echo "   • Superposition optimization (duplicate gate removal)"
    echo "   • Entanglement-aware analysis"
    echo "   • Basic gate scheduling"
    
    echo ""
    print_info "🎯 Best Use Cases:"
    echo "   • Educational quantum computing"
    echo "   • Research prototyping"
    echo "   • NISQ algorithm development"
    echo "   • Quantum compilation learning"
}

# Main execution
main() {
    clear
    
    print_header "🚀 QUANTUM LLVM COMPILER - COMPLETE DEMONSTRATION"
    echo -e "${PURPLE}This demo will showcase all capabilities of the quantum-llvm-compiler project${NC}"
    echo ""
    
    # Check environment
    check_environment
    
    # Run all demonstrations
    run_tests
    demo_basic_compilation
    demo_ir_generation
    demo_optimization
    demo_simulation
    demo_output_analysis
    demo_performance
    demo_capabilities
    
    # Final summary
    print_header "🎉 DEMONSTRATION COMPLETE"
    print_success "All quantum compiler features have been demonstrated successfully!"
    
    echo ""
    print_info "Generated files:"
    ls -la output_* *.qasm 2>/dev/null | grep -v "examples/" || echo "No additional files generated"
    
    echo ""
    print_info "To run individual components:"
    echo "   • Run specific circuit: PYTHONPATH=. python run_quantum_compiler.py <file.qasm>"
    echo "   • Run tests: PYTHONPATH=. python -m pytest tests/ -v"
    echo "   • Interactive mode: PYTHONPATH=. python -c 'from src.frontend.parser import *'"
    
    echo ""
    print_success "Quantum compilation demo completed! 🎊"
}

# Execute main function
main "$@"