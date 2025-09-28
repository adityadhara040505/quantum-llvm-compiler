; simple_demo.asm - Working simple assembly program
section .data
    msg db "Hello from x86_64 Assembly!", 10
    msg_len equ $ - msg
    array db 3, 5, 7, 2, 9, 1
    array_len equ 6

section .text
    global _start

_start:
    ; Print hello message
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, msg_len
    syscall

    ; Sum the array
    xor rax, rax        ; sum = 0
    xor rbx, rbx        ; index = 0

sum_loop:
    cmp rbx, array_len
    jge sum_done
    
    movzx rcx, byte [array + rbx]
    add rax, rcx
    inc rbx
    jmp sum_loop

sum_done:
    ; Convert sum to ASCII digit (assuming sum < 10)
    add al, '0'
    
    ; Print sum
    mov [msg], al       ; Reuse msg space
    mov rax, 1          ; sys_write
    mov rdi, 1
    mov rsi, msg
    mov rdx, 1
    syscall
    
    ; Print newline
    mov byte [msg], 10
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, 1
    syscall

    ; Exit
    mov rax, 60         ; sys_exit
    xor rdi, rdi
    syscall