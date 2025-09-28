; basics.asm
; Demonstrates common assembly building blocks for NASM x86_64 (Linux).
; Build:
;   nasm -f elf64 basics.asm -o basics.o
;   ld basics.o -o basics
; Run:
;   ./basics

; ------------------------------
; Constants / Equates
; ------------------------------
SYS_READ    equ 0
SYS_WRITE   equ 1
SYS_EXIT    equ 60

BUF_SIZE    equ 64      ; buffer size for input
INT_SIZE    equ 4       ; size of a 32-bit integer (for demonstration)

; ------------------------------
; Data section (initialized)
; ------------------------------
section .data
hello_msg:      db "Assembly basics demo", 10        ; string w/ newline
hello_len:      equ $ - hello_msg

prompt_msg:     db "Enter a small number (0-9): ", 0
prompt_len:     equ $ - prompt_msg

out_fmt:        db "You entered: ", 0
out_fmt_len:    equ $ - out_fmt

arr_msg:        db "Array contents: ", 0
arr_msg_len:    equ $ - arr_msg

sum_msg:        db "Sum of array = ", 0
sum_msg_len:    equ $ - sum_msg

; an initialized array of 8-bit numbers
my_array:       db 3, 5, 7, 2, 9, 1
my_array_len:   equ  $ - my_array    ; number of elements

; ------------------------------
; BSS section (uninitialized)
; ------------------------------
section .bss
input_buf:      resb BUF_SIZE       ; reserve input buffer
int_buf:        resb 16             ; temporary int -> ascii space

; ------------------------------
; Text section (code)
; ------------------------------
section .text
global _start        ; program entry point

; ------------------------------
; Macro example (NASM)
; ------------------------------
%macro PRINT_STR 2
    ; PRINT_STR addr, len
    mov rax, SYS_WRITE
    mov rdi, 1            ; stdout
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
    mov rcx, my_array_len     ; counter
    xor rbx, rbx              ; index = 0

.print_loop:
    cmp rbx, rcx
    jge .print_loop_end

    ; load byte from array
    movzx rax, byte [my_array + rbx]   ; zero-extend byte to rax

    ; convert small integer to ASCII digit (assumes 0..9)
    add al, '0'
    mov [int_buf], al
    mov byte [int_buf+1], 32    ; space
    ; write two bytes (digit + space)
    mov rax, SYS_WRITE
    mov rdi, 1
    lea rsi, [int_buf]
    mov rdx, 2
    syscall

    inc rbx
    jmp .print_loop

.print_loop_end:
    ; newline
    mov rax, SYS_WRITE
    mov rdi, 1
    mov rsi, hello_msg+hello_len-1  ; use newline from hello_msg
    mov rdx, 1
    syscall

    ; Now compute sum of array via a function call
    ; prepare arguments for sum_array:
    ; rdi = address of array
    ; rsi = length
    lea rdi, [my_array]
    mov rsi, my_array_len
    call sum_array             ; returns sum in rax

    ; print sum message
    PRINT_STR sum_msg, sum_msg_len

    ; convert rax (sum) to ASCII and write (supports small positive sums)
    ; Here we do a very small integer-to-string for demo.
    ; For general ints you'd implement division loop.
    mov rbx, rax               ; rbx = sum
    add bl, '0'
    mov [int_buf], bl
    mov byte [int_buf+1], 10   ; newline
    mov rax, SYS_WRITE
    mov rdi, 1
    lea rsi, [int_buf]
    mov rdx, 2
    syscall

    ; Prompt for user input
    PRINT_STR prompt_msg, prompt_len

    ; read up to BUF_SIZE bytes from stdin
    mov rax, SYS_READ
    mov rdi, 0                ; stdin
    lea rsi, [input_buf]
    mov rdx, BUF_SIZE
    syscall
    ; rax = number of bytes read

    ; simple parse: take first char, if digit convert to numeric value
    movzx rbx, byte [input_buf]
    cmp bl, '0'
    jl .bad_input
    cmp bl, '9'
    jg .bad_input
    sub bl, '0'               ; bl = numeric value 0..9

    ; show echo "You entered: <digit>"
    PRINT_STR out_fmt, out_fmt_len
    mov [int_buf], bl
    add byte [int_buf], '0'   ; convert back to ASCII
    mov byte [int_buf+1], 10
    mov rax, SYS_WRITE
    mov rdi, 1
    lea rsi, [int_buf]
    mov rdx, 2
    syscall
    jmp .good_exit

.bad_input:
    ; print error message
    PRINT_STR hello_msg, hello_len    ; reuse hello_msg as a simple error (demo)

.good_exit:
    ; exit with code 0
    mov rax, SYS_EXIT
    xor rdi, rdi
    syscall

; ------------------------------
; sum_array - sums bytes in an array
; Input: rdi -> array (address), rsi = length (count)
; Return: rax = sum (fits in 64-bit)
; Demonstrates: prologue/epilogue, push/pop, loop, conditional
; ------------------------------
sum_array:
    push rbp
    mov rbp, rsp

    ; save rdi and rsi if needed (we'll use rbx as index)
    push rbx
    xor rbx, rbx        ; index i = 0
    xor rax, rax        ; accumulator sum = 0

.sum_loop_begin:
    cmp rbx, rsi
    jge .sum_loop_end

    ; load byte [rdi + rbx] zero-extended
    movzx rcx, byte [rdi + rbx]
    add rax, rcx        ; sum += array[i]
    inc rbx
    jmp .sum_loop_begin

.sum_loop_end:
    pop rbx
    pop rbp
    ret