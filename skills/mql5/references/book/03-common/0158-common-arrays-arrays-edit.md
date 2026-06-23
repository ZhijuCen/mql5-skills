# Copying and editing arrays

In this section, we'll learn how to use built-in functions to insert and remove array elements, change their order, and copy entire arrays.

bool ArrayInsert(void &target[], const void &source[], uint to, uint from = 0, uint count = WHOLE_ARRAY)

The function inserts the specified number of elements from the source array 'source' into the destination target array. A position for insertion into the target array is set by the index in the to parameter. The starting index of the element at which to start copying from the source array is given by the index from. The WHOLE_ARRAY constant ((uint)-1) in the parameter count specifies the transfer of all elements of the source array.

All indexes and counts are relative to the first dimension of the arrays. In other words, for multidimensional arrays, the insertion is performed not by individual elements, but by the entire configuration described by the "higher" dimensions. For example, for a two-dimensional array, the value 1 in the parameter count means inserting a vector of length equal to the second dimension (see the example).

Due to this, the target array and the source array must have the same configurations. Otherwise, an error will occur and copying will fail. For one-dimensional arrays, this is not a limitation, but for multidimensional arrays, it is necessary to observe the equality of sizes in dimensions above the first one. In particular, elements from the array [][4] cannot be inserted into the array [][5] and vice versa.

The function is applicable only for arrays of fixed or dynamic size. Editing timeseries (arrays with [time series](/en/book/applications/timeseries)) cannot be performed with this function. It is prohibited to specify in the parameters target and source the same array.

When inserted into a fixed array, new elements shift existing elements to the right and displace count of the rightmost elements to the outside of the array. The to parameter must have a value between 0 and the size of the array minus 1.

When inserted into a dynamic array, the old elements are also shifted to the right, but they do not disappear, because the array itself expands by count elements. The to parameter must have a value between 0 and the size of the array. If it is equal to the size of the array, new elements are added to the end of the array.

The specified elements are copied from one array to another, i.e., they remain unchanged in the original array, and their "doubles" in the new array become independent instances that are not related to the "originals" in any way.

The function returns true if successful or false in case of error.

Let's consider some examples (ArrayInsert.mq5). The OnStart function provides descriptions of several arrays of different configurations, both fixed and dynamic.

```
#define PRTS(A) Print(#A, "=", (string)(A) + " / status:" + (string)GetLastError())
 
void OnStart()
{
   int dynamic[];
   int dynamic2Dx5[][5];
   int dynamic2Dx4[][4];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   int insert[] = {10, 11, 12};
   int array[1] = {100};
   ...

```

To begin with, for convenience, a macro is introduced that displays the error code (obtained through the function [GetLastError](/en/book/common/environment/env_last_error)) immediately after calling the instruction under test — PRTS. This is a slightly modified version of the familiar PRT macro.

Attempts to copy elements between arrays of different configurations end with error 4006 (ERR_INVALID_ARRAY).

```
   // you can't mix 1D and 2D arrays
   PRTS(ArrayInsert(dynamic, fixed, 0)); // false:4006, ERR_INVALID_ARRAY
   ArrayPrint(dynamic); // empty
   // you can't mix 2D arrays of different configurations by the second dimension
   PRTS(ArrayInsert(dynamic2Dx5, fixed, 0)); // false:4006, ERR_INVALID_ARRAY
   ArrayPrint(dynamic2Dx5); // empty
   // even if both arrays are fixed (or both are dynamic),
   // size by "higher" dimensions must match
   PRTS(ArrayInsert(fixed, insert, 0)); // false:4006, ERR_INVALID_ARRAY
   ArrayPrint(fixed); // not changed   
   ...

```

The target index must be within the array.

```
   // target index 10 is out of the range or the array 'insert',
   // could be 0, 1, 2, because its size = 3
   PRTS(ArrayInsert(insert, array, 10)); // false:5052, ERR_SMALL_ARRAY
   ArrayPrint(insert); // not changed   
   ...

```

