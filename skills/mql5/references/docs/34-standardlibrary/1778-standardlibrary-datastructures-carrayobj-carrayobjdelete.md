# Delete

Removes the element from the specified array position.

```
bool  Delete(
   int  pos      // position
   )

```

Parameters

pos

[in]  Position of the array element to be removed.

Return Value

true - successful, false - cannot remove the element.

Note

If the memory management is enabled, the memory of deleted elements is deallocated.

Example:

```
//--- example for CArrayObj::Delete(int)
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
   if(!array.Delete(0))
     {
      printf("Delete error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
