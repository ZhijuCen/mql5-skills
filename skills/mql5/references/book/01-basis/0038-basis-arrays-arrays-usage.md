# Using arrays

Values are written to and read from the array elements using a similar syntax and specifying the required indices in square brackets. To put a value into an element, we will use the [assignment operation](/en/book/basis/expressions/operator_assignment) '='. For example, to replace the value of the 0th element of a one-dimensional array:

```
array1D[0] = 11;

```

Indexing starts with 0. The index of the last element is equal to the quantity of elements minus 1. Of course, we can use as an index both a constant and any other expression that can be reduced to the integer type (for more details on expressions, see the [following chapter](/en/book/basis/expressions)), such as an integer variable, a function call, or an element of another array with integers (the indirect addressing).

```
int index;
// ... 
// index = ... // assign an index somehow
// ...
array1D[index] = 11;

```

For multidimensional arrays, indexes must be specified for all dimensions.

```
array2D[index1][index2] = 12;

```

Permitted integer types exclude long and ulong for indices. If we try to use the value of a "long integer" as an index, it will be implicitly converted into int, wherefore the compiler gives the warning "possible loss of data due to type conversion."

Reading access to the array elements is arranged according to the same principle. For example, this is how an array element can be printed in the log:

```
Print(array2D[1][2]);

```

In script GoodTimes, we have already seen the description of the local static array messages with the strings of greetings (inside the Greeting function) and the use of its elements in the return operator.

```
string Greeting() 
{
  static int counter = 0;
  static const string messages[3] = // description
  {
    "Good morning", "Good day", "Good evening" // initialization
  };
  return messages[counter++ % 3];   // using
}

```

When executing return, we read the element that has the index defined by the expression: counter++ % 3. Division modulo 3 (denoted as '%') ensures that counter increased every time increased by 1 will be forced to the range of the correct values of indices: 0, 1, or 2. If there were not modulo divisions, the index of the requested element would exceed the array size, starting from the 4th call of this function. In such cases, the program execution time error occurs ("array out of range"), and it is unloaded from the chart.

MQL5 API includes universal functions for many operations with arrays: Allocating memory (for dynamic arrays), filling, copying, sorting, and searching in arrays are all considered in the section [Working with Arrays](/en/book/common/arrays). However, we are presenting one of them now: [ArrayPrint](/en/book/common/arrays/arrays_print) allows the printing of the array elements in the log in a convenient format (considering dimensions).

Script Arrays.mq5 demonstrates some examples of describing arrays, and the results are printed in the log. We will consider manipulations with the elements of arrays later, upon having studied loops and expressions.

```
void OnStart()
{
  char array[100];      // without initialization
  int array2D[3][2] =
  {
    {1, 2},             // illustrative formatting
    {3, 4},
    {5, 6}
  };
  int array2Dt[2][3] =
  {
    {1, 3, 5},
    {2, 4, 6}
  };
  ENUM_APPLIED_PRICE prices[] =
  {
    PRICE_OPEN, PRICE_HIGH, PRICE_LOW, PRICE_CLOSE
  };
  // double d[5] = {1, 2, 3, 4, 5, 6}; // error: too many initializers
  ArrayPrint(array);    // printing random "garbage" values
  ArrayPrint(array2D);  // showing the 2D array in the log
  ArrayPrint(array2Dt); // a "transposed" appearance of the same data 2D
  ArrayPrint(prices);   // getting to know the values of the price enumeration elements
}

```

One of the log entry options is represented below.

```
[ 0]   0   0   0   0   0   0   0   0   0   0   0   0 -87 105  82 119   0
       0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
[34]   0   0   0 -32  -3  -1  -1   7   0   0   2   0   0   0   0   0   0
       0   2   0   0   0   0   0   0   0 -96 104  82 119   0   0   0   0
[68]   0   0   3   0   0   0   0   0  -1  -1  -1  -1   0   0   0   0 100
      48   0   0   0   0   0   0   0   0   0   0   0   0   0   0
    [,0][,1]
[0,]   1   2
[1,]   3   4
[2,]   5   6
    [,0][,1][,2]
[0,]   1   3   5
[1,]   2   4   6
2 3 4 1

```

The array named array does not have any initialization and therefore, memory allocated for it may contain random values. Values will change at each script run. It is recommended to always initialize local arrays, just in case.

Arrays array2D and array2Dt are printed in the log in an illustrative form, as matrices. It is in no way linked to the fact that we have formatted the initialization lists in the source code in the same manner.

The prices array has the type of the embedded enumeration ENUM_APPLIED_PRICE. Basically, arrays can be of any type, including structures, function pointers, and other things that we are going to consider. Since enumerations are based on the int type, the values are displayed by digits, not by the names of elements (to obtain the name of a specific element of the enumeration, there is the function [EnumToString](/en/book/common/conversions/conversions_enums), but its mode is not supported in [ArrayPrint](/en/book/common/arrays/arrays_print)).

The string with the d array description contains an error: Entity of initial values exceeds the array size.
