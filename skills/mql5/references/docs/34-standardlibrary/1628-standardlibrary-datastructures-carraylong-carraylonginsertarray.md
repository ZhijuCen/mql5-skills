# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   const long&  src[],     // source array
   int           pos        // position
   )

```

Parameters

src[]

[in]  Reference to an array used as a source of elements to insert

pos

[in]  Position in the array to insert

Return Value

true - successful, false - cannot insert items.

Example:

```
//--- example for CArrayLong::InsertArray(const long &[],int)
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
