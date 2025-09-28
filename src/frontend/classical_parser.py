"""
Classical Assembly Parser for generating LLVM IR
Handles traditional assembly language instructions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import re

@dataclass
class Instruction:
    """Represents a single assembly instruction"""
    opcode: str
    operands: List[str] = field(default_factory=list)
    label: Optional[str] = None
    line_number: int = 0

@dataclass
class DataDefinition:
    """Represents data definitions (DC, DS)"""
    name: str
    directive: str  # DC or DS
    value: Any
    size: int = 1

@dataclass
class ClassicalAST:
    """AST for classical assembly programs"""
    instructions: List[Instruction] = field(default_factory=list)
    data_definitions: Dict[str, DataDefinition] = field(default_factory=dict)
    labels: Dict[str, int] = field(default_factory=dict)  # label -> instruction index
    start_address: int = 0

class ClassicalAssemblyParser:
    """Parser for classical assembly language"""
    
    def __init__(self):
        self.ast = ClassicalAST()
        self.current_line = 0
    
    def parse_file(self, file_path: str) -> ClassicalAST:
        """Parse assembly file and return AST"""
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        return self.parse_lines(lines)
    
    def parse_text(self, text: str) -> ClassicalAST:
        """Parse assembly text and return AST"""
        lines = text.strip().split('\n')
        return self.parse_lines(lines)
    
    def parse_lines(self, lines: List[str]) -> ClassicalAST:
        """Parse list of assembly lines"""
        self.ast = ClassicalAST()
        instruction_index = 0
        
        for i, line in enumerate(lines):
            self.current_line = i + 1
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith(';'):
                continue
            
            # Handle START directive
            if line.startswith('START'):
                parts = line.split()
                if len(parts) > 1:
                    self.ast.start_address = int(parts[1])
                continue
            
            # Handle END directive
            if line == 'END':
                break
            
            # Check if line has a label
            label = None
            if ':' in line:
                label, line = line.split(':', 1)
                label = label.strip()
                line = line.strip()
                self.ast.labels[label] = instruction_index
            elif ' ' in line and not line.split()[0] in ['MOVER', 'ADD', 'SUB', 'MULT', 'COMP', 'BC', 'MOVEM', 'STOP']:
                # Check if first word might be a label
                parts = line.split()
                if len(parts) > 1 and parts[1] in ['MOVER', 'ADD', 'SUB', 'MULT', 'COMP', 'BC', 'MOVEM']:
                    label = parts[0]
                    line = ' '.join(parts[1:])
                    self.ast.labels[label] = instruction_index
            
            # Parse data definitions
            if self._is_data_definition(line):
                self._parse_data_definition(line, label)
                continue
            
            # Parse instructions
            if line and line != 'STOP':
                instruction = self._parse_instruction(line, label)
                if instruction:
                    self.ast.instructions.append(instruction)
                    instruction_index += 1
            elif line == 'STOP':
                # Add STOP as final instruction
                instruction = Instruction('STOP', [], label, self.current_line)
                self.ast.instructions.append(instruction)
                instruction_index += 1
        
        return self.ast
    
    def _is_data_definition(self, line: str) -> bool:
        """Check if line is a data definition"""
        parts = line.split()
        return len(parts) >= 3 and parts[1] in ['DC', 'DS']
    
    def _parse_data_definition(self, line: str, label: Optional[str]):
        """Parse data definition line"""
        parts = line.split()
        if len(parts) >= 3:
            name = parts[0]
            directive = parts[1]
            
            if directive == 'DC':
                value = int(parts[2]) if parts[2].isdigit() else parts[2]
                size = 1
            elif directive == 'DS':
                size = int(parts[2]) if parts[2].isdigit() else 1
                value = 0
            
            data_def = DataDefinition(name, directive, value, size)
            self.ast.data_definitions[name] = data_def
    
    def _parse_instruction(self, line: str, label: Optional[str]) -> Optional[Instruction]:
        """Parse a single instruction line"""
        parts = line.split()
        if not parts:
            return None
        
        opcode = parts[0]
        operands = []
        
        if len(parts) > 1:
            # Handle operands separated by commas
            operand_str = ' '.join(parts[1:])
            operands = [op.strip() for op in operand_str.split(',')]
        
        return Instruction(opcode, operands, label, self.current_line)


def parse_classical_assembly(text: str) -> ClassicalAST:
    """Convenience function to parse assembly text"""
    parser = ClassicalAssemblyParser()
    return parser.parse_text(text)