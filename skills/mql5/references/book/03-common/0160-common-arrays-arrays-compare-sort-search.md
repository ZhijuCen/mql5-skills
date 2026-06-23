# Comparing, sorting, and searching in arrays

The MQL5 API contains several functions that allow comparing and sorting arrays, as well as searching for the maximum, minimum, or any specific value in them.

int ArrayCompare(const void &array1[], const void &array2[], int start1 = 0, int start2 = 0, int count = WHOLE_ARRAY)

The function returns the result of comparing two arrays of built-in types or structures with fields of built-in types, excluding strings. Arrays of class objects are not supported. Also, you cannot compare arrays of structures that contain dynamic arrays, class objects, or pointers.

By default, the comparison is performed for entire arrays but, if necessary, you can specify parts of arrays, for which there are parameters start1 (starting position in the first array), start2 (starting position in the second array), and count.

Arrays can be fixed or dynamic, as well as multidimensional. During comparison, multidimensional arrays are represented as equivalent one-dimensional arrays (for example, for two-dimensional arrays, the elements of the second row follow the elements of the first, the elements of the third row follow the second, and so on). For this reason, the parameters start1, start2, and count for multidimensional arrays are specified through element numbering, and not an index along the first dimension.

Using various start1 and start2 offsets you can compare different parts of the same array.

Arrays are compared element by element until the first discrepancy is found or the end of one of the arrays is reached. The relationship between two elements (which are in the same positions in both arrays) depends on the type: for numbers, the operators '>', '<', '==' are used, and for strings, the [StringCompare](/en/book/common/strings/strings_comparison) function is used. Structures are compared byte by byte, which is equivalent to executing the following code for each pair of elements:

```
uchar bytes1[], bytes2[];
StructToCharArray(array1[i], bytes1);
StructToCharArray(array2[i], bytes2);
int cmp = ArrayCompare(bytes1, bytes2);

```

Based on the ratio of the first differing elements, the result of bulk comparison of the arrays array1 and array2 is obtained. If no differences are found, and the length of the arrays is equal, then the arrays are considered the same. If the length is different, then the longer array is considered greater.

The function returns -1 if array1 is "less than" array2, +1 if array1 is "greater than" array2, and 0 if they are "equal".

In case of an error, the result is -2.

Let's look at some examples in the script ArrayCompare.mq5.

Let's create a simple structure for filling the arrays to be compared.

```
struct Dummy
{
   int x;
   int y;
   
   Dummy()
   {
      x = rand() / 10000;
      y = rand() / 5000;
   }
};

```

The class fields are filled with random numbers (each time the script is run, we will receive new values).

In the OnStart function, we describe a small array of structures and compare successive elements with each other (as moving neighboring fragments of an array with the length of 1 element).

```
#define LIMIT 10
 
void OnStart()
{
   Dummy a1[LIMIT];
   ArrayPrint(a1);
   
   // pairwise comparison of neighboring elements
   // -1: [i] < [i + 1]
   // +1: [i] > [i + 1]
   for(int i = 0; i < LIMIT - 1; ++i)
   {
      PRT(ArrayCompare(a1, a1, i, i + 1, 1));
   }
   ...

```

Below are the results for one of the array options (for the convenience of analysis, the column with the signs "greater than" (+1) / "less than" (-1) is added directly to the right of the contents of the array):

```
       [x] [y]   // result
   [0]   0   3   // -1
   [1]   2   4   // +1
   [2]   2   3   // +1
   [3]   1   6   // +1
   [4]   0   6   // -1
   [5]   2   0   // +1
   [6]   0   4   // -1
   [7]   2   5   // +1
   [8]   0   5   // -1
   [9]   3   6

```

Comparing the two halves of the array to each other gives -1:

```
 // compare first and second half
   PRT(ArrayCompare(a1, a1, 0, LIMIT / 2, LIMIT / 2)); // -1

```

Next, we will compare arrays of strings with predefined data.

