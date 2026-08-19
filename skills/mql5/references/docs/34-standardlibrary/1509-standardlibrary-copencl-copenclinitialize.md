# Initialize

Initializes the OpenCL program.

```
bool  Initialize(
   const string  program,           // handle of the OpenCL program
   const bool    show_log=true      // keep a log
   );

```

Parameters

program

[in]  Handle of the OpenCL program.

show_log=true

[in]  Enable logging messages.

Return Value

Returns true, if the initialization succeeded. Otherwise, it returns false.
