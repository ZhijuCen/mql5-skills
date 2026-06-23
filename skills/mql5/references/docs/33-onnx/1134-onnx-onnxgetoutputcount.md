# OnnxGetOutputCount

Get the number of outputs in an ONNX model.

```
long  OnnxGetOutputCount(
   long   onnx_handle  // ONNX session handle
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

Return Value

Returns the number of output parameters on success; otherwise returns -1. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
