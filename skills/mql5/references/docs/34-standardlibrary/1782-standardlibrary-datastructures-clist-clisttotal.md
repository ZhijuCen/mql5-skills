# Total

Gets the number of elements in the list.

```
int  Total() const

```

Return Value

Number of elements in the list.

Example:

```
//--- example for CList::Total() 
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
   //--- check total 
   int total=list.Total(); 
   //--- use list 
   //--- ... 
   //--- delete list 
   delete list; 
  } 

```
