# CLExecute

The function runs an OpenCL program. There are 3 versions of the function:

1. Launching kernel functions using one kernel

```
bool  CLExecute(
   int          kernel                    // Handle to the kernel of an OpenCL program
   );

```

2. Launching several kernel copies (OpenCL function) with task space description

```
bool  CLExecute(
   int          kernel,                   // Handle to the kernel of an OpenCL program
   uint         work_dim,                 // Dimension of the tasks space
   const uint&  global_work_offset[],     // Initial offset in the tasks space
   const uint&  global_work_size[]        // Total number of tasks
   );

```

3. Launching several kernel copies (OpenCL function) with task space description and specification of the size of the group's local task subset

```
bool  CLExecute(
   int          kernel,                   // Handle to the kernel of an OpenCL program
   uint         work_dim,                 // Dimension of the tasks space
   const uint&  global_work_offset[],     // Initial offset in the tasks space
   const uint&  global_work_size[],       // Total number of tasks
   const uint&  local_work_size[]         // Number of tasks in the local group
   );

```

Parameters

kernel

[in]  Handle to the OpenCL kernel.

work_dim

[in]  Dimension of the tasks space.

global_work_offset[]

[in]  Initial offset in the tasks space.

global_work_size[]

[in]  The size of a subset of tasks.

local_work_size[]

[in]  The size of the group's local task subset.

Return Value

Returns true if successful, otherwise returns false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Consider the use of the parameters in the following example:

- work_dim specifies the size of work_items[] array that describes the tasks. If work_dim=3, three-dimensional array work_items[N1, N2, N3] is used.
- global_work_size[] contains the values that set the work_items[] array size. If work_dim=3, global_work_size[3] array can be {40, 100, 320}. Then we have work_items[40, 100, 320]. So, the total number of tasks is 40 x 100 x 320 = 1 280 000.
- local_work_size[] sets the subset of the tasks that will be executed by the specified kernel of OpenCL program. Its size is equal to work_items[] size and allows to split the common task subset into smaller subsets without loss of remainder in division. In fact, the size of local_work_size[] array should be selected so that the work_items[] global task set will be split into smaller subsets. In this example local_work_size[3]={10, 10, 10} will be OK, as work_items[40, 100, 320] can be gathered from local_items[10, 10, 10] array without division remainder.
