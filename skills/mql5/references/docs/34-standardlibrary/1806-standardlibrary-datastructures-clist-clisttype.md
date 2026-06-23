# Type

Gets the list type identifier.

```
virtual int  Type()

```

Return Value

List type identifier (for CList - 7779).

Example:

```
//--- example for CList::Type() 
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
   //--- get list type 
   int type=list.Type(); 
   //--- delete list 
   delete list; 
  } 

```
