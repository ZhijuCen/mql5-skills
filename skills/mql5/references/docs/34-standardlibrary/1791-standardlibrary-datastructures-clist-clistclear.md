# Clear

Removes all elements of the list.

```
void  Clear()

```

Note

If the memory management is enabled, the memory of deleted elements is deallocated.

Example:

```
//--- example for CList::Clear() 
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
   //--- clear list 
   list.Clear(); 
   //--- delete list 
   delete list; 
  } 

```