```
   string s[] = {"abc", "456", "$"};
   string s0[][3] = {{"abc", "456", "$"}};
   string s1[][3] = {{"abc", "456", ""}};
   string s2[][3] = {{"abc", "456"}}; // last element omitted: it is null
   string s3[][2] = {{"abc", "456"}};
   string s4[][2] = {{"aBc", "456"}};
   
   PRT(ArrayCompare(s0, s));  // s0 == s, 1D and 2D arrays contain the same data
   PRT(ArrayCompare(s0, s1)); // s0 > s1 since "$" > ""
   PRT(ArrayCompare(s1, s2)); // s1 > s2 since "" > null
   PRT(ArrayCompare(s2, s3)); // s2 > s3 due to different lengths: [3] > [2]
   PRT(ArrayCompare(s3, s4)); // s3 < s4 since "abc" < "aBc"

```

Finally, let's check the ratio of array fragments:

```
   PRT(ArrayCompare(s0, s1, 1, 1, 1)); // second elements (with index 1) are equal 
   PRT(ArrayCompare(s1, s2, 0, 0, 2)); // the first two elements are equal

```

bool ArraySort(void &array[])

The function sorts a numeric array (including possibly a multidimensional array) by the first dimension. The sorting order is ascending. To sort an array in descending order, apply the [ArrayReverse](/en/book/common/arrays/arrays_edit) function to the resulting array or process it in reverse order.

The function does not support arrays of strings, structures, or classes.

The function returns true if successful or false in case of error.

If the "timeseries" property is set for an array, then the elements in it are indexed in the reverse order (see details in section [Array indexing direction as in timeseries](/en/book/common/arrays/arrays_as_series)), and this has an "external" reversal effect on the sorting order: when you process such an array directly, you will get descending values. At the physical level, the array is always sorted in ascending order, and that is how it is stored.

In the script ArraySort.mq5 a 10 by 3, 2-dimensional array is generated and sorted using ArraySort:

```
#define LIMIT 10
#define SUBLIMIT 3
   
void OnStart()
{
   // generating random data
   int array[][SUBLIMIT];
   ArrayResize(array, LIMIT);
   for(int i = 0; i < LIMIT; ++i)
   {
      for(int j = 0; j < SUBLIMIT; ++j)
      {
         array[i][j] = rand();
      }
   }
   
   Print("Before sort");
   ArrayPrint(array);    // source array
   
   PRTS(ArraySort(array));
   
   Print("After sort");
   ArrayPrint(array);    // ordered array
   ...
}

```

According to the log, the first column is sorted in ascending order (specific numbers will vary due to random generation):

```
Before sort
      [,0]  [,1]  [,2]
[0,]  8955  2836 20011
[1,]  2860  6153 25032
[2,] 16314  4036 20406
[3,] 30366 10462 19364
[4,] 27506  5527 21671
[5,]  4207  7649 28701
[6,]  4838   638 32392
[7,] 29158 18824 13536
[8,] 17869 23835 12323
[9,] 18079  1310 29114
ArraySort(array)=true / status:0
After sort
      [,0]  [,1]  [,2]
[0,]  2860  6153 25032
[1,]  4207  7649 28701
[2,]  4838   638 32392
[3,]  8955  2836 20011
[4,] 16314  4036 20406
[5,] 17869 23835 12323
[6,] 18079  1310 29114
[7,] 27506  5527 21671
[8,] 29158 18824 13536
[9,] 30366 10462 19364

```

The values in the following columns have moved synchronously with the "leading" values in the first column. In other words, the entire rows are permuted, despite the fact that only the first column is the sorting criterion.

But what if you want to sort a two-dimensional array by a column other than the first one? You can write a special algorithm for that. One of the options is included in the file ArraySort.mq5 as a template function:

```
template<typename T>
bool ArraySort(T &array[][], const int column)
{
   if(!ArrayIsDynamic(array)) return false;
   
   if(column == 0)
   {
      return ArraySort(array); // standard function 
   }
   
   const int n = ArrayRange(array, 0);
   const int m = ArrayRange(array, 1);
   
   T temp[][2];
   
   ArrayResize(temp, n);
   for(int i = 0; i < n; ++i)
   {
      temp[i][0] = array[i][column];
      temp[i][1] = i;
   }
   
   if(!ArraySort(temp)) return false;
   
   ArrayResize(array, n * 2);
   for(int i = n; i < n * 2; ++i)
   {
      ArrayCopy(array, array, i * m, (int)(temp[i - n][1] + 0.1) * m, m);
      /* equivalent
      for(int j = 0; j < m; ++j)
      {
         array[i][j] = array[(int)(temp[i - n][1] + 0.1)][j];
      }
      */
   }
   
   return ArrayRemove(array, 0, n);
}

```

