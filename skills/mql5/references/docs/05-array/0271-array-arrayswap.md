# ArraySwap

Swaps the contents of two dynamic arrays of the same type. For multidimensional arrays, the number of elements in all dimensions except the first one should match.

```
bool  ArraySwap(
   void&  array1[],      // first array
   void&  array2[]       // second array
   );

```

Parameters

array1[]

[in][out]  Array of numerical type.

array2[]

[in][out]  Array of numerical type.

Return Value

Returns true if successful, otherwise false. In this case, [GetLastError()](/en/docs/check/getlasterror) returns the [ERR_INVALID_ARRAY](/en/docs/constants/errorswarnings/errorcodes) error code.

Note

The function accepts dynamic arrays of the same type and the same dimensions except the first one. For integer types, the sign is ignored, i.e. [char](/en/docs/basis/types/integer/integertypes)==uchar)

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- arrays for storing quotes
   double source_array[][8];
   double   dest_array[][8];
   MqlRates rates[];
//--- get the data of the last 20 candles on the current timeframe
   int copied=CopyRates(NULL,0,0,20,rates);
   if(copied<=0)
     {
      PrintFormat("CopyRates(%s,0,0,20,rates) failed, error=%d",
                  Symbol(),GetLastError());
      return;
     }
//--- set the array size for the amount of copied data
   ArrayResize(source_array,copied);
//--- fill the rate_array_1[] array by data from rates[]
   for(int i=0;i<copied;i++)
     {
      source_array[i][0]=(double)rates[i].time;
      source_array[i][1]=rates[i].open;
      source_array[i][2]=rates[i].high;
      source_array[i][3]=rates[i].low;
      source_array[i][4]=rates[i].close;
      source_array[i][5]=(double)rates[i].tick_volume;
      source_array[i][6]=(double)rates[i].spread;
      source_array[i][7]=(double)rates[i].real_volume;
     }
//--- swap data between source_array[] and dest_array[]
   if(!ArraySwap(source_array,dest_array))
     {
      PrintFormat("ArraySwap(source_array,rate_array_2) failed, error code=%d",GetLastError());
      return;
     }
//--- ensure that the source array has become zero after the swap
   PrintFormat("ArraySwap() done: ArraySize(source_array)=%d",ArraySize(source_array));
//--- display the data of the dest_array[] destination array
   ArrayPrint(dest_array);
  }

```

See also

[ArrayCopy](/en/docs/array/arraycopy), [ArrayFill](/en/docs/array/arrayfill), [ArrayRange](/en/docs/array/arrayrange), [ArrayIsDynamic](/en/docs/array/arrayisdynamic)
