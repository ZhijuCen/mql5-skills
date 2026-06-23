# Variables

### Declaring Variables

Variables must be declared before they are used. Unique names are used to identify variables. To declare a variable, you must specify its type and a unique name. Declaration of variable is not an operator.

Simple types are:

- char, short, int, long, uchar, ushort, uint, ulong – integers;

- color – integer representing the RGB-color;
- datetime – the date and time, an unsigned integer containing the number of seconds since 0 hour January 1, 1970;

- bool – boolean values true and false;
- double – double-precision floating point number;
- float – single-precision floating point number;
- string – character strings.

Examples:

```
string szInfoBox;
int    nOrders;
double dSymbolPrice;
bool   bLog;
datetime tBegin_Data   = D'2004.01.01 00:00';
color    cModify_Color = C'0x44,0xB9,0xE6';

```

Complex or compound types:

Structures are composite data types, constructed using other types.

```
struct MyTime
  {
   int hour;    // 0-23
   int minute;  // 0-59
   int second;  // 0-59
  };
...
MyTime strTime; // Variable of the previously declared structure MyTime

```

You can't declare variables of the structure type until you declare the structure.

Arrays

Array  is the indexed sequence of identical-type data:

```
int    a[50];       // One-dimensional array of 50 integers.
double m[7][50];    // Two-dimensional array of seven arrays,
                    // each of them consisting of 50 numbers.
MyTime t[100];      // Array containing elements such as MyTime

```

Only an integer can be an array index. No more than four-dimensional arrays are allowed. Numbering of array elements starts with 0. The last element of a one-dimensional array has the number which is 1 less than the array size. This means that call for the last element of an array consisting of 50 integers will appear as a[49]. The same concerns multidimensional arrays: A dimension is indexed from 0 to the dimension size-1. The last element of a two-dimensional array from the example will appear as m[6][49].

Static arrays can't be represented as timeseries, i.e., the [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function, which sets access to array elements from the end to beginning, can't be applied to them. If you want to provide access to an array the same as in [timeseries](/en/docs/series), use the [dynamic array object](/en/docs/basis/types/dynamic_array).

If there is an attempt to access out of the array range, the executing subsystem will generate a critical error and the program will be stopped.

### Built-in methods for working with arrays  #

The functions from the [Array Functions](/en/docs/array) section, as well as the built-in methods can be used to handle the arrays:

| Method | Analog | Description |
| --- | --- | --- |
| void array. Fill (const scalar value, const int start_pos=0, const int count=-1); | ArrayFill ,  ArrayInitialize | Fills the array with the specified value |
| void array. Free (); | ArrayFree | Releases the dynamic array buffer and sets the zero dimension size to 0 (zero) |
| int array. Resize (const int range0_size, const int reserve); 
 int array. Resize (const int range_sizes[], const int reserve); | ArrayResize | Sets a new size in the array first dimension |
| int array. Print (); | ArrayPrint | Displays simple type array values in the journal |
| int array. Size (const int range=-1); | ArraySize ,  ArrayRange | Returns the number of elements in the entire array (range=-1) or in the specified array dimension |
| bool array. IsDynamic (); | ArrayIsDynamic | Checks if the array is dynamic |
| bool array. IsIndicatorBuffer (); |  | Checks if the array is an indicator buffer |
| bool array. IsSeries (); | ArrayIsSeries | Checks if the array is a timeseries |
| bool array. AsSeries (); | ArrayGetAsSeries | Checks the array indexing direction |
| bool array. AsSeries (const bool as_series); | ArraySetAsSeries | Sets the indexing direction in the array |
| int array. Copy (const src_array[], const int dst_start, const int src_start, const int cnt); | ArrayCopy | Copies array values to another array |
| int array. Compare (const src_array[], const int dst_start, const int src_start, const int cnt); | ArrayCompare | Returns the result of comparing two simple type arrays or custom structures |
| int array. Insert (const src_array[], const int dst_start, const int src_start, const int cnt); | ArrayInsert | Inserts the specified number of elements from a source array to a receiving one starting from a specified index |
| int array. Remove (const int start_pos, const int count); | ArrayRemove | Removes the specified number of elements from the array starting with a specified index |
| int array. Reverse (const int start_pos, const int count); | ArrayReverse | Reverses the specified number of elements in the array starting with a specified index |
| bool array. Swap (array& arr[]); | ArraySwap | Exchanges the content with another dynamic array of the same type |
| void array. Sort (sort_function); | ArraySort | Sorts numeric arrays by the first dimension |
| int array. Search (scalar value, search_function); | ArrayBsearch | Returns the index of the first element detected in the array first dimension |
| int array. Find ((scalar value, search_function); |  | Performs a search in the array using the passed function and returns the index of the first detected element |
| array array. Select (scalar value, search_function); |  | Performs a search in the array using the passed function and returns the array with all detected elements |

### Access Specifiers

Access specifiers define how the compiler can access variables, members of structures or classes.

The const specifier declares a variable as a constant, and does not allow to change this variable during runtime. A single initialization of a variable is allowed when declaring it.

Example:

```
int OnCalculate (const int rates_total,      // size of the price[] array
                 const int prev_calculated,  // bars handled on a previous call
                 const int begin,            // where the significant data start from
                 const double& price[]       // array to calculate
   );

```

To access members of structures and classes use the following qualifiers:

- [public](/en/docs/basis/types/classes#public) – allows unrestricted access to the variable or class method
- [protected](/en/docs/basis/oop/inheritance) – allows access from methods of this class, as well as from methods of [publicly inherited](/en/docs/basis/oop/inheritance#public_inheritance) classes. Other access is impossible;
- private – allows access to variables and class methods only from methods of the same class.
- [virtual](/en/docs/basis/oop/virtual) – applies only to class methods (but not to methods of structures) and tells the compiler that this method should be placed in the table of virtual functions of the class.

### Storage Classes

There are three storage classes: [static](/en/docs/basis/variables/static), [input](/en/docs/basis/variables/inputvariables) and [extern](/en/docs/basis/variables/externvariables). These modifiers of a storage class explicitly indicate to the compiler that corresponding variables are distributed in a pre-allocated area of memory, which is called the global pool. Besides, these modifiers indicate the special processing of variable data. If a variable declared on a local level is not a [static](/en/docs/basis/variables/static) one, memory for such a variable is allocated automatically at a program stack. Freeing of memory allocated for a non-static array is also performed automatically when going beyond the visibility area of the block, in which the array is declared.

See also

[Data Types](/en/docs/basis/types), [Encapsulation and Extensibility of Types](/en/docs/basis/oop/incapsulation),[Initialization of Variables](/en/docs/basis/variables/initialization), [Visibility Scope and Lifetime of Variables](/en/docs/basis/variables/variable_scope), [Creating and Deleting Objects](/en/docs/basis/variables/object_live), [Static Members of a Class](/en/docs/basis/oop/staticmembers#const)
