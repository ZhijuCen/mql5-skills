# Predefined constants of the MQL5 language

This section describes all the constants defined by the runtime environment for any program. We have already seen some of them in previous sections. Some constants relate to applied MQL5 programming aspects, which will be presented in later chapters.

| Constant | Description | Value |
| --- | --- | --- |
| CHARTS_MAX | The maximum possible number of simultaneously open  charts | 100 |
| clrNONE | No  color | -1 (0xFFFFFFFF) |
| EMPTY_VALUE | Empty value in the indicator buffer | DBL_MAX |
| INVALID_HANDLE | Invalid handle | -1 |
| NULL | Any type null | 0 |
| WHOLE_ARRAY | The number of elements until the end of the array, i.e., the entire array will be processed | -1 |
| WRONG_VALUE | A constant can be implicitly cast to any enumeration type | -1 |

As shown in the [Files](/en/book/common/files) chapter, the INVALID_HANDLE constant can be used to validate file descriptors.

The WHOLE_ARRAY constant is intended for functions working with [arrays](/en/book/common/arrays) that require specifying the number of elements in the processed arrays: If it is necessary to process all the array values from the specified position to the end, specify the WHOLE_ARRAY value.

The EMPTY_VALUE constant is usually assigned to those elements in [indicator buffers](/en/book/applications/indicators_make), which should not be drawn on the chart. In other words, this constant means a default [empty value](/en/book/applications/indicators_make/indicators_empty_value). Later, we will describe how it can be replaced for a specific indicator buffer with another value, for example, 0.

The WRONG_VALUE constant is intended for those cases when it is required to designate an incorrect [enumeration](/en/book/basis/builtin_types/enums) value.

In addition, two constants have different values depending on the compilation method.

| Constant | Description |
| --- | --- |
| IS_DEBUG_MODE | An attribute of running an mq5 program in the debug mode: It is non-zero in the debug mode and 0 otherwise |
| IS_PROFILE_MODE | An attribute of running an mq5 program in the profiling mode: It is non-zero in the profiling mode and 0 otherwise |

The IS_PROFILE_MODE constant allows you to change the operation of the program for the correct collection of information in the [profiling](/en/book/automation/tester/tester_debug_profile) mode. Profiling allows you to measure the execution time of individual program fragments (functions and individual lines).

The compiler sets the IS_PROFILE_MODE constant value during compilation. Normally, it is set to 0. When the program is launched in a profiling mode, a special compilation is performed, and in this case, a non-zero value is used instead of IS_PROFILE_MODE.

The IS_DEBUG_MODE constant works in a similar way: it is equal to 0 as a result of native compilation and is greater than 0 after debug compilation. It is useful in cases where it is necessary to slightly change the operation of the MQL program for verification purposes: for example, to output additional information to the log or to create auxiliary graphical objects on the chart.

The preprocessor defines _DEBUG and _RELEASE constants that are similar in meaning (see [Predefined preprocessor constants](/en/book/basis/preprocessor/preprocessor_predefined)).

More detailed information about the program operation mode can be found at runtime using the MQLInfoInteger function (see [Terminal and program operating modes](/en/book/common/environment/env_mode)). In particular, the debug build of a program can be run without a debugger.
