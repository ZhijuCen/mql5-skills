# AssignArray

Copies the elements of one array to another.

```
bool  AssignArray(
   const double&  src[]      // source array
   )

```

Parameters

src[]

[in] Reference to an array used as a source of elements to copy.

Return Value

true - successful, false - cannot copy the items.

Example:

```
//--- example for CArrayDouble::AssignArray(const double &[])
#include <Arrays\ArrayDouble.mqh>
//---
double src[];
//---
void OnStart()
  {
   CArrayDouble *array=new CArrayDouble;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- assign another array
   if(!array.AssignArray(src))
     {
      printf("Array assigned error");
      delete array;
      return;
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