The following are successful array modifications:

```
   // copy second row from 'fixed', 'dynamic2Dx4' is allocated
   PRTS(ArrayInsert(dynamic2Dx4, fixed, 0, 1, 1)); // true
   ArrayPrint(dynamic2Dx4);
   // both rows from 'fixed' are added to the end of 'dynamic2Dx4', it expands
   PRTS(ArrayInsert(dynamic2Dx4, fixed, 1)); // true
   ArrayPrint(dynamic2Dx4);
   // memory is allocated for 'dynamic' for all elements 'insert'
   PRTS(ArrayInsert(dynamic, insert, 0)); // true
   ArrayPrint(dynamic);
   // 'dynamic' expands by 1 element
   PRTS(ArrayInsert(dynamic, array, 1)); // true
   ArrayPrint(dynamic);
   // new element will push the last one out of 'insert'
   PRTS(ArrayInsert(insert, array, 1)); // true
   ArrayPrint(insert);
}

```

Here's what will appear in the log:

```
ArrayInsert(dynamic2Dx4,fixed,0,1,1)=true
    [,0][,1][,2][,3]
[0,]   5   6   7   8
ArrayInsert(dynamic2Dx4,fixed,1)=true
    [,0][,1][,2][,3]
[0,]   5   6   7   8
[1,]   1   2   3   4
[2,]   5   6   7   8
ArrayInsert(dynamic,insert,0)=true
10 11 12
ArrayInsert(dynamic,array,1)=true
 10 100  11  12
ArrayInsert(insert,array,1)=true
 10 100  11
 

```

bool ArrayCopy(void &target[], const void &source[], int to = 0, int from = 0, int count = WHOLE_ARRAY)

The function copies part or all of the source array to the target array. The place in the target array where the elements are written is specified by the index in the to parameter. The starting index of the element from which to start copying from the source array is given by the from index. The WHOLE_ARRAY constant (-1) in the count parameter specifies the transfer of all elements of the source array. If count is less than zero or greater than the number of elements remaining from the from position to the end of the source array, the entire remainder of the array is copied.

Unlike the ArrayInsert function, the ArrayCopy function does not shift the existing elements of the receiving array but writes new elements to the specified positions over the old ones.

All indexes and the number of elements are set taking into account the continuous numbering of elements, regardless of the number of dimensions in the arrays and their configuration. In other words, elements can be copied from multidimensional arrays to one-dimensional arrays and vice versa, or between multidimensional arrays with different sizes according to the "higher" dimensions (see the example).

The function works with fixed and dynamic arrays, as well as time series arrays designated as [indicator buffers](/en/book/applications/indicators_make/indicators_buffers_plots).

It is permitted to copy elements from an array to itself. But if the target and source areas overlap, you need to keep in mind that the iteration is done from left to right.

A dynamic destination array is automatically expanded as needed. Fixed arrays retain their dimensions, and what is copied must fit in the array, otherwise an error will occur.

Arrays of built-in types and arrays of structures with simple type fields are supported. For numeric types, the function will try to convert the data if the source and destination types differ. A string array can only be copied to a string array. Class objects are not allowed, but pointers to objects can be copied.

The function returns the number of elements copied (0 on error).

In the script ArrayCopy.mq5 there are several examples of using the function.

```
class Dummy
{
   int x;
};
   
void OnStart()
{
   Dummy objects1[5], objects2[5];
 // error: structures or classes with objects are not allowed
   PRTS(ArrayCopy(objects1, objects2));
   ...

```

Arrays with objects generate a compilation error stating that "structures or classes containing objects are not allowed", but pointers can be copied.

```
   Dummy *pointers1[5], *pointers2[5];
   for(int i = 0; i < 5; ++i)
   {
      pointers1[i] = &objects1[i];
   }
   PRTS(ArrayCopy(pointers2, pointers1)); // 5 / status:0
   for(int i = 0; i < 5; ++i)
   {
      Print(i, " ", pointers1[i], " ", pointers2[i]);
   }
 // it outputs some pairwise identical object descriptors
   /*
   0 1048576 1048576
   1 2097152 2097152
   2 3145728 3145728
   3 4194304 4194304
   4 5242880 5242880
   */

```

