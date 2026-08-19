# Max

Gets the maximum possible size of the array without memory reallocation.

```
int  Max() const

```

Return Value

The maximum possible size of the array without memory reallocation.

Example:

```
//--- example for CArray::Max()
#include <Arrays\Array.mqh>
//---
void OnStart()
  {
   CArray *array=new CArray;
   //---
   if(array==NULL)
     {
      printf("Object create error");
      return;
     }
   //--- check maximum size
   int max=array.Max();
   //--- use array
   //--- ...
   //--- delete array
   delete array;
  }

```
