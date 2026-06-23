# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   CArrayChar*  src,     // pointer to the source
   int           pos     // position
   )

```

Parameters

src

[in]  Pointer to an instance of the CArrayChar class used as a source of elements to insert.

pos

[in]  Position in the array to insert

Return Value

true - successful, false - cannot insert items.

Example:

```
//--- example for CArrayChar::InsertArray(const CArrayChar*,int)
#include <Arrays\ArrayChar.mqh>
//---
void OnStart()
  {
   CArrayChar *array=new CArrayChar;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- create source array
   CArrayChar *src=new CArrayChar;
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
