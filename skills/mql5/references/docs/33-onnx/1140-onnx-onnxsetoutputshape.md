# OnnxSetOutputShape

Set the shape of a model's output data by index.

```
bool  OnnxSetOutputShape(
   long          onnx_handle,   // ONNX session handle
   long          output_index,  // output parameter index
   const ulong&  shape[]        // array describing output data shape
   );

```

Parameters

onnx_handle

[in]  ONNX session object handle created via [OnnxCreate](/en/docs/onnx/onnxcreate) or [OnnxCreateFromBuffer](/en/docs/onnx/onnxcreatefrombuffer).

output_index

[in]  Index of the output parameter, starting from 0.

shape

[in]  Array describing model's output data shape.

Return Value

Returns the name of the input parameter on success; otherwise returns NULL. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError](/en/docs/check/getlasterror) function.

Example:

```
//---- describe the shapes of the model's input and output data
   const long  ExtOutputShape[] = {1,1};
   const long  ExtInputShape [] = {1,10,4};
//--- create the model
   long handle=OnnxCreateFromBuffer(model,ONNX_DEBUG_LOGS);
//--- specify the shape of the input data
   if(!OnnxSetInputShape(handle,0,ExtInputShape))
     {
      Print("failed, OnnxSetInputShape error ",GetLastError());
      OnnxRelease(handle);
      return(-1);
     }
//--- specify the shape of the output data
   if(!OnnxSetOutputShape(handle,0,ExtOutputShape))
     {
      Print("failed, OnnxSetOutputShape error ",GetLastError());
      OnnxRelease(handle);
      return(-1);
     }

```

See also

[OnnxSetInputShape](/en/docs/onnx/onnxsetinputshape)
