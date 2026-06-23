# CreateElement

Creates a new element of the list.

```
CObject*  CreateElement()

```

Return Value

Pointer to the newly created element - successful, NULL - cannot create an element.

Note

Method CreateElement () in the CList class always returns NULL and does not perform any actions. If necessary, method CreateElement () should be implemented in a derived class.

Example:

```
//--- example for CList::CreateElement(int) 
#include <Arrays\List.mqh> 
//--- 
void OnStart() 
  { 
   int    size=100; 
   CList *list=new CList; 
   //--- 
   if(list==NULL) 
     { 
      printf("Object create error"); 
      return; 
     } 
   //--- fill list 
   for(int i=0;i<size;i++) 
     { 
      CObject *object=list.CreateElement(); 
      if(object==NULL) 
        { 
         printf("Element create error"); 
         delete list; 
         return; 
        } 
      list.Add(object); 
     } 
   //--- use list 
   //--- . . . 
   //--- delete list 
   delete list; 
  } 

```
