# Dynamic arrays

Dynamic arrays can change their size during program execution at the request of the programmer. Let's remember that to describe a dynamic array, you should leave the first pair of brackets after the array identifier empty. MQL5 requires that all subsequent dimensions (if there are more than one) must have a fixed size specified with a constant.

It is impossible to dynamically increase the number of elements for any dimension "older" than the first one. In addition, due to the strict size description, arrays have a "square" shape, i.e., for example, it is impossible to construct a two-dimensional array with columns or rows of different lengths. If any of these restrictions are critical for the implementation of the algorithm, you should use not standard MQL5 arrays, but your own structures or classes written in MQL5.

Note that if an array does not have a size in the first dimension, but does have an initialization list that allows you to determine the size, then such an array is a fixed-size array, not a dynamic one.

For example, in the previous section, we used the array1D array:

```
int array1D[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

```

Because of the initialization list, its size is known to the compiler, and therefore the array is fixed.

Unlike this simple example, it is not always easy to determine whether a particular array in a real program is dynamic. In particular, an array can be passed as a parameter into a function. However, it may be important to know if an array is dynamic because memory can be manually allocated by calling ArrayResize only for such arrays.

In such cases, the ArrayIsDynamic function allows you to determine the type of the array.

Let's consider some technical descriptions of functions for working with dynamic arrays and then test them using the ArrayDynamic.mq5 script.

bool ArrayIsDynamic(const void &array[])

The function checks if the passed array is dynamic. An array can be of any allowed dimension from 1 to 4. Array elements can be of any type.

The function returns true for a dynamic array, or false in other cases (fixed array, or array with [timeseries](/en/book/applications/timeseries), controlled by the terminal itself or by the indicator).

int ArrayResize(void &array[], int size, int reserve = 0)

The function sets the new size in the first dimension of the dynamic array. An array can be of any allowed dimension from 1 to 4. Array elements can be of any type.

If the reserve parameter is greater than zero, memory is allocated for the array with a reserve for the specified number of elements. This makes can increase the speed of the program which has many consecutive function calls. Until the new requested size of the array exceeds the current one taking into account the reserve, there will be no physical memory reallocation and new elements will be taken from the reserve.

The function returns the new size of the array if its modification was successful, or -1 in case of an error.

If the function is applied to a fixed array or timeseries, its size does not change. In these cases, if the requested size is less than or equal to the current size of the array, the function will return the value of the size parameter, otherwise, it will return -1.

When increasing the size of an already existing array, all the data of its elements is preserved. The added elements are not initialized with anything and may contain arbitrary incorrect data ("garbage").

Setting the array size to 0, ArrayResize(array, 0), does not release the memory actually allocated for it, including a possible reserve. Such a call will only reset the metadata for the array. This is done for the purpose of optimizing future operations with the array. To force memory release, use ArrayFree (see below).

It is important to understand that the reserve parameter is not used every time the function is called, but only at those moments when the reallocation of memory is actually performed, i.e., when the requested size exceeds the current capacity of the array including the reserve. To visually show how this works, we will create an incomplete copy of the internal array object and implement the twin function ArrayResize for it, and also the analogs ArrayFree and ArraySize, to have a complete toolkit.

```
template<typename T>
struct DynArray
{
   int size;
   int capacity;
   T memory[];
};
 
template<typename T>
int DynArraySize(DynArray<T> &array)
{
   return array.size;
}
 
template<typename T>
void DynArrayFree(DynArray<T> &array)
{
   ArrayFree(array.memory);
   ZeroMemory(array);
}
 
template<typename T>
int DynArrayResize(DynArray<T> &array, int size, int reserve = 0)
{
   if(size > array.capacity)
   {
      static int temp;
      temp = array.capacity;
      long ul = (long)GetMicrosecondCount();
      array.capacity = ArrayResize(array.memory, size + reserve);
      array.size = MathMin(size, array.capacity);
      ul -= (long)GetMicrosecondCount();
      PrintFormat("Reallocation: [%d] -> [%d], done in %d µs", 
         temp, array.capacity, -ul);
   }
   else
   {
      array.size = size;
   }
   return array.size;
}

```

An advantage of the DynArrayResize function compared to the built-in ArrayResize is in that that here we insert a debug printing for those situations when the internal capacity of the array is reallocated.