The given function only works with dynamic arrays because the size of array is doubled to assemble intermediate results in the second half of the array, and finally, the first half (original) is removed with ArrayRemove. That is why the original test array in the OnStart function was distributed through ArrayResize.

We encourage you to study the sorting principle on your own (or turn over a couple of pages).

Something similar should be implemented for arrays with a large number of dimensions (for example, array[][][]).

Now recall that in the previous section, we raised the issue of sorting an array of structures by an arbitrary field. As we know, the standard ArraySort function is not able to do this. Let's try to come up with a "bypass route". Let's take the class from the ArraySwapSimple.mq5 file from the previous section as a basis. Let's copy it to ArrayWorker.mq5 and add the required code.

In the Worker::process method, we will provide a call to the auxiliary sorting method arrayStructSort, and the field to be sorted will be specified by number (how it can be done, we will describe below):

```
   ...
   bool process(const int mode)
   {
      ...
      switch(mode)
      {
      ...
      case -1:
         ArrayReverse(array);
         break;
      default: // sorting by field number 'mode'
         arrayStructSort(mode);
         break;
      }
      return true;
   }
   
private:
   bool arrayStructSort(const int field)
   {
      ...
   }

```

Now it becomes clear why all the previous modes (values of the mode parameter) in the process method were negative: zero and positive values are reserved for sorting and correspond to the "column" number.

The idea of sorting an array of structures is taken from sorting a two-dimensional array. We only need to somehow map a single structure to a one-dimensional array (representing a row of a two-dimensional array). To do this, firstly, you need to decide what type the array should be.

Since the worker class is already a template, we will add one more parameter to the template so that the array type can be flexibly set.

```
template<typename T, typename R>
class Worker
{
   T array[];
   ...

```

Now, let's get back to [associations](/en/book/oop/structs_and_unions/unions), which allow you to overlay variables of different types on top of each other. Thus, we get the following tricky construction:

```
   union Overlay
   {
      T r;
      R d[sizeof(T) / sizeof(R)];
   };

```

In this union, the type of the structure is combined with an array of type R, and its size is automatically calculated by the compiler based on the ratio of the sizes of two types, T and R.

Now, inside the arrayStructSort method, we can partially duplicate the code of two-dimensional array sorting.

```
   bool arrayStructSort(const int field)
   {
      const int n = ArraySize(array);
      
      R temp[][2];
      Overlay overlay;
      
      ArrayResize(temp, n);
      for(int i = 0; i < n; ++i)
      {
         overlay.r = array[i];
         temp[i][0] = overlay.d[field];
         temp[i][1] = i;
      }
      ...

```

Instead of an array with the original structures, we prepare the temp[][2] array of type R, extend it to the number of records in array, and write the following in the loop: the "display" of the required field field from the structure at the 0th index of each row, and the original index of this element at the 1st index.

The "display" is based on the fact that fields in structures are usually aligned in some way since they use standard types. Therefore, with a properly chosen R type, it is possible to provide full or partial hitting of fields in the array elements in the "overlay".

For example, in the standard structure [MqlRates](/en/book/applications/timeseries/timeseries_mqlrates) the first 6 fields are 8 bytes in size, and therefore map correctly onto the array double or long (these are R template type candidates).

```
struct MqlRates 
{ 
   datetime time; 
   double   open; 
   double   high; 
   double   low; 
   double   close; 
   long     tick_volume; 
   int      spread; 
   long     real_volume; 
};

```

With the last two fields, the situation is more complicated. If the field spread still can be reached using type int as R, then the field real_volume turns out to be at an offset that is not a multiple of its own size (due to the field type int, i.e. 4 bytes, before it). These are problems of a particular method. It can be improved, or another method can be invented.

