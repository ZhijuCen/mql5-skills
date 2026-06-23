# IndexOf

Gets the index of the specified list element.

```
int  IndexOf(
   CObject*  element      // pointer to the element
   )

```

Parameters

element

[in] pointer to the list element.

Return Value

List element index, or -1.

Example:

```
//--- example for CList::IndexOf(CObject*) 
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
   CObject *object=new CObject; 
   if(object==NULL) 
     { 
      printf("Element create error"); 
      delete list; 
      return; 
     } 
   if(list.Add(object)) 
     { 
      int pos=list.IndexOf(object); 
     } 
   //--- delete list 
   delete list; 
  } 

```
