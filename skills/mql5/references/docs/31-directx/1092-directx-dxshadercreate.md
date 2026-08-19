# DXShaderCreate

Creates a shader of a specified type.

```
int  DXShaderCreate(
   int                  context,           // graphic context handle   
   ENUM_DX_SHADER_TYPE  shader_type,       // shader type 
   const string         source,            // shader source code
   const string         entry_point,       // entry point
   string&              compile_error      // string for receiving compiler messages
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

shader_type

[out]  The value from the [ENUM_DX_SHADER_TYPE](/en/docs/directx/dxshadercreate#enum_dx_shader_type) enumeration.

source

[in]  Shader source code in [HLSL 5](https://en.wikipedia.org/wiki/High-Level_Shading_Language).

entry_point

[in]  Entry point – function name in a source code.

compile_error

[in]  String for receiving compilation errors.

Return Value

Handle for shader or INVALID_HANDLE in case of an error. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

A created handle that is no longer in use should be explicitly released by the [DXRelease()](/en/docs/directx/dxrelease) function.

ENUM_DX_SHADER_TYPE

| ID | Value | Description |
| --- | --- | --- |
| DX_SHADER_VERTEX | 0 | Vertex shader |
| DX_SHADER_GEOMETRY | 1 | Geometry shader |
| DX_SHADER_PIXEL | 2 | Pixel shader |
