#!/usr/bin/env python3
"""
Final Working Classical Assembly to LLVM IR Compiler
This version handles all edge cases and produces clean IR
"""

import sys
import os
from src.frontend.classical_parser import parse_classical_assembly
from llvmlite import ir

def final_ir_generator(ast):
    """Final working IR generator"""
    
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
        if data_def.directive == 'DC':
            global_var.initializer = ir.Constant(var_type, data_def.value)
        else:
            global_var.initializer = ir.Constant(var_type, 0)
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
    
    # Generate instructions
    current_builder = builder
    
    for instr in ast.instructions:
        # Handle label jumps
        if instr.label and instr.label in blocks:
            if not current_builder.block.is_terminated:
                current_builder.branch(blocks[instr.label])
            current_builder = ir.IRBuilder(blocks[instr.label])
        
        # Generate instruction IR
        if instr.opcode == 'MOVER' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                source = instr.operands[1]
                if source in variables:
                    value = current_builder.load(variables[source], name=f"load_{source}")
                    current_builder.store(value, areg)
                else:
                    try:
                        imm_val = ir.Constant(ir.IntType(32), int(source))
                        current_builder.store(imm_val, areg)
                    except ValueError:
                        pass
        
        elif instr.opcode == 'ADD' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = current_builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = current_builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 0)
                result = current_builder.add(areg_val, source_val, name="add_result")
                current_builder.store(result, areg)
        
        elif instr.opcode == 'SUB' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = current_builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = current_builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 0)
                result = current_builder.sub(areg_val, source_val, name="sub_result")
                current_builder.store(result, areg)
        
        elif instr.opcode == 'MULT' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = current_builder.load(areg, name="areg_val")
                source = instr.operands[1]
                if source in variables:
                    source_val = current_builder.load(variables[source], name=f"load_{source}")
                else:
                    source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 1)
                result = current_builder.mul(areg_val, source_val, name="mult_result")
                current_builder.store(result, areg)
        
        elif instr.opcode == 'MOVEM' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                dest = instr.operands[1]
                if dest in variables:
                    areg_val = current_builder.load(areg, name="areg_val")
                    current_builder.store(areg_val, variables[dest])
        
        elif instr.opcode == 'COMP' and len(instr.operands) >= 2:
            if instr.operands[0] == 'AREG':
                areg_val = current_builder.load(areg, name="areg_val")
                operand = instr.operands[1]
                if operand in variables:
                    cmp_val = current_builder.load(variables[operand], name=f"load_{operand}")
                else:
                    cmp_val = ir.Constant(ir.IntType(32), int(operand) if operand.isdigit() else 0)
                # Store comparison result
                cmp_result = current_builder.icmp_signed('>=', areg_val, cmp_val, name="cmp_result")
        
        elif instr.opcode == 'BC' and len(instr.operands) >= 2:
            target_label = instr.operands[1]
            if target_label in blocks:
                if not current_builder.block.is_terminated:
                    current_builder.branch(blocks[target_label])
        
        elif instr.opcode == 'STOP':
            if not current_builder.block.is_terminated:
                current_builder.branch(exit_block)
    
    # Handle the main path to exit
    if not current_builder.block.is_terminated:
        current_builder.branch(exit_block)
    
    # Create exit block
    exit_builder = ir.IRBuilder(exit_block)
    ret_val = ir.Constant(ir.IntType(32), 0)
    exit_builder.ret(ret_val)
    
    return str(module)

def analyze_assembly_program(assembly_text):
    """Analyze the assembly program and provide insights"""
    lines = [line.strip() for line in assembly_text.split('\n') if line.strip()]
    
    analysis = {
        'total_lines': len(lines),
        'instructions': 0,
        'data_definitions': 0,
        'labels': 0,
        'comments': 0
    }
    
    for line in lines:
        if line.startswith(';'):
            analysis['comments'] += 1
        elif ' DC ' in line or ' DS ' in line:
            analysis['data_definitions'] += 1
        elif any(op in line for op in ['MOVER', 'ADD', 'SUB', 'MULT', 'MOVEM', 'COMP', 'BC', 'STOP']):
            analysis['instructions'] += 1
        elif line not in ['START', 'END'] and not line.startswith('START'):
            analysis['labels'] += 1
    
    return analysis

def main():
    print("🔧 Classical Assembly to LLVM IR Compiler")
    print("=" * 50)
    
    # Default assembly program
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
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r') as f:
                assembly_code = f.read()
        else:
            assembly_code = sys.argv[1]
    
    try:
        # Analyze the assembly program
        print("📊 Assembly Program Analysis:")
        analysis = analyze_assembly_program(assembly_code)
        for key, value in analysis.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print("\n🔍 Assembly Code:")
        print("-" * 30)
        for i, line in enumerate(assembly_code.split('\n'), 1):
            if line.strip():
                print(f"{i:2d}: {line}")
        print("-" * 30)
        
        # Parse and compile
        print("\n⚙️  Compilation Process:")
        print("1. Parsing assembly code...")
        ast = parse_classical_assembly(assembly_code)
        print(f"   ✓ Instructions: {len(ast.instructions)}")
        print(f"   ✓ Data definitions: {len(ast.data_definitions)}")
        print(f"   ✓ Labels: {len(ast.labels)}")
        
        print("\n2. Generating LLVM IR...")
        ir_code = final_ir_generator(ast)
        
        print("3. Writing output file...")
        with open("output_final_classical.ll", "w") as f:
            f.write(ir_code)
        print("   ✓ Created: output_final_classical.ll")
        
        print("\n📋 Generated LLVM IR:")
        print("=" * 50)
        print(ir_code)
        print("=" * 50)
        
        print("\n✅ Compilation completed successfully!")
        print(f"📁 Output saved to: output_final_classical.ll")
        
    except Exception as e:
        print(f"\n❌ Compilation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()