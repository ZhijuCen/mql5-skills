# FreeMode

Sets the flag of memory management.

```
void  FreeMode(
   bool  mode      // new flag
   )

```

Parameters

mode

[in] New value of the memory management flag.

Return Value

None.

Note

Setting the memory management flag is an important part in the CArrayObj class use. Since the array elements are pointers to dynamic objects, it is important to determine what to do with them when removing from the array.

If the flag is set, removing an element from the array, the element is automatically deleted by the delete operator. If the flag is not set, it is assumed that a pointer to the deleted object is still somewhere in the user program and will be deallocated by the program afterwards.

If the user program resets the flag of memory management, the user must understand his responsibility for the removal of the array before the termination of the program. Otherwise the memory allocated for elements by the new operator is not released.

For large amounts of data this could lead even to crash of your terminal.

If the user does not reset the memory management flag, there is another pitfall. When pointer elements in array are stored somewhere in the local variables, then removing the array will lead to a critical error and crash of the user program. By default, the memory management flag is set, i.e. the class of the array is responsible for freeing the memory elements.

Example:

```
//--- example for CArrayObj::FreeMode(bool)
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
   //--- reset free mode flag
   array.FreeMode(false);
   //--- use array
   //--- . . .
   //--- delete array
   delete array;
  }

```
