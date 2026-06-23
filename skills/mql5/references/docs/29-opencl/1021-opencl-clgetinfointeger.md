# CLGetInfoInteger

Returns the value of an integer property for an OpenCL object or device.

```
long  CLGetInfoInteger(
   int  handle,                           // The handle of the OpenCL object or the number of the OpenCL device
   ENUM_OPENCL_PROPERTY_INTEGER  prop     // Requested property
   );

```

Parameters

handle

[in]  A handle to the OpenCL object or number of the OpenCL device. Numbering of OpenCL devices starts with zero.

prop

[in]  The type of a requested property from the [ENUM_OPENCL_PROPERTY_INTEGER](/en/docs/opencl/clgetinfointeger#enum_opencl_property_integer) enumeration, the value of which you want to obtain.

Return Value

The value of the property if successful or -1 in case of an error. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

ENUM_OPENCL_PROPERTY_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| CL_DEVICE_COUNT | The number of devices with OpenCL support. This property does not require specification of the first parameter, i.e. you can pass a zero value for the  handle  parameter. | int |
| CL_DEVICE_TYPE | Type of device | ENUM_CL_DEVICE_TYPE |
| CL_DEVICE_VENDOR_ID | Unique vendor identifier | uint |
| CL_DEVICE_MAX_COMPUTE_UNITS | Number of parallel calculated tasks in OpenCL device. One working group solves one computational task. The lowest value is 1 | uint |
| CL_DEVICE_MAX_CLOCK_FREQUENCY | Highest set frequency of the device in MHz. | uint |
| CL_DEVICE_GLOBAL_MEM_SIZE | Size of the global memory of the device in bytes | ulong |
| CL_DEVICE_LOCAL_MEM_SIZE | Size of the processed data (scene) local memory in bytes | uint |
| CL_BUFFER_SIZE | Actual size of the OpenCL buffer in bytes | ulong |
| CL_DEVICE_MAX_WORK_GROUP_SIZE | The total number of the local working groups available for an OpenCL device. | ulong |
| CL_KERNEL_WORK_GROUP_SIZE | The total number of the local working groups available for an OpenCL program. | ulong |
| CL_KERNEL_LOCAL_MEM_SIZE | Size of the local memory (in bytes) used by an OpenCL program for solving all parallel tasks in a group. Use CL_DEVICE_LOCAL_MEM_SIZE to receive the maximum available value | ulong |
| CL_KERNEL_PRIVATE_MEM_SIZE | The minimum size of the private memory (in bytes) used by each task in the OpenCL program kernel. | ulong |
| CL_LAST_ERROR | The value of the last OpenCL error | int |

The ENUM_CL_DEVICE_TYPE enumeration contains possible types of devices supporting OpenCL. You can receive the type of device by its number or the handle of the OpenCL object by calling CLGetInfoInteger(handle_or_deviceN, CL_DEVICE_TYPE).

ENUM_CL_DEVICE_TYPE

| Identifier | Description |
| --- | --- |
| CL_DEVICE_ACCELERATOR | Dedicated OpenCL accelerators (for example, the IBM CELL Blade). These devices communicate with the host processor using a peripheral interconnect such as PCIe. |
| CL_DEVICE_CPU | An OpenCL device that is the host processor. The host processor runs the OpenCL implementations and is a single or multi-core CPU. |
| CL_DEVICE_GPU | An OpenCL device that is a GPU. |
| CL_DEVICE_DEFAULT | The default OpenCL device in the system. The default device cannot be a CL_DEVICE_TYPE_CUSTOM device. |
| CL_DEVICE_CUSTOM | Dedicated accelerators that do not support programs written in OpenCL C. |

Example:

```
void OnStart()
  {
   int cl_ctx;
//--- initialize OpenCL context
   if((cl_ctx=CLContextCreate(CL_USE_GPU_ONLY))==INVALID_HANDLE)
     {
      Print("OpenCL not found");
      return;
     }
//--- Display general information about OpenCL device
   Print("OpenCL type: ",EnumToString((ENUM_CL_DEVICE_TYPE)CLGetInfoInteger(cl_ctx,CL_DEVICE_TYPE)));
   Print("OpenCL vendor ID: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_VENDOR_ID));
   Print("OpenCL units: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_MAX_COMPUTE_UNITS));
   Print("OpenCL freq: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_MAX_CLOCK_FREQUENCY)," MHz");
   Print("OpenCL global mem: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_GLOBAL_MEM_SIZE)," bytes");
   Print("OpenCL local mem: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_LOCAL_MEM_SIZE)," bytes");
//--- free OpenCL context
   CLContextFree(cl_ctx);
  }

```
