# ArrayReverse

Reverses the specified number of elements in the array starting with a specified index.

```
bool  ArrayReverse(
   void&        array[],            // array of any type
   uint         start=0,            // index to start reversing the array from
   uint         count=WHOLE_ARRAY   // number of elements
   );

```

Parameters

array[]

[in][out]  Array.

start=0

[in]  Index the array reversal starts from.

count=WHOLE_ARRAY

[in]  Number of reversed elements. If WHOLE_ARRAY, then all array elements are moved in the inversed manner starting with the specified start index up to the end of the array.

Return Value

Returns true if successful, otherwise - false.

Note

The [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function does not move the array elements physically. Instead, it only changes the indexation direction backwards to arrange the access to the elements as in the [timeseries](/en/docs/series). The ArrayReverse() function physically moves the array elements so that the array is "reversed".

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare the fixed-size array and fill in the values
   int array[10];
   for(int i=0;i<10;i++)
     {
      array[i]=i;
     }
//--- display the array before reversing the elements
   Print("Before calling ArrayReverse()");
   ArrayPrint(array);
//--- reverse 3 elements in the array and show the new set
   ArrayReverse(array,4,3);
   Print("After calling ArrayReverse()");
   ArrayPrint(array);
/*
  Execution result:
  Before calling ArrayReverse()
   0 1 2 3 4 5 6 7 8 9
  After calling ArrayReverse()
   0 1 2 3 6 5 4 7 8 9
*/

```

See also

[ArrayInsert](/en/docs/array/arrayinsert), [ArrayRemove](/en/docs/array/arrayremove), [ArrayCopy](/en/docs/array/arraycopy), [ArrayResize](/en/docs/array/arrayresize), [ArrayFree](/en/docs/array/arrayfree), [ArrayGetAsSeries](/en/docs/array/arraygetasseries), [ArraySetAsSeries](/en/docs/array/arraysetasseries)
