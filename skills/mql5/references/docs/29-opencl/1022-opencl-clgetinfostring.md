# CLGetInfoString

Returns string value of a property for OpenCL object or device.

```
bool  CLGetInfoString(
   int  handle,                           // OpenCL object handle or OpenCL device number
   ENUM_OPENCL_PROPERTY_STRING  prop,     // requested property
   string&  value                         // referenced string
   );

```

Parameters

handle

[in]  OpenCL object handle or OpenCL device number. The numbering of OpenCL devices starts with zero.

prop

[in]  Type of requested property from [ENUM_OPENCL_PROPERTY_STRING](/en/docs/opencl/clgetinfostring#enum_opencl_property_string) enumeration, the value of which should be obtained.

value

[out]  String for receiving the property value.

Return Value

true if successful, otherwise false. For information about the error, use the [GetLastError()](/en/docs/check/getlasterror) function.

ENUM_OPENCL_PROPERTY_STRING

| Identifier | Description |
| --- | --- |
| CL_PLATFORM_PROFILE | CL_PLATFORM_PROFILE - OpenCL Profile.  Profile name may be one of the following values: 
 
 FULL_PROFILE - implementation supports OpenCL (functionality is defined as the part of the kernel specification without requiring additional extensions for OpenCL support); 
 EMBEDDED_PROFILE - implementation supports OpenCL as a supplement. Amended profile is defined as a subset for each OpenCL version. |
| CL_PLATFORM_VERSION | OpenCL version |
| CL_PLATFORM_VENDOR | Platform vendor name |
| CL_PLATFORM_EXTENSIONS | List of extensions supported by the platform. Extension names should be supported by all devices related to this platform |
| CL_DEVICE_NAME | Device name |
| CL_DEVICE_VENDOR | Vendor name |
| CL_DRIVER_VERSION | OpenCL driver version in major_number.minor_number format |
| CL_DEVICE_PROFILE | OpenCL device profile. Profile name may be one of the following values: 
 
 FULL_PROFILE - implementation supports OpenCL (functionality is defined as the part of the kernel specification without requiring additional extensions for OpenCL support); 
 EMBEDDED_PROFILE - implementation supports OpenCL as a supplement. Amended profile is defined as a subset for each OpenCL version. |
| CL_DEVICE_VERSION | OpenCL version in "OpenCL<space><major_version.minor_version><space><vendor-specific information>" format |
| CL_DEVICE_EXTENSIONS | List of extensions supported by the device. The list may contain extensions supported by the vendor, as well as one or more approved names: 
     cl_khr_int64_base_atomics 
     cl_khr_int64_extended_atomics 
     cl_khr_fp16 
     cl_khr_gl_sharing 
     cl_khr_gl_event 
     cl_khr_d3d10_sharing 
     cl_khr_dx9_media_sharing 
     cl_khr_d3d11_sharing |
| CL_DEVICE_BUILT_IN_KERNELS | The list of supported kernels separated by ";". |
| CL_DEVICE_OPENCL_C_VERSION | The maximum version supported by the compiler for this device. Version format: 
 "OpenCL<space>C<space><major_version.minor_version><space><vendor-specific information> " |
| CL_ERROR_DESCRIPTION | Text description of an OpenCL error |

Example:

```
void OnStart()
  {
   int cl_ctx;
   string str;
//--- initialize OpenCL context
   if((cl_ctx=CLContextCreate(CL_USE_GPU_ONLY))==INVALID_HANDLE)
     {
      Print("OpenCL not found");
      return;
     }
//--- Display information about the platform
   if(CLGetInfoString(cl_ctx,CL_PLATFORM_NAME,str))
      Print("OpenCL platform name: ",str);
   if(CLGetInfoString(cl_ctx,CL_PLATFORM_VENDOR,str))
      Print("OpenCL platform vendor: ",str);
   if(CLGetInfoString(cl_ctx,CL_PLATFORM_VERSION,str))
      Print("OpenCL platform ver: ",str);
   if(CLGetInfoString(cl_ctx,CL_PLATFORM_PROFILE,str))
      Print("OpenCL platform profile: ",str);
   if(CLGetInfoString(cl_ctx,CL_PLATFORM_EXTENSIONS,str))
      Print("OpenCL platform ext: ",str);
//--- Display information about the device
   if(CLGetInfoString(cl_ctx,CL_DEVICE_NAME,str))
      Print("OpenCL device name: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_PROFILE,str))
      Print("OpenCL device profile: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_BUILT_IN_KERNELS,str))
      Print("OpenCL device kernels: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_EXTENSIONS,str))
      Print("OpenCL device ext: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_VENDOR,str))
      Print("OpenCL device vendor: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_VERSION,str))
      Print("OpenCL device ver: ",str);
   if(CLGetInfoString(cl_ctx,CL_DEVICE_OPENCL_C_VERSION,str))
      Print("OpenCL open c ver: ",str);
//--- Display general information about the OpenCL device
   Print("OpenCL type: ",EnumToString((ENUM_CL_DEVICE_TYPE)CLGetInfoInteger(cl_ctx,CL_DEVICE_TYPE)));
   Print("OpenCL vendor ID: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_VENDOR_ID));
   Print("OpenCL units: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_MAX_COMPUTE_UNITS));
   Print("OpenCL freq: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_MAX_CLOCK_FREQUENCY));
   Print("OpenCL global mem: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_GLOBAL_MEM_SIZE));
   Print("OpenCL local mem: ",CLGetInfoInteger(cl_ctx,CL_DEVICE_LOCAL_MEM_SIZE));
//--- free OpenCL context
   CLContextFree(cl_ctx); 
  }

```
