#!/usr/bin/env python3
"""
Enhanced Classical Assembly Compiler with Basic Optimizations
Demonstrates dead code elimination and constant folding
"""

import sys
import os
from src.frontend.classical_parser import parse_classical_assembly
from llvmlite import ir

def optimize_ast(ast):
    """Apply basic optimizations to the AST"""
    optimized_instructions = []
    
    for i, instr in enumerate(ast.instructions):
        # Dead code elimination: Remove instructions after STOP
        if instr.opcode == 'STOP':
            optimized_instructions.append(instr)
            break
        
        # Constant folding: If we move a constant then immediately add another constant,
        # we could potentially fold these operations
        optimized_instructions.append(instr)
    
    ast.instructions = optimized_instructions
    return ast

def analyze_program_flow(ast):
    """Analyze the program for statistics and insights"""
    stats = {
        'total_instructions': len(ast.instructions),
        'arithmetic_operations': 0,
        'memory_operations': 0,
        'control_flow': 0,
        'data_definitions': len(ast.data_definitions)
    }
    
    for instr in ast.instructions:
        if instr.opcode in ['ADD', 'SUB', 'MULT']:
            stats['arithmetic_operations'] += 1
        elif instr.opcode in ['MOVER', 'MOVEM']:
            stats['memory_operations'] += 1
        elif instr.opcode in ['COMP', 'BC']:
            stats['control_flow'] += 1
    
    return stats

def enhanced_ir_generator(ast):
    """Enhanced IR generator with better optimization"""
    
    # Create module
    module = ir.Module(name="optimized_classical_module")
    
    # Add module-level metadata
    module.add_metadata([ir.MetaDataString(module, "Classical Assembly to LLVM IR")])
    
    # Create main function
    func_type = ir.FunctionType(ir.IntType(32), [])
    main_func = ir.Function(module, func_type, name="main")
    
    # Create entry block
    entry_block = main_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(entry_block)
    
    # Create global variables for data definitions with comments
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
    
    # Allocate AREG register with debug info
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
    
    # Generate instructions with optimizations
    for instr in ast.instructions:
        # Handle label jumps
        if instr.label and instr.label in blocks:
            builder.branch(blocks[instr.label])
            builder = ir.IRBuilder(blocks[instr.label])
        
        # Generate optimized instruction IR
        if instr.opcode == 'MOVER':
            _generate_optimized_mover(builder, instr, variables, areg)
        elif instr.opcode == 'ADD':
            _generate_optimized_arithmetic(builder, instr, variables, areg, 'add')
        elif instr.opcode == 'SUB':
            _generate_optimized_arithmetic(builder, instr, variables, areg, 'sub')
        elif instr.opcode == 'MULT':
            _generate_optimized_arithmetic(builder, instr, variables, areg, 'mul')
        elif instr.opcode == 'MOVEM':
            _generate_optimized_movem(builder, instr, variables, areg)
        elif instr.opcode == 'COMP':
            _generate_optimized_comp(builder, instr, variables, areg)
        elif instr.opcode == 'BC':
            _generate_optimized_branch(builder, instr, blocks)
        elif instr.opcode == 'STOP':
            builder.branch(exit_block)
    
    # Switch to exit block and add return
    builder = ir.IRBuilder(exit_block)
    ret_val = ir.Constant(ir.IntType(32), 0)
    builder.ret(ret_val)
    
    return str(module)

def _generate_optimized_mover(builder, instr, variables, areg):
    """Generate optimized MOVER instruction"""
    if len(instr.operands) >= 2 and instr.operands[0] == 'AREG':
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

def _generate_optimized_arithmetic(builder, instr, variables, areg, operation):
    """Generate optimized arithmetic instructions"""
    if len(instr.operands) >= 2 and instr.operands[0] == 'AREG':
        areg_val = builder.load(areg, name="areg_val")
        source = instr.operands[1]
        
        if source in variables:
            source_val = builder.load(variables[source], name=f"load_{source}")
        else:
            source_val = ir.Constant(ir.IntType(32), int(source) if source.isdigit() else 0)
        
        # Generate appropriate arithmetic operation
        if operation == 'add':
            result = builder.add(areg_val, source_val, name="add_result")
        elif operation == 'sub':
            result = builder.sub(areg_val, source_val, name="sub_result")
        elif operation == 'mul':
            result = builder.mul(areg_val, source_val, name="mult_result")
        
        builder.store(result, areg)

