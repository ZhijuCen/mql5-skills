# AssignArrayconst

Compares the array with another one.

```
bool  AssignArrayconst(
   const CArrayFloat*  src      // pointer to the source
   ) const

```

Parameters

src

[in]  Pointer to an instance of the CArrayFloat class used as a source of elements for comparison.

Return Value

true - successful, false - cannot copy the items.

Example:

```
//--- example for CArrayFloat::CompareArray(const CArrayFloat*)
#include <Arrays\ArrayFloat.mqh>
//---
void OnStart()
  {
   CArrayFloat *array=new CArrayFloat;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- create source array
   CArrayFloat *src=new CArrayFloat;
   if(src==NULL)
     {
      printf("Object create error");
      delete array;
      return;
     }
   //--- add source arrays elements
   //--- . . .
   //--- compare with another array
   int result=array.CompareArray(src);
   //--- delete arrays
   delete src;
   delete array;
  }

```
