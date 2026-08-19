# DXBufferSet

Sets a buffer for the current rendering.

```
bool  DXBufferSet(
   int   context,               // graphic context handle
   int   buffer,                // vertex or index buffer handle
   uint  start=0,               // initial index
   uint  count=WHOLE_ARRAY      // number of elements 
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

buffer

[in]  Handle of the vertex or index buffer created in [DXBufferCreate()](/en/docs/directx/dxbuffercreate).

start=0

[in]  Index of the buffer first element. The data from the beginning of the buffer is used by default.

count=WHOLE_ARRAY

[in]  Number of values to be used. The default is all buffer values.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The DXBufferSet() function should be called to set vertex and index buffers for rendering using [DXDraw()](/en/docs/directx/dxdraw).
