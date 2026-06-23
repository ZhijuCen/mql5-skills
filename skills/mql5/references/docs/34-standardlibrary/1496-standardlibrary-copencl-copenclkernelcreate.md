# KernelCreate

Creates an entry point into the OpenCL program at the specified index.

```
bool  KernelCreate(
   const int     kernel_index,     // index of the kernel
   const string  kernel_name       // name of the kernel
   );

```

Parameters

kernel_index

[in]  Index of the kernel object.

kernel_name

[in]  Name of the kernel object.

Return Value

In case of successful execution, returns true, otherwise - false.