Arrays of structures with fields of simple types are also copied without problems.

```
struct Simple
{
   int x;
};
   
void OnStart()
{
   ...
   Simple s1[3] = {{123}, {456}, {789}}, s2[];
   PRTS(ArrayCopy(s2, s1)); // 3 / status:0
   ArrayPrint(s2);
   /*
       [x]
   [0] 123
   [1] 456
   [2] 789
   */
   ...

```

To further demonstrate how to work with arrays of different types and configurations, the following arrays are defined (including fixed, dynamic, and arrays with a different number of dimensions):

```
   int dynamic[];
   int dynamic2Dx5[][5];
   int dynamic2Dx4[][4];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   int insert[] = {10, 11, 12};
   double array[1] = {M_PI};
   string texts[];
   string message[1] = {"ok"};
   ...

```

When copying one element from the fixed array from position 1 (number 2), a whole row of 4 elements is allocated in the receiving dynamic array dynamic2Dx4, and since only 1 element is copied, the remaining three will contain random "garbage" (highlighted in yellow).

```
   PRTS(ArrayCopy(dynamic2Dx4, fixed, 0, 1, 1)); // 1 / status:0
   ArrayPrint(dynamic2Dx4);
   /*
       [,0][,1][,2][,3]
   [0,]   2   1   2   3
   */
   ...

```

Next, we copy all the elements from the fixed array, starting from the third one, into the same array dynamic2Dx4, but starting from position 1. Since 5 elements are copied (the total number in the array fixed is 8 minus the initial position 3), and they are placed at index 1, in total, 1 + 5 will be occupied in the receiving array, for a total of 6 elements. And since the array dynamic2Dx4 has 4 elements in each row (in the second dimension), it is possible to allocate memory for it only for the number of elements that is a multiple of 4, i.e., 2 more elements will be distributed, in which random data will remain.

```
   PRTS(ArrayCopy(dynamic2Dx4, fixed, 1, 3)); // 5 / status:0
   ArrayPrint(dynamic2Dx4);
   /*
       [,0][,1][,2][,3]
   [0,]   2   4   5   6
   [1,]   7   8   3   4
   */

```

When copying a multidimensional array to a one-dimensional array, the elements will be presented in a "flat" form.

```
   PRTS(ArrayCopy(dynamic, fixed)); // 8 / status:0
   ArrayPrint(dynamic);
   /*
   1 2 3 4 5 6 7 8
   */

```

When copying a one-dimensional array to a multidimensional one, the elements are "expanded" according to the dimensions of the receiving array.

```
   PRTS(ArrayCopy(dynamic2Dx5, insert)); // 3 / status:0
   ArrayPrint(dynamic2Dx5);
   /*
       [,0][,1][,2][,3][,4]
   [0,]  10  11  12   4   5
   */

```

In this case, 3 elements were copied and they fit into one row which is 5 elements long (according to the configuration of the receiving array). The memory for the remaining two elements of the series was allocated, but not filled (contains "garbage").

We can overwrite the array dynamic2Dx5 from another source, including from a multidimensional array of a different configuration. Since two rows of 5 elements each were allocated in the receiving array, and 2 rows of 4 elements each were allocated in the source array, 2 additional elements were left unfilled.

```
   PRTS(ArrayCopy(dynamic2Dx5, fixed)); // 8 / status:0
   ArrayPrint(dynamic2Dx5);
   /*
       [,0][,1][,2][,3][,4]
   [0,]   1   2   3   4   5
   [1,]   6   7   8   0   0
   */

```

By using ArrayCopy it is possible to change elements in fixed receiver arrays.

