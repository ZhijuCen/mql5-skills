# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   CArrayShort*  src,     // pointer to the source
   int            pos      // position
   )

```

Parameters

src

[in]  Pointer to an instance of the CArrayShort class used as a source of elements to insert.

pos

[in]  Position in the array to insert.

Return Value

true - successful, false - cannot insert items.

Example:

```
//--- example for CArrayShort::InsertArray(const CArrayShort*,int)
#include <Arrays\ArrayShort.mqh>
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
   //--- create source array
   CArrayShort *src=new CArrayShort;
   if(src==NULL)
     {
      printf("Object create error");
      delete array;
      return;
     }
   //--- add source arrays elements
   //--- . . .
   //--- insert another array
   if(!array.InsertArray(src,0))
     {
      printf("Array inserting error");
      delete src;
      delete array;
      return;
     }
   //--- delete source array
   delete src;
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
