section .data
    prompt db 'Enter a number: ', 0
    prompt_len equ $ - prompt - 1
    
    array_msg db 'Array contents: ', 0
    array_msg_len equ $ - array_msg - 1
    
    result_msg db 'Result: ', 0
    result_msg_len equ $ - result_msg - 1
    
    newline db 10, 0
    space db ' ', 0
    
    ; Fixed array with explicit count
    my_array dd 3, 5, 7, 2, 9, 1
    array_count equ 6    ; EXPLICIT count, not calculated!

section .bss
    number resb 32
    result resb 32

section .text
    global _start

_start:
    ; Show prompt
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    mov rsi, prompt
    mov rdx, prompt_len
    syscall
    
    ; Read input
    mov rax, 0          ; sys_read
    mov rdi, 0          ; stdin
    mov rsi, number
    mov rdx, 32
    syscall
    
    ; Show array message
    mov rax, 1
    mov rdi, 1
    mov rsi, array_msg
    mov rdx, array_msg_len
    syscall
    
    ; Print array with FIXED bounds
    mov rcx, 0          ; index counter
    
print_loop:
    cmp rcx, array_count    ; Compare with EXPLICIT count
    jge print_done
    
    ; Get array element
    mov eax, dword [my_array + rcx*4]
    
    ; Convert to string and print
    call print_number
    
    ; Print space
    mov rax, 1
    mov rdi, 1
    mov rsi, space
    mov rdx, 1
    syscall
    
    inc rcx
    jmp print_loop

print_done:
    ; Print newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall
    
    ; Show result message
    mov rax, 1
    mov rdi, 1
    mov rsi, result_msg
    mov rdx, result_msg_len
    syscall
    
    ; Simple calculation (sum first 3 elements)
    mov eax, dword [my_array]     ; first element
    add eax, dword [my_array + 4] ; second element
    add eax, dword [my_array + 8] ; third element
    
    call print_number
    
    ; Print newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall
    
    ; Exit
    mov rax, 60
    mov rdi, 0
    syscall

; Function to print a number
print_number:
    push rbx
    push rcx
    push rdx
    push rdi
    
    mov rbx, 10
    mov rcx, 0
    
    ; Handle zero case
    test eax, eax
    jnz convert_loop
    
    ; Print '0'
    mov rax, 1
    mov rdi, 1
    mov rsi, zero_char
    mov rdx, 1
    syscall
    jmp print_number_done
    
convert_loop:
    xor rdx, rdx
    div rbx
    add dl, '0'
    push rdx
    inc rcx
    test eax, eax
    jnz convert_loop
    
print_digits:
    pop rdx
    mov [temp_char], dl
    mov rax, 1
    mov rdi, 1
    mov rsi, temp_char
    mov rdx, 1
    syscall
    loop print_digits
    
print_number_done:
    pop rdi
    pop rdx
    pop rcx
    pop rbx
    ret

section .data
    zero_char db '0', 0
    temp_char db 0