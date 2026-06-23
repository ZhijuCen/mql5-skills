# CLGetDeviceInfo

The function receives device property from OpenCL driver.

```
bool  CLGetDeviceInfo(
   int     handle,          // OpenCL device handle
   int     property_id,     // requested property ID 
   uchar&  data[],          // array for receiving data
   uint&   size             // shift in the array elements, default value is 0
   );

```

Parameters

handle

[in]  OpenCL device index or OpenCL handle created by [CLContextCreate()](/en/docs/opencl/clcontextcreate) function.

property_id

[in]  ID of the OpenCL device property that should be received. The values can be of one of the predetermined ones listed in the [table below](/en/docs/opencl/clgetdeviceinfo#openclpropertyids).

data[]

[out]  The array for receiving data on the requested property.

size

[out]  Size of the received data in the array data[].

Return Value

true if successful, otherwise false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

For one-dimensional arrays, the number of the element, from which data reading for OpenCL buffer starts, is calculated considering [AS_SERIES](/en/docs/array/arraygetasseries) flag.

The list of available IDs of OpenCL device properties

Exact description of the property and its functions can be found at [the official OpenCL web site](https://www.khronos.org/opencl/).

| Identifier | Value |
| --- | --- |
| CL_DEVICE_TYPE | 0x1000 |
| CL_DEVICE_VENDOR_ID | 0x1001 |
| CL_DEVICE_MAX_COMPUTE_UNITS | 0x1002 |
| CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS | 0x1003 |
| CL_DEVICE_MAX_WORK_GROUP_SIZE | 0x1004 |
| CL_DEVICE_MAX_WORK_ITEM_SIZES | 0x1005 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_CHAR | 0x1006 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_SHORT | 0x1007 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_INT | 0x1008 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_LONG | 0x1009 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_FLOAT | 0x100A |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_DOUBLE | 0x100B |
| CL_DEVICE_MAX_CLOCK_FREQUENCY | 0x100C |
| CL_DEVICE_ADDRESS_BITS | 0x100D |
| CL_DEVICE_MAX_READ_IMAGE_ARGS | 0x100E |
| CL_DEVICE_MAX_WRITE_IMAGE_ARGS | 0x100F |
| CL_DEVICE_MAX_MEM_ALLOC_SIZE | 0x1010 |
| CL_DEVICE_IMAGE2D_MAX_WIDTH | 0x1011 |
| CL_DEVICE_IMAGE2D_MAX_HEIGHT | 0x1012 |
| CL_DEVICE_IMAGE3D_MAX_WIDTH | 0x1013 |
| CL_DEVICE_IMAGE3D_MAX_HEIGHT | 0x1014 |
| CL_DEVICE_IMAGE3D_MAX_DEPTH | 0x1015 |
| CL_DEVICE_IMAGE_SUPPORT | 0x1016 |
| CL_DEVICE_MAX_PARAMETER_SIZE | 0x1017 |
| CL_DEVICE_MAX_SAMPLERS | 0x1018 |
| CL_DEVICE_MEM_BASE_ADDR_ALIGN | 0x1019 |
| CL_DEVICE_MIN_DATA_TYPE_ALIGN_SIZE | 0x101A |
| CL_DEVICE_SINGLE_FP_CONFIG | 0x101B |
| CL_DEVICE_GLOBAL_MEM_CACHE_TYPE | 0x101C |
| CL_DEVICE_GLOBAL_MEM_CACHELINE_SIZE | 0x101D |
| CL_DEVICE_GLOBAL_MEM_CACHE_SIZE | 0x101E |
| CL_DEVICE_GLOBAL_MEM_SIZE | 0x101F |
| CL_DEVICE_MAX_CONSTANT_BUFFER_SIZE | 0x1020 |
| CL_DEVICE_MAX_CONSTANT_ARGS | 0x1021 |
| CL_DEVICE_LOCAL_MEM_TYPE | 0x1022 |
| CL_DEVICE_LOCAL_MEM_SIZE | 0x1023 |
| CL_DEVICE_ERROR_CORRECTION_SUPPORT | 0x1024 |
| CL_DEVICE_PROFILING_TIMER_RESOLUTION | 0x1025 |
| CL_DEVICE_ENDIAN_LITTLE | 0x1026 |
| CL_DEVICE_AVAILABLE | 0x1027 |
| CL_DEVICE_COMPILER_AVAILABLE | 0x1028 |
| CL_DEVICE_EXECUTION_CAPABILITIES | 0x1029 |
| CL_DEVICE_QUEUE_PROPERTIES | 0x102A |
| CL_DEVICE_NAME | 0x102B |
| CL_DEVICE_VENDOR | 0x102C |
| CL_DRIVER_VERSION | 0x102D |
| CL_DEVICE_PROFILE | 0x102E |
| CL_DEVICE_VERSION | 0x102F |
| CL_DEVICE_EXTENSIONS | 0x1030 |
| CL_DEVICE_PLATFORM | 0x1031 |
| CL_DEVICE_DOUBLE_FP_CONFIG | 0x1032 |
| CL_DEVICE_PREFERRED_VECTOR_WIDTH_HALF | 0x1034 |
| CL_DEVICE_HOST_UNIFIED_MEMORY | 0x1035 |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_CHAR | 0x1036 |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_SHORT | 0x1037 |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_INT | 0x1038 |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_LONG | 0x1039 |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_FLOAT | 0x103A |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_DOUBLE | 0x103B |
| CL_DEVICE_NATIVE_VECTOR_WIDTH_HALF | 0x103C |
| CL_DEVICE_OPENCL_C_VERSION | 0x103D |
| CL_DEVICE_LINKER_AVAILABLE | 0x103E |
| CL_DEVICE_BUILT_IN_KERNELS | 0x103F |
| CL_DEVICE_IMAGE_MAX_BUFFER_SIZE | 0x1040 |
| CL_DEVICE_IMAGE_MAX_ARRAY_SIZE | 0x1041 |
| CL_DEVICE_PARENT_DEVICE | 0x1042 |
| CL_DEVICE_PARTITION_MAX_SUB_DEVICES | 0x1043 |
| CL_DEVICE_PARTITION_PROPERTIES | 0x1044 |
| CL_DEVICE_PARTITION_AFFINITY_DOMAIN | 0x1045 |
| CL_DEVICE_PARTITION_TYPE | 0x1046 |
| CL_DEVICE_REFERENCE_COUNT | 0x1047 |
| CL_DEVICE_PREFERRED_INTEROP_USER_SYNC | 0x1048 |
| CL_DEVICE_PRINTF_BUFFER_SIZE | 0x1049 |
| CL_DEVICE_IMAGE_PITCH_ALIGNMENT | 0x104A |
| CL_DEVICE_IMAGE_BASE_ADDRESS_ALIGNMENT | 0x104B |

Example:

```
void OnStart()
  {
//--- 
   int dCount= CLGetInfoInteger(0,CL_DEVICE_COUNT);
   for(int i = 0; i<dCount; i++)
     {
      int clCtx=CLContextCreate(i);
      if(clCtx == -1)
         Print("ERROR in CLContextCreate");
      string device;
      CLGetInfoString(clCtx,CL_DEVICE_NAME,device);
      Print(i,": ",device);
      uchar data[1024];
      uint size;
      CLGetDeviceInfo(clCtx,CL_DEVICE_VENDOR,data,size);
      Print("size = ",size);
      string str=CharArrayToString(data);
      Print(str);
     }
  }
//--- example of entries in Experts journal
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      2: Advanced Micro Devices, Inc.
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      size = 32
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      Tahiti
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      Intel(R) Corporation
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      size = 21
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      1:        Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      NVIDIA Corporation
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      size = 19
//  2013.07.24 10:50:48     opencl (EURUSD,H1)      0: GeForce GTX 580

```
