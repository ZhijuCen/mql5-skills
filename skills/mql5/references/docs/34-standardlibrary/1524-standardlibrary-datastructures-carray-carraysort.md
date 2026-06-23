# Sort

Sorts an array using the specified option.

```
void  Sort(
   int  mode=0      // sorting mode
   )

```

Parameters

mode=0

[in]  Mode of array sorting.

Return Value

No.

Note

Sorting an array is always ascending. For arrays of primitive data types (CArrayChar, CArrayShort, etc.), the 'mode' parameter is not used. For the CArrayObj array, multivariate sorting should be implemented in the Sort(int) method of derived classes.

Example:

```
//--- example for CArray::Sort(int)
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
   //--- sorting by mode 0
   array.Sort(0);
   //--- use array
   //--- ...
   //--- delete array
   delete array;
  }

```
