# DXHandleType

Returns a handle type.

```
ENUM_DX_HANDLE_TYPE  DXHandleType(
   int  handle      // handle 
   );

```

Parameters

handle

[in]     Handle.

Return Value

The value from the [ENUM_DX_HANDLE_TYPE](/en/docs/directx/dxhandletype#enum_dx_handle_type) enumeration

ENUM_DX_HANDLE_TYPE

| ID | Value | Description |
| --- | --- | --- |
| DX_HANDLE_INVALID | 0 | Invalid handle |
| DX_HANDLE_CONTEXT | 1 | Graphic context handle |
| DX_HANDLE_SHADER | 2 | Shader handle |
| DX_HANDLE_BUFFER | 3 | Vertex or index buffer handle |
| DX_HANDLE_INPUT | 4 | Handle for shader inputs |
| DX_HANDLE_TEXTURE | 5 | Texture handle |
