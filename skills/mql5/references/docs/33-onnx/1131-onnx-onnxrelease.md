# OnnxRelease

Close an ONNX session.

```
bool  OnnxRelease(
   long   onnx_handle  // ONNX session handle
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

Return Value

Returns true on success; otherwise returns false. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
