# Update

Changes the element at the specified array position.

```
bool  Update(
   int     pos,         // position
   double  element      // value
   )

```

Parameters

pos

[in] Position of the element in the array to change

element

[in]  New value of the element.

Return Value

true - successful, false - cannot change the element.

Example:

```
//--- example for CArrayDouble::Update(int,double)
#include <Arrays\ArrayDouble.mqh>
//---
void OnStart()
  {
   CArrayDouble *array=new CArrayDouble;
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
