# Resize

Sets a new (smaller) size of the array.

```
bool  Resize(
   int  size      // size
   )

```

Parameters

size

[in] New size of the array.

Return Value

true - successful, false - there was an attempt to set the size less than zero.

Note

Changing the size of the array allows using the memory optimally. Excessive elements on the right are lost. The memory of the lost elements is released or not depending on the memory management mode.

To reduce fragmentation of memory, change the size of the array is made with a step previously given through the method of Step (int), or 16 (default).

Example:

```
//--- example for CArrayObj::Resize(int)
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
   //--- resize array
   if(!array.Resize(10))
     {
      printf("Resize error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
