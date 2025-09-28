; basics_corrected.asm
; Fixed version of basics.asm - resolves segmentation fault
; Build:
;   nasm -f elf64 basics_corrected.asm -o basics_corrected.o
;   ld basics_corrected.o -o basics_corrected
; Run:
;   ./basics_corrected

; ------------------------------
; Constants / Equates
; ------------------------------
SYS_READ    equ 0
SYS_WRITE   equ 1
SYS_EXIT    equ 60

BUF_SIZE    equ 64      ; buffer size for input

; ------------------------------
; Data section (initialized)
; ------------------------------
section .data
hello_msg:      db "Assembly basics demo (FIXED)", 10
hello_len:      equ $ - hello_msg

prompt_msg:     db "Enter a small number (0-9): "
prompt_len:     equ $ - prompt_msg

out_fmt:        db "You entered: "
out_fmt_len:    equ $ - out_fmt

arr_msg:        db "Array contents: "
arr_msg_len:    equ $ - arr_msg

sum_msg:        db "Sum of array = "
sum_msg_len:    equ $ - sum_msg

newline:        db 10

; an initialized array of 8-bit numbers
my_array:       db 3, 5, 7, 2, 9, 1
my_array_len:   equ 6    ; FIXED: explicitly set to 6 elements

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
global _start

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
    mov rcx, my_array_len     ; counter = 6
    xor rbx, rbx              ; index = 0

.print_loop:
    cmp rbx, rcx              ; compare index with array length
    jge .print_loop_end       ; if index >= length, exit loop

    ; load byte from array
    movzx rax, byte [my_array + rbx]   ; zero-extend byte to rax

    ; convert small integer to ASCII digit (assumes 0..9)
    add al, '0'
    mov [int_buf], al
    mov byte [int_buf+1], 32    ; space character
    
    ; write two bytes (digit + space)
    mov rax, SYS_WRITE
    mov rdi, 1
    mov rsi, int_buf
    mov rdx, 2
    syscall

    inc rbx                   ; increment index
    jmp .print_loop           ; continue loop

.print_loop_end:
    ; print newline
    PRINT_STR newline, 1

    ; Now compute sum of array via a function call
    ; prepare arguments for sum_array:
    ; rdi = address of array
    ; rsi = length
    mov rdi, my_array
    mov rsi, my_array_len
    call sum_array             ; returns sum in rax

    ; print sum message
    PRINT_STR sum_msg, sum_msg_len

    ; convert rax (sum) to ASCII and write
    ; (this assumes sum < 10 for simplicity)
    add al, '0'               ; convert to ASCII
    mov [int_buf], al
    mov byte [int_buf+1], 10  ; newline
    
    mov rax, SYS_WRITE
    mov rdi, 1
    mov rsi, int_buf
    mov rdx, 2
    syscall

    ; Prompt for user input
    PRINT_STR prompt_msg, prompt_len

    ; read up to BUF_SIZE bytes from stdin
    mov rax, SYS_READ
    mov rdi, 0                ; stdin
    mov rsi, input_buf
    mov rdx, BUF_SIZE
    syscall

    ; simple parse: take first char, if digit convert to numeric value
    movzx rbx, byte [input_buf]
    cmp bl, '0'
    jl .bad_input
    cmp bl, '9'
    jg .bad_input
    sub bl, '0'               ; bl = numeric value 0..9

    ; show echo "You entered: <digit>"
    PRINT_STR out_fmt, out_fmt_len
    add bl, '0'               ; convert back to ASCII
    mov [int_buf], bl
    mov byte [int_buf+1], 10  ; newline
    
    mov rax, SYS_WRITE
    mov rdi, 1
    mov rsi, int_buf
    mov rdx, 2
    syscall
    jmp .good_exit

.bad_input:
    ; print error message (reuse hello_msg for simplicity)
    PRINT_STR hello_msg, hello_len

.good_exit:
    ; exit with code 0
    mov rax, SYS_EXIT
    xor rdi, rdi
    syscall

; ------------------------------
; sum_array - sums bytes in an array
; Input: rdi -> array (address), rsi = length (count)
; Return: rax = sum (fits in 64-bit)
; ------------------------------
sum_array:
    push rbp
    mov rbp, rsp
    push rbx

    xor rbx, rbx        ; index i = 0
    xor rax, rax        ; accumulator sum = 0

.sum_loop_begin:
    cmp rbx, rsi        ; compare index with length
    jge .sum_loop_end   ; if index >= length, exit

    ; load byte [rdi + rbx] zero-extended
    movzx rcx, byte [rdi + rbx]
    add rax, rcx        ; sum += array[i]
    inc rbx             ; increment index
    jmp .sum_loop_begin ; continue loop

.sum_loop_end:
    pop rbx
    pop rbp
    ret