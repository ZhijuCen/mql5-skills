# DXDraw

Renders the vertices of the vertex buffer set in [DXBufferSet()](/en/docs/directx/dxbufferset).

```
bool  DXDraw(
   int   context,               // graphic context handle 
   uint  start=0,               // first vertex index
   uint  count=WHOLE_ARRAY      // number of vertices
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

start=0

[in]  Index of the first vertex for rendering.

count=WHOLE_ARRAY

[in]  Number of vertices to render.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

Shaders should be preliminarily set using [DXShaderSet()](/en/docs/directx/dxshaderset) for rendering vertices.
