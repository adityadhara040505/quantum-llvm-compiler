; ModuleID = "classical_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"AREG" = alloca i32
  store i32 0, i32* %"AREG"
  br label %"label_array_msg db 'Array"
"label_array_msg db 'Array":
  br label %"label_result_msg db 'Maximum element"
"label_result_msg db 'Maximum element":
  br label %"exit"
label__start:
label_print_array_loop:
label_array_done:
label_find_max_loop:
label_skip_update:
label_found_max:
label_print_number:
label_convert_digits:
label_print_digits:
exit:
  ret i32 0
}
