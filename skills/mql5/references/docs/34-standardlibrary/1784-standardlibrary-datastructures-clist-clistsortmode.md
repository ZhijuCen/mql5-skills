# SortMode

Gets the version of the sorting.

```
int  SortMode() const

```

Return Value

Sorting mode, or -1 if the list is not sorted.

Example:

```
//--- example for CList::SortMode() 
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
   //--- check sort mode 
   int sort_mode=list.SortMode(); 
   //--- use list 
   //--- ... 
   //--- delete list 
   delete list; 
  } 

```
