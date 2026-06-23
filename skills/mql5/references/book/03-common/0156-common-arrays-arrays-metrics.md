# Array measurement

One of the main characteristics of an array is its size, that is, the total number of elements in it. It is important to note that for multidimensional arrays, the size is the product of the lengths of all its dimensions.

For fixed arrays, you can calculate their size at compile stage using the [sizeof](/en/book/basis/expressions/operators_sizeof_typename) operator-based language construct:

```
sizeof(array) / sizeof(type)

```

where array is an identifier, and type is the array type.

For example, if an array is defined in the code fixed:

```
int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};

```

then its size is:

```
int n = sizeof(fixed) / sizeof(int); // 8

```

For dynamic arrays, this rule does not work, since the sizeof operator always generates the same size of the internal dynamic array object: 52 bytes.

Note that in functions, all array parameters are represented internally as dynamic array wrapper objects. This is done so that an array with any method of memory allocation, including a fixed one, can be passed to the function. That's why sizeof(array) will return 52 for the parameter array, even if a fixed size array was passed through it.  

   

The presence of "wrappers" affects only sizeof. The ArrayIsDynamic function always correctly determines the category of the actual argument passed through the parameter array.

To get the size of any array at the stage of program execution, use the ArraySize function.

int ArraySize(const void &array[])

The function returns the total number of elements in the array. The dimension and type of the array can be any. For a one-dimensional array, the function call is similar to ArrayRange(array, 0) (see below).

If the array was distributed with a reserve (the third parameter of the [ArrayResize](/en/book/common/arrays/arrays_dynamic) function), its value is not taken into account.

Until memory is allocated for the dynamic array using ArrayResize, the ArraySize function will return 0. Also, the size becomes zero after calling [ArrayFree](/en/book/common/arrays/arrays_dynamic) for the array.

int ArrayRange(const void &array[], int dimension)

The ArrayRange function returns the number of elements in the specified array dimension. The dimension and type of the array can be any. Parameter dimension must be between 0 and the number of array dimensions minus 1. Index 0 corresponds to the first dimension, index 1 to the second, and so on.

Product of all values of ArrayRange(array, i) with i running over all dimensions gives ArraySize(array).

Let's see the examples of the functions described above (see file ArraySize.mq5).

```
void OnStart()
{
   int dynamic[];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   
   PRT(sizeof(fixed) / sizeof(int));   // 8
   PRT(ArraySize(fixed));              // 8
   
   ArrayResize(dynamic, 10);
   
   PRT(sizeof(dynamic) / sizeof(int)); // 13 (incorrect)
   PRT(ArraySize(dynamic));            // 10
   
   PRT(ArrayRange(fixed, 0));          // 2
   PRT(ArrayRange(fixed, 1));          // 4
   
   PRT(ArrayRange(dynamic, 0));        // 10
   PRT(ArrayRange(dynamic, 1));        // 0
   int size = 1;
   for(int i = 0; i < 2; ++i)
   {
      size *= ArrayRange(fixed, i);
   }
   PRT(size == ArraySize(fixed));      // true
}

```
