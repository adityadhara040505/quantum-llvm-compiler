section .data
    msg db 'Assembly basics demo (MINIMAL)', 10, 0
    msg_len equ 29
    
    ; Simple array of 6 integers  
    my_array dd 3, 5, 7, 2, 9, 1
    
    space db ' ', 0
    newline db 10, 0

section .text
    global _start

_start:
    ; Print title message
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, msg
    mov rdx, msg_len
    syscall
    
    ; Print exactly 6 array elements
    xor rcx, rcx        ; counter = 0
    
print_loop:
    cmp rcx, 6          ; check if we've printed 6 elements
    jge done
    
    ; Get array element at index rcx
    mov eax, [my_array + rcx*4]
    
    ; Simple number printing (only works for single digits 0-9)
    add al, '0'         ; convert to ASCII
    mov [temp_digit], al
    
    ; Print the digit
    mov rax, 1
    mov rdi, 1
    mov rsi, temp_digit
    mov rdx, 1
    syscall
    
    ; Print space
    mov rax, 1
    mov rdi, 1
    mov rsi, space
    mov rdx, 1
    syscall
    
    inc rcx
    jmp print_loop

done:
    ; Print newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall
    
    ; Exit
    mov rax, 60         ; sys_exit
    mov rdi, 0          ; exit status
    syscall

section .bss
    temp_digit resb 1