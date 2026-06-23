# InsertSort

Inserts an element in a sorted array.

```
bool  InsertSort(
   CObject*  element      // element to insert
   )

```

Parameters

element

[in] Value of the element to be inserted into a sorted array

Return Value

true - successful, false - cannot insert the element.

Note

Element is not added to the array if an invalid pointer (such as NULL) is passed as a parameter.

Example:

```
//--- example for CArrayObj::InsertSort(CObject*)
#include <Arrays\ArrayObj.mqh>
//---
void OnStart()
  {
   CArrayObj *array=new CArrayObj;
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
   if(!array.InsertSort(new CObject))
     {
      printf("Insert error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
