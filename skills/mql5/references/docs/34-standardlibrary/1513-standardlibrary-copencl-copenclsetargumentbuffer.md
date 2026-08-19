# SetArgumentBuffer

Sets an OpenCL buffer as a parameter of the OpenCL function at the specified index.

```
bool  SetArgumentBuffer(
   const int  kernel_index,     // index of the kernel
   const int  arg_index,        // index of the function argument
   const int  buffer_index      // buffer index
   );

```

Parameters

kernel_index

[in]  Index of the kernel object.

arg_index

[in]  Index of the function argument.

buffer_index

[in]  Index buffer.

Return Value

In case of successful execution, returns true, otherwise - false.
