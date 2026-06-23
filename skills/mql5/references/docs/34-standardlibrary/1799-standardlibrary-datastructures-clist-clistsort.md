# Sort

Sorts a list.

```
void  Sort(
   int  mode      // sorting mode
   )

```

Parameters

mode

[in] Sorting mode.

Return Value

No.

Note

The list is always sorted in ascending order.

Example:

```
//--- example for CList::Sort(int) 
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
   //--- sorting by mode 0 
   list.Sort(0); 
   //--- use list 
   //--- ... 
   //--- delete list 
   delete list; 
  } 

```
