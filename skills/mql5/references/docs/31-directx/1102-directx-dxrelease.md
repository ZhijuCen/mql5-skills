# DXRelease

Releases a handle.

```
bool  DXRelease(
   int  handle      // handle 
   );

```

Parameters

context

[in]  Released handle.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

All created handles that are no longer in use should be explicitly released by the DXRelease() function.
