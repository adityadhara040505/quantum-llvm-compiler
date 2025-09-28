; ModuleID = "classical_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"AREG" = alloca i32
  store i32 0, i32* %"AREG"
  %"load_X" = load i32, i32* @"X"
  store i32 %"load_X", i32* %"AREG"
  %"areg_val" = load i32, i32* %"AREG"
  %"load_Y" = load i32, i32* @"Y"
  %"add_result" = add i32 %"areg_val", %"load_Y"
  store i32 %"add_result", i32* %"AREG"
  %"areg_val.1" = load i32, i32* %"AREG"
  store i32 %"areg_val.1", i32* @"TEMP"
  %"load_Z" = load i32, i32* @"Z"
  store i32 %"load_Z", i32* %"AREG"
  %"areg_val.2" = load i32, i32* %"AREG"
  %"load_TEMP" = load i32, i32* @"TEMP"
  %"mult_result" = mul i32 %"areg_val.2", %"load_TEMP"
  store i32 %"mult_result", i32* %"AREG"
  %"areg_val.3" = load i32, i32* %"AREG"
  store i32 %"areg_val.3", i32* @"RESULT"
  br label %"exit"
exit:
  ret i32 0
}

@"X" = internal global i32 10
@"Y" = internal global i32 20
@"Z" = internal global i32 3
@"TEMP" = internal global i32 0
@"RESULT" = internal global i32 0