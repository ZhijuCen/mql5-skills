# Reserve

Allocates memory to increase the size of the array.

```
bool  Reserve(
   int  size      // number
   )

```

Parameters

size

[in]  The number of additional elements of the array.

Return Value

true - successful, false - there was an attempt to request for an amount less than or equal to zero, or failed to increase the array.

Note

To reduce fragmentation of memory, the array size is changed using the step previously determined by the Step(int) method or the default step of 16.

Example:

```
//--- example for CArrayLong::Reserve(int)
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
   //--- reserve memory
   if(!array.Reserve(1024))
     {
      printf("Reserve error");
      delete array;
      return;
     }
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
