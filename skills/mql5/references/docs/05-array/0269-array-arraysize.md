# ArraySize

The function returns the number of elements of a selected array.

```
int  ArraySize(
   const void&  array[]    // checked array
   );

```

Parameters

array[]

[in]  Array of any type.

Return Value

Value of [int](/en/docs/basis/types/integer/integertypes) type.

Note

For a one-dimensional array, the value to be returned by the ArraySize is equal to that of [ArrayRange](/en/docs/array/arrayrange)(array,0).

Example:

```
void OnStart()
  {
//--- create arrays
   double one_dim[];
   double four_dim[][10][5][2];
//--- sizes
   int one_dim_size=25;
   int reserve=20;
   int four_dim_size=5;
//--- auxiliary variable
   int size;
//--- allocate memory without backup
   ArrayResize(one_dim,one_dim_size);
   ArrayResize(four_dim,four_dim_size);
//--- 1. one-dimensional array
   Print("+==========================================================+");
   Print("Array sizes:");
   Print("1. One-dimensional array");
   size=ArraySize(one_dim);
   PrintFormat("Zero dimension size = %d, Array size = %d",one_dim_size,size);
//--- 2. multidimensional array
   Print("2. Multidimensional array");
   size=ArraySize(four_dim);
   PrintFormat("Zero dimension size = %d, Array size = %d",four_dim_size,size);
//--- dimension sizes
   int d_1=ArrayRange(four_dim,1);
   int d_2=ArrayRange(four_dim,2);
   int d_3=ArrayRange(four_dim,3);
   Print("Check:");
   Print("Zero dimension = Array size / (First dimension * Second dimension * Third dimension)");
   PrintFormat("%d = %d / (%d * %d * %d)",size/(d_1*d_2*d_3),size,d_1,d_2,d_3);
//--- 3. one-dimensional array with memory backup
   Print("3. One-dimensional array with memory backup");
//--- double the value
   one_dim_size*=2;
//--- allocate memory with backup
   ArrayResize(one_dim,one_dim_size,reserve);
//--- print out the size
   size=ArraySize(one_dim);
   PrintFormat("Size with backup = %d, Actual array size = %d",one_dim_size+reserve,size);
  }

```
