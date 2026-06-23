# Shift

Moves an item from a given position in the array to the specified offset.

```
bool  Shift(
   int  pos,       // position
   int  shift      // shift
   )

```

Parameters

pos

[in] Position of the moved element in the array

shift

[in] The shift value (both positive and negative).

Return Value

true - successful, false - cannot move the element.

Example:

```
//--- example for CArrayObj::Shift(int,int)
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
   //--- shift element
   if(!array.Shift(10,-5))
     {
      printf("Shift error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
