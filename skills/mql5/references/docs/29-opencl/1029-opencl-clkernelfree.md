# CLKernelFree

Removes an OpenCL start function.

```
void  CLKernelFree(
   int  kernel     // Handle to the kernel of an OpenCL program
   );

```

Parameters

kernel_name

[in]  Handle of the kernel object.

Return Value

None. In the case of an internal error the value of [_LastError](/en/docs/predefined/_lasterror) changes. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.