```
   PRTS(ArrayCopy(fixed, insert)); // 3 / status:0
   ArrayPrint(fixed);
   /*
       [,0][,1][,2][,3]
   [0,]  10  11  12   4
   [1,]   5   6   7   8
   */

```

Here we have overwritten the first three elements of the array fixed. And then let's overwrite the last 3.

```
   PRTS(ArrayCopy(fixed, insert, 5)); // 3 / status:0
   ArrayPrint(fixed);
   /*
       [,0][,1][,2][,3]
   [0,]  10  11  12   4
   [1,]   5  10  11  12
   */

```

Copying to a position equal to the length of the fixed array will not work (the dynamic destination array would expand in this case).

```
   PRTS(ArrayCopy(fixed, insert, 8)); // 4006, ERR_INVALID_ARRAY
   ArrayPrint(fixed); // no changes

```

String arrays combined with arrays of other types will throw an error:

```
   PRTS(ArrayCopy(texts, insert)); // 5050, ERR_INCOMPATIBLE_ARRAYS
   ArrayPrint(texts); // empty

```

But between string arrays, copying is possible:

```
   PRTS(ArrayCopy(texts, message));
   ArrayPrint(texts); // "ok"

```

Arrays of different numeric types are copied with the necessary conversion.

```
   PRTS(ArrayCopy(insert, array, 1)); // 1 / status:0
   ArrayPrint(insert); // 10  3 12

```

Here we have written the number Pi in an integer array, and therefore received the value 3 (it replaced 11).

bool ArrayRemove(void &array[], uint start, uint count = WHOLE_ARRAY)

The function removes the specified number of elements from the array starting from the index start. An array can be multidimensional and have any built-in or structure type with fields of built-in types, with the exception of strings.

The index start and quantity count refer to the first dimension of the arrays. In other words, for multidimensional arrays, deletion is performed not by individual elements, but by the entire configuration described by "higher" dimensions. For example, for a two-dimensional array, the value 1 in the parameter count means deleting a whole series of length equal to the second dimension (see the example).

The value start must be between 0 and the size of the first dimension minus 1.

The function cannot be applied to arrays with time series (built-in [timeseries](/en/book/applications/timeseries) or [indicator buffers](/en/book/applications/indicators_make/indicators_setindexbuffer)).

To test the function, we prepared the script ArrayRemove.mq5. In particular, it defines 2 structures:

```
struct Simple
{
   int x;
};
   
struct NotSoSimple
{
   int x;
   string s; // a field of type string causes the compiler to make an implicit destructor
};

```

Arrays with a simple structure can be processed by the function ArrayRemove successfully, while arrays of objects with destructors (even with implicit ones, as in NotSoSimple) cause an error:

```
void OnStart()
{
   Simple structs1[10];
   PRTS(ArrayRemove(structs1, 0, 5)); // true / status:0
   
   NotSoSimple structs2[10];
   PRTS(ArrayRemove(structs2, 0, 5)); // false / status:4005,
                                      // ERR_STRUCT_WITHOBJECTS_ORCLASS
   ...

```

Next, arrays of various configurations are defined and initialized.

```
   int dynamic[];
   int dynamic2Dx4[][4];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   
   // make 2 copies
   ArrayCopy(dynamic, fixed);
   ArrayCopy(dynamic2Dx4, fixed);
   
   // show initial data
   ArrayPrint(dynamic);
   /*
   1 2 3 4 5 6 7 8
   */
   ArrayPrint(dynamic2Dx4);
   /*
       [,0][,1][,2][,3]
   [0,]   1   2   3   4
   [1,]   5   6   7   8
   */

```

When deleting from a fixed array, all elements after the fragment being removed are shifted to the left. It is important that the size of the array does not change, and therefore copies of the shifted elements appear in duplicate.

```
   PRTS(ArrayRemove(fixed, 0, 1));
   ArrayPrint(fixed);
   /*
   ArrayRemove(fixed,0,1)=true / status:0
       [,0][,1][,2][,3]
   [0,]   5   6   7   8
   [1,]   5   6   7   8
   */

```

