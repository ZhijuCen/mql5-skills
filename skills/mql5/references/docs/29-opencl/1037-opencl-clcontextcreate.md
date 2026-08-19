# CLContextCreate

Creates an OpenCL context and returns its handle.

```
int  CLContextCreate(
   int  device=CL_USE_ANY     // Serial number of the OpenCL device or macro
   );

```

Parameter

device

[in]  The ordinal number of the OpenCL-device in the system. Instead of a specific number, you can specify one of the following values:

- CL_USE_ANY – any available device with OpenCL support is allowed;
- CL_USE_CPU_ONLY – only OpenCL emulation on CPU is allowed;
- CL_USE_GPU_ONLY – OpenCL emulation is prohibited and only specialized devices with OpenCL support (video cards) can be used;

- CL_USE_GPU_DOUBLE_ONLY –  only the GPUs that support type [double](/en/docs/basis/types/double) are allowed.

Return Value

A handle to the OpenCL context if successful, otherwise -1. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.
