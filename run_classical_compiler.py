#!/usr/bin/env python3
"""
Classical Assembly to LLVM IR Compiler Runner
Usage: python run_classical_compiler.py [assembly_text_or_file]
"""

import sys
import os
from src.frontend.classical_parser import parse_classical_assembly
from llvmlite import ir

def simple_ir_generator(ast):
    """Simplified IR generator that works with the current project structure"""
    
    # Create module
    module = ir.Module(name="classical_module")
    
    # Create main function
    func_type = ir.FunctionType(ir.IntType(32), [])
    main_func = ir.Function(module, func_type, name="main")
    
    # Create entry block
    entry_block = main_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(entry_block)
    
    # Create global variables for data definitions
    variables = {}
    for name, data_def in ast.data_definitions.items():
        var_type = ir.IntType(32)
        global_var = ir.GlobalVariable(module, var_type, name=name)
        global_var.linkage = 'internal'
        global_var.initializer = ir.Constant(var_type, data_def.value if data_def.directive == 'DC' else 0)
        variables[name] = global_var
    
    # Allocate AREG register
    areg = builder.alloca(ir.IntType(32), name="AREG")
    zero = ir.Constant(ir.IntType(32), 0)
    builder.store(zero, areg)
    
    # Create basic blocks for labels
    blocks = {}
    for label in ast.labels.keys():
        block = main_func.append_basic_block(name=f"label_{label}")
        blocks[label] = block
    
    exit_block = main_func.append_basic_block(name="exit")
    blocks['exit'] = exit_block
    
    # Generate instructions (simplified)
    for instr in ast.instructions:
        # Handle label jumps
        if instr.label and instr.label in blocks:
            if not builder.block.is_terminated:
                builder.branch(blocks[instr.label])
            builder = ir.IRBuilder(blocks[instr.label])
        
        # Generate instruction IR
        if instr.opcode == 'MOVER' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                source = instr.operands[1]
                if source in variables:
                    value = builder.load(variables[source], name=f"load_{source}")
                    builder.store(value, areg)
                else:
                    try:
                        imm_val = ir.Constant(ir.IntType(32), int(source))
                        builder.store(imm_val, areg)
                    except ValueError:
                        pass
        
        elif instr.opcode == 'ADD' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 0)
                result = builder.add(areg_val, source_val, name="add_result")
                builder.store(result, areg)
        
        elif instr.opcode == 'SUB' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 0)
                result = builder.sub(areg_val, source_val, name="sub_result")
                builder.store(result, areg)
        
        elif instr.opcode == 'MULT' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 1)
                result = builder.mul(areg_val, source_val, name="mult_result")
                builder.store(result, areg)
        
        elif instr.opcode == 'MOVEM' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                dest = instr.operands[1]
                if dest in variables:
                    areg_val = builder.load(areg, name="areg_val")
                    builder.store(areg_val, variables[dest])
        
        elif instr.opcode == 'COMP' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = builder.load(areg, name="areg_val")
                operand = instr.operands[1]
                if operand in variables:
                    cmp_val = builder.load(variables[operand], name=f"load_{operand}")
                else:
                    cmp_val = ir.Constant(ir.IntType(32), int(operand) if operand.isdigit() else 0)
                # Store comparison result (simplified)
                cmp_result = builder.icmp_signed('>=', areg_val, cmp_val, name="cmp_result")
        
        elif instr.opcode == 'BC' and len(instr.operands) >= 2:
            target_label = instr.operands[1]
            if target_label in blocks:
                if not builder.block.is_terminated:
                    builder.branch(blocks[target_label])
        
        elif instr.opcode == 'STOP':
            if not builder.block.is_terminated:
                builder.branch(exit_block)
    
    # Switch to exit block and add return
    if not builder.block.is_terminated:
        builder.branch(exit_block)
    
    builder = ir.IRBuilder(exit_block)
    ret_val = ir.Constant(ir.IntType(32), 0)
    builder.ret(ret_val)
    
    return str(module)

def run_classical_compiler(assembly_text):
    """Run the classical assembly compilation pipeline."""
    print("🚀 Running classical assembly compiler")
    print("=" * 50)
    
    # 1. Parse assembly to AST
    print("1. Parsing assembly code...")
    ast = parse_classical_assembly(assembly_text)
    print(f"   ✓ Parsed {len(ast.instructions)} instructions")
    print(f"   ✓ Found {len(ast.data_definitions)} data definitions")
    print(f"   ✓ Found {len(ast.labels)} labels")
    
    # 2. Generate LLVM IR
    print("2. Generating LLVM IR...")
    ir_code = simple_ir_generator(ast)
    print("   ✓ IR generation complete")
    
    # 3. Write output file
    print("3. Writing output files...")
    with open("output_classical.ll", "w") as f:
        f.write(ir_code)
    print("   ✓ Generated: output_classical.ll")
    
    # 4. Display results
    print("4. Generated IR code:")
    print("-" * 30)
    print(ir_code)
    print("-" * 30)
    
    print("=" * 50)
    print("✅ Classical assembly compilation completed successfully!")
    return True

def main():
    assembly_code = """START 100
MOVER AREG, ONE
ADD AREG, B
MOVEM AREG, RESULT
SUB AREG, C
AGAIN MULT AREG, D
COMP AREG, E
BC ANY, AGAIN
STOP
ONE DC 1
B DC 2
C DC 3
D DC 4
E DC 5
RESULT DS 1
END"""
    
    if len(sys.argv) > 1:
        # If file provided, read it
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r') as f:
                assembly_code = f.read()
        else:
            # Treat as direct assembly code
            assembly_code = sys.argv[1]
    
    try:
        run_classical_compiler(assembly_code)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()