But let's go back to the sorting algorithm. After the array temp is populated, it can be sorted with the usual function ArraySort, and then the original indexes can be used to form a new array with the correct structure order.

```
      ...
      if(!ArraySort(temp)) return false;
      T result[];
      
      ArrayResize(result, n);
      for(int i = 0; i < n; ++i)
      {
         result[i] = array[(int)(temp[i][1] + 0.1)];
      }
      
      return ArraySwap(result, array);
   }

```

Before exiting the function, we use ArraySwap again, in order to replace the contents of an intra-object array array in a resource-efficient way with something new and ordered, which is received in the local array result.

Let's check the class worker in action: in the function OnStart let's define an array of structures MqlRates and ask the terminal for several thousand records.

```
#define LIMIT 5000
 
void OnStart()
{
   MqlRates rates[];
   int n = CopyRates(_Symbol, _Period, 0, LIMIT, rates);
   ...

```

The CopyRates function will be described in a [separate section](/en/book/applications/timeseries/timeseries_mqlrates). For now, it's enough for us to know that it fills the passed array rates with quotes of the symbol and timeframe of the current chart on which the script is running. The macro LIMIT specifies the number of requested bars: you need to make sure that this value is not greater than your terminal's setting for the number of bars in each window.

To process the received data, we will create an object worker with types T=MqlRates and R=double:

```
Worker<MqlRates, double> worker(rates);

```

Sorting can be started with an instruction of the following form:

```
worker.process(offsetof(MqlRates, open) / sizeof(double));

```

Here we use the [offsetof](/en/book/oop/structs_and_unions/structs_pack_dll) operator to get the byte offset of the field open inside the structure. It is further divided by the size double and gives the correct "column" number for sorting by the open price. You can read the sorting result element by element, or get the entire array:

```
Print(worker[i].open);
...
worker.get(rates);
ArrayPrint(rates);

```

Note that getting an array by the method get moves it out of the inner array array to the outer one (passed as an argument) with ArraySwap. So, after that the calls worker.process() are pointless: there is no more data in the object worker.

To simplify the start of sorting by different fields, an auxiliary function sort has been implemented:

```
void sort(Worker<MqlRates, double> &worker, const int offset, const string title)
{
   Print(title);
   worker.process(offset);
   Print("First struct");
   StructPrint(worker[0]);
   Print("Last struct");
   StructPrint(worker[worker.size() - 1]);
}

```

It outputs a header and the first and last elements of the sorted array to the log. With its help, testing in OnStart for three fields looks like this:

```
void OnStart()
{
   ...
   Worker<MqlRates, double> worker(rates);
   sort(worker, offsetof(MqlRates, open) / sizeof(double), "Sorting by open price...");
   sort(worker, offsetof(MqlRates, tick_volume) / sizeof(double), "Sorting by tick volume...");
   sort(worker, offsetof(MqlRates, time) / sizeof(double), "Sorting by time...");
}

```

Unfortunately, the standard function print does not support printing of single structures, and there is no built-in function StructPrint in MQL5. Therefore, we had to write it ourselves, based on ArrayPrint: in fact, it is enough to put the structure in an array of size 1.

```
template<typename S>
void StructPrint(const S &s)
{
   S temp[1];
   temp[0] = s;
   ArrayPrint(temp);
}

```

As a result of running the script, we can get something like the following (depending on the terminal settings, namely on which symbol/timeframe it is executed):

```
Sorting by open price...
First struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.07.21 10:30:00 1.17557 1.17584 1.17519 1.17561          1073        0             0
Last struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.05.25 15:15:00 1.22641 1.22664 1.22592 1.22618           852        0             0
Sorting by tick volume...
First struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.05.24 00:00:00 1.21776 1.21811 1.21764 1.21794            52       20             0
Last struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.06.16 21:30:00 1.20436 1.20489 1.20149 1.20154          4817        0             0
Sorting by time...
First struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.05.14 16:15:00 1.21305 1.21411 1.21289 1.21333           888        0             0
Last struct
                 [time]  [open]  [high]   [low] [close] [tick_volume] [spread] [real_volume]
[0] 2021.07.27 22:45:00 1.18197 1.18227 1.18191 1.18225           382        0             0

```

