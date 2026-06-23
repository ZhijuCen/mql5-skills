# Exchange

Swaps two elements in the list.

```
bool  Exchange(
   CObject*  node1,     // list element
   CObject*  node2      // list element
   )

```

Parameters

node1

[in] list element

node2

[in] list element

Return Value

true - successful, false - cannot swap the elements.

Example:

```
//--- example for CList::Exchange(CObject*,CObject*) 
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
   //--- exchange 
   list.Exchange(list.GetFirstNode(),list.GetLastNode()); 
   //--- use list 
   //--- . . . 
   //--- delete list 
   delete list; 
  } 

```
