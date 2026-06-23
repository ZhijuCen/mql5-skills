# CLBufferCreate

Creates an OpenCL buffer and returns its handle.

```
int  CLBufferCreate(
   int   context,     // Handle to an OpenCL context
   uint  size,        // Buffer size
   uint  flags        // Flags combination which specify properties of OpenCL buffer 
   );

```

Parameters

context

[in]  A handle to context OpenCL.

size

[in]  Buffer size in bytes.

flags

[in]  Buffer properties that are set using a combination of flags: CL_MEM_READ_WRITE, CL_MEM_WRITE_ONLY, CL_MEM_READ_ONLY, CL_MEM_ALLOC_HOST_PTR.

Return Value

A handle to an OpenCL buffer if successful. In case of error -1 is returned. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

At the moment, the following error codes are used:

- ERR_OPENCL_INVALID_HANDLE  - invalid handle to OpenCL context.
- ERR_NOT_ENOUGH_MEMORY – insufficient memory.
- ERR_OPENCL_BUFFER_CREATE – internal error creating buffers.
