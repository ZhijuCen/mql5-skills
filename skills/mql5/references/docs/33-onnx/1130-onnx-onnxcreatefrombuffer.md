# OnnxCreateFromBuffer

Create an ONNX session, loading a model from a data array.

```
long  OnnxCreateFromBuffer(
   const uchar&  buffer[],   // array reference
   ulong         flags       // model creation flags
   );

```

Parameters

buffer

[in] Array with ONNX model data.

flags

[in] Flags from [ENUM_ONNX_FLAGS](/en/docs/onnx/onnx_structures#enum_onnx_flags), describing the model creation mode: ONNX_COMMON_FOLDER and ONNX_DEBUG_LOGS.

Return Value

The handle of the created session or INVALID_HANDLE if error occurs. To obtain the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
