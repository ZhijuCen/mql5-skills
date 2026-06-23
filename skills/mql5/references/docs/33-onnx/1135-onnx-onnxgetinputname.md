# OnnxGetInputName

Get the name of a model's input by index.

```
string  OnnxGetInputName(
   long   onnx_handle,  // ONNX session handle
   long   index         // parameter index
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

index

[in]  Index of the input parameter, starting with 0.

Return Value

Returns the name of the input parameter on success; otherwise returns NULL. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
