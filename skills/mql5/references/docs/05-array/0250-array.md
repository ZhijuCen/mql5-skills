# Group of Functions for Working with Arrays

[Arrays](/en/docs/basis/variables#array_define) are allowed to be maximum four-dimensional. Each dimension is indexed from 0 to dimension_size-1. In a particular case of a one-dimensional array of 50 elements, calling of the first element will appear as array[0], of the last one - as array[49].

| Function | Action |
| --- | --- |
| ArrayBsearch | Returns index of the first found element in the first array dimension |
| ArrayCopy | Copies one array into another |
| ArrayCompare | Returns the result of comparing two arrays of  simple types  or custom structures without  complex objects |
| ArrayFree | Frees up buffer of any dynamic array and sets the size of the zero dimension in 0. |
| ArrayGetAsSeries | Checks direction of array indexing |
| ArrayInitialize | Sets all elements of a numeric array into a single value |
| ArrayFill | Fills an array with the specified value |
| ArrayIsSeries | Checks whether an array is a timeseries |
| ArrayIsDynamic | Checks whether an array is dynamic |
| ArrayMaximum | Search for an element with the maximal value |
| ArrayMinimum | Search for an element with the minimal value |
| ArrayPrint | Prints an array of a simple type or a simple structure into journal |
| ArrayRange | Returns the number of elements in the specified dimension of the array |
| ArrayResize | Sets the new size in the first dimension of the array |
| ArrayInsert | Inserts the specified number of elements from a source array to a receiving one starting from a specified index |
| ArrayRemove | Removes the specified number of elements from the array starting with a specified index |
| ArrayReverse | Reverses the specified number of elements in the array starting with a specified index |
| ArraySetAsSeries | Sets the direction of array indexing |
| ArraySize | Returns the number of elements in the array |
| ArraySort | Sorting of numeric arrays by the first dimension |
| ArraySwap | Swaps the contents of two dynamic arrays of the same type |
| ArrayToFP16 | Copies an array of type float or double into an array of type  ushort  with the given format |
| ArrayToFP8 | Copies an array of type float or double into an array of type  uchar  with the given format |
| ArrayFromFP16 | Copies an array of type  ushort  into an array of float or double type with the given format |
| ArrayFromFP8 | Copies an array of type  uchar  into an array of float or double type with the given format |
