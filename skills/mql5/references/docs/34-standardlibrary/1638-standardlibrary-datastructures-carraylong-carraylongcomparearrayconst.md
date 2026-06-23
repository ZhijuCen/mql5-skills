# CompareArrayconst

Compares the array with another one.

```
bool  CompareArrayconst(
   const CArrayLong*  src      // pointer to the source
   ) const

```

Parameters

src

[in]  Pointer to an instance of the CArrayLong class used as a source of elements for comparison.

Return Value

true - arrays are equal, false - arrays are not equal.

Example:

```
//--- example for CArrayLong::CompareArray(const CArrayLong*)
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
   //--- compare with another array
   int result=array.CompareArray(src);
   //--- delete arrays
   delete src;
   delete array;
  }

```
