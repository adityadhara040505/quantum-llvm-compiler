; ModuleID = "quantum_module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"q0" = internal global i8 0
declare void @"qop.h"(i32 %".1")

@"q1" = internal global i8 0
@"q2" = internal global i8 0
declare void @"qop.cx"(i32 %".1", i32 %".2")

declare void @"qop.measure"(i32 %".1")
