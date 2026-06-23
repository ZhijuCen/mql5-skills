# InsertSort

Inserts an element in a sorted array.

```
bool  InsertSort(
   char  element      // element to insert
   )

```

Parameters

element

[in]  Value of the element to be inserted into a sorted array

Return Value

true - successful, false - cannot insert the element.

Example:

```
//--- example for CArrayChar::InsertSort(char)
#include <Arrays\ArrayChar.mqh>
//---
void OnStart()
  {
   CArrayChar *array=new CArrayChar;
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
   if(!array.InsertSort('A'))
     {
      printf("Insert error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
