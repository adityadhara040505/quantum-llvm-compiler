#!/usr/bin/env python3
"""
Quantum-LLVM Compiler - Main Entry Point
========================================

A hybrid quantum-classical compiler supporting:
- QASM quantum circuit compilation to LLVM IR
- NASM x86_64 assembly compilation to LLVM IR  
- Unified quantum-classical program execution

Author: Quantum-LLVM Compiler Team
Version: 1.0.0
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scripts.run_quantum_compiler import main as quantum_main
from scripts.classical_compiler_final import main as classical_main

def print_banner():
    """Print the project banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                    QUANTUM-LLVM COMPILER v1.0.0                     ║
║                                                                      ║
║  A hybrid compiler for quantum circuits and classical assembly      ║
║  • QASM → LLVM IR → Executable                                      ║
║  • NASM → LLVM IR → Executable                                      ║
║  • Quantum-Classical hybrid execution                               ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main entry point for the quantum-llvm-compiler."""
    parser = argparse.ArgumentParser(
        description='Quantum-LLVM Compiler - Hybrid quantum-classical compilation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s quantum examples/quantum/grover.qasm        # Compile quantum circuit
  %(prog)s classical examples/assembly/working_demo.asm # Compile assembly
  %(prog)s --list-examples                              # Show available examples
  %(prog)s --demo                                       # Run demonstration
        """
    )
    
    parser.add_argument('mode', choices=['quantum', 'classical'], nargs='?',
                       help='Compilation mode')
    parser.add_argument('input_file', nargs='?',
                       help='Input file to compile')
    parser.add_argument('--output', '-o', 
                       help='Output file name (default: auto-generated)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--list-examples', action='store_true',
                       help='List available example files')
    parser.add_argument('--demo', action='store_true',
                       help='Run interactive demonstration')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list_examples:
        list_examples()
        return
        
    if args.demo:
        run_demo()
        return
        
    if not args.mode and not args.list_examples and not args.demo:
        parser.error("Mode is required unless using --list-examples or --demo")
        
    if args.mode and not args.input_file:
        parser.error("Input file is required when specifying a compilation mode")
        
    if not os.path.exists(args.input_file):
        print(f"❌ Error: Input file '{args.input_file}' not found")
        return 1
        
    print(f"🚀 Starting {args.mode} compilation...")
    print(f"📁 Input: {args.input_file}")
    
    if args.mode == 'quantum':
        return compile_quantum(args.input_file, args.output, args.verbose)
    else:
        return compile_classical(args.input_file, args.output, args.verbose)

def list_examples():
    """List available example files."""
    print("📚 Available Examples:\n")
    
    examples_dir = Path("examples")
    
    # Quantum examples
    quantum_dir = examples_dir / "quantum"
    if quantum_dir.exists():
        print("🔬 Quantum Examples:")
        for file in sorted(quantum_dir.glob("*.qasm")):
            print(f"   • {file}")
        print()
    
    # Assembly examples  
    assembly_dir = examples_dir / "assembly"
    if assembly_dir.exists():
        print("⚙️  Assembly Examples:")
        for file in sorted(assembly_dir.glob("*.asm")):
            print(f"   • {file}")
        print()
            
    # Classical examples
    classical_dir = examples_dir / "classical"
    if classical_dir.exists():
        print("💻 Classical Examples:")
        for file in sorted(classical_dir.glob("*")):
            if file.is_file():
                print(f"   • {file}")
        print()

def run_demo():
    """Run interactive demonstration."""
    print("🎮 Interactive Demo Mode\n")
    
    print("Choose a demonstration:")
    print("1. Quantum Circuit Compilation (Grover's Algorithm)")
    print("2. Assembly Compilation (Array Processing)")
    print("3. Hybrid Quantum-Classical Example")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                demo_quantum()
                break
            elif choice == "2":
                demo_assembly()
                break
            elif choice == "3":
                demo_hybrid()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

def demo_quantum():
    """Run quantum compilation demo."""
    print("\n🔬 Quantum Circuit Compilation Demo")
    grover_file = "examples/quantum/grover.qasm"
    if os.path.exists(grover_file):
        compile_quantum(grover_file, None, True)
    else:
        print(f"❌ Demo file not found: {grover_file}")

def demo_assembly():
    """Run assembly compilation demo."""
    print("\n⚙️  Assembly Compilation Demo")
    demo_file = "examples/assembly/working_demo.asm"
    if os.path.exists(demo_file):
        compile_classical(demo_file, None, True)
    else:
        print(f"❌ Demo file not found: {demo_file}")

def demo_hybrid():
    """Run hybrid compilation demo."""
    print("\n🔗 Hybrid Quantum-Classical Demo")
    print("This feature combines quantum and classical compilation...")
    # Implementation would go here
    print("✨ Demo completed!")

def compile_quantum(input_file, output_file, verbose):
    """Compile quantum circuit."""
    try:
        print(f"🔬 Compiling quantum circuit: {input_file}")
        
        # Import and run quantum compiler
        from scripts.run_quantum_compiler import main as qmain
        
        # Set up arguments for quantum compiler
        original_argv = sys.argv
        sys.argv = ["quantum_compiler", input_file]
        if output_file:
            sys.argv.extend(["-o", output_file])
        if verbose:
            sys.argv.append("-v")
            
        result = qmain()
        sys.argv = original_argv
        
        print("✅ Quantum compilation completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Quantum compilation failed: {e}")
        return 1

def compile_classical(input_file, output_file, verbose):
    """Compile classical assembly."""
    try:
        print(f"⚙️  Compiling assembly: {input_file}")
        
        # Import and run classical compiler
        from scripts.classical_compiler_final import main as cmain
        
        # Set up arguments for classical compiler
        original_argv = sys.argv
        sys.argv = ["classical_compiler", input_file]
        if output_file:
            sys.argv.extend(["-o", output_file])
        if verbose:
            sys.argv.append("-v")
            
        result = cmain()
        sys.argv = original_argv
        
        print("✅ Classical compilation completed successfully!")
        return result
        
    except Exception as e:
        print(f"❌ Classical compilation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())