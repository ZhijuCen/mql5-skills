# FreeMode

Sets the flag of memory management when deleting list elements.

```
void  FreeMode(
   bool  mode      // new value
   )

```

Parameters

mode

[in] New value of the memory management flag.

Note

Setting the memory management flag is an important part in the CList class use. Since the list elements are pointers to dynamic objects, it is important to determine what to do with them when removing from the list.

If the flag is set, when removing an element from the list, the element is automatically deleted by the delete operator. If the flag is not set, it is assumed that a pointer to the deleted object is still somewhere in the user program and will be deallocated by the program afterwards.

If the user program resets the flag of memory management, users should understand their responsibility for the removal of the list elements before the termination of the program. Otherwise, the memory allocated for elements by the new operator is not released.

For large amounts of data this could lead even to a terminal crash.

If the user program does not reset the memory management flag, there is another "pitfall". When pointer elements in list are stored somewhere in the local variables, then removing the list will lead to a critical error and crash of the user program. By default, the memory management flag is set, i.e. the class of the list is responsible for releasing the memory elements.

Example:

```
//--- example for CList::FreeMode(bool)  
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
   //--- reset free mode flag  
   list.FreeMode(false);  
   //--- use list  
   //--- . . .  
   //--- delete list  
   delete list;  
  }  

```
