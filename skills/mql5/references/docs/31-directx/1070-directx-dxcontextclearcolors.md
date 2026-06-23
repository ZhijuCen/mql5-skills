# DXContextClearColors

Sets a specified color to all pixels for the rendering buffer.

```
bool  DXContextClearColors(
   int              context,      // graphic context handle
   const DXVector&  color         // color
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

color

[in]  Rendering color.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The DXContextClearColors() function can be used for clearing the color buffer before rendering the next frame.
