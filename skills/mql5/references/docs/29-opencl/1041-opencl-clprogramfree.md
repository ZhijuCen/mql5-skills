# CLProgramFree

Removes an OpenCL program.

```
void  CLProgramFree(
   int  program     // Handle to an OpenCL object
   );

```

Parameters

program

[in]  Handle of the OpenCL object.

Return Value

None. In the case of an internal error the value of [_LastError](/en/docs/predefined/_lasterror) changes. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.
