# ArrayFill

The function fills an array with the specified value.

```
void  ArrayFill(
   void&  array[],      // array
   int    start,         // starting index
   int    count,         // number of elements to fill
   void   value          // value
   );

```

Parameters

array[]

[out]  Array of simple type ([char](/en/docs/basis/types/integer/integertypes), [uchar](/en/docs/basis/types/integer/integertypes), [short](/en/docs/basis/types/integer/integertypes), [ushort](/en/docs/basis/types/integer/integertypes), [int](/en/docs/basis/types/integer/integertypes), [uint](/en/docs/basis/types/integer/integertypes), [long](/en/docs/basis/types/integer/integertypes), [ulong](/en/docs/basis/types/integer/integertypes), [bool](/en/docs/basis/types/integer/boolconst), [color](/en/docs/basis/types/integer/color), [datetime](/en/docs/basis/types/integer/datetime), [float](/en/docs/basis/types/double), [double](/en/docs/basis/types/double)).

start

[in]  Starting index.  In such a case, specified [AS_SERIES flag](/en/docs/array/arraysetasseries) is ignored.

count

[in]  Number of elements to fill.

value

[in]  Value to fill the array with.

Return Value

No return value.

Note

When ArrayFill() function is called, normal indexation direction (from left to right) is always implied. It means that the change of the order of access to the array elements using [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function is ignored.

A multidimensional array is shown as one-dimensional when processed by ArrayFill() function. For example, array[2][4] is processed as array[8]. Therefore, you may specify the initial element's index to be equal to 5 when working with this array. Thus, the call of ArrayFill(array, 5, 2, 3.14) for array[2][4] fills array[1][1] and array[1][2] elements with 3.14.

Example:

```
void OnStart()
  {
//--- declare dynamic array
   int a[];
//--- set size
   ArrayResize(a,10);
//--- fill first 5 elements with 123
   ArrayFill(a,0,5,123);
//--- fill next 5 elements with 456
   ArrayFill(a,5,5,456);
//--- show values
   for(int i=0;i<ArraySize(a);i++) printf("a[%d] = %d",i,a[i]);
  }

```
