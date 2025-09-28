# Architecture Overview

Pipeline:
1. Frontend
   - Lex/QASM parse (QASM3 based) → Quantum AST
2. IR
   - QIRBuilder: build an LLVM-like module with quantum intrinsics
   - Passes: (stubs) superposition optimization, entanglement-aware def-use analysis
   - Verifier: lightweight type/semantic checks
3. Backend
   - Transpiler: lower generic gates to target device-native gates
   - Scheduler: noise-aware qubit selection and scheduling heuristics
   - Emitter: produce target QASM / Qiskit circuit
4. Execution
   - HybridExecutor: uses Qiskit Aer simulator or hardware (if configured)
   - Profiler: collect counts, estimated fidelity metrics

Important: This is a simplified research prototype to experiment with ideas from the paper.
