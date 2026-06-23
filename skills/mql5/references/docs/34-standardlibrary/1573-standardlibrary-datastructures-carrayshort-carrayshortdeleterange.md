# DeleteRange

Deletes a group of elements from the specified array position.

```
bool  DeleteRange(
   int  from,     // position of the first element
   int  to        // position of the last element
   )

```

Parameters

from

[in]   Position of the first array element to be removed.

to

[in]  Position of the last array element to be removed.

Return Value

true - successful, false - cannot remove the elements.

Example:

```
//--- example for CArrayShort::DeleteRange(int,int)
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
   //--- delete elements
   if(!array.DeleteRange(0,10))
     {
      printf("Delete error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
