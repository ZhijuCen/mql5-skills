# DXContextCreate

Creates a graphic context for rendering frames of a specified size.

```
int  DXContextCreate(
   uint  width,      // width in pixels
   uint  height      // height in pixels
   );

```

Parameters

width

[in]  Frame width in pixels.

height

[in]  Frame height in pixels.

Return Value

A handle for a created context or INVALID_HANDLE in case of an error. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

All graphical objects created using the [DXBufferCreate](/en/docs/directx/dxbuffercreate), [DXInputCreate](/en/docs/directx/dxinputcreate), [DXShaderCreate](/en/docs/directx/dxshadercreate) and [DXTextureCreate](/en/docs/directx/dxtexturecreate) functions can be used only in a graphic context they were created in.

A frame size can subsequently be changed to [DXContextSetSize()](/en/docs/directx/dxcontextsetsize).

A created handle that is no longer in use should be explicitly released by the [DXRelease()](/en/docs/directx/dxrelease) function.
