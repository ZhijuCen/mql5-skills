# Update

Changes the element at the specified array position.

```
bool  Update(
   int    pos,         // position
   float  element      // value
   )

```

Parameters

pos

[in]  Position of the element in the array to change

element

[in]  New value of the element

Return Value

true - successful, false - cannot change the element.

Example:

```
//--- example for CArrayFloat::Update(int,float)
#include <Arrays\ArrayFloat.mqh>
//---
void OnStart()
  {
   CArrayFloat *array=new CArrayFloat;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- add arrays elements
   //--- . . .
   //--- update element
   if(!array.Update(0,100.0))
     {
      printf("Update error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
