# OnnxGetOutputName

Get the name of a model's output by index.

```
string  OnnxGetOutputName(
   long   onnx_handle,  // ONNX session handle
   long   index         // parameter index
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

index

[in]  Index of the output parameter, starting with 0.

Return Value

Returns the name of the output parameter on success; otherwise returns NULL. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
