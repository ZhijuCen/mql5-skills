# DetachCurrent

Extracts an element from the current position in the list without its "physical" deletion.

```
CObject*  DetachCurrent()

```

Return Value

Pointer to the removed element in case of success, NULL - cannot remove the element.

Note

When removed from the list, the element is not removed in any state of the memory management flag. The pointer to the extracted element should be released after it has been used.

Example:

```
//--- example for CList::DetachCurrent() 
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
   CObject *object=list.DetachCurrent(); 
   if(object==NULL) 
     { 
      printf("Detach error"); 
      delete list; 
      return; 
     } 
   //--- use element 
   //--- . . . 
   //--- delete element 
   delete object; 
   //--- delete list 
   delete list; 
  } 

```
