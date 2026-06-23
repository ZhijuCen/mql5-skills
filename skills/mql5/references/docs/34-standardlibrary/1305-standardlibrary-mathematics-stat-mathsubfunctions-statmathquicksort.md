# MathQuickSort

# The function for the simultaneous sorting of the array[] and indices[] arrays using the QuickSort algorithm.

```
void  MathQuickSort(
   double&  array[],     // array of values
   int&     indices[],   // array of indexes
   int      first,       // initial value
   int      last,        // final value
   int      mode         // direction
   )

```

Parameters

array[]

[in][out] Array to be sorted.

indices[]

[in][out] Array to store the indexes of the original array.

first

[in] Index of the element to start sorting from.

last

[in] Index of the element to stop sorting at.

mode

[in] Direction of sorting (>0 ascending; otherwise, descending).
