; ModuleID = "classical_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"AREG" = alloca i32
  store i32 0, i32* %"AREG"
  %"load_ONE" = load i32, i32* @"ONE"
  store i32 %"load_ONE", i32* %"AREG"
  %"areg_val" = load i32, i32* %"AREG"
  %"load_B" = load i32, i32* @"B"
  %"add_result" = add i32 %"areg_val", %"load_B"
  store i32 %"add_result", i32* %"AREG"
  %"areg_val.1" = load i32, i32* %"AREG"
  store i32 %"areg_val.1", i32* @"RESULT"
  %"areg_val.2" = load i32, i32* %"AREG"
  %"load_C" = load i32, i32* @"C"
  %"sub_result" = sub i32 %"areg_val.2", %"load_C"
  store i32 %"sub_result", i32* %"AREG"
  br label %"label_AGAIN"
label_AGAIN:
  %"areg_val.3" = load i32, i32* %"AREG"
  %"load_D" = load i32, i32* @"D"
  %"mult_result" = mul i32 %"areg_val.3", %"load_D"
  store i32 %"mult_result", i32* %"AREG"
  %"areg_val.4" = load i32, i32* %"AREG"
  %"load_E" = load i32, i32* @"E"
  %"cmp_result" = icmp sge i32 %"areg_val.4", %"load_E"
  br label %"label_AGAIN"
exit:
  ret i32 0
}

@"ONE" = internal global i32 1
@"B" = internal global i32 2
@"C" = internal global i32 3
@"D" = internal global i32 4
@"E" = internal global i32 5
@"RESULT" = internal global i32 0