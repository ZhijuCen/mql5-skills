# Autoconvert input and output values when running ONNX models

The current ONNX version in MQL5 supports only tensors for [input/output](https://onnxruntime.ai/docs/api/python/api_summary.html#data-inputs-and-outputs) values. Tensors are data arrays with the elements of the following data types:

| ONNX type | Corresponds to MQL5 type |
| --- | --- |
| ONNX_DATA_TYPE_BOOL | bool |
| ONNX_DATA_TYPE_FLOAT | float |
| ONNX_DATA_TYPE_UINT8 | uchar |
| ONNX_DATA_TYPE_INT8 | char |
| ONNX_DATA_TYPE_UINT16 | ushort |
| ONNX_DATA_TYPE_INT16 | short |
| ONNX_DATA_TYPE_INT32 | int |
| ONNX_DATA_TYPE_INT64 | long |
| ONNX_DATA_TYPE_FLOAT16 | — |
| ONNX_DATA_TYPE_DOUBLE | double |
| ONNX_DATA_TYPE_UINT32 | uint |
| ONNX_DATA_TYPE_UINT64 | ulong |
| ONNX_DATA_TYPE_COMPLEX64 | — |
| ONNX_DATA_TYPE_COMPLEX128 | complex |
| ONNX_DATA_TYPE_BFLOAT16 | — |
| ONNX_DATA_TYPE_STRING | — |

Only arrays, [vectors and matrices](/en/docs/basis/types/matrix_vector) (we will refer to them as the Data) can be fed into ONNX models as input/output values.

If the parameter types does not match the ONNX model's parameter type, and the [OnnxRun](/en/docs/onnx/onnxrun) is called without the [ONNX_NO_CONVERSION](/en/docs/onnx/onnx_structures#enum_onnx_flags) flag specified, automatic data conversion will be applied. Autoconversion implies that before running an ONNX model, user Data will be copied into ONNX tensors with the relevant conversion.

When an ONNX model is run without the autoconversion, the model will be calculated using the Data without any additional copying.

IMPORTANT! Autoconversion does not control overflow (truncate), therefore you should carefully monitor the data and the data types input into the ONNX model.

Autoconversion supports the following ONNX types:

- ONNX_DATA_TYPE_BOOL
- ONNX_DATA_TYPE_FLOAT
- ONNX_DATA_TYPE_UINT8
- ONNX_DATA_TYPE_INT8
- ONNX_DATA_TYPE_UINT16
- ONNX_DATA_TYPE_INT16
- ONNX_DATA_TYPE_INT32
- ONNX_DATA_TYPE_INT64
- ONNX_DATA_TYPE_FLOAT16
- ONNX_DATA_TYPE_DOUBLE
- ONNX_DATA_TYPE_UINT32
- ONNX_DATA_TYPE_UINT64
- ONNX_DATA_TYPE_COMPLEX64
- ONNX_DATA_TYPE_COMPLEX128

Unsupported types:

- ONNX_DATA_TYPE_BFLOAT16
- ONNX_DATA_TYPE_STRING

### Autoconversion Rules by Tensor Types

If the [MQL5 type](/en/docs/basis/types) is not included into the list of types supported by the model, running the ONNX model will return the ERR_ONNX_NOT_SUPPORTED error (error code 5802).

Note: During autoconversion, the [color](/en/docs/basis/types/integer/boolconst) type is processed as uint, while [datetime](/en/docs/basis/types/integer/datetime) is processed as long.

Autoconversion of input values

| ONNX type (tensor item type) | MQL5 type supported by autoconversion |
| --- | --- |
| ONNX_DATA_TYPE_BOOL | bool, char, uchar, short, ushort, int, color, uint, datetime, long,  folat, double, complex 
   
 During conversion,  Data  elements are checked by a simple comparison against 0 |
| ONNX_DATA_TYPE_FLOAT16 | float, double |
| ONNX_DATA_TYPE_FLOAT | char, uchar, short, ushort, int, color, uint, datetime, long, ulong, float, double |
| ONNX_DATA_TYPE_UINT8 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT8 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT16 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT16 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT32 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT64 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_DOUBLE | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT32 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT64 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_COMPLEX64 | complex |
| ONNX_DATA_TYPE_COMPLEX128 | complex |

Autoconversion of output values

| ONNX type (tensor item type) | MQL5 type supported by autoconversion |
| --- | --- |
| ONNX_DATA_TYPE_BOOL | bool, char, uchar, short, ushort, int, color, uint, datetime, long,  folat, double, complex 
   
 If the tensor element is zero, then the Data element is set to 0; otherwise, the value is 1 |
| ONNX_DATA_TYPE_FLOAT16 | float, double |
| ONNX_DATA_TYPE_FLOAT | char, uchar, short, ushort, int, color, uint, datetime, long, ulong, float, double |
| ONNX_DATA_TYPE_UINT8 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT8 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT16 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT16 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT32 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_INT64 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_DOUBLE | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT32 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_UINT64 | See ONNX_DATA_TYPE_FLOAT |
| ONNX_DATA_TYPE_COMPLEX64 | complex |
| ONNX_DATA_TYPE_COMPLEX128 | complex |

See also

[Type Casting](/en/docs/basis/types/casting)
