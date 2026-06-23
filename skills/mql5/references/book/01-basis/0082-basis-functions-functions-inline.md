# Inlining

In order to improve code efficiency, modern compilers often use the following trick. When generating executable code, some function calls are replaced directly by the function body (its statements). This technique is called inlining. This speeds up the operation by avoiding the overhead associated with the organization of the call and return from the function. From a programmer's point of view, inlining doesn't change anything.

MQL5 supports inlining by default. If necessary, it can be disabled, but only in [code profiling](/en/book/automation/tester/tester_debug_profile) mode. The inline keyword is reserved in MQL5 for compatibility with C++ source codes. Its presence or absence before the function definition does not affect the generated program.
