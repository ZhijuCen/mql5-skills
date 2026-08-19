# Delete

Removes the element from the given position in the list.

```
bool  Delete(
   int  pos      // position
   )

```

Parameters

pos

[in] position of element to be removed from the list.

Return Value

true - successful, false - cannot remove the element.

Note

If the memory management flag is enabled, the memory used for the deleted element is released.

Example:

```
//--- example for CList::Delete(int) 
#include <Arrays\List.mqh> 
//--- 
void OnStart() 
  { 
   CList *list=new CList; 
   //--- 
   if(list==NULL) 
     { 
      printf("Object create error"); 
      return; 
     } 
   //--- add list elements 
   //--- . . . 
   if(!list.Delete(0)) 
     { 
      printf("Delete error"); 
      delete list; 
      return; 
     } 
   //--- delete list 
   delete list; 
  } 

```
