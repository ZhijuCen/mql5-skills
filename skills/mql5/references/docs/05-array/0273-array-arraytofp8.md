# ArrayToFP8

Copies an array of type float or double into an array of type [uchar](/en/docs/basis/types/integer/integertypes#uchar) with the given format.

```
bool   ArrayToFP8(
   const uchar&         dst_array[],        // copy to
   const float&         src_array[],        // copy from
   ENUM_FLOAT8_FORMAT   fmt                 // format
   );

```

Overloading for the double type

```
bool   ArrayToFP8(
   const uchar&         dst_array[],        // copy to
   const double&        src_array[],        // copy from
   ENUM_FLOAT8_FORMAT   fmt                 // format
   );

```

Parameters

dst_array[]

[out]  Receiver array or type uchar.

src_array[]

[in]  Source array of type float or double.

fmt

[in]  Copying format from the [ENUM_FLOAT8_FORMAT](/en/docs/onnx/onnx_structures#enum_float8_format) enumeration.

Return Value

Returns true if successful or false otherwise.

Note

All kinds of FP8 format are defined in the [ENUM_FLOAT8_FORMAT](/en/docs/onnx/onnx_structures#enum_float8_format) enumeration and are used in MQL5 only for operations with [ONNX models](/en/docs/onnx).

The function converts input parameters of type float or double into one of FP8 types. These input parameters are then used in the [OnnxRun](/en/docs/onnx/onnxrun) function.

FP8 (8-bit floating point) is one of the data types used to represent floating point numbers. In FP8, each number is represented by 8 data bits, typically divided into three components: sign, exponent and mantissa. This format offers a balance between accuracy and storage efficiency, making it attractive for applications that require memory and computational efficiency.

By employing compact number representation, FP8 reduces memory requirements and accelerates calculations. In addition, FP8 can be useful for implementing low-level operations such as arithmetic calculations and signal processing.

Example: function from the article [Working with ONNX models in float16 and float8 formats ](https://www.mql5.com/ru/articles/14330)

```
//+------------------------------------------------------------------+
//| RunCastFloat8Float                                               |
//+------------------------------------------------------------------+
bool RunCastFloat8ToFloat(long model_handle,const ENUM_FLOAT8_FORMAT fmt)
  {
   PrintFormat("TEST: %s(%s)",__FUNCTION__,EnumToString(fmt));
//---
   float test_data[15]   = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
   uchar data_float8[15] = {};
   if(!ArrayToFP8(data_float8,test_data,fmt))
     {
      Print("error in ArrayToFP8. error code=",GetLastError());
      OnnxRelease(model_handle);
      return(false);
     }
   U<uchar> input_float8_values[3*5];
   U<float> output_float_values[3*5];
   float    test_data_float[];
//--- convert float8 to float
   if(!ArrayFromFP8(test_data_float,data_float8,fmt))
     {
      Print("error in ArrayFromFP8. error code=",GetLastError());
      OnnxRelease(model_handle);
      return(false);
     }
   for(uint i=0; i<data_float8.Size(); i++)
     {
      input_float8_values[i].value=data_float8[i];
      PrintFormat("%d input value =%f  Hex float8 = %s  ushort value=%d",i,test_data_float[i],ArrayToHexString(input_float8_values[i].uc),input_float8_values[i].value);
     }
   Print("ONNX input array: ",ArrayToString(input_float8_values));
//--- execute model (convert float8 to float using ONNX)
   if(!OnnxRun(model_handle,ONNX_NO_CONVERSION,input_float8_values,output_float_values))
     {
      PrintFormat("error in OnnxRun. error code=%d",GetLastError());
      OnnxRelease(model_handle);
      return(false);
     }
   Print("ONNX output array: ",ArrayToString(output_float_values));
//--- calculate error (compare ONNX and ArrayFromFP8 results)
   double sum_error=0.0;
   for(uint i=0; i<test_data.Size(); i++)
     {
      double delta=test_data_float[i]-(double)output_float_values[i].value;
      sum_error+=MathAbs(delta);
      PrintFormat("%d output float %f = %s difference=%f",i,output_float_values[i].value,ArrayToHexString(output_float_values[i].uc),delta);
     }
//---
   PrintFormat("%s(%s): sum_error=%f\n",__FUNCTION__,EnumToString(fmt),sum_error);
   return(true);
  }

```

See also

[ArrayFromFP8](/en/docs/array/arrayfromfp8), [ArrayCopy](/en/docs/array/arraycopy)
