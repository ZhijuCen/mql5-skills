# IsSorted

Gets the sorted list flag.

```
bool  IsSorted(
   int  mode=0      // sorting mode
   ) const

```

Parameters

mode=0

[in] Checked sort mode.

Return Value

Flag of the sorted list. Returns true if the list is sorted using the specified mode, otherwise returns false.

Note

Flag of the sorted list cannot be changed directly. The flag is set by Sort(int) and resets by any add/insert methods.

Example:

```
//--- example for CList::IsSorted() 
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
   //--- check sorted 
   if(list.IsSorted(0)) 
     { 
      //--- use methods for sorted list 
      //--- ... 
     } 
   //--- delete list 
   delete list; 
  } 

```
