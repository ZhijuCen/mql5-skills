# Logging arrays

Printing variables, arrays, and messages about the status of an MQL program to the log is the simplest means for informing the user, debugging, and diagnosing problems. As for the array, we can implement element-wise printing using the Print function which we already know from demo scripts. We will formally describe it a little later, in the section on [interaction with the user](/en/book/common/output).

However, it is more convenient to entrust the whole routine related to iteration over elements and their accurate formatting to the MQL5 environment. The API provides a special ArrayPrint function for this purpose.

We have already seen examples of working with this function in the [Using arrays](/en/book/basis/arrays/arrays_usage) section. Now let's talk about its capabilities in more detail.

void ArrayPrint(const void &array[], uint digits = _Digits, const string separator = NULL,  

   ulong start = 0, ulong count = WHOLE_ARRAY,  

   ulong flags = ARRAYPRINT_HEADER | ARRAYPRINT_INDEX | ARRAYPRINT_LIMIT | ARRAYPRINT_DATE | ARRAYPRINT_SECONDS)

The function logs an array using the specified settings. The array must be one of the built-in types or a simple structure type. A simple structure is a structure with fields of built-in types, with the exception of strings and dynamic arrays. The presence of class objects and pointers in the composition of the structure takes it out of the simple category.

The array must have a dimension of 1 or 2. The formatting automatically adjusts to the array configuration and, if possible, displays it in a visual form (see below). Despite the fact that MQL5 supports arrays with dimensions of up to 4, the function does not display arrays with 3 or more dimensions, because it is difficult to represent them in a "flat" form. This happens without generating errors at the program compilation or execution step.

All parameters except the first one can be omitted, and default values are defined for them.

The digits parameter is used for arrays of real numbers and for numeric fields of structures. It sets the number of displayed characters in the fractional part of numbers. The default value is one of the [predefined chart variables](/en/book/applications/charts/charts_main_properties), namely _Digits which is the number of decimal places in the current chart's symbol price.

The separating character separator is used to designate columns when displaying fields in an array of structures. With the default value (NULL), the function uses a space as a separator.

The start and count parameters set the number of the starting element and the number of elements to be printed, respectively. By default, the function prints the entire array, but the result can be additionally affected by the presence of the ARRAYPRINT_LIMIT flag (see below).

The flags parameter accepts a combination of flags that control various display features. Here are some of them:

- ARRAYPRINT_HEADER outputs the header with the names of the fields of the structure before the array of structures; it does not affect arrays of non-structures.
- ARRAYPRINT_INDEX outputs indexes of elements by dimensions (for one-dimensional arrays, indexes are displayed on the left, for two-dimensional arrays they are displayed on the left and above).
- ARRAYPRINT_LIMIT is used for large arrays, and the output is limited to the first hundred and last hundred records (this limit is enabled by default).
- ARRAYPRINT_DATE is used for values of the datetime type to display the date.
- ARRAYPRINT_MINUTES is used for values of the datetime type to display the time to the nearest minute.
- ARRAYPRINT_SECONDS is used for values of the datetime type to display the time to the nearest second.

Values of the datetime type are output by default in the format ARRAYPRINT_DATE | ARRAYPRINT_SECONDS.

Values of type color are output in hexadecimal format.

Enumeration values are displayed as integers.

The function does not output nested arrays, structures, and pointers to objects. Three dots are displayed instead of those.

The ArrayPrint.mq5 script demonstrates how the function works.

The OnStart function provides definitions of several arrays (one-, two- and three-dimensional), which are output using ArrayPrint (with default settings).

```
void OnStart()
{
   int array1D[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
   double array2D[][5] = {{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}};
   double array3D[][3][5] =
   {
      {{ 1,  2,  3,  4,  5}, { 6,  7,  8,  9, 10}, {11, 12, 13, 14, 15}},
      {{16, 17, 18, 19, 20}, {21, 22, 23, 24, 25}, {26, 27, 28, 29, 30}},
   };
   
   Print("array1D");
   ArrayPrint(array1D);
   Print("array2D");
   ArrayPrint(array2D);
   Print("array3D");
   ArrayPrint(array3D);
   ...
}

```

We will get the following lines in the log:

```
array1D
 1  2  3  4  5  6  7  8  9 10
array2D
         [,0]     [,1]     [,2]     [,3]     [,4]
[0,]  1.00000  2.00000  3.00000  4.00000  5.00000
[1,]  6.00000  7.00000  8.00000  9.00000 10.00000
array3D

```

The array1D array is not large enough (it fits in one row), so indexes are not shown for it.

The array2D array has multiple rows (indexes), and therefore their indexes are displayed (ARRAYPRINT_INDEX is enabled by default).

Please note that since the script was run on the EURUSD chart with five-digit prices, _Digits=5, which affects the formatting of values of type double.

The array3D array is ignored: no rows were output for it.

Additionally, the Pair and SimpleStruct structures are defined in the script:

```
struct Pair
{
   int x, y;
};
   
struct SimpleStruct
{
   double value;
   datetime time;
   int count;
   ENUM_APPLIED_PRICE price;
   color clr;
   string details;
   void *ptr;
   Pair pair;
};

```

SimpleStruct contains fields of built-in types, a pointer to void, as well as a field of type Pair.

In the OnStart function, an array of type SimpleStruct is created and output using ArrayPrint in two modes: with default settings and with custom ones (the number of digits after the "comma" is 3, the separator is ";", the format for datetime is date only).

```
void OnStart()
{
   ...
   SimpleStruct simple[] =
   {
      { 12.57839, D'2021.07.23 11:15', 22345, PRICE_MEDIAN, clrBlue, "text message"},
      {135.82949, D'2021.06.20 23:45', 8569, PRICE_TYPICAL, clrAzure},
      { 1087.576, D'2021.05.15 10:01:30', -3298, PRICE_WEIGHTED, clrYellow, "note"},
   };
   Print("SimpleStruct (default)");
   ArrayPrint(simple);
   
   Print("SimpleStruct (custom)");
   ArrayPrint(simple, 3, ";", 0, WHOLE_ARRAY, ARRAYPRINT_DATE);
}

```

This produces the following result:

```
SimpleStruct (default)
       [value]              [time] [count] [type]    [clr]      [details] [ptr] [pair]
[0]   12.57839 2021.07.23 11:15:00   22345      5 00FF0000 "text message"   ...    ...
[1]  135.82949 2021.06.20 23:45:00    8569      6 00FFFFF0 null             ...    ...
[2] 1087.57600 2021.05.15 10:01:30   -3298      7 0000FFFF "note"           ...    ...
SimpleStruct (custom)
  12.578;2021.07.23;  22345;     5;00FF0000;"text message";  ...;   ...
 135.829;2021.06.20;   8569;     6;00FFFFF0;null          ;  ...;   ...
1087.576;2021.05.15;  -3298;     7;0000FFFF;"note"        ;  ...;   ...

```

Please note that the log that we use in this case and in the previous sections is generated in the terminal and is available to the user in the tab Experts of the Toolbox window. However, in the future we will get acquainted with the tester, which provides the same execution environment for certain types of MQL programs (indicators and Expert Advisors) as the terminal itself. If they are launched in the tester, the ArrayPrint function and other related functions, which are described in the section [User interaction](/en/book/common/output), will output messages to the log of [testing agents](/en/book/automation/tester).  

   

Until now, we have worked, and will continue to work for some time, only with scripts, and they can only be executed in the terminal.
