# CLContextFree

Removes an OpenCL context.

```
void  CLContextFree(
   int  context     // Handle to an OpenCL context
   );

```

Parameters

context

[in]  Handle of the OpenCL context.

Return Value

None. In the case of an internal error the value of [_LastError](/en/docs/predefined/_lasterror) changes. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.
