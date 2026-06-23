# Predefined preprocessor constants

MQL5 has several predefined constants that are equivalent to simple macros, but they are defined by the compiler itself. The following table lists some of their names and meanings.

| Name | Description |
| --- | --- |
| __COUNTER__ | Counter (each mention in the text during macro expansion results in an increase of 1) |
| __DATE__ | Compilation date (day) |
| __DATETIME__ | Compilation date and time |
| __FILE__ | The name of the compiled file |
| __FUNCSIG__ | Current function signature |
| __FUNCTION__ | Current function name |
| __LINE__ | Line number in the compiled file |
| __MQLBUILD__, __MQL5BUILD__ | Compiler version |
| __RANDOM__ | Random number of type ulong |
| __PATH__ | Path to compiled file |
| _DEBUG | Defined when compiling in debug mode |
| _RELEASE | Defined when compiling in normal mode |
