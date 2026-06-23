# Moving (swapping) arrays

MQL5 provides the ability to swap the contents of two arrays in a resource-efficient way (without physical allocation of memory and copying data). In some other programming languages, a similar operation is supported not only for arrays, but also for other variables, and is called moving.

bool ArraySwap(void &array1[], void &array2[])

The function swaps the contents of two dynamic arrays of the same type. Arrays of any type are supported. However, the function is not applicable to timeseries arrays and indicator buffers, as well as to any arrays with the const modifier.

For multidimensional arrays, the number of elements in all dimensions except the first must match.

The function returns true if successful or false in case of error.

The main use of the function is to speed up the program by eliminating the physical copying of the array when it is passed to or returned from the function, and it is known that the source array is no longer needed. The fact is that swapping takes place almost instantly since the application data does not move in any way. Instead, there is an exchange of meta-data about arrays stored in service structures that describe dynamic arrays (and this takes only 52 bytes).

Suppose there is a class intended for processing an array by certain algorithms. The same array can be subjected to different operations and therefore it makes sense to keep it as a class member. But then there is a question, how to transfer it to an object? In MQL5, methods (as well as functions in general) allow passing arrays only by reference. Putting aside all kinds of wrapper classes that contain an array and are passed by pointer, the only simple solution seems to be the following: to describe, for example, an array parameter in the class constructor and copy it to the internal array using ArrayCopy. But it is more efficient to use ArraySwap.

```
template<typename T>
class Worker
{
   T array[];
   
public:
   Worker(T &source[])
   {
      // ArrayCopy(array, source); // memory and time consuming 
      ArraySwap(source, array);
   }
   ...
};

```

Since the array array was empty before the swap, after the operation the array used as the source argument will become empty, while array will be filled with input data with little or no overhead.

After the object of the class becomes the "owner" of the array, we can modify it with the required algorithms, for example, through a special method process, which takes the code of the requested algorithm as a parameter. It can be sorting, smoothing, mixing, adding noise and much more. But first, let's try to test the idea on a simple operation of array reversal by the function ArrayReverse (see file ArraySwapSimple.mq5).

```
   bool process(const int mode)
   {
      if(ArraySize(array) == 0) return false;
      switch(mode)
      {
      case -4:
         // example: shuffling
         break;
      case -3:
         // example: logarithm
         break;
      case -2:
         // example: adding noise
         break;
      case -1:
         ArrayReverse(array);
         break;
      ...
      }
      return true;
   }

```

You can provide access to the results of work using two methods: element by element (by overloading the '[]' operator) or by an entire array (again we use ArraySwap in the corresponding method get, but you can also provide a method for copying through ArrayCopy).

```
   T operator[](int i)
   {
      return array[i];
   }
   
   void get(T &result[])
   {
      ArraySwap(array, result);
   }

```

For the purpose of universality, the class is made template. This will allow adapting it in the future for arrays of arbitrary structures, but for now, you can check the inversion of a simple array of the type double:

```
void OnStart()
{
   double data[];
   ArrayResize(data, 3);
   data[0] = 1;
   data[1] = 2;
   data[2] = 3;
   
   PRT(ArraySize(data));        // 3
   Worker<double> simple(data);
   PRT(ArraySize(data));        // 0
   simple.process(-1);  // reversing array
   
   double res[];
   simple.get(res);
   ArrayPrint(res); // 3.00000 2.00000 1.00000
}

```

The task of sorting is more realistic, and for an array of structures, sorting by any field may be required. In the [next section](/en/book/common/arrays/arrays_compare_sort_search) we will study in detail the function ArraySort, which allows you to sort in ascending order an array of any built-in type, but not structures. There we will try to eliminate this "gap", leaving ArraySwap in action.
