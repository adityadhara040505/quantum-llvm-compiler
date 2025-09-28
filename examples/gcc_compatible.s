# 🔧 **Complete Guide: Running Assembly Code**

## **Multiple Approaches to Assembly Programming**

Your NASM x86_64 assembly code represents a different paradigm from the custom assembly language we implemented in the quantum-llvm-compiler project. Here are all the ways to handle assembly code:

---

## **🎯 Method 1: Standard NASM Assembly (Your Code)**

### **✅ Successfully Working Now!**

**Your Code Type:** NASM x86_64 Linux Assembly
**Status:** ✅ **WORKING** - Simple version compiled and runs successfully!

### **Steps to Run:**

```bash
# 1. Install NASM (done)
sudo apt install nasm

# 2. Compile to object file
nasm -f elf64 your_file.asm -o your_file.o

# 3. Link to executable
ld your_file.o -o your_file

# 4. Run
./your_file
```

### **Working Example Output:**
```
Hello from x86_64 Assembly!
K
```
*(K represents sum of array: 3+5+7+2+9+1 = 27, displayed as ASCII character)*

---

## **🎯 Method 2: Using GCC with Assembly**

You can also use GCC to compile assembly:

<function_calls>
<invoke name="create_file">
<parameter name="content">; gcc_compatible.asm
.section .data
    msg: .ascii "Hello from GCC Assembly!\n"
    msg_len = . - msg

.section .text
    .global _start

_start:
    # Write system call
    movq $1, %rax           # sys_write
    movq $1, %rdi           # stdout
    movq $msg, %rsi         # message
    movq $msg_len, %rdx     # length
    syscall
    
    # Exit system call
    movq $60, %rax          # sys_exit
    movq $0, %rdi           # status
    syscall