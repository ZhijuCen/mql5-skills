# Delta

Sets the comparison tolerance.

```
void  Delta(
   double  delta      // tolerance
   )

```

Parameters

delta

[in]  The new value of the comparison tolerance.

Return Value

No

Note

Comparison tolerance is used in the search. Values are considered equal if their difference is less than or equal to tolerance. The default tolerance is 0.0.

Example:

```
//--- example for CArrayDouble::Delta(double)
#include <Arrays\ArrayDouble.mqh>
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
   //--- set compare variation
   array.Delta(0.001);
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
