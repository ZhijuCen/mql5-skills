# BufferRead

Reads an OpenCL buffer at the specified index into an array.

```
template<typename T>
bool  BufferRead(
   const int   buffer_index,          // buffer index
   T           &data[],               // array of values
   const uint  cl_buffer_offset,      // offset in the OpenCL buffer, in bytes
   const uint  data_array_offset,     // shift in the array elements
   const uint  data_array_count       // number of values from the buffer to read
   );

```

Parameters

buffer_index

[in]  Index buffer.

&data[]

[in]  Array to obtain the values of the OpenCL buffer.

cl_buffer_offset

[in]  Offset in the OpenCL buffer in bytes, from which to start reading values.

data_array_offset

[in]  Index of the first element of the array to write values of the OpenCL buffer.

data_array_count

[in]  The number of values to be read.

Return Value

In case of successful execution, returns true, otherwise - false.
