# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   CArrayLong*  src,     // pointer to the source
   int           pos      // position
   )

```

Parameters

src

[in]  Pointer to an instance of the CArrayLong class used as a source of elements to insert.

pos

[in]  Position in the array to insert

Return Value

true - successful, false - cannot insert items.

Example:

```
//--- example for CArrayLong::InsertArray(const CArrayLong*,int)
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
   //--- create source array
   CArrayLong *src=new CArrayLong;
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
