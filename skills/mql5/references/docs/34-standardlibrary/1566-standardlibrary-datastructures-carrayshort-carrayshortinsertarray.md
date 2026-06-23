# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   const short&  src[],     // source array
   int            pos        // position
   )

```

Parameters

src[]

[in] Reference to an array used as a source of elements to insert

pos

[in]  Position in the array to insert

Return Value

true - successful, false - cannot insert items.

Example:

```
//--- example for CArrayShort::InsertArray(const short &[],int)
#include <Arrays\ArrayShort.mqh>
//---
short src[];
//---
void OnStart()
  {
   CArrayShort *array=new CArrayShort;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- insert another array
   if(!array.InsertArray(src,0))
     {
      printf("Array inserting error");
      delete array;
      return;
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
