# Add

Adds an element to the end of the list.

```
int  Add(
   CObject*  element      // element to add
   )

```

Parameters

element

[in] Value of the element to add to the list.

Return Value

Index of the added element - success, -1 - error.

Note

The element is not added to the list, if an invalid pointer (for example, NULL) is passed as a parameter.

Example:

```
//--- example for CList::Add(Cobject*) 
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
   //--- add 100 elements 
   for(int i=0;i<100;i++) 
     { 
      if(list.Add(new CObject)==-1) 
        { 
         printf("Element addition error"); 
         delete list; 
         return; 
        } 
     } 
   //--- use list 
   //--- . . . 
   //--- delete list 
   delete list; 
  } 

```
