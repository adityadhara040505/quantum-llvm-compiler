; ModuleID = "nasm_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"rax" = alloca i64
  store i64 0, i64* %"rax"
  %"rbx" = alloca i64
  store i64 0, i64* %"rbx"
  %"rcx" = alloca i64
  store i64 0, i64* %"rcx"
  %"rdx" = alloca i64
  store i64 0, i64* %"rdx"
  %"rdi" = alloca i64
  store i64 0, i64* %"rdi"
  %"rsi" = alloca i64
  store i64 0, i64* %"rsi"
  ; ; syscall
  ; ; cmp rbx rcx
  ; ; jge .print_loop_end
  store i64 1, i64* %"rdi"
  store i64 2, i64* %"rdx"
  ; ; syscall
  %"load_rbx" = load i64, i64* %"rbx"
  %"inc_result" = add i64 %"load_rbx", 1
  store i64 %"inc_result", i64* %"rbx"
  ; ; jmp .print_loop
  store i64 1, i64* %"rdi"
  store i64 1, i64* %"rdx"
  ; ; syscall
  store i64 1, i64* %"rdi"
  store i64 2, i64* %"rdx"
  ; ; syscall
  ; ; syscall
  ; ; cmp bl '0'
  ; ; jl .bad_input
  ; ; cmp bl '9'
  store i64 1, i64* %"rdi"
  store i64 2, i64* %"rdx"
  ; ; syscall
  ; ; jmp .good_exit
  store i64 0, i64* %"rdi"
  ; ; syscall
  ; ; cmp rbx rsi
  ; ; jge .sum_loop_end
  %"load_rax" = load i64, i64* %"rax"
  %"add_result" = add i64 %"load_rax", 0
  store i64 %"add_result", i64* %"rax"
  %"load_rbx.1" = load i64, i64* %"rbx"
  %"inc_result.1" = add i64 %"load_rbx.1", 1
  store i64 %"inc_result.1", i64* %"rbx"
  ; ; jmp .sum_loop_begin
  ret i32 0
}

@"prompt_msg" = internal global i8 0
@"out_fmt" = internal global i8 0
@"arr_msg" = internal global i8 0
@"sum_msg" = internal global i8 0
@"my_array" = internal global i8 0