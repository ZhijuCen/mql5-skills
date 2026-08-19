# CLKernelCreate

Creates the OpenCL program kernel and returns its handle.

```
int  CLKernelCreate(
   int           program,        // Handle to an OpenCL object
   const string  kernel_name     // Kernel name
   );

```

Parameters

program

[in]  Handle to an object of the OpenCL program.

kernel_name

[in]  The name of the kernel function in the appropriate OpenCL program, in which execution begins.

Return Value

A handle to an OpenCL object if successful. In case of error -1 is returned. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

At the moment, the following error codes are used:

- ERR_OPENCL_INVALID_HANDLE - invalid handle to OpenCL program.
- ERR_INVALID_PARAMETER - invalid string parameter.
- ERR_OPENCL_TOO_LONG_KERNEL_NAME - kernel name contains more than 127 characters.
- ERR_OPENCL_KERNEL_CREATE - internal error occurred while creating an OpenCL object.
