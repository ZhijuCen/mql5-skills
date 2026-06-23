# Shutdown

Clears the array with full deallocation of memory for it (but not for its elements).

```
bool  Shutdown()

```

Return Value

true - successful, false - an error occurred.

Note

If memory management is enabled, the memory of deleted elements is deallocated.

Example:

```
//--- example for CArrayObj::Shutdown()
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
   //--- shutdown array
   if(!array.Shutdown())
     {
      printf("Shutdown error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
