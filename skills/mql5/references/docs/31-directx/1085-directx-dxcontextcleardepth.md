# DXContextClearDepth

Clears the depth buffer.

```
bool  DXContextClearDepth(
   int  context      // graphic context handle 
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

The DXContextClearDepth() function can be used for clearing the depth buffer before rendering the next frame.
