# DXShaderTexturesSet

Sets shader textures.

```
bool  DXShaderTexturesSet(
   int          shader,         // shader handle
   const  int&  textures[]      // array of structure handles
   );

```

Parameters

shader

[in]  Handle of a shader created in [DXShaderCreate()](/en/docs/directx/dxshadercreate).

textures[]

[in]  Array of texture handles created using [DXTextureCreate()](/en/docs/directx/dxtexturecreate).

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The size of the texture array should be equal to the number of [Texture2D](https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-type) objects declared in the shader code.
