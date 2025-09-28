"""
Extended NASM Assembly Parser for quantum-llvm-compiler
Handles NASM x86_64 syntax and converts to LLVM IR
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from llvmlite import ir

@dataclass
class NASMInstruction:
    """Represents a NASM assembly instruction"""
    opcode: str
    operands: List[str] = field(default_factory=list)
    label: Optional[str] = None
    section: Optional[str] = None

@dataclass
class NASMProgram:
    """Complete NASM program representation"""
    data_section: Dict[str, Any] = field(default_factory=dict)
    text_instructions: List[NASMInstruction] = field(default_factory=list)
    bss_section: Dict[str, Any] = field(default_factory=dict)

class NASMToLLVMCompiler:
    """Compiles NASM x86_64 assembly to LLVM IR"""
    
    def __init__(self):
        self.program = NASMProgram()
        self.current_section = None

    def parse_nasm_file(self, filepath: str) -> NASMProgram:
        """Parse NASM assembly file"""
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            # Handle sections
            if line.startswith('section '):
                self.current_section = line.split()[1]
                continue
            
            # Handle data definitions
            if self.current_section == '.data':
                self._parse_data_line(line)
            elif self.current_section == '.text':
                self._parse_instruction_line(line)
        
        return self.program

    def _parse_data_line(self, line: str):
        """Parse data section lines"""
        # Skip comments and empty lines
        if line.startswith(';') or not line.strip():
            return
            
        # Handle equates (constants)
        if 'equ' in line:
            return  # Skip equates for now
            
        if ':' in line and ('db' in line or 'dw' in line or 'dd' in line or 'resb' in line):
            parts = line.split(':', 1)
            name = parts[0].strip()
            definition = parts[1].strip()
            
            if 'db' in definition:
                # Handle byte definitions
                content = definition.replace('db', '').strip()
                if content.startswith('"') and content.endswith('"'):
                    # String literal
                    self.program.data_section[name] = {
                        'type': 'string',
                        'value': content[1:-1]  # Remove quotes
                    }
                else:
                    # Numeric values - handle mixed content
                    values = []
                    parts = content.split(',')
                    for part in parts:
                        part = part.strip()
                        if part.isdigit():
                            values.append(int(part))
                        elif part == '10':  # newline
                            values.append(10)
                        elif part == '0':
                            values.append(0)
                        elif len(part) == 1 and ord(part) < 256:
                            values.append(ord(part))
                    
                    if values:  # Only add if we have values
                        self.program.data_section[name] = {
                            'type': 'bytes',
                            'value': values
                        }
            elif 'resb' in definition:
                # Reserved bytes (BSS section)
                size_str = definition.replace('resb', '').strip()
                if size_str.isdigit():
                    size = int(size_str)
                    self.program.data_section[name] = {
                        'type': 'reserved',
                        'size': size
                    }

    def _parse_instruction_line(self, line: str):
        """Parse instruction lines"""
        # Handle labels
        if ':' in line and not any(op in line for op in ['mov', 'add', 'sub', 'cmp', 'jmp']):
            label = line.split(':')[0].strip()
            remaining = line.split(':', 1)[1].strip() if ':' in line else ""
            if remaining:
                # Label with instruction on same line
                instr = self._parse_single_instruction(remaining)
                instr.label = label
                self.program.text_instructions.append(instr)
            else:
                # Label only
                label_instr = NASMInstruction("LABEL", [label])
                self.program.text_instructions.append(label_instr)
        else:
            # Regular instruction
            instr = self._parse_single_instruction(line)
            self.program.text_instructions.append(instr)

    def _parse_single_instruction(self, line: str) -> NASMInstruction:
        """Parse a single instruction"""
        parts = line.split()
        if not parts:
            return NASMInstruction("NOP")
        
        opcode = parts[0]
        operands = []
        
        if len(parts) > 1:
            operand_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operand_str.split(',')]
        
        return NASMInstruction(opcode, operands)

    def generate_llvm_ir(self) -> str:
        """Generate LLVM IR from parsed NASM program"""
        module = ir.Module(name="nasm_module")
        
        # Create main function
        func_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(module, func_type, name="main")
        
        # Create entry block
        entry_block = main_func.append_basic_block(name="entry")
        builder = ir.IRBuilder(entry_block)
        
        # Generate global variables for data section (simplified approach)
        globals_map = {}
        for name, data in self.program.data_section.items():
            # Create a simple global variable as placeholder (like QIR builder does)
            global_var = ir.GlobalVariable(module, ir.IntType(8), name=name)
            global_var.linkage = 'internal'
            global_var.initializer = ir.Constant(ir.IntType(8), 0)
            globals_map[name] = global_var
        
        # Allocate virtual registers
        registers = {}
        for reg in ['rax', 'rbx', 'rcx', 'rdx', 'rdi', 'rsi']:
            registers[reg] = builder.alloca(ir.IntType(64), name=reg)
            # Initialize to 0
            builder.store(ir.Constant(ir.IntType(64), 0), registers[reg])
        
        # Simple linear instruction generation (no control flow for now)
        for instr in self.program.text_instructions:
            # Skip labels for now
            if instr.opcode == "LABEL":
                continue
            
            # Translate x86_64 instructions to LLVM IR
            if instr.opcode == 'mov':
                self._generate_mov(builder, instr, registers, globals_map)
            elif instr.opcode == 'add':
                self._generate_add(builder, instr, registers)
            elif instr.opcode == 'xor':
                self._generate_xor(builder, instr, registers)
            elif instr.opcode == 'inc':
                self._generate_inc(builder, instr, registers)
            # Skip complex control flow instructions for now
            elif instr.opcode in ['cmp', 'jmp', 'jge', 'jl', 'je', 'jne', 'syscall']:
                # Add as comment in IR
                builder.comment(f"; {instr.opcode} {' '.join(instr.operands)}")
        
        # Add return
        ret_val = ir.Constant(ir.IntType(32), 0)
        builder.ret(ret_val)
        
        return str(module)

    def _generate_mov(self, builder, instr, registers, globals_map):
        """Generate LLVM IR for mov instruction"""
        if len(instr.operands) >= 2:
            dest = instr.operands[0]
            src = instr.operands[1]
            
            # Handle register to register moves
            if dest in registers and src in registers:
                src_val = builder.load(registers[src], name=f"load_{src}")
                builder.store(src_val, registers[dest])
            elif dest in registers:
                # Move immediate or global to register
                if src.isdigit():
                    imm_val = ir.Constant(ir.IntType(64), int(src))
                    builder.store(imm_val, registers[dest])
                elif src in globals_map:
                    # Address of global
                    addr = builder.gep(globals_map[src], [ir.Constant(ir.IntType(32), 0)], name=f"addr_{src}")
                    builder.store(addr, registers[dest])

    def _generate_add(self, builder, instr, registers):
        """Generate LLVM IR for add instruction"""
        if len(instr.operands) >= 2:
            dest = instr.operands[0]
            src = instr.operands[1]
            
            if dest in registers:
                dest_val = builder.load(registers[dest], name=f"load_{dest}")
                if src in registers:
                    src_val = builder.load(registers[src], name=f"load_{src}")
                else:
                    src_val = ir.Constant(ir.IntType(64), int(src) if src.isdigit() else 0)
                
                result = builder.add(dest_val, src_val, name="add_result")
                builder.store(result, registers[dest])

    def _generate_xor(self, builder, instr, registers):
        """Generate LLVM IR for xor instruction"""
        if len(instr.operands) >= 2:
            dest = instr.operands[0]
            src = instr.operands[1]
            
            if dest in registers and dest == src:
                # xor reg, reg = set to 0
                zero = ir.Constant(ir.IntType(64), 0)
                builder.store(zero, registers[dest])

    def _generate_cmp(self, builder, instr, registers):
        """Generate LLVM IR for cmp instruction"""
        # Simplified: just store comparison result in a flag (not implemented fully)
        pass

    def _generate_jump(self, builder, instr, blocks):
        """Generate LLVM IR for jump instructions"""
        if len(instr.operands) >= 1:
            target = instr.operands[0]
            if target in blocks and not builder.block.is_terminated:
                builder.branch(blocks[target])

    def _generate_inc(self, builder, instr, registers):
        """Generate LLVM IR for inc instruction"""
        if len(instr.operands) >= 1:
            reg = instr.operands[0]
            if reg in registers:
                reg_val = builder.load(registers[reg], name=f"load_{reg}")
                one = ir.Constant(ir.IntType(64), 1)
                result = builder.add(reg_val, one, name="inc_result")
                builder.store(result, registers[reg])

    def _generate_syscall(self, builder, registers):
        """Generate LLVM IR for syscall (simplified)"""
        # This is a placeholder - real syscall implementation would be more complex
        pass


def compile_nasm_to_llvm(nasm_file: str) -> str:
    """Compile NASM assembly file to LLVM IR"""
    compiler = NASMToLLVMCompiler()
    program = compiler.parse_nasm_file(nasm_file)
    return compiler.generate_llvm_ir()


# Example usage
if __name__ == "__main__":
    print("NASM to LLVM IR Compiler Ready!")
    print("This extends the quantum-llvm-compiler to handle x86_64 assembly!")