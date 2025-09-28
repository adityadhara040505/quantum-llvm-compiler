; basics_fixed.asm
; Fixed version of the assembly program
; Build:
;   nasm -f elf64 basics_fixed.asm -o basics_fixed.o
;   ld basics_fixed.o -o basics_fixed

; ------------------------------
; Constants / Equates
; ------------------------------
SYS_READ    equ 0
SYS_WRITE   equ 1
SYS_EXIT    equ 60

; ------------------------------
; Data section (initialized)
; ------------------------------
section .data
hello_msg:      db "Assembly basics demo", 10
hello_len:      equ $ - hello_msg

arr_msg:        db "Array contents: "
arr_msg_len:    equ $ - arr_msg

sum_msg:        db 10, "Sum of array = "
sum_msg_len:    equ $ - sum_msg

newline:        db 10
space:          db 32

; an initialized array of 8-bit numbers
my_array:       db 3, 5, 7, 2, 9, 1
my_array_len:   equ 6    ; Fixed: explicit count

; ------------------------------
; BSS section (uninitialized)
; ------------------------------
section .bss
int_buf:        resb 16

; ------------------------------
; Text section (code)
; ------------------------------
section .text
global _start

; ------------------------------
; Macro for printing strings
; ------------------------------
%macro PRINT_STR 2
    mov rax, SYS_WRITE
    mov rdi, 1
    mov rsi, %1
    mov rdx, %2
    syscall
%endmacro

; ------------------------------
; _start: program entry
; ------------------------------
_start:
    ; Print greeting
    PRINT_STR hello_msg, hello_len

    ; Print array message
    PRINT_STR arr_msg, arr_msg_len

    ; Print array as numbers using loop
    mov rcx, my_array_len     ; counter (fixed: use explicit length)
    xor rbx, rbx              ; index = 0

.print_loop:
    cmp rbx, rcx
    jge .print_loop_end

    ; load byte from array
    movzx rax, byte [my_array + rbx]

    ; convert small integer to ASCII digit (assumes 0..9)
    add al, '0'
    mov [int_buf], al
    
    ; Print digit
    PRINT_STR int_buf, 1
    
    ; Print space
    PRINT_STR space, 1

    inc rbx
    jmp .print_loop

.print_loop_end:
    ; Print newline
    PRINT_STR newline, 1

    ; Compute sum of array
    lea rdi, [my_array]
    mov rsi, my_array_len
    call sum_array

    ; Print sum message
    PRINT_STR sum_msg, sum_msg_len

    ; Convert sum to ASCII (simple version for small sums)
    add al, '0'
    mov [int_buf], al
    PRINT_STR int_buf, 1
    PRINT_STR newline, 1

    ; Exit
    mov rax, SYS_EXIT
    xor rdi, rdi
    syscall

; ------------------------------
; sum_array function
; ------------------------------
sum_array:
    push rbp
    mov rbp, rsp
    push rbx
    
    xor rbx, rbx        ; index = 0
    xor rax, rax        ; sum = 0

.sum_loop:
    cmp rbx, rsi
    jge .sum_done

    movzx rcx, byte [rdi + rbx]
    add rax, rcx
    inc rbx
    jmp .sum_loop

.sum_done:
    pop rbx
    pop rbp
    ret