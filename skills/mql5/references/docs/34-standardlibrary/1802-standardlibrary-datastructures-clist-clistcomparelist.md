# CompareList

Compares the list with another one.

```
bool  CompareList(
   CList*  list      // pointer to the source
   )

```

Parameters

list

[in] a pointer to an instance of the CList class used as a source of elements for comparison.

Return Value

true - the lists are equal, false - the lists are not equal.

Example:

```
//--- example for CList::CompareList(const CList*) 
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
   //--- create source list 
   CList *src=new CList; 
   if(src==NULL) 
     { 
      printf("Object create error"); 
      delete list; 
      return; 
     } 
   //--- fill source list 
   //--- . . . 
   //--- compare with another list 
   bool result=list.CompareList(src); 
   //--- delete lists 
   delete src; 
   delete list; 
  } 

```
