"""
Enhanced NASM Demo for basics.asm
Tests the extended quantum-llvm-compiler with complex assembly features
"""

import sys
import os
sys.path.append('src')

from frontend.nasm_parser import compile_nasm_to_llvm

def demo_basics_compilation():
    """Demo compilation of the complex basics.asm file"""
    print("=" * 70)
    print("Enhanced NASM Assembly Compilation - basics.asm")
    print("=" * 70)
    
    asm_file = "examples/basics.asm"
    
    if not os.path.exists(asm_file):
        print(f"❌ File not found: {asm_file}")
        return
    
    try:
        print(f"🔄 Compiling {asm_file} with quantum-llvm-compiler NASM parser...")
        
        # Compile to LLVM IR
        llvm_ir = compile_nasm_to_llvm(asm_file)
        
        # Save the output
        output_file = "output_basics_enhanced.ll"
        with open(output_file, 'w') as f:
            f.write(llvm_ir)
        
        print(f"✅ Successfully compiled {asm_file}")
        print(f"📄 Enhanced LLVM IR saved to: {output_file}")
        
        # Show stats
        lines = llvm_ir.split('\n')
        print(f"📊 Generated IR Statistics:")
        print(f"   • Total lines: {len(lines)}")
        print(f"   • Functions: {llvm_ir.count('define ')}")
        print(f"   • Global variables: {llvm_ir.count('@')}")
        print(f"   • Allocations: {llvm_ir.count('alloca')}")
        
        print("\n🔍 Generated LLVM IR Preview (first 15 lines):")
        print("-" * 50)
        for i, line in enumerate(lines[:15]):
            print(f"{i+1:2d}: {line}")
        if len(lines) > 15:
            print(f"... and {len(lines) - 15} more lines")
        
        print("\n💡 Features Detected in Assembly:")
        features = []
        with open(asm_file, 'r') as f:
            content = f.read()
            
        if 'section .data' in content:
            features.append("✓ Data section with initialized variables")
        if 'section .bss' in content:
            features.append("✓ BSS section with uninitialized buffers")
        if '%macro' in content:
            features.append("✓ NASM macros (PRINT_STR)")
        if 'syscall' in content:
            features.append("✓ System calls (read/write/exit)")
        if 'call' in content:
            features.append("✓ Function calls (sum_array)")
        if '.print_loop:' in content:
            features.append("✓ Loops with labels")
        if 'push rbp' in content:
            features.append("✓ Function prologue/epilogue")
        
        for feature in features:
            print(f"   {feature}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error compiling: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_with_traditional():
    """Compare quantum-llvm-compiler output with traditional NASM"""
    print(f"\n{'='*70}")
    print("Comparison: quantum-llvm-compiler vs Traditional NASM")
    print("="*70)
    
    print("🔧 Traditional NASM approach:")
    print("   1. nasm -f elf64 basics.asm -o basics.o")
    print("   2. ld basics.o -o basics")
    print("   3. ./basics")
    print("   → Produces native x86_64 executable")
    
    print("\n🚀 quantum-llvm-compiler approach:")
    print("   1. python basics_demo.py")
    print("   2. Generates LLVM IR representation")
    print("   3. Could be further compiled with LLVM tools")
    print("   → Produces portable LLVM IR for analysis/optimization")
    
    print("\n🎯 Benefits of quantum-llvm-compiler approach:")
    print("   • Unified framework for quantum + classical code")
    print("   • LLVM IR enables advanced optimizations")
    print("   • Cross-platform intermediate representation")
    print("   • Integration with quantum compilation pipeline")
    print("   • Educational tool for understanding assembly→IR translation")

def main():
    """Main demo function"""
    print("🚀 Enhanced NASM Assembly Compiler Demo")
    print("Demonstrates quantum-llvm-compiler's ability to handle complex x86_64 assembly")
    
    # Compile the complex assembly file
    output_file = demo_basics_compilation()
    
    # Show comparison
    compare_with_traditional()
    
    if output_file:
        print(f"\n🎉 Demo Complete!")
        print(f"📁 Check the generated file: {output_file}")
        print("💡 This demonstrates the extensibility of the quantum-llvm-compiler")
        print("   to handle both quantum circuits AND classical assembly code!")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    main()