# OnnxCreate

Create an ONNX session, loading a model from an *.onnx file.

```
long  OnnxCreate(
   string  filename,  // file path
   uint    flags      // flags to create the model
   );

```

Parameters

filename

[in]  Path to the *.onnx file of the model relative to the \MQL5\Files\ folder.

flags

[in] Flags from [ENUM_ONNX_FLAGS](/en/docs/onnx/onnx_structures#enum_onnx_flags), describing the model creation mode: ONNX_COMMON_FOLDER and ONNX_DEBUG_LOGS.

Return Value

The handle of the created session or INVALID_HANDLE if error occurs. To obtain the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.

Note

If the specified file is not found on disk, the system retries to open the file, appending the '.onnx' extension to the name.
