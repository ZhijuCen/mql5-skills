# DXShaderSetLayout

Sets vertex layout for the vertex shader.

```
bool  DXShaderSetLayout(
   int                    shader,       // shader handle
   const DXVertexLayout&  layout[]      // 
   );

```

Parameters

shader

[in]  Handle of a vertex shader created in [DXShaderCreate()](/en/docs/directx/dxshadercreate).

layout[]

[in]  Array of vertex fields description. The description is set by the DXVertexLayout structure:

```
struct DXVertexLayout
  {
   string         semantic_name;       // The HLSL semantic associated with this element in a shader input-signature.
   uint           semantic_index;      // The semantic index for the element. A semantic index modifies a semantic, with an integer index number. A semantic index is only needed in a case where there is more than one element with the same semantic
   ENUM_DX_FORMAT format;              // The data type of the element data.
  };

```

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The layout should match the type of vertices in a specified vertex buffer. It should also match the input type of vertices used at the entry point in the vertex shader code.

The vertex buffer for a shader is set in [DXBufferSet()](/en/docs/directx/dxbufferset).

The DXVertexLayout structure is a version of the [D3D11_INPUT_ELEMENT_DESC](https://docs.microsoft.com/en-us/windows/win32/api/d3d11/ns-d3d11-d3d11_input_element_desc) MSDN structure.
