# Terminal build number

Since the terminal is constantly being improved and new features appear in its new versions, an MQL program may need to analyze the current version in order to apply different algorithm options. In addition, no program is immune to errors, including the terminal itself. Therefore, if problems occur, you should provide a diagnostic output that includes the current version of the terminal. This can help in reproducing and fixing bugs.

You can get the build number of the terminal using the TERMINAL_BUILD property in ENUM_TERMINAL_INFO_INTEGER.

```
if(TerminalInfoInteger(TERMINAL_BUILD) >= 3000)
{
   ...
}

```

Recall that the build number of the compiler with which the program is built is available in the source code through the macro definitions __MQLBUILD__ or __MQL5BUILD__ (see [Predefined Constants](/en/book/basis/preprocessor/preprocessor_predefined)).
