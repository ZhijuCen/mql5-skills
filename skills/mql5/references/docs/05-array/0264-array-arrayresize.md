# ArrayResize

The function sets a new size for the first dimension

```
int  ArrayResize(
   void&  array[],              // array passed by reference
   int    new_size,             // new array size
   int    reserve_size=0        // reserve size value (excess)
   );

```

Parameters

array[]

[out] Array for changing sizes.

new_size

[in]  New size for the first dimension.

reserve_size=0

[in]  Distributed size to get reserve.

Return Value

If executed successfully, it returns count of all elements contained in the array after resizing, otherwise, returns -1, and array is not resized.

If ArrayResize() is applied to a [static](/en/docs/basis/types/dynamic_array#static_array) array, a [timeseries](/en/docs/series/bufferdirection) or an [indicator buffer](/en/docs/customind/setindexbuffer), the array size remains the same – these arrays will not be reallocated. In this case, if new_size<=[ArraySize(](/en/docs/array/arraysize)array[)](/en/docs/array/arrayresize), the function will only return new_size; otherwise a value of -1 will be returned.

Note

The function can be applied only to [dynamic arrays](/en/docs/basis/types/dynamic_array). It should be noted that you cannot change the size of dynamic arrays assigned as indicator buffers by the [SetIndexBuffer()](/en/docs/customind/setindexbuffer) function. For indicator buffers, all operations of resizing are performed by the runtime subsystem of the terminal.

Total amount of elements in the array cannot exceed 2147483647.

With the frequent memory allocation, it is recommended to use a third parameter that sets a reserve to reduce the number of physical memory allocations. All the subsequent calls of ArrayResize do not lead to physical reallocation of memory, but only change the size of the first array dimension within the reserved memory. It should be remembered that the third parameter will be used only during physical memory allocation. For example:

```
ArrayResize(arr,1000,1000);
for(int i=1;i<3000;i++)
   ArrayResize(arr,i,1000);

```

In this case the memory will be reallocated twice, first before entering the 3000 iterations loop (the array size will be set to 1000), and the second time with i equal to 2000. If we skip the third parameter, there will be 2000 physical reallocations of memory, which will slow down the program.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- Counters
   ulong start=GetTickCount();
   ulong now;
   int   count=0;
//--- An array for demonstration of a quick version
   double arr[];
   ArrayResize(arr,100000,100000);
//--- Check how fast the variant with memory reservation works
   Print("--- Test Fast: ArrayResize(arr,100000,100000)");
   for(int i=1;i<=300000;i++)
     {
      //--- Set a new array size specifying the reserve of 100,000 elements!
      ArrayResize(arr,i,100000);
      //--- When reaching a round number, show the array size and the time spent
      if(ArraySize(arr)%100000==0)
        {
         now=GetTickCount();
         count++;
         PrintFormat("%d. ArraySize(arr)=%d Time=%d ms",count,ArraySize(arr),(now-start));
         start=now; 
        }
     }
//--- Now show, how slow the version without memory reservation is
   double slow[];
   ArrayResize(slow,100000,100000);
//--- 
   count=0;
   start=GetTickCount();
   Print("---- Test Slow: ArrayResize(slow,100000)");
//---
   for(int i=1;i<=300000;i++)
     {
      //--- Set a new array size, but without the additional reserve
      ArrayResize(slow,i);
      //--- When reaching a round number, show the array size and the time spent
      if(ArraySize(slow)%100000==0)
        {
         now=GetTickCount();
         count++;
         PrintFormat("%d. ArraySize(slow)=%d Time=%d ms",count,ArraySize(slow),(now-start));
         start=now;
        }
     }
  }
//--- A sample result of the script
/*
   Test_ArrayResize (EURUSD,H1)   --- Test Fast: ArrayResize(arr,100000,100000)
   Test_ArrayResize (EURUSD,H1)   1. ArraySize(arr)=100000 Time=0 ms
   Test_ArrayResize (EURUSD,H1)   2. ArraySize(arr)=200000 Time=0 ms
   Test_ArrayResize (EURUSD,H1)   3. ArraySize(arr)=300000 Time=0 ms
   Test_ArrayResize (EURUSD,H1)   ---- Test Slow: ArrayResize(slow,100000)
   Test_ArrayResize (EURUSD,H1)   1. ArraySize(slow)=100000 Time=0 ms
   Test_ArrayResize (EURUSD,H1)   2. ArraySize(slow)=200000 Time=0 ms
   Test_ArrayResize (EURUSD,H1)   3. ArraySize(slow)=300000 Time=228511 ms
*/

```

See also

[ArrayInitialize](/en/docs/array/arrayinitialize)
