# OnnxGetInputCount

Get the number of inputs in an ONNX model.

```
long  OnnxGetInputCount(
   long   onnx_handle  // ONNX session handle
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

Return Value

Returns the number of input parameters on success; otherwise returns -1. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
