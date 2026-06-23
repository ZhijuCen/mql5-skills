# DXInputSet

Sets shader inputs.

```
bool  DXInputSet(
   int          input,      // graphic context handle
   const void&  data        // data for setting  
   );

```

Parameters

input

[in]  Handle of inputs for a shader obtained in [DXInputCreate()](/en/docs/directx/dxinputcreate).

data

[in]  Data for setting shader inputs.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.
