# AddArray

Adds elements of one array to the end of another.

```
bool  AddArray(
   const long&  src[]      // source array
   )

```

Parameters

src[]

[in]  Reference to an array of source elements to add.

Return Value

true - successful, false - cannot add items.

Example:

```
//--- example for CArrayLong::AddArray(const long &[])
#include <Arrays\ArrayLong.mqh>
//---
long src[];
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
   //--- add another array
   if(!array.AddArray(src))
     {
      printf("Array addition error");
      delete array;
      return;
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
