"""
Glue between QIRBuilder and backend stages.
For prototype: convert QIR metadata into a qiskit circuit via transpiler.
"""
from ..ir.qir_builder import QIRBuilder
from ..backend.transpiler import ast_to_qiskit_circuit

def qir_to_qiskit(ast, qir_builder=None):
    # Simplified path: AST -> qiskit circuit
    return ast_to_qiskit_circuit(ast)
