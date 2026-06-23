# SetArgumentLocalMemory

Sets a parameter in local memory for the OpenCL function at the specified index.

```
bool  SetArgumentLocalMemory(
   const int  kernel_index,          // index of the kernel
   const int  arg_index,             // index of the function argument
   const int  local_memory_size      // size of the local memory
   );

```

Parameters

kernel_index

[in]  Index of the kernel object.

arg_index

[in]  Index of the function argument.

local_memory_size

[in]  Size of the local memory.

Return Value

In case of successful execution, returns true, otherwise - false.
