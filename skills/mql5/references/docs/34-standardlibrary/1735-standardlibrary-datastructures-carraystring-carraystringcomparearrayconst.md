# CompareArray

Compares the array with another one.

```
bool  CompareArrays(
   const CArrayString*  src      // pointer to the source
   ) const

```

Parameters

src

[in] Pointer to an instance of the CArrayString class used as a source of elements for comparison.

Return Value

true - successful, false - cannot copy the items.

Example:

```
//--- example for CArrayString::CompareArray(const CArrayString*)
#include <Arrays\ArrayString.mqh>
//---
void OnStart()
  {
   CArrayString *array=new CArrayString;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- create source array
   CArrayString *src=new CArrayString;
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
