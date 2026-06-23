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

Example:

```
//--- example for CArrayString::Delete(int)
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
   //--- delete element
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
