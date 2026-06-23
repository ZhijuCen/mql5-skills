# SearchGreat

Searches for an element with a value exceeding the value of the sample in the sorted array.

```
int  SearchGreat(
   float  element      // sample
   ) const

```

Parameters

element

[in]  The sample element to search in the array.

Return Value

The position of the found element - successful, -1 - the element not found.

Example:

```
//--- example for CArrayFloat::SearchGreat(float)
#include <Arrays\ArrayFloat.mqh>
//---
void OnStart()
  {
   CArrayFloat *array=new CArrayFloat;
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
   if(array.SearchGreat(100.0)!=-1) printf("Element found");
   else                             printf("Element not found");
   //--- delete array
   delete array;
  }

```
