# DXShaderInputsSet

Sets shader inputs.

```
bool  DXShaderInputsSet(
   int         shader,       // shader handle
   const int&  inputs[]      // array of input handles
   );

```

Parameters

shader

[in]  Handle of a shader created in [DXShaderCreate()](/en/docs/directx/dxshadercreate).

inputs[]

[in]  Array of input handles created using [DXInputCreate()](/en/docs/directx/dxinputcreate).

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The size of the input parameter should be equal to the number of [cbuffer](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-constants) objects declared in the shader code.
