# OnnxGetOutputTypeInfo

Get the description of the output type from the model.

```
bool  OnnxGetOutputTypeInfo(
   long           onnx_handle,  // ONNX session handle
   long           index,        // parameter index
   OnnxTypeInfo&  typeinfo      // parameter type description
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

index

[in]  Index of the output parameter, starting with 0.

typeinfo

[out]  The [OnnxTypeInfo](/en/docs/onnx/onnx_structures#onnxtypeinfo) structure that describes the type of the output parameter.

Return Value

Returns true on success; otherwise returns false. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.
