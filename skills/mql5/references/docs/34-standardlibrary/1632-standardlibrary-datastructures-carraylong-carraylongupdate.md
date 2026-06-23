# Update

Changes the element at the specified array position.

```
bool  Update(
   int   pos,         // position
   long  element      // value
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
//--- example for CArrayLong::Update(int,long)
#include <Arrays\ArrayLong.mqh>
//---
void OnStart()
  {
   CArrayLong *array=new CArrayLong;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- add arrays elements
   //--- . . .
   //--- update element
   if(!array.Update(0,1000000))
     {
      printf("Update error");
      delete array;
      return;
     }
   //--- delete array
   delete array;
  }

```
