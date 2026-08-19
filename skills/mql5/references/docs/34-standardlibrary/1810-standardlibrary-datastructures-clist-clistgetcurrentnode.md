# GetCurrentNode

Gets the current list element.

```
CObject*  GetCurrentNode()

```

Return Value

Pointer to the current element - successful, NULL - cannot get a pointer.

Example:

```
//--- example for CList::GetCurrentNode() 
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
   CObject *object=list.GetCurrentNode(); 
   if(object==NULL) 
     { 
      printf("Get node error"); 
      delete list; 
      return; 
     } 
   //--- use element 
   //--- . . . 
   //--- do not delete element 
   //--- delete list 
   delete list; 
  } 

```
