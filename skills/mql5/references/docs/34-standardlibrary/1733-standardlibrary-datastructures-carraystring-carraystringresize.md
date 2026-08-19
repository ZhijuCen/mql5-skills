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

Changing the size of the array allows using the memory optimally. Excessive elements on the right are lost. To reduce fragmentation of memory, the array size is changed by the step previously determined by the Step(int) method or the default step of 16.

Example:

```
//--- example for CArrayString::Resize(int)
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
