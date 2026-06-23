# DXContextGetSize

Gets a frame size of a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

```
bool  DXContextGetSize(
   int    context,      // graphic context handle   
   uint&  width,        // width in pixels 
   uint&  height        // height in pixels 
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

width

[out]  Frame width in pixels.

height

[out]  Frame height in pixels.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.
