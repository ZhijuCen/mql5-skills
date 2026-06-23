# DXBufferCreate

Creates a buffer of a specified type based on a data array.

```
int  DXBufferCreate(
   int                  context,               // graphic context handle
   ENUM_DX_BUFFER_TYPE  buffer_type,           // type of a created buffer
   const void&          data[],                // buffer data
   uint                 start=0,               // initial index
   uint                 count=WHOLE_ARRAY      // number of elements
   );

```

Parameters

context

[in]  Handle for a graphic context created in [DXContextCreate()](/en/docs/directx/dxcontextcreate).

buffer_type

[in]  Buffer type from the ENUM_DX_BUFFER_TYPE enumeration.

data[]

[in]  Data for creating a buffer.

start=0

[in]  Index of the first element of the array, starting from which the array values are used to create a buffer. By default, the data is taken from the beginning of the array.

count=WHOLE_ARRAY

[in]  Number of values.  By default, the entire array is used (count=[WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants)).

Return Value

The handle for a created buffer or INVALID_HANDLE in case of an error. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

For the index buffer, the data[] array should be of 'uint' type, while the vertex buffer receives the array of structures describing vertices.

A created handle that is no longer in use should be explicitly released by the [DXRelease()](/en/docs/directx/dxrelease) function.

ENUM_DX_BUFFER_TYPE

| ID | Value | Description |
| --- | --- | --- |
| DX_BUFFER_VERTEX | 1 | Vertex buffer |
| DX_BUFFER_INDEX | 2 | Index buffer |
