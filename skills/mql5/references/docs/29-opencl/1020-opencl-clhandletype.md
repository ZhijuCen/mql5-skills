# CLHandleType

Returns the type of an OpenCL handle as a value of the ENUM_OPENCL_HANDLE_TYPE enumeration.

```
ENUM_OPENCL_HANDLE_TYPE  CLHandleType(
   int  handle     // Handle of an OpenCL object
   );

```

Parameters

handle

[in]  A handle to an OpenCL object: a context, a kernel or an OpenCL program.

Return Value

The type of the OpenCL handle as a value of the [ENUM_OPENCL_HANDLE_TYPE](/en/docs/opencl/clhandletype#enum_opencl_handle_type) enumeration.

ENUM_OPENCL_HANDLE_TYPE

| Identifier | Description |
| --- | --- |
| OPENCL_INVALID | Incorrect handle |
| OPENCL_CONTEXT | A handle of the OpenCL context |
| OPENCL_PROGRAM | A handle of the OpenCL program |
| OPENCL_KERNEL | A handle of the OpenCL kernel |
| OPENCL_BUFFER | A handle of the OpenCL buffer |
