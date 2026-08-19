# SetArgument

Sets a parameter for the OpenCL function at the specified index.

```
template<typename T>
bool  SetArgument(
   const int  kernel_index,     // index of the kernel
   const int  arg_index,        // index of the function argument
   T          value             // source code
   );

```

Parameters

kernel_index

[in]  Index of the kernel object.

arg_index

[in]  Index of the function argument.

value

[in]  The value of the function argument.

Return Value

In case of successful execution, returns true, otherwise - false.
