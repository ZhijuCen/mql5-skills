# Add

Adds an element to the end of the array.

```
bool  Add(
   CObject*  element      // element to add
   )

```

Parameters

element

[in] value of the element to add to the array.

Return Value

true - successful, false - cannot add an element.

Note

Element is not added to the array if an invalid pointer (such as NULL) is passed as a parameter.

Example:

```
//--- example for CArrayObj::Add(CObject*)
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
   //--- add 100 arrays elements
   for(int i=0;i<100;i++)
     {
      if(!array.Add(new CObject))
        {
         printf("Element addition error");
         delete array;
         return;
        }
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
