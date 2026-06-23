# Timeseries indexing direction in arrays

Due to the applied trading specifics, MQL5 brings additional features to working with arrays. One of them is that array elements can contain data corresponding to time points. These include for example, arrays with financial instrument quotes, price ticks, and readings of technical indicators. The chronological order of the data means that new elements are constantly added to the end of the array and their indexes increase.

However, from the point of view of trading, it is more convenient to count from the present to the past. Then element 0 always contains the most recent, up-to-date value, element 1 always contains the previous value, and so on.

MQL5 allows you to select and switch the direction of array indexing on the go. An array numbered from the present to the past is called a timeseries. If the indexing increase occurs from the past to the present, this is a regular array. In timeseries, the time decreases with the growth of indices. In ordinary arrays, the time increases, as in real life.

It is important to note that an array does not have to contain time-related values in order to be able to switch the addressing order for it. It's just that this feature is most in demand and, in fact, appeared to work with historical data.

This array attribute does not affect the layout of data in memory. Only the order of numbering changes. In particular, we could implement its analogue in MQL5 ourselves by traversing the array in a "back to front" loop. But MQL5 provides ready-made functions to hide all this routine from application programmers.

Timeseries can be any one-dimensional dynamic array described in an MQL program, as well as external arrays passed to the MQL program from the MetaTrader 5 core, such as parameters of utility functions. For example, a special type of MQL programs, [indicators](/en/book/applications/indicators_make) receives arrays with price data of the current chart in the [OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate) event handler. We will study all the features of the applied use of timeseries later, in the fifth Part of the book.

Arrays defined in an MQL program are not timeseries by default.

Let's consider a set of functions for determining and changing the "series" attribute of an array, as well as its "belonging" to the terminal. The general ArrayAsSeries.mq5 script with examples will be given after the description.

bool ArrayIsSeries(const void &array[])

The function returns a sign of whether the specified array is a "real" timeseries, i.e., it is controlled and provided by the terminal itself. You cannot change this characteristic of an array. Such arrays are available to the MQL program in the "read-only" mode.

In the MQL5 documentation, the terms "timeseries" and "series" are used to describe both the reverse indexing of an array and the fact that the array can "belong" to the terminal (the terminal allocates memory for it and fills it with data). In the book, we will try to avoid this ambiguity and refer to arrays with reverse indexing as "timeseries". And the terminal arrays will be just terminal's own arrays.

You can change the indexing of any custom array of the terminal at your discretion by switching it to the timeseries mode or back to the standard one. This is done using the function ArraySetAsSeries, which is applicable not only to own, but also to custom dynamic arrays (see below).

bool ArrayGetAsSeries(const void &array[])

The function returns a sign of whether the timeseries indexing mode is enabled for the specified array, that is, indexing increases in the direction from the present to the past. You can change the indexing direction using the ArraySetAsSeries function.

The direction of indexing affects values returned by the functions ArrayBsearch, ArrayMaximum, and ArrayMinimum (see section [Comparing, sorting and searching in arrays](/en/book/common/arrays/arrays_compare_sort_search)).

bool ArraySetAsSeries(const void &array[], bool as_series)

The function sets the indexing direction in the array according to the as_series parameter: the true value means the reverse order of indexing, while false means the normal order of elements.

The function returns true on successful attribute setting, or false in case of an error.

Arrays of any type are supported, but changing the direction of indexing is prohibited for multidimensional and fixed-size arrays.

The ArrayAsSeries.mq5 script describes several small arrays for experiments involving the above functions.

```
#define LIMIT 10
 
template<typename T>
void indexArray(T &array[])
{
   for(int i = 0; i < ArraySize(array); ++i)
   {
      array[i] = (T)(i + 1);
   }
}
 
class Dummy
{
   int data[];
};
 
void OnStart()
{
   double array2D[][2];
   double fixed[LIMIT];
   double dynamic[];
   MqlRates rates[];
   Dummy dummies[];
   
   ArrayResize(dynamic, LIMIT); // allocating memory
   // fill in a couple of arrays with numbers: 1, 2, 3,...
   indexArray(fixed);
   indexArray(dynamic);
   ...

```

