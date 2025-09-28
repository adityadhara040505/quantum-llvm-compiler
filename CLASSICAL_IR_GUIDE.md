# Classical Assembly to LLVM IR Compilation Guide

## Overview

This guide explains how to extend the quantum-llvm-compiler project to generate LLVM IR for traditional assembly language codes. The implementation demonstrates how compiler principles can be applied to both quantum and classical computing paradigms.

## Your Assembly Code Analysis

Your assembly program performs the following operations:

```assembly
START 100              ; Program starts at address 100
MOVER AREG, ONE        ; AREG = 1 (load ONE into AREG)
ADD AREG, B            ; AREG = AREG + B = 1 + 2 = 3
MOVEM AREG, RESULT     ; RESULT = AREG = 3 (store AREG to RESULT)
SUB AREG, C            ; AREG = AREG - C = 3 - 3 = 0
AGAIN MULT AREG, D     ; AREG = AREG * D = 0 * 4 = 0 (loop label)
COMP AREG, E           ; Compare AREG with E (0 vs 5)
BC ANY, AGAIN          ; Branch to AGAIN if condition met
STOP                   ; End program
```

**Data Section:**
- ONE = 1, B = 2, C = 3, D = 4, E = 5
- RESULT = storage location

## Generated LLVM IR Explanation

### 1. Module Structure
```llvm
; ModuleID = "classical_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""
```

### 2. Global Variables (Data Section)
```llvm
@"ONE" = internal global i32 1      ; DC 1
@"B" = internal global i32 2        ; DC 2
@"C" = internal global i32 3        ; DC 3
@"D" = internal global i32 4        ; DC 4
@"E" = internal global i32 5        ; DC 5
@"RESULT" = internal global i32 0   ; DS 1 (storage)
```

### 3. Main Function with Register Allocation
```llvm
define i32 @"main"() {
entry:
  %"AREG" = alloca i32              ; Allocate AREG register
  store i32 0, i32* %"AREG"         ; Initialize AREG = 0
```

### 4. Instruction Translation

#### MOVER AREG, ONE → Load and Store
```llvm
%"load_ONE" = load i32, i32* @"ONE"     ; Load value of ONE
store i32 %"load_ONE", i32* %"AREG"     ; Store into AREG
```

#### ADD AREG, B → Arithmetic Operation
```llvm
%"areg_val" = load i32, i32* %"AREG"    ; Load current AREG value
%"load_B" = load i32, i32* @"B"         ; Load value of B
%"add_result" = add i32 %"areg_val", %"load_B"  ; Perform addition
store i32 %"add_result", i32* %"AREG"   ; Store result back to AREG
```

#### Control Flow (Labels and Branches)
```llvm
br label %"label_AGAIN"                 ; Unconditional branch to loop

label_AGAIN:                            ; Loop entry point
  ; ... loop body instructions ...
  %"cmp_result" = icmp sge i32 %"areg_val.4", %"load_E"  ; Compare
  br label %"label_AGAIN"               ; Branch back to loop
```

## Implementation Architecture

### 1. Frontend Parser (`src/frontend/classical_parser.py`)
- **Purpose**: Converts assembly text to Abstract Syntax Tree (AST)
- **Key Components**:
  - `Instruction` class: Represents individual assembly instructions
  - `DataDefinition` class: Handles DC/DS data definitions
  - `ClassicalAST` class: Container for the entire program structure

### 2. IR Generator (`run_classical_compiler.py`)
- **Purpose**: Converts AST to LLVM IR
- **Key Features**:
  - Global variable creation for data definitions
  - Register allocation for AREG
  - Basic block creation for control flow
  - Instruction-by-instruction IR generation

### 3. Assembly Instruction Mapping

| Assembly | LLVM IR Operation | Description |
|----------|-------------------|-------------|
| `MOVER reg, src` | `load` + `store` | Move data to register |
| `ADD reg, src` | `add` | Addition operation |
| `SUB reg, src` | `sub` | Subtraction operation |
| `MULT reg, src` | `mul` | Multiplication |
| `MOVEM reg, dest` | `load` + `store` | Move register to memory |
| `COMP reg, src` | `icmp` | Integer comparison |
| `BC cond, label` | `br` or `cbranch` | Conditional/unconditional branch |

## Usage Instructions

### 1. Running the Classical Compiler

```bash
# Activate the environment
source .venv/bin/activate

# Run with default assembly code
PYTHONPATH=. python run_classical_compiler.py

# Run with custom assembly file
PYTHONPATH=. python run_classical_compiler.py examples/sample_assembly.asm

# Run with inline assembly code
PYTHONPATH=. python run_classical_compiler.py "MOVER AREG, 5\nADD AREG, 3\nSTOP"
```

### 2. Output Files
- `output_classical.ll`: Generated LLVM IR code
- Console output: Compilation steps and generated IR

## Extending the Implementation

### 1. Adding New Instructions
```python
# In the IR generator, add new instruction handling:
elif instr.opcode == 'NEW_INSTRUCTION':
    # Generate appropriate LLVM IR
    result = builder.operation(operands...)
    builder.store(result, target)
```

### 2. Adding More Registers
```python
# Allocate additional registers
registers['BREG'] = builder.alloca(ir.IntType(32), name="BREG")
registers['CREG'] = builder.alloca(ir.IntType(32), name="CREG")
```

### 3. Enhanced Data Types
```python
# Support different data types
if data_def.type == 'float':
    var_type = ir.FloatType()
elif data_def.type == 'double':
    var_type = ir.DoubleType()
```

## Comparison: Quantum vs Classical IR Generation

### Similarities:
1. **AST-based parsing**: Both use structured representation
2. **LLVM integration**: Both generate LLVM-compatible IR
3. **Modular design**: Separation of frontend, IR, and backend
4. **Optimization opportunities**: Both support optimization passes

### Differences:

| Aspect | Quantum IR | Classical IR |
|--------|------------|--------------|
| **Operations** | Quantum gates (H, CNOT) | CPU instructions (ADD, SUB) |
| **State** | Qubit superposition | Register values |
| **Memory Model** | Quantum registers | Classical memory/registers |
| **Control Flow** | Quantum measurements | Conditional branches |
| **Optimization** | Gate cancellation | Traditional compiler optimizations |

## Benefits of This Approach

### 1. **Educational Value**
- Demonstrates compiler construction principles
- Shows how LLVM can target different computational models
- Provides hands-on experience with IR generation

### 2. **Extensibility**
- Easy to add new assembly instructions
- Support for multiple register architectures
- Pluggable optimization passes

### 3. **Integration**
- Works within existing quantum compiler framework
- Reuses LLVM infrastructure
- Maintains consistent tooling approach

### 4. **Research Potential**
- Foundation for hybrid quantum-classical compilation
- Platform for studying different IR representations
- Base for advanced optimization research

## Execution Flow Summary

```
Assembly Code → Parser → AST → IR Generator → LLVM IR → Output Files
     ↓             ↓       ↓         ↓            ↓         ↓
Your assembly  → Tokens → Tree → LLVM Module → .ll file → Analysis
```

This implementation successfully bridges traditional assembly language with modern LLVM compilation infrastructure, demonstrating how the same compiler principles apply across different computational paradigms.