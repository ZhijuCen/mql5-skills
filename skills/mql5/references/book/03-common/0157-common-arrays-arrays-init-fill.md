# Initializing and populating arrays

Describing an array with an initialization list is possible only for arrays of a fixed size. Dynamic arrays can be populated only after allocating memory for them by the function [ArrayResize](/en/book/common/arrays/arrays_dynamic). They are populated using the ArrayInitialize or ArrayFill functions. They are also useful in a program when you want to bulk-replace values in fixed arrays or time series.

Examples of using the functions are given after their description.

int ArrayInitialize(type &array[], type value)

The function sets all array elements to the specified value. Only arrays of built-in numeric types are supported (char, uchar, short, ushort, int, uint, long, ulong, bool, color, datetime, float, double). String, structure and pointer arrays cannot be filled in this way: they will need to implement their own initialization functions. An array can be multidimensional.

The function returns the number of elements.

If the dynamic array is allocated with a reserve (the third parameter of the ArrayResize function), then the reserve is not initialized.

If, after the array is initialized, its size is increased using ArrayResize, the added elements will not be automatically set to value. They can be populated using the ArrayFill function.

void ArrayFill(type &array[], int start, int count, type value)

The function fills a numeric array or part of it with a specified value. Part of the array is given by parameters start and count, which denote the initial number of the element and the number of elements to be filled, respectively.

It does not matter to the function whether the numbering order of the array elements is set [like in timeseries](/en/book/common/arrays/arrays_as_series) or not: this property is ignored. In other words, the elements of an array are always counted from its beginning to its end.

For a multidimensional array, the start parameter can be obtained by converting the coordinates in all dimensions into a through index for an equivalent one-dimensional array. So, for a two-dimensional array, the elements with the 0th index in the first dimension are located in memory first, then there will be the elements with the index 1 in the first dimension, and so on. The formula to calculate start is as follows:

```
start = D1 * N2 + D2

```

where D1 and D2 are the indexes for the first and second dimensions, respectively, N2 is the number of elements for the second dimension. D2 changes from 0 to (N2-1), D1 changes from 0 to (N1-1). For example, in an array array[3][4] the element with indexes [1][3] is the seventh one in a row, and therefore the call ArrayFill(array, 7, 2, ...) will fill two elements:array[1][3] and following after him array[2][0]. On the diagram, this can be depicted as follows (each cell contains a through index of the element):

```
      [][0]  [][1]  [][2]  [][3]
[0][]    0      1      2      3
[1][]    4      5      6      7
[2][]    8      9     10     11

```

The ArrayFill.mq5 script provides examples of using the aforementioned functions.

```
void OnStart()
{
   int dynamic[];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   
   PRT(ArrayInitialize(fixed, -1));
   ArrayPrint(fixed);
   ArrayFill(fixed, 3, 4, +1);
   ArrayPrint(fixed);
   
   PRT(ArrayResize(dynamic, 10, 50));
   PRT(ArrayInitialize(dynamic, 0));
   ArrayPrint(dynamic);
   PRT(ArrayResize(dynamic, 50));
   ArrayPrint(dynamic);
   ArrayFill(dynamic, 10, 40, 0);
   ArrayPrint(dynamic);
}

```

Here's what a possible result looks like (random data in uninitialized elements of a dynamic array will be different):

```
ArrayInitialize(fixed,-1)=8
    [,0][,1][,2][,3]
[0,]  -1  -1  -1  -1
[1,]  -1  -1  -1  -1
    [,0][,1][,2][,3]
[0,]  -1  -1  -1   1
[1,]   1   1   1  -1
ArrayResize(dynamic,10,50)=10
ArrayInitialize(dynamic,0)=10
0 0 0 0 0 0 0 0 0 0
ArrayResize(dynamic,50)=50
[ 0]           0           0           0           0           0
               0           0           0           0           0
[10] -1402885947  -727144693   699739629   172950740 -1326090126
           47384           0           0     4194184           0
[20]           2           0           2           0           0
               0           0  1765933056  2084602885 -1956758056
[30]    73910037 -1937061701          56           0          56
               0     1048601  1979187200       10851           0
[40]           0           0           0  -685178880 -1720475236
       782716519 -1462194191  1434596297   415166825 -1944066819
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

```