Here is the data for EURUSD,M15.

The above implementation of sorting is potentially one of the fastest because it uses the built-in ArraySort.

If, however, the difficulties with aligning the fields of the structure or the skepticism towards the very approach of "mapping" the structure into an array force us to abandon this method (and thus, the function ArraySort), the proven "do-it-yourself" method remains at our disposal.

There are a large number of sorting algorithms that are easy to adapt to MQL5. One of the quick sorting options is presented in the file QuickSortStructT.mqh attached to the book. This is an improved version QuickSortT.mqh, which we used in the section [String comparison](/en/book/common/strings/strings_comparison). It has the method Compare of the template class QuickSortStructT which is made purely virtual and must be redefined in the descendant class to return an analog of the comparison operator '>' for the required type and its fields. For the user convenience, a macro has been created in the header file:

```
#define SORT_STRUCT(T, A, F)                                           \
{                                                                    \
   class InternalSort : public QuickSortStructT<T>                   \
   {                                                                 \
      virtual bool Compare(const T &a, const T &b) override          \
      {                                                              \
         return a.##F > b.##F;                                       \
      }                                                              \
   } sort;                                                           \
   sort.QuickSort(A);                                                \
}

```

Using it, to sort an array of structures by a given field, it is enough to write one instruction. For example:

```
   MqlRates rates[];
   CopyRates(_Symbol, _Period, 0, 10000, rates);
   SORT_STRUCT(MqlRates, rates, high);

```

Here the rates array of type MqlRates is sorted by the high price.

int ArrayBsearch(const type &array[], type value)

The function searches a given value in a numeric array. Arrays of all built-in numeric types are supported. The array must be sorted in ascending order by the first dimension, otherwise the result will be incorrect.

The function returns the index of the matching element (if there are several, then the index of the first of them) or the index of the element closest in value (if there is no exact match), ti.e., it can be an element with either a larger or smaller value than the one being searched for. If the desired value is less than the first (minimum), then 0 is returned. If the searched value is greater than the last (maximum), its index is returned.

The index depends on the direction of the numbering of the elements in the array: direct (from the beginning to the end) or reverse (from the end to the beginning). It can be recognized and changed using the functions described in the section [Array indexing direction as in timeseries](/en/book/common/arrays/arrays_as_series).

If an error occurs, -1 is returned.

For multidimensional arrays, the search is limited to the first dimension.

In the script ArraySearch.mq5 one can find examples of using the function ArrayBsearch.

```
void OnStart()
{
   int array[] = {1, 5, 11, 17, 23, 23, 37};
     // indexes  0  1   2   3   4   5   6
   int data[][2] = {{1, 3}, {3, 2}, {5, 10}, {14, 10}, {21, 8}};
     // indexes     0       1       2         3         4
   int empty[];
   ...

```

For three predefined arrays (one of them is empty), the following statements are executed:

```
   PRTS(ArrayBsearch(array, -1)); // 0
   PRTS(ArrayBsearch(array, 11)); // 2
   PRTS(ArrayBsearch(array, 12)); // 2
   PRTS(ArrayBsearch(array, 15)); // 3
   PRTS(ArrayBsearch(array, 23)); // 4
   PRTS(ArrayBsearch(array, 50)); // 6
   
   PRTS(ArrayBsearch(data, 7));   // 2
   PRTS(ArrayBsearch(data, 9));   // 2
   PRTS(ArrayBsearch(data, 10));  // 3
   PRTS(ArrayBsearch(data, 11));  // 3
   PRTS(ArrayBsearch(data, 14));  // 3
   
   PRTS(ArrayBsearch(empty, 0));  // -1, 5053, ERR_ZEROSIZE_ARRAY
   ...

```

Further, in the populateSortedArray helper function, the numbers array is filled with random values, and the array is constantly maintained in a sorted state using ArrayBsearch.

