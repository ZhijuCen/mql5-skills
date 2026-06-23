# DXDrawIndexed

Renders graphic primitives described by the index buffer from [DXBufferSet()](/en/docs/directx/dxbufferset).

```
bool  DXDrawIndexed(
   int   context,               // graphic context handle 
   uint  start=0,               // first primitive index
   uint  count=WHOLE_ARRAY      // number of primitives
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

start=0

[in]  Index of the first primitive for rendering.

count=WHOLE_ARRAY

[in]  Number of primitives for rendering.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The type of primitives described by the index buffer is set using [DXPrimiveTopologySet()](/en/docs/directx/dxprimivetopologyset).

The vertex buffer in [DXBufferSet()](/en/docs/directx/dxbufferset) should be preliminarily set to render primitives.

Also, shaders should be preliminarily set using [DXShaderSet()](/en/docs/directx/dxshaderset).
