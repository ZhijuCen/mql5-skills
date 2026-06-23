# InsertSort

Inserts an element in a sorted array.

```
bool  InsertSort(
   short  element      // element to insert
   )

```

Parameters

element

[in]  Value of the element to be inserted into a sorted array

Return Value

true - successful, false - cannot insert the element.

Example:

```
//--- example for CArrayShort::InsertSort(short)
#include <Arrays\ArrayShort.mqh>
//---
void OnStart()
  {
   CArrayShort *array=new CArrayShort;
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
   if(!array.InsertSort(100))
     {
      printf("Insert error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
