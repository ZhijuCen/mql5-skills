# ArrayToFP16

Copies an array of type float or double into an array of type [ushort](/en/docs/basis/types/integer/integertypes#ushort) with the given format.

```
bool   ArrayToFP16(
   const ushort&        dst_array[],        // copy to
   const float&         src_array[],        // copy from
   ENUM_FLOAT16_FORMAT  fmt                 // format
   );

```

Overloading for the double type

```
bool   ArrayToFP16(
   const ushort&        dst_array[],        // copy to
   const double&        src_array[],        // copy from
   ENUM_FLOAT16_FORMAT  fmt                 // format
   );

```

Parameters

dst_array[]

[out]  Receiver array or type ushort.

src_array[]

[in]  Source array of type float or double.

fmt

[in]  Copying format from the [ENUM_FLOAT16_FORMAT](/en/docs/onnx/onnx_structures#enum_float16_format) enumeration.

Return Value

Returns true if successful or false otherwise.

Note

Formats FLOAT16 and BFLOAT16 are defined in the [ENUM_FLOAT16_FORMAT](/en/docs/onnx/onnx_structures#enum_float16_format) enumeration and are used in MQL5 only for operations with [ONNX models](/en/docs/onnx).

The function converts input parameters of type float or double to type FLOAT16 and BFLOAT16. These input parameters are then used in the [OnnxRun](/en/docs/onnx/onnxrun) function.

FLOAT16, also known as [half-precision float](https://en.wikipedia.org/wiki/Half-precision_floating-point_format), uses 16 bits to represent floating-point numbers. This format provides a balance between accuracy and computational efficiency. FLOAT16 is widely used in deep learning algorithms and neural networks, which require high-performance processing of large datasets. This format accelerates computations calculations by reducing the size of numbers, which is especially important when training deep neural networks on GPUs.

BFLOAT16 (or [Brain Floating Point 16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format)) also uses 16 bits but differs from FLOAT16 in the approach to format representation. In this format, 8 bits are allocated for representing the exponent, while the remaining 7 bits are used for representing the mantissa. This format was developed for use in deep learning and artificial intelligence, especially in Google's Tensor Processing Unit (TPU). BFLOAT16 demonstrates excellent performance in neural network training and can effectively accelerate computations.

Example: function from the article [Working with ONNX models in float16 and float8 formats ](https://www.mql5.com/ru/articles/14330)

```
//+------------------------------------------------------------------+
//| RunCastFloat16ToDouble                                           |
//+------------------------------------------------------------------+
bool RunCastFloat16ToDouble(long model_handle)
  {
   PrintFormat("test=%s",__FUNCTION__);
   double test_data[12]= {1,2,3,4,5,6,7,8,9,10,11,12};
   ushort data_uint16[12];
   if(!ArrayToFP16(data_uint16,test_data,FLOAT_FP16))
     {
      Print("error in ArrayToFP16. error code=",GetLastError());
      return(false);
     }
   Print("test array:");
   ArrayPrint(test_data);
   Print("ArrayToFP16:");
   ArrayPrint(data_uint16);
   U<ushort> input_float16_values[3*4];
   U<double> output_double_values[3*4];
   float test_data_float[];
   if(!ArrayFromFP16(test_data_float,data_uint16,FLOAT_FP16))
     {
      Print("error in ArrayFromFP16. error code=",GetLastError());
      return(false);
     }
   for(int i=0; i<12; i++)
     {
      input_float16_values[i].value=data_uint16[i];
      PrintFormat("%d input value =%f  Hex float16 = %s  ushort value=%d",i,test_data_float[i],ArrayToString(input_float16_values[i].uc),input_float16_values[i].value);
     }
   Print("ONNX input array:");
   ArrayPrint(input_float16_values);
   bool res=OnnxRun(model_handle,ONNX_NO_CONVERSION,input_float16_values,output_double_values);
   if(!res)
     {
      PrintFormat("error in OnnxRun. error code=%d",GetLastError());
      return(false);
     }
   Print("ONNX output array:");
   ArrayPrint(output_double_values);
//---
   double sum_error=0.0;
   for(int i=0; i<12; i++)
     {
      double delta=test_data[i]-output_double_values[i].value;
      sum_error+=MathAbs(delta);
      PrintFormat("%d output double %f = %s  difference=%f",i,output_double_values[i].value,ArrayToString(output_double_values[i].uc),delta);
     }
//---
   PrintFormat("test=%s   sum_error=%f",__FUNCTION__,sum_error);
//---
   return(true);
  }

```

See also

[ArrayFromFP16](/en/docs/array/arrayfromfp16), [ArrayCopy](/en/docs/array/arraycopy)
