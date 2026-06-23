# InsertSort

Inserts an element in a sorted array.

```
bool  InsertSort(
   string  element      // element to insert
   )

```

Parameters

element

[in] Value of the element to be inserted into a sorted array

Return Value

true - successful, false - cannot insert the element.

Example:

```
//--- example for CArrayString::InsertSort(string)
#include <Arrays\ArrayString.mqh>
//---
void OnStart()
  {
   CArrayString *array=new CArrayString;
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
   //--- insert element
   if(!array.InsertSort("ABC"))
     {
      printf("Insert error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
