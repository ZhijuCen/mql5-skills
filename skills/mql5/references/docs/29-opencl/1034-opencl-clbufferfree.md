# CLBufferFree

Deletes an OpenCL buffer.

```
void  CLBufferFree(
   int   buffer     // Handle to an OpenCL buffer
   );

```

Parameters

buffer

[in]  A handle to an OpenCL buffer.

Return Value

None. In the case of an internal error the value of [_LastError](/en/docs/predefined/_lasterror) changes. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.
