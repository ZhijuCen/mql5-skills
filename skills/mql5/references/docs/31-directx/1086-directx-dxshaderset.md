# DXShaderSet

Sets a shader for rendering.

```
bool  DXShaderSet(
   int  context,      // graphic context handle
   int  shader        // shader handle
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

shader

[in]  Handle of a shader created in [DXShaderCreate()](/en/docs/directx/dxshadercreate).

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

Several types of shaders can simultaneously be used for rendering (vertex, geometry and pixel ones).
