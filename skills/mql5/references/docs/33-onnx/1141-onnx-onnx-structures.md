# Data structures

The following data structures are used for operations with ONNX models:

## OnnxTypeInfo  #

The structure describes the type of an [input](/en/docs/onnx/onnxgetinputtypeinfo) or [output parameter](/en/docs/onnx/onnxgetoutputtypeinfo) of an ONNX model

```
struct OnnxTypeInfo
 {
  ENUM_ONNX_TYPE        type;          // parameter type
  OnnxTensorTypeInfo    tensor;        // tensor description
  OnnxMapTypeInfo       map;           // map description
  OnnxSequenceTypeInfo  sequence;      // sequence description
 };

```

Only tensor (ONNX_TYPE_TENSOR) can be used as an input. In this case, only the OnnxTypeInfo::tensor field is filled with values, while other fields (map and sequence) are not defined.

Only one of the three OnnxTypeInfo types (ONNX_TYPE_TENSOR, ONNX_TYPE_MAP or ONNX_TYPE_SEQUENCE) can be used as an input. The corresponding substructure (OnnxTypeInfo::tensor, OnnxTypeInfo::map or OnnxTypeInfo::sequence) is filled depending on the type.

OnnxTensorTypeInfo

The structure describes the tensor in the [input](/en/docs/onnx/onnxgetinputtypeinfo) or [output parameter](/en/docs/onnx/onnxgetoutputtypeinfo) of an ONNX model

```
struct OnnxTensorTypeInfo
 {
  const ENUM_ONNX_DATA_TYPE   data_type;      // data type in the tensor
  const long                  dimensions[];   // number of elements in the tensor
 };

```

## OnnxMapTypeInfo  #

The structure describes the map obtained in the [output parameter](/en/docs/onnx/onnxgetoutputtypeinfo) of an ONNX model

```
struct OnnxMapTypeInfo
 {
  const ENUM_ONNX_DATA_TYPE   key_type;       // key type
  const OnnxTypeInfo &        value_type;     // value type
 };

```

## OnnxSequenceTypeInfo  #

The structure describes the sequence obtained in the [output parameter](/en/docs/onnx/onnxgetoutputtypeinfo) of an ONNX model

```
struct OnnxSequenceTypeInfo
 {
  const OnnxTypeInfo&        value_type;      // data type in the sequence
 };

```

### 

### 

### ENUM_ONNX_TYPE  #

The ENUM_ONNX_TYPE enumeration describes the type of a model parameter

| ID | Description |
| --- | --- |
| ONNX_TYPE_UNKNOWN | Unknown |
| ONNX_TYPE_TENSOR | Tensor |
| ONNX_TYPE_SEQUENCE | Sequence |
| ONNX_TYPE_MAP | Map |
| ONNX_TYPE_OPAQUE | Abstract (opaque) |
| ONNX_TYPE_SPARSETENSOR | Sparse tensor |

### ENUM_ONNX_DATA_TYPE  #

The ENUM_ONNX_DATA_TYPE enumeration describes the type of data used

| ID | Description |
| --- | --- |
| ONNX_DATA_TYPE_UNDEFINED | Undefined |
| ONNX_DATA_TYPE_FLOAT | float |
| ONNX_DATA_TYPE_INT8 | 8-bit int |
| ONNX_DATA_TYPE_UINT16 | 16-bit uint |
| ONNX_DATA_TYPE_INT16 | 16-bit int |
| ONNX_DATA_TYPE_INT32 | 32-bit int |
| ONNX_DATA_TYPE_INT64 | 64-bit int |
| ONNX_DATA_TYPE_STRING | string |
| ONNX_DATA_TYPE_BOOL | bool |
| ONNX_DATA_TYPE_FLOAT16 | 16-bit float |
| ONNX_DATA_TYPE_DOUBLE | double |
| ONNX_DATA_TYPE_UINT32 | 32-bit uint |
| ONNX_DATA_TYPE_UINT64 | 64-bit uint |
| ONNX_DATA_TYPE_COMPLEX64 | 64-bit complex number |
| ONNX_DATA_TYPE_COMPLEX128 | 128-bit complex number |
| ONNX_DATA_TYPE_BFLOAT16 | 16-bit bfloat (Brain Floating Point) |

### ENUM_ONNX_FLAGS  #

The ENUM_ONNX_FLAGS enumeration describes the model run mode