We have a two-dimensional array array2D, fixed and dynamic array, all of which are of type double, as well as arrays of structures and class objects. The fixed and dynamic arrays are filled with consecutive integers (using the auxiliary function indexArray) for demonstration purposes. For other array types of arrays, we will only check the applicability of the "series" mode, since the idea of the reversal indexing effect will become clear from the example of filled arrays.

First, make sure none of the arrays are the terminal's own array:

```
   PRTS(ArrayIsSeries(array2D)); // false
   PRTS(ArrayIsSeries(fixed));   // false
   PRTS(ArrayIsSeries(dynamic)); // false
   PRTS(ArrayIsSeries(rates));   // false

```

All ArrayIsSeries calls return false since we defined all arrays in the MQL program. We will see the true value for parameter arrays of the function OnCalculate in indicators (in the fifth Part).

Next, let's check the initial direction of array indexing:

```
   PRTS(ArrayGetAsSeries(array2D)); // false, cannot be true
   PRTS(ArrayGetAsSeries(fixed));   // false
   PRTS(ArrayGetAsSeries(dynamic)); // false
   PRTS(ArrayGetAsSeries(rates));   // false
   PRTS(ArrayGetAsSeries(dummies)); // false

```

And again we will get false everywhere.

Let's output arrays fixed and dynamic to the journal to see the original order of the elements.

```
   ArrayPrint(fixed, 1);
   ArrayPrint(dynamic, 1);
   /*
       1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0 10.0
       1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0 10.0
   */

```

Now we try to change the indexing order:

```
   // error: parameter conversion not allowed
   // PRTS(ArraySetAsSeries(array2D, true));
 
   // warning: cannot be used for static allocated array
   PRTS(ArraySetAsSeries(fixed, true));   // false
 
   // after this everything is standard
   PRTS(ArraySetAsSeries(dynamic, true)); // true
   PRTS(ArraySetAsSeries(rates, true));   // true
   PRTS(ArraySetAsSeries(dummies, true)); // true

```

A statement for the array2D array causes a compilation error and is therefore commented out.

A statement for the fixed array issues a compiler warning that it cannot be applied to an array of constant size. At runtime, all 3 last statements returned success (true). Let's see how the attributes of the arrays have changed:

```
   // attribute checks:
   // first, whether they are native to the terminal
   PRTS(ArrayIsSeries(fixed));            // false
   PRTS(ArrayIsSeries(dynamic));          // false
   PRTS(ArrayIsSeries(rates));            // false
   PRTS(ArrayIsSeries(dummies));          // false
   
   // second, indexing direction
   PRTS(ArrayGetAsSeries(fixed));         // false
   PRTS(ArrayGetAsSeries(dynamic));       // true
   PRTS(ArrayGetAsSeries(rates));         // true
   PRTS(ArrayGetAsSeries(dummies));       // true

```

As expected, the arrays didn't turn into the terminal's own arrays. However, three out of four arrays changed their indexing to timeseries mode, including an array of structures and objects. To demonstrate the result, the fixed and dynamic arrays are again displayed in the log.

```
   ArrayPrint(fixed, 1);    // without changes 
   ArrayPrint(dynamic, 1);  // reverse order
   /*
       1.0  2.0  3.0  4.0  5.0  6.0  7.0  8.0  9.0 10.0
      10.0  9.0  8.0  7.0  6.0  5.0  4.0  3.0  2.0  1.0
   */

```

Since the mode was not applied to the array of constant size, it remained unchanged. The dynamic array is now displayed in reverse order.

If you put the array into reverse indexing mode, resize it, and then return the previous indexing, then the added elements will be inserted at the beginning of the array.