Here we removed one element of the first dimension of a two-dimensional array fixed by offset 0, that is, the initial row. The elements of the next row moved up and remained in the same row.

If we perform the same operation with a dynamic array (identical in content to the array fixed), its size will be automatically reduced by the number of elements removed.

```
   PRTS(ArrayRemove(dynamic2Dx4, 0, 1));
   ArrayPrint(dynamic2Dx4);
   /*
   ArrayRemove(dynamic2Dx4,0,1)=true / status:0
       [,0][,1][,2][,3]
   [0,]   5   6   7   8
   */

```

In a one-dimensional array, each element removed corresponds to a single value. For example, in the array dynamic, when removing three elements starting at index 2, we get the following result:

```
   PRTS(ArrayRemove(dynamic, 2, 3));
   ArrayPrint(dynamic);
   /*
   ArrayRemove(dynamic,2,3)=true / status:0
   1 2 6 7 8
   */

```

The values 3, 4, 5 have been removed, the array size has been reduced by 3.

bool ArrayReverse(void &array[], uint start = 0, uint count = WHOLE_ARRAY)

The function reverses the order of the specified elements in the array. Elements to be reversed are determined by a starting position start and quantity count. If start = 0, and count = WHOLE_ARRAY, the entire array is accessed.

Arrays of arbitrary dimensions and types are supported, both fixed and dynamic (including time series in [indicator buffers](/en/book/applications/indicators_make/indicators_setindexbuffer)). An array can contain objects, pointers, or structures. For multidimensional arrays, only the first dimension is reversed.

The count value must be between 0 and the number of elements in the first dimension. Please note that count less than 2 will not give a noticeable effect, but it can be used to unify loops in algorithms.

The function returns true if successful or false in case of error.

The ArrayReverse.mq5 script can be used to test the function. At its beginning, a class is defined for generating objects stored in an array. The presence of strings and other "complex" fields is not a problem.

```
class Dummy
{
   static int counter;
   int x;
   string s; // a field of type string causes the compiler to create an implicit destructor
public:
   Dummy() { x = counter++; }
};
   
static int Dummy::counter;

```

Objects are identified by a serial number (assigned at the time of creation).

```
void OnStart()
{
   Dummy objects[5];
   Print("Objects before reverse");
   ArrayPrint(objects);
   /*
       [x]  [s]
   [0]   0 null
   [1]   1 null
   [2]   2 null
   [3]   3 null
   [4]   4 null
   */

```

After applying ArrayReverse we get the expected reverse order of the objects.

```
   PRTS(ArrayReverse(objects)); // true / status:0
   Print("Objects after reverse");
   ArrayPrint(objects);
   /*
       [x]  [s]
   [0]   4 null
   [1]   3 null
   [2]   2 null
   [3]   1 null
   [4]   0 null
   */

```

Next, numerical arrays of different configurations are prepared and unfolded with different parameters.

```
   int dynamic[];
   int dynamic2Dx4[][4];
   int fixed[][4] = {{1, 2, 3, 4}, {5, 6, 7, 8}};
   
   ArrayCopy(dynamic, fixed);
   ArrayCopy(dynamic2Dx4, fixed);
   
   PRTS(ArrayReverse(fixed)); // true / status:0
   ArrayPrint(fixed);
   /*
       [,0][,1][,2][,3]
   [0,]   5   6   7   8
   [1,]   1   2   3   4
   */
   
   PRTS(ArrayReverse(dynamic, 4, 3)); // true / status:0
   ArrayPrint(dynamic);
   /*
   1 2 3 4 7 6 5 8
   */
   
   PRTS(ArrayReverse(dynamic, 0, 1)); // does nothing (count = 1)
   PRTS(ArrayReverse(dynamic2Dx4, 2, 1)); // false / status:5052, ERR_SMALL_ARRAY
}

```

In the latter case, the value start (2) exceeds the size in the first dimension, so an error occurs.
