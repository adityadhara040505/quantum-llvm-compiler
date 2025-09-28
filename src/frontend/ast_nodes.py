from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class ASTNode:
    pass

@dataclass
class GateNode(ASTNode):
    name: str
    qubits: List[int]
    params: List[Any] = field(default_factory=list)

@dataclass
class MeasureNode(ASTNode):
    qubit: int
    cbit: int

@dataclass
class QuantumAST:
    nodes: List[ASTNode] = field(default_factory=list)

    def add_node(self, node: ASTNode):
        self.nodes.append(node)

    def __repr__(self):
        return f"QuantumAST(nodes={self.nodes})"
