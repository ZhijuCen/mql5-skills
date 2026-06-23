# Update

Changes the element at the specified array position.

```
bool  Update(
   int       pos,         // position
   CObject*  element      // value
   )

```

Parameters

pos

[in] Position of the element in the array to change

element

[in] New value of the element

Return Value

true - successful, false - cannot change the element.

Note

The element will not change if an invalid pointer (for example, NULL) is passed as a parameter. If the memory management is enabled, the memory of a replaced element is deallocated.

Example:

```
//--- example for CArrayObj::Update(int,CObject*)
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
   //--- update element
   if(!array.Update(0,new CObject))
     {
      printf("Update error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
