# Search

Searches for an element equal to the sample in the sorted list.

```
CObject*  Search(
   CObject*  element      // sample
   )

```

Parameters

element

[in] element sample to search for in the list.

Return Value

Pointer to the found element - successful, NULL - the element is not found.

Example:

```
//--- example for CList::Search(CObject*) 
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
   //--- add lists elements 
   //--- . . . 
   //--- sort list 
   list.Sort(0); 
   //--- create sample 
   CObject *sample=new CObject; 
   if(sample==NULL) 
     { 
      printf("Sample create error"); 
      delete list; 
      return; 
     } 
   //--- set sample attributes 
   //--- . . . 
   //--- search element 
   if(list.Search(sample)!=NULL) printf("Element found"); 
   else                          printf("Element not found"); 
   //--- delete list 
   delete list; 
  } 

```
