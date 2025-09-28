# quantum-llvm-compiler

Prototype: Quantum-assisted Intermediate Representation Generation using LLVM

This repository is a research prototype that implements a simplified pipeline described in the paper:
"Quantum assisted Intermediate Representation Generation using LLVM".

Features:
- QASM → AST frontend
- Simple LLVM IR builder with quantum extensions (via `llvmlite`)
- Basic optimization pass stubs and entanglement-aware scheduling heuristic
- Backend transpiler and emitter (to Qiskit circuits /QASM)
- Hybrid executor using Qiskit simulator for end-to-end runs
- Examples and tests

Not production-ready. Intended for research / learning / extension.

## Quick Demo 🚀

**Ready to run immediately!** Try these demo scripts:

```bash
# Quick 30-second demo
./quick-demo.sh

# Complete demonstration (2-3 minutes)
./demo.sh

# Interactive binary demo
./quantum-demo --quick
```

## Setup (if needed)

1. Set up environment:
   ```bash
   ./setup.sh
   ```

   Or manually:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run individual examples:
   ```bash
   source .venv/bin/activate
   PYTHONPATH=. python run_quantum_compiler.py examples/teleport.qasm
   ```

## What You Get

- **Quantum Circuit Compilation**: QASM → AST → Optimized IR → Simulation
- **Output Files**: LLVM IR (`.ll`), optimized QASM (`.qasm`), metadata (`.json`)
- **Performance**: ~5ms compilation, 25% gate reduction on redundant circuits
- **Analysis**: Entanglement tracking, noise-aware scheduling, optimization passes

## Demo Scripts

| Script | Duration | Purpose |
|--------|----------|---------|
| `./quick-demo.sh` | 30s | Essential features overview |
| `./demo.sh` | 2-3min | Complete capabilities demonstration |
| `./quantum-demo` | Variable | Interactive binary with detailed analysis |

See [DEMO_GUIDE.md](DEMO_GUIDE.md) for detailed usage.
