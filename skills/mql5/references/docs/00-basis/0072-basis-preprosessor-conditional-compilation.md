# Conditional Compilation (#ifdef, #ifndef, #else, #endif)

The preprocessor directives are used by the compiler to preprocess the source code before compiling it. The directive always begins with #, therefore the compiler prohibits using the symbol in names of variables, functions etc.

Each directive is described by a separate entry and is valid until the line break. You cannot use several directives in one entry. If the directive entry is too big, it can be broken into several lines using the '\' symbol. In this case, the next line is considered a continuation of the directive entry.

Preprocessor conditional compilation directives allow compiling or skipping a part of the program depending on the fulfillment of a certain condition.

That condition can take one of the following forms.

```
#ifdef identifier
   // the code located here is compiled if the identifier has already been defined for the preprocessor in #define directive.
#endif

```

```
#ifndef identifier
   // the code located here is compiled if the identifier is not currently defined by #define preprocessor directive.
#endif

```

Any of the conditional compilation directives can be followed by any number of lines possibly containing #else directive and ending with #endif. If the verified condition is true, the lines between #else and #endif are ignored. If the verified condition is not fulfilled, all lines between checking and #else directive (or #endif directive if the former is absent) are ignored.

Example:

```
#ifndef TestMode
   #define TestMode
#endif
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   #ifdef TestMode
      Print("Test mode");
   #else
      Print("Normal mode");
   #endif
  }

```

Depending on the program type and compilation mode, the standard macros are defined the following way:

__MQL5__  macro is defined when compiling *.mq5 file, __MQL4__ macro is defined when compiling *.mq4 one.  

_DEBUG macro is defined when compiling in debug mode.  

_RELEASE macro is defined when compiling in release mode.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   #ifdef __MQL5__
      #ifdef _DEBUG
         Print("Hello from MQL5 compiler [DEBUG]");
      #else
        #ifdef _RELEASE
           Print("Hello from MQL5 compiler [RELEASE]");
        #endif
      #endif
   #else
      #ifdef __MQL4__
        #ifdef _DEBUG
           Print("Hello from MQL4 compiler [DEBUG]");
        #else
           #ifdef _RELEASE
              Print("Hello from MQL4 compiler [RELEASE]");
           #endif
        #endif
      #endif
   #endif
  }

```
