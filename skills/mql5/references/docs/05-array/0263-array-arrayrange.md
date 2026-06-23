# ArrayRange

The function returns the number of elements in a selected array dimension.

```
int  ArrayRange(
   const void&   array[],      // array for check
   int           rank_index    // index of dimension
   );

```

Parameters

array[]

[in]  Checked array.

rank_index

[in]  Index of dimension.

Return Value

Number of elements in a selected array dimension.

Note

Since indexes start at zero, the number of the array dimensions is one greater than the index of the last dimension.

Example:

```
void OnStart()
  {
//--- create four-dimensional array
   double array[][5][2][4];
//--- set the size of the zero dimension
   ArrayResize(array,10,10);
//--- print dimensions
   int temp;
   for(int i=0;i<4;i++)
     {
      //--- receive the size of i dimension
      temp=ArrayRange(array,i);
      //--- print
      PrintFormat("dim = %d, range = %d",i,temp);
     }
//--- Result
// dim = 0, range = 10
// dim = 1, range = 5
// dim = 2, range = 2
// dim = 3, range = 4
  }

```