Now we can take the standard example for the ArrayResize function from the MQL5 documentation and replace the built-in function calls with "self-made" analogs with the "Dyn" prefix. The modified result is presented in the script ArrayCapacity.mq5.

```
void OnStart()
{
   ulong start = GetTickCount();
   ulong now;
   int   count = 0;
   
   DynArray<double> a;
   
 // fast option with memory reservation
   Print("--- Test Fast: ArrayResize(arr,100000,100000)");
   
   DynArrayResize(a, 100000, 100000);
   
   for(int i = 1; i <= 300000 && !IsStopped(); i++)
   {
 // set the new size and reserve to 100000 elements
      DynArrayResize(a, i, 100000);
 // on "round" iterations, show the size of the array and the elapsed time
      if(DynArraySize(a) % 100000 == 0)
      {
         now = GetTickCount();
         count++;
         PrintFormat("%d. ArraySize(arr)=%d Time=%d ms", 
            count, DynArraySize(a), (now - start));
         start = now;
      }
   }
   DynArrayFree(a);
   
 // now this is a slow option without redundancy (with less redundancy)
   count = 0;
   start = GetTickCount();
   Print("---- Test Slow: ArrayResize(slow,100000)");
   
   DynArrayResize(a, 100000, 100000);
   
   for(int i = 1; i <= 300000 && !IsStopped(); i++)
   {
 // set new size but with 100 times smaller margin: 1000
      DynArrayResize(a, i, 1000);
 // on "round" iterations, show the size of the array and the elapsed time
      if(DynArraySize(a) % 100000 == 0)
      {
         now = GetTickCount();
         count++;
         PrintFormat("%d. ArraySize(arr)=%d Time=%d ms", 
            count, DynArraySize(a), (now - start));
         start = now;
      }
   }
}

```

The only significant difference is the following: in the slow version, the call ArrayResize(a, i) is replaced by a more moderate one DynArrayResize(a, i, 1000), that is, the redistribution is requested not at every iteration, but at every 1000th (otherwise the log will be overfilled with messages).

After running the script, we will see the following timing in the log (absolute time intervals depend on your computer, but we are interested in the difference between performance variants with and without the reserve):

```
--- Test Fast: ArrayResize(arr,100000,100000)
Reallocation: [0] -> [200000], done in 17 µs
1. ArraySize(arr)=100000 Time=0 ms
2. ArraySize(arr)=200000 Time=0 ms
Reallocation: [200000] -> [300001], done in 2296 µs
3. ArraySize(arr)=300000 Time=0 ms
---- Test Slow: ArrayResize(slow,100000)
Reallocation: [0] -> [200000], done in 21 µs
1. ArraySize(arr)=100000 Time=0 ms
2. ArraySize(arr)=200000 Time=0 ms
Reallocation: [200000] -> [201001], done in 1838 µs
Reallocation: [201001] -> [202002], done in 1994 µs
Reallocation: [202002] -> [203003], done in 1677 µs
Reallocation: [203003] -> [204004], done in 1983 µs
Reallocation: [204004] -> [205005], done in 1637 µs
...
Reallocation: [295095] -> [296096], done in 2921 µs
Reallocation: [296096] -> [297097], done in 2189 µs
Reallocation: [297097] -> [298098], done in 2152 µs
Reallocation: [298098] -> [299099], done in 2767 µs
Reallocation: [299099] -> [300100], done in 2115 µs
3. ArraySize(arr)=300000 Time=219 ms

```

The time gain is significant. In addition, we see at which iterations and how the real capacity of the array (reserve) is changed.

void ArrayFree(void &array[])

The function releases all the memory of the passed dynamic array (including the possible reserve set using the third parameter of the function ArrayResize) and sets the size of its first dimension to zero.

In theory, arrays in MQL5 release memory automatically when the execution of the algorithm in the current block ends. It doesn't matter if an array is defined locally (within functions) or globally, whether it is fixed or dynamic, as the system will free the memory itself in any case, without requiring explicit actions from the programmer.

Thus, it is not necessary to call this function. However, there are situations when an array is used in an algorithm to re-fill with something from scratch, i.e., it needs to be freed before each filling. Then this feature might come in handy.

Keep in mind that if the array elements contain pointers to dynamically allocated objects, the function does not delete them: the programmer must call delete for them (see below).

