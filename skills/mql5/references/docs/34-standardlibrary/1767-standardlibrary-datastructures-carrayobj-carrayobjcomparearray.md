# CompareArray

Compares the array with another one.

```
bool  CompareArray(
   const CArrayObj*  src      // pointer to the source
   ) const

```

Parameters

src

[in] Pointer to an instance of the CArrayObj class used as a source of elements for comparison.

Return Value

true - the arrays are equal - the arrays are not equal.

Example:

```
//--- example for CArrayObj::CompareArray(const CArrayObj*)
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
   //--- fill source array
   //--- . . .
   //--- compare with another array
   int result=array.CompareArray(src);
   //--- delete arrays
   delete src;
   delete array;
  }

```
