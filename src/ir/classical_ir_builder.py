"""
Classical IR Builder: Generate LLVM IR from classical assembly AST
Converts traditional assembly instructions to LLVM IR
"""

from llvmlite import ir
from typing import Dict, List, Optional, Any
from ..frontend.classical_parser import ClassicalAST, Instruction, DataDefinition

class ClassicalIRBuilder:
    """Builds LLVM IR from classical assembly AST"""
    
    def __init__(self, module_name: str = "classical_module"):
        self.module = ir.Module(name=module_name)
        self.builder: Optional[ir.IRBuilder] = None
        self.variables: Dict[str, ir.GlobalVariable] = {}
        self.registers: Dict[str, Any] = {}  # ir.AllocaInst
        self.basic_blocks: Dict[str, Any] = {}  # ir.Block
        self.function: Optional[ir.Function] = None
        self.last_cmp: Optional[Any] = None
        
        # Create main function
        self._create_main_function()
    
    def _create_main_function(self):
        """Create the main function structure"""
        # Function signature: int main()
        func_type = ir.FunctionType(ir.IntType(32), [])
        self.function = ir.Function(self.module, func_type, name="main")
        
        # Create entry block
        entry_block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(entry_block)
        
        # Allocate AREG register (assuming 32-bit integer)
        self.registers['AREG'] = self.builder.alloca(ir.IntType(32), name="AREG")
        
        # Initialize AREG to 0
        zero = ir.Constant(ir.IntType(32), 0)
        self.builder.store(zero, self.registers['AREG'])
    
    def build_ir_from_ast(self, ast: ClassicalAST) -> str:
        """Generate LLVM IR from classical assembly AST"""
        
        # First pass: Create global variables for data definitions
        self._create_global_variables(ast.data_definitions)
        
        # Second pass: Create basic blocks for labels
        self._create_basic_blocks(ast)
        
        # Third pass: Generate instructions
        self._generate_instructions(ast.instructions)
        
        # Add return statement
        ret_val = ir.Constant(ir.IntType(32), 0)
        self.builder.ret(ret_val)
        
        return str(self.module)
    
    def _create_global_variables(self, data_defs: Dict[str, DataDefinition]):
        """Create global variables for data definitions"""
        for name, data_def in data_defs.items():
            if data_def.directive == 'DC':  # Define Constant
                var_type = ir.IntType(32)
                initializer = ir.Constant(var_type, data_def.value)
                global_var = ir.GlobalVariable(self.module, var_type, name=name)
                global_var.initializer = initializer
                global_var.linkage = 'internal'
                self.variables[name] = global_var
                
            elif data_def.directive == 'DS':  # Define Storage
                var_type = ir.IntType(32)
                initializer = ir.Constant(var_type, 0)
                global_var = ir.GlobalVariable(self.module, var_type, name=name)
                global_var.initializer = initializer
                global_var.linkage = 'internal'
                self.variables[name] = global_var
    
    def _create_basic_blocks(self, ast: ClassicalAST):
        """Create basic blocks for labels and control flow"""
        current_block = self.builder.block
        
        # Create blocks for each label
        for label, _ in ast.labels.items():
            if label not in self.basic_blocks:
                block = self.function.append_basic_block(name=f"label_{label}")
                self.basic_blocks[label] = block
        
        # Create a block for instructions after loops
        exit_block = self.function.append_basic_block(name="exit")
        self.basic_blocks['exit'] = exit_block
    
    def _generate_instructions(self, instructions: List[Instruction]):
        """Generate LLVM IR for each instruction"""
        for i, instr in enumerate(instructions):
            
            # Handle labels - switch to appropriate basic block
            if instr.label and instr.label in self.basic_blocks:
                # Branch to the labeled block if not already there
                if self.builder.block != self.basic_blocks[instr.label]:
                    if not self.builder.block.is_terminated:
                        self.builder.branch(self.basic_blocks[instr.label])
                    self.builder = ir.IRBuilder(self.basic_blocks[instr.label])
            
            # Generate instruction
            if instr.opcode == 'MOVER':
                self._generate_mover(instr)
            elif instr.opcode == 'ADD':
                self._generate_add(instr)
            elif instr.opcode == 'SUB':
                self._generate_sub(instr)
            elif instr.opcode == 'MULT':
                self._generate_mult(instr)
            elif instr.opcode == 'MOVEM':
                self._generate_movem(instr)
            elif instr.opcode == 'COMP':
                self._generate_comp(instr, instructions, i)
            elif instr.opcode == 'BC':
                self._generate_branch(instr)
            elif instr.opcode == 'STOP':
                self._generate_stop()
    
    def _generate_mover(self, instr: Instruction):
        """Generate IR for MOVER (move to register)"""
        if len(instr.operands) >= 2:
            dest_reg = instr.operands[0]
            source = instr.operands[1]
            
            if dest_reg == 'AREG':
                if source in self.variables:
                    # Load from global variable
                    value = self.builder.load(self.variables[source], name=f"load_{source}")
                    self.builder.store(value, self.registers['AREG'])
                else:
                    # Immediate value
                    try:
                        imm_val = ir.Constant(ir.IntType(32), int(source))
                        self.builder.store(imm_val, self.registers['AREG'])
                    except ValueError:
                        # Handle as variable name
                        pass
    
    def _generate_add(self, instr: Instruction):
        """Generate IR for ADD"""
        if len(instr.operands) >= 2:
            dest_reg = instr.operands[0]
            source = instr.operands[1]
            
            if dest_reg == 'AREG':
                areg_val = self.builder.load(self.registers['AREG'], name="areg_val")
                
                if source in self.variables:
                    source_val = self.builder.load(self.variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source))
                
                result = self.builder.add(areg_val, source_val, name="add_result")
                self.builder.store(result, self.registers['AREG'])
    
    def _generate_sub(self, instr: Instruction):
        """Generate IR for SUB"""
        if len(instr.operands) >= 2:
            dest_reg = instr.operands[0]
            source = instr.operands[1]
            
            if dest_reg == 'AREG':
                areg_val = self.builder.load(self.registers['AREG'], name="areg_val")
                
                if source in self.variables:
                    source_val = self.builder.load(self.variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source))
                
                result = self.builder.sub(areg_val, source_val, name="sub_result")
                self.builder.store(result, self.registers['AREG'])
    
    def _generate_mult(self, instr: Instruction):
        """Generate IR for MULT"""
        if len(instr.operands) >= 2:
            dest_reg = instr.operands[0]
            source = instr.operands[1]
            
            if dest_reg == 'AREG':
                areg_val = self.builder.load(self.registers['AREG'], name="areg_val")
                
                if source in self.variables:
                    source_val = self.builder.load(self.variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source))
                
                result = self.builder.mul(areg_val, source_val, name="mult_result")
                self.builder.store(result, self.registers['AREG'])
    
    def _generate_movem(self, instr: Instruction):
        """Generate IR for MOVEM (move from register to memory)"""
        if len(instr.operands) >= 2:
            source_reg = instr.operands[0]
            dest = instr.operands[1]
            
            if source_reg == 'AREG' and dest in self.variables:
                areg_val = self.builder.load(self.registers['AREG'], name="areg_val")
                self.builder.store(areg_val, self.variables[dest])
    
    def _generate_comp(self, instr: Instruction, instructions: List[Instruction], current_index: int):
        """Generate IR for COMP (compare)"""
        if len(instr.operands) >= 2:
            reg = instr.operands[0]
            operand = instr.operands[1]
            
            if reg == 'AREG':
                areg_val = self.builder.load(self.registers['AREG'], name="areg_val")
                
                if operand in self.variables:
                    cmp_val = self.builder.load(self.variables[operand], name=f"load_{operand}")
                else:
                    cmp_val = ir.Constant(ir.IntType(32), int(operand))
                
                # Store comparison result for next BC instruction
                # For simplicity, we'll use a simple comparison
                self.last_cmp = self.builder.icmp_signed('<', areg_val, cmp_val, name="cmp_result")
    
    def _generate_branch(self, instr: Instruction):
        """Generate IR for BC (branch conditional)"""
        if len(instr.operands) >= 2:
            condition = instr.operands[0]  # ANY, etc.
            target_label = instr.operands[1]
            
            if target_label in self.basic_blocks:
                if hasattr(self, 'last_cmp'):
                    # Conditional branch based on last comparison
                    self.builder.cbranch(self.last_cmp, 
                                       self.basic_blocks[target_label], 
                                       self.basic_blocks['exit'])
                else:
                    # Unconditional branch
                    self.builder.branch(self.basic_blocks[target_label])
    
    def _generate_stop(self):
        """Generate IR for STOP"""
        if not self.builder.block.is_terminated:
            self.builder.branch(self.basic_blocks['exit'])
        
        # Switch to exit block
        self.builder = ir.IRBuilder(self.basic_blocks['exit'])


def generate_classical_ir(ast: ClassicalAST) -> str:
    """Convenience function to generate LLVM IR from classical AST"""
    builder = ClassicalIRBuilder()
    return builder.build_ir_from_ast(ast)