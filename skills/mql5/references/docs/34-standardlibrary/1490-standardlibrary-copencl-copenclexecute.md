# Execute

Executes the OpenCL program at the specified index.

```
bool  Execute(
   const int   kernel_index,           // index of the kernel
   const int   work_dim,               // dimension of the tasks space
   const uint  &work_offset[],         // initial offset in the tasks space
   const uint  &work_size[]            // total number of tasks
   );

```

Executes the OpenCL kernel with the specified index and number of tasks in the local group.

```
bool  Execute(
   const int   kernel_index,           // index of the kernel
   const int   work_dim,               // dimension of the tasks space
   const uint  &work_offset[],         // initial offset in the tasks space
   const uint  &work_size[],           // total number of tasks
   const uint  &local_work_size[]      // number of tasks in the local group
   );

```

Parameters

kernel_index

[in]  Index of the kernel object.

work_dim

[in]  Dimension of the tasks space.

&work_offset[]

[in][out]  Initial offset in the tasks space. Passed by reference.

&work_size[]

[in][out]  The size of the tasks subset. Passed by reference.

&local_work_size[]

[in][out]  The size of the local tasks subset in the group. Passed by reference.

Return Value

In case of successful execution, returns true, otherwise - false.
