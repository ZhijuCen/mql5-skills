# Insert

Inserts an element to the specified position in the list.

```
int  Insert(
   CObject*  element,     // element to insert
   int       pos          // position
   )

```

Parameters

element

[in] value of the element to insert in the list

pos

[in] position in the list to insert

Return Value

index of inserted element - success, -1 - error.

Note

The element is not added to the list, if an invalid pointer (for example, NULL) is passed as a parameter.

Example:

```
//--- example for CList::Insert(CObject*,int) 
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
   //--- insert 100 elements 
   for(int i=0;i<100;i++) 
     { 
      if(list.Insert(new CObject,0)==-1) 
        { 
         printf("Element insert error"); 
         delete list; 
         return; 
        } 
     } 
   //--- use list 
   //--- . . . 
   //--- delete list 
   delete list; 
  } 

```
