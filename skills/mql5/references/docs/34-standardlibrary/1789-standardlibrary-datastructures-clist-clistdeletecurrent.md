# DeleteCurrent

Removes the element from the current position in the list.

```
bool  DeleteCurrent()

```

Return Value

true - successful, false - cannot remove the element.

Note

If the memory management is enabled, memory for the removed element is deallocated.

Example:

```
//--- example for CList::DeleteCurrent() 
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
   if(!list.DeleteCurrent()) 
     { 
      printf("Delete error"); 
      delete list; 
      return; 
     } 
   //--- delete list 
   delete list; 
  } 

```
