"""
Optimization passes (stubs & small heuristics).
- superposition_opt: naive pass to remove consecutive identical gates
- entanglement_aware_pass: analyzes AST to mark entangling gates
"""

from collections import defaultdict

def superposition_opt(ast):
    """Naive removal of consecutive duplicate single-qubit gates on same qubit."""
    new_nodes = []
    prev = None
    for node in ast.nodes:
        if prev and isinstance(prev, type(node)) and getattr(prev, 'name', None) == getattr(node, 'name', None):
            # if same gate and same target qubit(s) and single-qubit, remove the duplicate
            if hasattr(node, 'qubits') and hasattr(prev, 'qubits') and node.qubits == prev.qubits and len(node.qubits) == 1:
                # skip duplicate
                continue
        new_nodes.append(node)
        prev = node
    ast.nodes = new_nodes
    return ast

def entanglement_aware_pass(ast):
    """
    Mark nodes as 'entangling' if they operate on >=2 qubits (cx, cz, etc.)
    Return metadata mapping qubit -> entanglement partners set
    """
    ent_map = defaultdict(set)
    for node in ast.nodes:
        if hasattr(node, 'qubits') and len(node.qubits) >= 2:
            q0, q1 = node.qubits[0], node.qubits[1]
            ent_map[q0].add(q1)
            ent_map[q1].add(q0)
    return dict(ent_map)
