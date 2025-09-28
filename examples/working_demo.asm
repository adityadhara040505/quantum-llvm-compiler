section .data
    title_msg db 'Assembly demo (MAX example)', 10, 0
    title_len equ $ - title_msg

    array_msg db 'Array: ', 0
    array_len equ $ - array_msg

    result_msg db 'Maximum element: ', 0
    result_len equ $ - result_msg

    ; Our 6-element array (same as before)
    my_array dd 3, 5, 7, 2, 9, 1

    space db ' ', 0
    newline db 10, 0

section .bss
    digit_buffer resb 12    ; buffer for number conversion

section .text
    global _start

_start:
    ; Print title
    mov rax, 1
    mov rdi, 1
    mov rsi, title_msg
    mov rdx, title_len
    syscall

    ; Print "Array: "
    mov rax, 1
    mov rdi, 1
    mov rsi, array_msg
    mov rdx, array_len
    syscall

    ; Print all 6 array elements
    xor rbx, rbx            ; counter = 0
print_array_loop:
    cmp rbx, 6
    jge array_done

    mov eax, [my_array + rbx*4]
    call print_number

    ; Print space
    mov rax, 1
    mov rdi, 1
    mov rsi, space
    mov rdx, 1
    syscall

    inc rbx
    jmp print_array_loop

array_done:
    ; Print newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    ; Print result message
    mov rax, 1
    mov rdi, 1
    mov rsi, result_msg
    mov rdx, result_len
    syscall

    ; Find maximum element
    mov ecx, 6              ; number of elements
    mov eax, [my_array]     ; assume first element is max
    mov rbx, 1              ; index = 1

find_max_loop:
    cmp rbx, rcx
    jge found_max

    mov edx, [my_array + rbx*4]
    cmp edx, eax
    jle skip_update
    mov eax, edx            ; update max

skip_update:
    inc rbx
    jmp find_max_loop

found_max:
    ; Print the max value in EAX
    call print_number

    ; Print final newline
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

    ; Exit
    mov rax, 60
    xor rdi, rdi
    syscall

; -------------------------------------------------
; Function: print_number
; Prints positive integer in EAX
; -------------------------------------------------
print_number:
    push rax
    push rbx
    push rcx
    push rdx
    push rsi

    mov rbx, 10
    xor rcx, rcx
    mov rsi, digit_buffer + 11
    mov byte [rsi], 0
    dec rsi

    test eax, eax
    jnz convert_digits
    mov byte [rsi], '0'
    inc rcx
    jmp print_digits

convert_digits:
    xor rdx, rdx
    div rbx
    add dl, '0'
    mov [rsi], dl
    dec rsi
    inc rcx
    test eax, eax
    jnz convert_digits

print_digits:
    inc rsi
    mov rax, 1
    mov rdi, 1
    mov rdx, rcx
    syscall

    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret
