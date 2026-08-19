# DXInputCreate

Creates shader inputs.

```
int  DXInputCreate(
   int   context,        // graphic context handle
   uint  input_size      // size of inputs in bytes 
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

input_size

[in]  Size of the parameter structure in bytes.

Return Value

The handle for shader inputs or INVALID_HANDLE in case of an error. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

A created handle that is no longer in use should be explicitly released by the [DXRelease()](/en/docs/directx/dxrelease) function.
