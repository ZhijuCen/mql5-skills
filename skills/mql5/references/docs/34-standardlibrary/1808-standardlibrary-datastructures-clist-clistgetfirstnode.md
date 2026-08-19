# GetFirstNode

Gets the first element of the list.

```
CObject*  GetFirstNode()

```

Return Value

Pointer to the first element - success, NULL - cannot get a pointer.

Example:

```
//--- example for CList::GetFirstNode() 
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
   CObject *object=list.GetFirstNode(); 
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
