# CLSetKernelArg

Sets a parameter for the OpenCL function.

```
bool  CLSetKernelArg(
   int   kernel,        // Handle to the kernel of an OpenCL program
   uint  arg_index,     // The number of the argument of the OpenCL function
   void  arg_value      // Source code
   );

```

Parameters

kernel

[in]  Handle to a kernel of the OpenCL program.

arg_index

[in]  The number of the function argument, numbering starts with zero.

arg_value

[in]  The value of the function argument.

Return Value

Returns true if successful, otherwise returns false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

At the moment, the following error codes are used:

- ERR_INVALID_PARAMETER,
- ERR_OPENCL_INVALID_HANDLE – invalid handle to the OpenCL kernel.
- ERR_OPENCL_SET_KERNEL_PARAMETER - internal error of OpenCL.
