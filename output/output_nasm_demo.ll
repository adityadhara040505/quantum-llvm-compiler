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
  ; ; cmp rbx array_len
  ; ; jge sum_done
  %"load_rax" = load i64, i64* %"rax"
  %"load_rcx" = load i64, i64* %"rcx"
  %"add_result" = add i64 %"load_rax", %"load_rcx"
  store i64 %"add_result", i64* %"rax"
  %"load_rbx" = load i64, i64* %"rbx"
  %"inc_result" = add i64 %"load_rbx", 1
  store i64 %"inc_result", i64* %"rbx"
  ; ; jmp sum_loop
  store i64 1, i64* %"rdi"
  store i64 1, i64* %"rdx"
  ; ; syscall
  store i64 1, i64* %"rax"
  store i64 1, i64* %"rdi"
  store i64 1, i64* %"rdx"
  ; ; syscall
  store i64 0, i64* %"rdi"
  ; ; syscall
  ret i32 0
}
