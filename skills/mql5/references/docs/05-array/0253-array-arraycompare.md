# ArrayCompare

The function returns the result of comparing two arrays of the same type. It can be used to compare arrays of [simple types](/en/docs/basis/types#base_types) or custom structures without [complex objects](/en/docs/basis/types#complex_types), that is the custom structures that do not contain [strings](/en/docs/basis/types/stringconst), [dynamic arrays](/en/docs/basis/types/dynamic_array), classes and other structures with complex objects.

```
int  ArrayCompare(
   const void&  array1[],            // first array
   const void&  array2[],            // second array
   int          start1=0,            // initial offset in the first array
   int          start2=0,            // initial offset in the second array
   int          count=WHOLE_ARRAY    // number of elements for comparison
   );

```

Parameters

array1[]

[in]  First array.

array2[]

[in]  Second array.

start1=0

[in]  The element's initial index in the first array, from which comparison starts. The default start index - 0.

start2=0

[in]  The element's initial index in the second array, from which comparison starts. The default start index - 0.

count=WHOLE_ARRAY

[in]  Number of elements to be compared. All elements of both arrays participate in comparison by default (count=[WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants)).

Return Value

- -1, if array1[] less than array2[]
- 0, if array1[] equal to array2[]
- 1, if array1[] more than array2[]
- -2, if an error occurs due to incompatibility of the types of compared arrays or if start1, start2 or count values lead to falling outside the array.

Note

The function will not return 0 (the arrays will not be considered equal) if the arrays differ in size and count=WHOLE_ARRAY for the case when one array is a faithful subset of another one. In this case, the result of comparing the sizes of that arrays will be returned: -1, if the size of array1[] is less than the size of array2[] , otherwise 1.

Example:

```
//--- global variables 
double   ExtArrayFirst[];
double   ExtArraySecond[];
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- set the array sizes
   if(ArrayResize(ExtArrayFirst,10)!=10)
     {
      Print("ArrayResize() failed for ExtArrayFirst. Error code: ",GetLastError());
      return;
     }
   if(ArrayResize(ExtArraySecond,10)!=10)
     {
      Print("ArrayResize() failed for ExtArraySecond. Error code: ",GetLastError());
      return;
     }
     
//--- fill the arrays with the values of i and j indices in a loop
   int total=ArraySize(ExtArrayFirst);
   for(int i=0, j=total-1; i<total; i++,j--)
     {
      //--- fill the ExtArrayFirst array from left to right
      //--- fill the ExtArraySecond array from right to left
      ExtArrayFirst[i]=i;
      ExtArraySecond[i]=j;
     }
//--- compare the arrays and print the result in the log
   ArrayComparePrint(ExtArrayFirst,ExtArraySecond);
   /*
   Result:
   ExtArrayFirst:
   0.00000 1.00000 2.00000 3.00000 4.00000 5.00000 6.00000 7.00000 8.00000 9.00000
   ExtArraySecond:
   9.00000 8.00000 7.00000 6.00000 5.00000 4.00000 3.00000 2.00000 1.00000 0.00000
   Result ArrayCompare(): ExtArrayFirst is smaller than ExtArraySecond (result = -1)
   */
   
//--- now let's flip the arrays
//--- fill the arrays with the values of i and j indices in a loop
   for(int i=0, j=total-1; i<total; i++,j--)
     {
      //--- fill the ExtArrayFirst array from right to left
      //--- fill the ExtArraySecond array from left to right
      ExtArrayFirst[i]=j;
      ExtArraySecond[i]=i;
     }
//--- compare the arrays and print the result in the log
   ArrayComparePrint(ExtArrayFirst,ExtArraySecond);
   /*
   Result:
   ExtArrayFirst:
   9.00000 8.00000 7.00000 6.00000 5.00000 4.00000 3.00000 2.00000 1.00000 0.00000
   ExtArraySecond:
   0.00000 1.00000 2.00000 3.00000 4.00000 5.00000 6.00000 7.00000 8.00000 9.00000
   Result ArrayCompare(): ExtArrayFirst is larger than ExtArraySecond (result = 1)
   */
   
//--- now let's fill the arrays in one direction
//--- fill the arrays with the values of i index in a loop
   for(int i=0; i<total; i++)
     {
      //--- fill both arrays from left to right
      ExtArrayFirst[i]=i;
      ExtArraySecond[i]=i;
     }
//--- compare the arrays and print the result in the log
   ArrayComparePrint(ExtArrayFirst,ExtArraySecond);
   /*
   Result:
   ExtArrayFirst:
   0.00000 1.00000 2.00000 3.00000 4.00000 5.00000 6.00000 7.00000 8.00000 9.00000
   ExtArraySecond:
   0.00000 1.00000 2.00000 3.00000 4.00000 5.00000 6.00000 7.00000 8.00000 9.00000
   Result ArrayCompare(): ExtArrayFirst and ExtArraySecond are equal (result = 0)
   */
  }
//+------------------------------------------------------------------+
//| Compare and display the result                                   |
//+------------------------------------------------------------------+
void ArrayComparePrint(const double &array1[], const double &array2[])
  {
   //--- print the header and contents of the arrays
   Print("ExtArrayFirst:");
   ArrayPrint(array1);
   Print("ExtArraySecond:");
   ArrayPrint(array2);
   //--- compare the arrays and print the comparison result
   int    res=ArrayCompare(array1,array2);
   string res_str=(res>0 ? "ExtArrayFirst is larger than ExtArraySecond" : res<0 ? "ExtArrayFirst is smaller than ExtArraySecond" : "ExtArrayFirst and ExtArraySecond are equal");
   PrintFormat("Result ArrayCompare(): %s (result = %d)\n",res_str,res);
  }
//+------------------------------------------------------------------+

```
