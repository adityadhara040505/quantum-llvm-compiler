"""
QIRBuilder: create a simple LLVM-like IR using llvmlite, with 'quantum intrinsics' as functions.
This module produces a textual IR (llvmlite.Module) and keeps a qubit table.
"""
from llvmlite import ir

class QIRBuilder:
    def __init__(self, module_name="quantum_module"):
        self.module = ir.Module(name=module_name)
        self.qubit_count = 0
        self.qubits = {}  # name -> GlobalVariable (as placeholder)

    def allocate_qubit(self, name: str = None):
        """Allocate a qubit as a global i8* placeholder (we use i8 to represent qubit handle)."""
        if name is None:
            name = f"q{self.qubit_count}"
        gv = ir.GlobalVariable(self.module, ir.IntType(8), name=name)
        gv.linkage = 'internal'
        gv.initializer = ir.Constant(ir.IntType(8), 0)
        self.qubits[name] = gv
        self.qubit_count += 1
        return name

    def add_intrinsic_gate(self, gate_name: str, qubit_names):
        """
        Add a dummy intrinsic function declaration for the quantum gate.
        We're not generating gate bodies here — only declarations so the module reflects operations.
        """
        # All gate intrinsics accept a pointer to qubit(s). We'll model with i8* or i32 int(s).
        arg_types = [ir.IntType(32) for _ in qubit_names]
        func_type = ir.FunctionType(ir.VoidType(), arg_types)
        func_name = f"qop.{gate_name}"
        # avoid redeclaration
        if func_name in self.module.globals:
            return func_name
        ir.Function(self.module, func_type, name=func_name)
        return func_name

    def emit_gate_call(self, builder, func_name: str, qubit_ids):
        """In a real IR builder we'd insert calls. Here we accumulate textual metadata only."""
        # Placeholder: store as metadata comment in module
        # Append a module-level named metadata for operations
        md_name = f"qops"
        if md_name not in self.module.global_scope:
            pass
        # We'll just return a tuple describing the call
        return (func_name, tuple(qubit_ids))

    def get_ir(self) -> str:
        return str(self.module)