Let's test the functions discussed above: ArrayIsDynamic, ArrayResize, ArrayFree.

In the ArrayDynamic.mq5 script, the ArrayExtend function is written, which increases the size of the dynamic array by 1 and writes the passed value to the new element.

```
template<typename T>
void ArrayExtend(T &array[], const T value)
{
   if(ArrayIsDynamic(array))
   {
      const int n = ArraySize(array);
      ArrayResize(array, n + 1);
      array[n] = (T)value;
   }
}

```

The ArrayIsDynamic function is used to make sure that the array is only updated if it is dynamic. This is done in a conditional statement. The ArrayResize function allows you to change the size of the array, and the ArraySize function is used to find out the current size (it will be discussed in the next section).

In the main function of the script, we will apply ArrayExtend for arrays of different categories: dynamic and fixed.

```
void OnStart()
{
   int dynamic[];
   int fixed[10] = {}; // padding with zeros
   
   PRT(ArrayResize(fixed, 0)); // warning: not applicable for fixed array
   
   for(int i = 0; i < 10; ++i)
   {
      ArrayExtend(dynamic, (i + 1) * (i + 1));
      ArrayExtend(fixed, (i + 1) * (i + 1));
   }
   
   Print("Filled");
   ArrayPrint(dynamic);
   ArrayPrint(fixed);
   
   ArrayFree(dynamic);
   ArrayFree(fixed); // warning: not applicable for fixed array
   
   Print("Free Up");
   ArrayPrint(dynamic); // outputs nothing
   ArrayPrint(fixed);
   ...
}

```

In the code lines calling the functions that cannot be used for fixed arrays, the compiler generates a "cannot be used for static allocated array" warning. It is important to note that there are no such warnings inside the ArrayExtend function because an array of any category can be passed to the function. That is why we check this using ArrayIsDynamic.

After a loop in OnStart, the dynamic array will expand to 10 and get the elements equal to the squared indices. The fixed array will remain filled with zeros and will not change size.

Freeing a fixed array with ArrayFree will have no effect, and the dynamic array will actually be deleted. In this case, the last attempt to print it will not produce any lines in the log.

Let's look at the script execution result.

```
   ArrayResize(fixed,0)=0
   Filled   
     1   4   9  16  25  36  49  64  81 100
   0 0 0 0 0 0 0 0 0 0
   Free Up
   0 0 0 0 0 0 0 0 0 0

```

Of particular interest are dynamic arrays with pointers to objects. Let's define a simple dummy class Dummy and create an array of pointers to such objects.

```
class Dummy
{
};
 
void OnStart()
{
   ...
   Dummy *dummies[] = {};
   ArrayExtend(dummies, new Dummy());
   ArrayFree(dummies);
}

```

After extending the dummy array with a new pointer, we free it with ArrayFree, but there are entries in the terminal log indicating that the object was left in memory.

```
1 undeleted objects left
1 object of type Dummy left
24 bytes of leaked memory

```

The fact is that the function manages only the memory that is allocated for the array. In this case, this memory held one pointer, but what it points to does not belong to the array. In other words, if the array contains pointers to "external" objects, then you need to take care of them yourself. For example:

```
for(int i = 0; i < ArraySize(dummies); ++i)
{
   delete dummies[i];
}

```

This deletion must be started before calling ArrayFree.

To shorten the entry, you can use the following macros (loop over elements, call delete for each of them):

```
#define FORALL(A) for(int _iterator_ = 0; _iterator_ < ArraySize(A); ++_iterator_)
#define FREE(P) { if(CheckPointer(P) == POINTER_DYNAMIC) delete (P); }
#define CALLALL(A, CALL) FORALL(A) { CALL(A[_iterator_]) }

```

Then deletion of pointers is simplified to the following notation:

```
   ...
   CALLALL(dummies, FREE);
   ArrayFree(dummies);

```

As an alternative solution, you can use a pointer wrapper class like AutoPtr, which we discussed in the section [Object type templates](/en/book/oop/templates/templates_objects). Then the array should be declared with the type AutoPtr. Since the array will store wrapper objects, not pointers, when the array is cleared, the destructors for each "wrapper" will be automatically called, and the pointer memory will in turn be freed from them.
