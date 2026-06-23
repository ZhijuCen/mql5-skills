# GetNodeAtIndex

Gets an element from the specified position in the list.

```
CObject*  GetNodeAtIndex(
   int  pos      // position
   )

```

Parameters

pos

[in]  element position in the list.

Return Value

pointer to the element - success, NULL - cannot receive a pointer.

Example:

```
//--- example for CList::GetNodeAtIndex(int)  
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
   //--- add list elements  
   //--- . . .  
   CObject *object=list.GetNodeAtIndex(10);  
   if(object==NULL)  
     {  
      printf("Get node error");  
      delete list;  
      return;  
     }  
   //--- use element  
   //--- . . .  
   //--- do not delete element  
   //--- delete list  
   delete list;  
  }  

```