| ID | Description |
| --- | --- |
| ONNX_LOGLEVEL_VERBOSE | Log all messages |
| ONNX_LOGLEVEL_INFO | Log info messages, warnings, and errors (this flag replaces ONNX_DEBUG_LOGS) |
| ONNX_LOGLEVEL_WARNING | Log warnings and errors (default) |
| ONNX_LOGLEVEL_ERROR | Log errors only |
| ONNX_NO_CONVERSION | Disable auto conversion, use user data as is |
| ONNX_COMMON_FOLDER | Load a model file from the Common\Files folder; the value is equal to the  FILE_COMMON  flag |
| ONNX_USE_CPU_ONLY | Execute the ONNX model using CPU only |
| ONNX_GPU_DEVICE_0 | CUDA device with index 0 (default) |
| ONNX_GPU_DEVICE_1 | CUDA device with index 1 * |
| ONNX_GPU_DEVICE_2 | CUDA device with index 2 * |
| ONNX_GPU_DEVICE_3 | CUDA device with index 3  * |
| ONNX_GPU_DEVICE_4 | CUDA device with index 4  * |
| ONNX_GPU_DEVICE_5 | CUDA device with index 5  * |
| ONNX_GPU_DEVICE_6 | CUDA device with index 6  * |
| ONNX_GPU_DEVICE_7 | CUDA device with index 7  * |
| ONNX_ENABLE_PROFILING | Enable ONNX model profiling |

* Flags of the form ONNX_GPU_DEVICE_N should be used on systems with two or more CUDA-capable GPUs. If multiple GPU selection flags are specified, the device with the lowest index will be used.

If a non-existent device index is specified, the GPU will be selected automatically.

### ONNX Profiling

The ONNX_ENABLE_PROFILING flag enables profiling of ONNX model execution. When this flag is set, a profiling report file <module_name>_date_time.json> will be created in the following directory<data_folder>/MQL5/Files/OnnxProfileReports>:

Here <module_name> is the name of the MQL program EX5 file.

The file contains a detailed ONNX model execution profiling report in JSON format, including:

- session loading and initialization time;
- execution time of individual graph nodes (Conv, Relu, MaxPool, Gemm, etc.);
- the execution provider used (for example, CUDAExecutionProvider);
- input and output tensor size information;
- thread scheduling statistics.

An example of profiling report data is shown below:

```
{"cat" : "Session","pid" :34368,"tid" :39520,"dur" :698,"ts" :11,"ph" : "X","name" :"model_loading_array","args" : {}},
{"cat" : "Session","pid" :34368,"tid" :39520,"dur" :15496,"ts" :869,"ph" : "X","name" :"session_initialization","args" : {}},
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :66055,"ts" :16800,"ph" : "X","name" :"Convolution28_kernel_time","args" : {"parameter_size" : "832","provider" : "CUDAExecutionProvider","op_name" : "Conv","input_type_shape" : [{"float":[1,1,28,28]},{"float
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :775,"ts" :82867,"ph" : "X","name" :"ReLU32_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "Relu","input_type_shape" : [{"float":[1,8,28,28]}],"node_index" : "3
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :8818,"ts" :83647,"ph" : "X","name" :"Pooling66_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "MaxPool","input_type_shape" : [{"float":[1,8,28,28]}],"node_inde
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :1120,"ts" :92476,"ph" : "X","name" :"Convolution110_kernel_time","args" : {"parameter_size" : "12864","provider" : "CUDAExecutionProvider","op_name" : "Conv","input_type_shape" : [{"float":[1,8,14,14]},{"flo
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :23,"ts" :93603,"ph" : "X","name" :"ReLU114_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "Relu","input_type_shape" : [{"float":[1,16,14,14]}],"node_index" : "
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :21,"ts" :93629,"ph" : "X","name" :"Pooling160_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "MaxPool","input_type_shape" : [{"float":[1,16,14,14]}],"node_inde
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :16,"ts" :93654,"ph" : "X","name" :"Times212_reshape0_kernel_time","args" : {"parameter_size" : "16","provider" : "CUDAExecutionProvider","op_name" : "Reshape","input_type_shape" : [{"float":[1,16,4,4]},{"int
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :32264,"ts" :93673,"ph" : "X","name" :"Times212/MatMulAddFusion_kernel_time","args" : {"parameter_size" : "10280","provider" : "CUDAExecutionProvider","op_name" : "Gemm","input_type_shape" : [{"float":[1,256]
{"cat" : "Session","pid" :34368,"tid" :39520,"dur" :109165,"ts" :16794,"ph" : "X","name" :"SequentialExecutor::Execute","args" : {}},
{"cat" : "Session","pid" :34368,"tid" :39520,"dur" :109600,"ts" :16433,"ph" : "X","name" :"model_run","args" : {}},
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :87,"ts" :126313,"ph" : "X","name" :"Convolution28_kernel_time","args" : {"parameter_size" : "832","provider" : "CUDAExecutionProvider","op_name" : "Conv","input_type_shape" : [{"float":[1,1,28,28]},{"float":
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :23,"ts" :126403,"ph" : "X","name" :"ReLU32_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "Relu","input_type_shape" : [{"float":[1,8,28,28]}],"node_index" : "3
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :31,"ts" :126431,"ph" : "X","name" :"Pooling66_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "MaxPool","input_type_shape" : [{"float":[1,8,28,28]}],"node_index
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :35,"ts" :126466,"ph" : "X","name" :"Convolution110_kernel_time","args" : {"parameter_size" : "12864","provider" : "CUDAExecutionProvider","op_name" : "Conv","input_type_shape" : [{"float":[1,8,14,14]},{"floa
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :15,"ts" :126505,"ph" : "X","name" :"ReLU114_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "Relu","input_type_shape" : [{"float":[1,16,14,14]}],"node_index" : 
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :22,"ts" :126523,"ph" : "X","name" :"Pooling160_kernel_time","args" : {"parameter_size" : "0","provider" : "CUDAExecutionProvider","op_name" : "MaxPool","input_type_shape" : [{"float":[1,16,14,14]}],"node_ind
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :12,"ts" :126548,"ph" : "X","name" :"Times212_reshape0_kernel_time","args" : {"parameter_size" : "16","provider" : "CUDAExecutionProvider","op_name" : "Reshape","input_type_shape" : [{"float":[1,16,4,4]},{"in
{"cat" : "Node","pid" :34368,"tid" :39520,"dur" :40,"ts" :126562,"ph" : "X","name" :"Times212/MatMulAddFusion_kernel_time","args" : {"parameter_size" : "10280","provider" : "CUDAExecutionProvider","op_name" : "Gemm","input_type_shape" : [{"float":[1,256]},

```

