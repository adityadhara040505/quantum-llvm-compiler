# How to Run the Quantum LLVM Compiler

## Quick Start

The quantum-llvm-compiler is now ready to run! Here are several ways to use it:

### Method 1: Using the Simple Runner Script (Recommended)

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run with default example (teleport)
PYTHONPATH=. python run_quantum_compiler.py

# Run with specific QASM file
PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm
PYTHONPATH=. python run_quantum_compiler.py examples/grover.qasm
```

### Method 2: Using the Original Example Script

```bash
source .venv/bin/activate
PYTHONPATH=. python examples/run_example.py
```

### Method 3: Running Tests

```bash
source .venv/bin/activate
PYTHONPATH=. python -m pytest tests/ -v
```

## What the Compiler Does

The quantum compilation pipeline includes these steps:

1. **QASM Parsing**: Converts OpenQASM 2.0 files to Abstract Syntax Tree (AST)
2. **Optimization Passes**: 
   - Superposition optimization (removes duplicate gates)
   - Entanglement analysis (tracks qubit relationships)
3. **AST Verification**: Validates the quantum circuit structure
4. **QIR Generation**: Creates LLVM-style Quantum Intermediate Representation
5. **Circuit Conversion**: Transforms QIR to executable Qiskit circuits
6. **File Emission**: Outputs `.ll` (LLVM IR), `.qasm` (OpenQASM), and `.json` (metadata)
7. **Simulation**: Runs the circuit on Qiskit Aer quantum simulator

## Output Files

After running, you'll get three output files:
- `output_[name].ll` - LLVM-style intermediate representation
- `output_[name].qasm` - Optimized OpenQASM circuit
- `output_[name].json` - Circuit metadata (qubits, depth, etc.)

## Available Examples

- `examples/teleport.qasm` - Quantum teleportation circuit
- `examples/grover.qasm` - Grover's search algorithm

## Creating Your Own QASM Files

You can create your own OpenQASM 2.0 files and run them through the compiler:

```qasm
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
```

## Troubleshooting

If you encounter issues:

1. Make sure the virtual environment is activated: `source .venv/bin/activate`
2. Set the Python path: `PYTHONPATH=.`
3. Check that all dependencies are installed: `pip list`
4. Run tests to verify everything works: `PYTHONPATH=. python -m pytest tests/ -v`

## Understanding the Output

The simulation results show measurement outcomes:
- `{'0': 500, '1': 524}` means qubit measured as |0⟩ 500 times and |1⟩ 524 times out of 1024 shots
- Entanglement map shows which qubits are entangled: `{0: {1}, 1: {0}}` means qubits 0 and 1 are entangled

Enjoy exploring quantum compilation! 🚀