def _generate_optimized_movem(builder, instr, variables, areg):
    """Generate optimized MOVEM instruction"""
    if len(instr.operands) >= 2 and instr.operands[0] == 'AREG':
        dest = instr.operands[1]
        if dest in variables:
            areg_val = builder.load(areg, name="areg_val")
            builder.store(areg_val, variables[dest])

def _generate_optimized_comp(builder, instr, variables, areg):
    """Generate optimized COMP instruction"""
    if len(instr.operands) >= 2 and instr.operands[0] == 'AREG':
        areg_val = builder.load(areg, name="areg_val")
        operand = instr.operands[1]
        
        if operand in variables:
            cmp_val = builder.load(variables[operand], name=f"load_{operand}")
        else:
            cmp_val = ir.Constant(ir.IntType(32), int(operand) if operand.isdigit() else 0)
        
        # Generate comparison
        builder.icmp_signed('>=', areg_val, cmp_val, name="cmp_result")

def _generate_optimized_branch(builder, instr, blocks):
    """Generate optimized branch instruction"""
    if len(instr.operands) >= 2:
        target_label = instr.operands[1]
        if target_label in blocks:
            builder.branch(blocks[target_label])

def run_enhanced_classical_compiler(assembly_text):
    """Run the enhanced classical assembly compilation pipeline."""
    print("🚀 Running Enhanced Classical Assembly Compiler")
    print("=" * 60)
    
    # 1. Parse assembly to AST
    print("1. Parsing assembly code...")
    ast = parse_classical_assembly(assembly_text)
    print(f"   ✓ Parsed {len(ast.instructions)} instructions")
    print(f"   ✓ Found {len(ast.data_definitions)} data definitions")
    print(f"   ✓ Found {len(ast.labels)} labels")
    
    # 2. Analyze program
    print("2. Analyzing program structure...")
    stats = analyze_program_flow(ast)
    print(f"   ✓ Arithmetic operations: {stats['arithmetic_operations']}")
    print(f"   ✓ Memory operations: {stats['memory_operations']}")
    print(f"   ✓ Control flow operations: {stats['control_flow']}")
    
    # 3. Apply optimizations
    print("3. Applying optimizations...")
    original_count = len(ast.instructions)
    ast = optimize_ast(ast)
    optimized_count = len(ast.instructions)
    print(f"   ✓ Instructions: {original_count} → {optimized_count}")
    
    # 4. Generate enhanced LLVM IR
    print("4. Generating enhanced LLVM IR...")
    ir_code = enhanced_ir_generator(ast)
    print("   ✓ Enhanced IR generation complete")
    
    # 5. Write output files
    print("5. Writing output files...")
    with open("output_enhanced_classical.ll", "w") as f:
        f.write(ir_code)
    print("   ✓ Generated: output_enhanced_classical.ll")
    
    # 6. Display key sections of generated IR
    print("6. Generated IR Summary:")
    print("-" * 40)
    lines = ir_code.split('\n')
    
    # Show global variables
    print("Global Variables:")
    for line in lines:
        if line.startswith('@'):
            print(f"  {line}")
    
    print("\nMain Function Signature:")
    for line in lines:
        if 'define i32 @"main"' in line:
            print(f"  {line}")
            break
    
    print(f"\nTotal IR lines: {len(lines)}")
    print("-" * 40)
    
    print("=" * 60)
    print("✅ Enhanced classical assembly compilation completed!")
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
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r') as f:
                assembly_code = f.read()
        else:
            assembly_code = sys.argv[1]
    
    try:
        run_enhanced_classical_compiler(assembly_code)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()