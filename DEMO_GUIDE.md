# Demo Scripts Usage Guide

This directory contains several demonstration scripts to showcase the quantum-llvm-compiler project:

## Available Demo Scripts

### 🚀 `./quick-demo.sh` (Recommended for first time)
**Duration: ~30 seconds**
- Runs essential examples quickly
- Compiles teleportation and Grover circuits
- Shows output files and performance metrics
- Best for getting a quick overview

### 🔬 `./demo.sh` (Complete demonstration)
**Duration: ~2-3 minutes**
- Comprehensive demonstration of all features
- Runs full test suite
- Shows IR generation, optimization passes
- Performance benchmarking with multiple circuits
- Detailed output analysis
- Complete project capabilities overview

### ⚡ `./quantum-demo` (Interactive binary)
**Duration: Variable**
- Python-based executable demonstration
- Can run in quick mode: `./quantum-demo --quick`
- Full mode shows all capabilities with detailed analysis
- Self-contained with error handling

### 🛠️ Individual Components

```bash
# Run specific circuit
PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm

# Run tests only
PYTHONPATH=. python -m pytest tests/ -v

# Interactive mode
PYTHONPATH=. python -c "from src.frontend.parser import *"
```

## Quick Start

1. **First time users**: `./quick-demo.sh`
2. **Complete overview**: `./demo.sh` 
3. **Custom exploration**: `./quantum-demo --quick`

## What You'll See

- ✅ Quantum circuit parsing (QASM → AST)
- ✅ Optimization passes (gate reduction, entanglement analysis)
- ✅ LLVM IR generation for quantum operations
- ✅ Circuit transpilation and simulation
- ✅ Performance benchmarks and file outputs
- ✅ Complete project capability overview

## Expected Output Files

After running demos, you'll get:
- `output_*.ll` - LLVM IR representations
- `output_*.qasm` - Optimized quantum circuits
- `output_*.json` - Circuit metadata

## Troubleshooting

If demos fail:
1. Ensure virtual environment is activated: `source .venv/bin/activate`
2. Check dependencies: `pip list | grep -E "(qiskit|llvmlite)"`
3. Run setup if needed: `./setup.sh`
4. Verify tests pass: `PYTHONPATH=. python -m pytest tests/ -v`

Enjoy exploring quantum compilation! 🎊