```
void populateSortedArray(const int limit)
{
   double numbers[];  // array to fill
 doubleelement[1];// new value to insert
   
   ArrayResize(numbers, 0, limit); // allocate memory beforehand
   
   for(int i = 0; i < limit; ++i)
   {
      // generate a random number
      element[0] = NormalizeDouble(rand() * 1.0 / 32767, 3);
      // find where its place in the array
      int cursor = ArrayBsearch(numbers, element[0]);
      if(cursor == -1)
      {
         if(_LastError == 5053) // empty array
         {
            ArrayInsert(numbers, element, 0);
         }
         else break; // error
      }
      else
      if(numbers[cursor] > element[0]) // insert at 'cursor' position 
      {
         ArrayInsert(numbers, element, cursor);
      }
      else // (numbers[cursor] <= value) // insert after 'cursor'
      {
         ArrayInsert(numbers, element, cursor + 1);
      }
   }
   ArrayPrint(numbers, 3);
}

```

Each new value goes first into a one-element array element, because this way it's easier to insert it into the resulting array numbers using the function [ArrayInsert](/en/book/common/arrays/arrays_edit).

ArrayBsearch allows you to determine where the new value should be inserted.

The result of the function is displayed in the log:

```
void OnStart()
{
   ...
   populateSortedArray(80);
   /*
    example (will be different on each run due to randomization)
   [ 0] 0.050 0.065 0.071 0.106 0.119 0.131 0.145 0.148 0.154 0.159
        0.184 0.185 0.200 0.204 0.213 0.216 0.220 0.224 0.236 0.238
   [20] 0.244 0.259 0.267 0.274 0.282 0.293 0.313 0.334 0.346 0.366
        0.386 0.431 0.449 0.461 0.465 0.468 0.520 0.533 0.536 0.541
   [40] 0.597 0.600 0.607 0.612 0.613 0.617 0.621 0.623 0.631 0.634
        0.646 0.658 0.662 0.664 0.670 0.670 0.675 0.686 0.693 0.694
   [60] 0.725 0.739 0.759 0.762 0.768 0.783 0.791 0.791 0.791 0.799
        0.838 0.850 0.854 0.874 0.897 0.912 0.920 0.934 0.944 0.992
   */

```

int ArrayMaximum(const type &array[], int start = 0, int count = WHOLE_ARRAY)

int ArrayMinimum(const type &array[], int start = 0, int count = WHOLE_ARRAY)

The functions ArrayMaximum and ArrayMinimum search a numeric array for the elements with the maximum and minimum values, respectively. The range of indexes for searching is set by start and count parameters: with default values, the entire array is searched.

The function returns the position of the found element.

If the "serial" property ("timeseries") is set for an array, the indexing of elements in it is carried out in the reverse order, and this affects the result of this function (see the example). Built-in functions for working with the "serial" property are discussed in the [next section](/en/book/common/arrays/arrays_as_series). More details about "serial" arrays will be discussed in the chapters on [timeseries](/en/book/applications/timeseries) and [indicators](/en/book/applications/indicators_make).

In multidimensional arrays, the search is performed on the first dimension.

If there are several identical elements in the array with a maximum or minimum value, the function will return the index of the first of them.

An example of using functions is given in the file ArrayMaxMin.mq5.

```
#define LIMIT 10
   
void OnStart()
{
   // generating random data
   int array[];
   ArrayResize(array, LIMIT);
   for(int i = 0; i < LIMIT; ++i)
   {
      array[i] = rand();
   }
   
   ArrayPrint(array);
   // by default, the new array is not a timeseries
   PRTS(ArrayMaximum(array));
   PRTS(ArrayMinimum(array));
   // turn on the "serial" property
   PRTS(ArraySetAsSeries(array, true));
   PRTS(ArrayMaximum(array));
   PRTS(ArrayMinimum(array));
}

```

The script will log something like the following set of strings (due to random data generation, each run will be different):

```
22242 5909 21570 5850 18026 24740 10852 2631 24549 14635
ArrayMaximum(array)=5 / status:0
ArrayMinimum(array)=7 / status:0
ArraySetAsSeries(array,true)=true / status:0
ArrayMaximum(array)=4 / status:0
ArrayMinimum(array)=2 / status:0

```
