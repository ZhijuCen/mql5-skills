# InsertArray

Inserts elements of one array from the specified position of another array.

```
bool  InsertArray(
   const CArrayObj*  src,     // pointer to the source
   int               pos      // position
   )

```

Parameters

src

[in] Pointer to an instance of the CArrayObj class used as a source of elements to insert.

pos

[in] Position in the array to insert

Return Value

true - successful, false - cannot insert items.

Note

See: [CArrayObj::AddArray(const CArrayObj*)](/en/docs/standardlibrary/datastructures/carrayobj/carrayobjaddarray#addarrayremark).

Example:

```
//--- example for CArrayObj::InsertArray(const CArrayObj*,int)
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
   //--- create source array
   CArrayObj *src=new CArrayObj;
   if(src==NULL)
     {
      printf("Object create error");
      delete array;
      return;
     }
   //--- reset free mode flag
   src.FreeMode(false);
   //--- fill source array
   //--- . . .
   //--- insert another array
   if(!array.InsertArray(src,0))
     {
      printf("Array inserting error");
      delete src;
      delete array;
      return;
     }
   //--- delete source array without elements
   delete src;
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
