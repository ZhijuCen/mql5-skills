# AssignArray

Compares the array with another one.

```
bool  AssignArray(
   const CArrayObj*  src      // pointer to the source
   )

```

Parameters

src

[in] Pointer to an instance of the CArrayObj class used as a source of elements to copy.

Return Value

true - successful, false - cannot copy the elements.

Note

If the receiver array is not empty when calling AssignArray, then all its elements will be removed; and if the memory management flag is set, the memory used for the deleted elements will be released. The receiver array becomes an exact copy of the source one. Additionally, see [CArrayObj::AddArray(const CArrayObj*)](/en/docs/standardlibrary/datastructures/carrayobj/carrayobjaddarray#addarrayremark).

Example:

```
//--- example for CArrayObj::AssignArray(const CArrayObj*)
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
   //--- assign another array
   if(!array.AssignArray(src))
     {
      printf("Array assigned error");
      delete src;
      delete array;
      return;
     }
   //--- arrays is identical
   //--- delete source array without elements
   delete src;
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