Additional information about ONNX profiling:: [https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html](https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html)

### Array conversion when working with ONNX models

Machine learning tasks do not always require greater computational accuracy. To speed up calculations, some models use lower-precision data types such as Float16 and even Float8. To allow users to input the relevant data into models, MQL5 provides four special functions which convert standard MQL5 types into special FP16 and FP8 types.

| Function | Action |
| --- | --- |
| ArrayToFP16 | Copies an array of type float or double into an array of type  ushort  with the given format |
| ArrayToFP8 | Copies an array of type float or double into an array of type  uchar  with the given format |
| ArrayFromFP16 | Copies an array of type  ushort  into an array of float or double type with the given format |
| ArrayFromFP8 | Copies an array of type  uchar  into an array of float or double type with the given format |

These array conversion functions use special formats specified in the below enumerations.

### ENUM_FLOAT16_FORMAT  #

The ENUM_FLOAT16_FORMAT enumeration describes two FP16 type formats.

| ID | Description |
| --- | --- |
| FLOAT_FP16 | Standard 16-bit format, also known as  half |
| FLOAT_BFP16 | Special  brain float point  format |

Each of these formats has its advantages and limitations. FLOAT16 provides higher accuracy but requires more storage and computation resources. BFLOAT16, on the other hand, provides higher performance and efficiency in data processing, but may be less accurate.

### ENUM_FLOAT8_FORMAT  #

The ENUM_FLOAT8_FORMAT enumeration describes four FP8 type formats.

FP8 (8-bit floating point) is one of the data types used to represent floating point numbers. In FP8, each number is represented by 8 data bits, typically divided into three components: sign, exponent and mantissa. This format offers a balance between accuracy and storage efficiency, making it attractive for applications that require memory and computational efficiency.

| ID | Description |
| --- | --- |
| FLOAT_FP8_E4M3FN | 8-bit floating point number, 4 bits for the exponent and 3 bits for the mantissa. Typically used as coefficients. |
| FLOAT_FP8_E4M3FNUZ | 8-bit floating point number, 4 bits for the exponent and 3 bits for the mantissa. Supports NaN, does not support negative zero and Inf. Typically used as coefficients. |
| FLOAT_FP8_E5M2FN | 8-bit floating point number, 5 bits for the exponent and 2 bits for the mantissa. Supports NaN and Inf. Typically used for gradients. |
| FLOAT_FP8_E5M2FNUZ | 8-bit floating point number, 5 bits for the exponent and 2 bits for the mantissa. Supports NaN, does not support negative zero and Inf. Also used for gradients. |

One of the key advantages of FP8 is its efficiency in processing large datasets. By employing compact number representation, FP8 reduces memory requirements and accelerates calculations. This is especially important in machine learning and artificial intelligence applications which often process large datasets.
