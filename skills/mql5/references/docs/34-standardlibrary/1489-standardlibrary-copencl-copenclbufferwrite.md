# BufferWrite

Writes an array of values into buffer at the specified index.

```
template<typename T>
bool  BufferWrite(
   const int   buffer_index,          // buffer index
   T           &data[],               // array of values
   const uint  cl_buffer_offset,      // offset in the OpenCL buffer, in bytes
   const uint  data_array_offset,     // shift in the array elements
   const uint  data_array_count       // number of values from the array to write
   );

```

Parameters

buffer_index

[in]  Index buffer.

&data[]

[in]  An array of values to be written into the OpenCL buffer.

cl_buffer_offset

[in]  Offset in the OpenCL buffer in bytes, from which to start writing values.

data_array_offset

[in]  Index of the first element of the array, starting from which the array values are written to the OpenCL buffer.

data_array_count

[in] The number of values to be written.

Return Value

In case of successful execution, returns true, otherwise - false.
