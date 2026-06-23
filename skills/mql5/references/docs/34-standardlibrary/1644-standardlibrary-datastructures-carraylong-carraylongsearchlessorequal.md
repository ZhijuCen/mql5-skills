# SearchLessOrEqual

Searches for an element with a value less than or equal to the value of the sample in the sorted array.

```
int  SearchLessOrEqual(
   long  element      // sample
   ) const

```

Parameters

element

[in]  The sample element to search in the array.

Return Value

The position of the found element - successful, -1 - the element not found.

Example:

```
//--- example for CArrayLong::SearchLessOrEqual(long)
#include <Arrays\ArrayLong.mqh>
//---
void OnStart()
  {
   CArrayLong *array=new CArrayLong;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- add arrays elements
   //--- . . .
   //--- sort array
   array.Sort();
   //--- search element
   if(array.SearchLessOrEqual(1000000)!=-1) printf("Element found");
   else                                     printf("Element not found");
   //--- delete array
   delete array;
  }

```
