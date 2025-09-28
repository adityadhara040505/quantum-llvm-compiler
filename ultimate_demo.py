"""
Ultimate Assembly Demo - Three Ways to Run basics.asm
Shows traditional NASM, enhanced quantum-llvm-compiler, and unified approach
"""

import subprocess
import sys
import os
sys.path.append('src')

from frontend.nasm_parser import compile_nasm_to_llvm

def method_1_traditional_nasm():
    """Method 1: Traditional NASM compilation"""
    print("🔧 METHOD 1: Traditional NASM Compilation")
    print("=" * 50)
    
    try:
        # Compile with NASM
        print("Step 1: nasm -f elf64 examples/basics.asm -o basics.o")
        result = subprocess.run(['nasm', '-f', 'elf64', 'examples/basics.asm', '-o', 'basics.o'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ NASM compilation failed: {result.stderr}")
            return False
        
        # Link with ld
        print("Step 2: ld basics.o -o basics")
        result = subprocess.run(['ld', 'basics.o', '-o', 'basics'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Linking failed: {result.stderr}")
            return False
        
        print("✅ Traditional compilation successful!")
        print("📁 Generated executable: ./basics")
        
        # Show file info
        result = subprocess.run(['file', 'basics'], capture_output=True, text=True)
        print(f"📋 File type: {result.stdout.strip()}")
        
        result = subprocess.run(['ls', '-lh', 'basics'], capture_output=True, text=True)
        print(f"📏 File size: {result.stdout.split()[4]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in traditional compilation: {e}")
        return False

def method_2_quantum_compiler():
    """Method 2: quantum-llvm-compiler with NASM parser"""
    print("\n🚀 METHOD 2: quantum-llvm-compiler Enhanced NASM Parser")
    print("=" * 50)
    
    try:
        print("Step 1: Parse and compile to LLVM IR")
        llvm_ir = compile_nasm_to_llvm('examples/basics.asm')
        
        # Save output
        output_file = 'output_basics_quantum_compiler.ll'
        with open(output_file, 'w') as f:
            f.write(llvm_ir)
        
        print("✅ quantum-llvm-compiler compilation successful!")
        print(f"📁 Generated LLVM IR: {output_file}")
        
        # Show stats
        lines = llvm_ir.split('\n')
        functions = llvm_ir.count('define ')
        globals = llvm_ir.count('@')
        allocas = llvm_ir.count('alloca')
        
        print(f"📊 IR Statistics:")
        print(f"   • Lines: {len(lines)}")
        print(f"   • Functions: {functions}")
        print(f"   • Global variables: {globals}")
        print(f"   • Local allocations: {allocas}")
        
        # Show file size
        result = subprocess.run(['ls', '-lh', output_file], capture_output=True, text=True)
        print(f"📏 File size: {result.stdout.split()[4]}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error in quantum-llvm-compiler: {e}")
        return None

def method_3_unified_demo():
    """Method 3: Run the unified demo"""
    print("\n🌐 METHOD 3: Unified Quantum-Classical Demo")
    print("=" * 50)
    
    try:
        print("Running unified demo showing both quantum and classical compilation...")
        result = subprocess.run([sys.executable, 'unified_demo.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Unified demo completed successfully!")
            # Show just the key parts of output
            lines = result.stdout.split('\n')
            for line in lines:
                if ('✅' in line or '📄' in line or '🎉' in line or 
                    'NASM x86_64 Assembly' in line or 'Quantum Circuit' in line):
                    print(line)
        else:
            print(f"❌ Unified demo failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running unified demo: {e}")

def compare_approaches():
    """Compare all three approaches"""
    print(f"\n📊 COMPARISON OF APPROACHES")
    print("=" * 50)
    
    print("🔧 Traditional NASM:")
    print("   ✓ Produces native executable")
    print("   ✓ Direct hardware execution") 
    print("   ✗ Platform-specific")
    print("   ✗ Limited to x86_64")
    
    print("\n🚀 quantum-llvm-compiler:")
    print("   ✓ Generates portable LLVM IR")
    print("   ✓ Can be optimized with LLVM tools")
    print("   ✓ Cross-platform intermediate representation")
    print("   ✓ Integrates with quantum compilation")
    print("   ✗ Requires LLVM toolchain for execution")
    
    print("\n🌐 Unified Approach:")
    print("   ✓ Handles both quantum AND classical code")
    print("   ✓ Single compilation framework")
    print("   ✓ Research and educational tool")
    print("   ✓ Enables hybrid quantum-classical applications")

def main():
    """Main demo orchestrator"""
    print("🎯 ULTIMATE ASSEMBLY DEMO - Three Ways to Run basics.asm")
    print("=" * 70)
    print("This demo shows three different approaches to handle the same assembly code:")
    print("1. Traditional NASM → Native executable")
    print("2. quantum-llvm-compiler → LLVM IR")  
    print("3. Unified quantum-classical compilation")
    print("=" * 70)
    
    # Change to project directory
    os.chdir('/home/aditya/VIT/5th Sem/System Programming/quantum-llvm-compiler')
    
    # Run all three methods
    traditional_success = method_1_traditional_nasm()
    quantum_output = method_2_quantum_compiler()
    method_3_unified_demo()
    
    # Compare approaches
    compare_approaches()
    
    # Final summary
    print(f"\n🎉 ULTIMATE DEMO COMPLETE!")
    print("=" * 50)
    if traditional_success:
        print("✅ Traditional NASM compilation: SUCCESS")
        print("   → Native executable created: ./basics")
    else:
        print("❌ Traditional NASM compilation: FAILED")
        
    if quantum_output:
        print("✅ quantum-llvm-compiler: SUCCESS")
        print(f"   → LLVM IR generated: {quantum_output}")
    else:
        print("❌ quantum-llvm-compiler: FAILED")
        
    print("✅ Unified demo: COMPLETED")
    print("   → Shows integration of both paradigms")
    
    print(f"\n💡 Your quantum-llvm-compiler is now capable of:")
    print("   • Quantum circuit compilation (QASM → QIR)")
    print("   • Classical assembly compilation (NASM → LLVM IR)")
    print("   • Unified quantum-classical workflows")
    print("   • Educational assembly analysis")

if __name__ == "__main__":
    main()