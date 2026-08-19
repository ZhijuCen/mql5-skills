# Load

Loads list data from the file.

```
virtual bool  Load(
   int  file_handle      // file handle
   )

```

Parameters

file_handle

[in] Handle of the binary file previously opened using the FileOpen () function.

Return Value

true - successfully completed, false - error.

Note

When reading list elements from the file, the [CList::CreateElement(int)](/en/docs/standardlibrary/datastructures/clist/clistcreateelement) method is called to create each element.

Example:

```
//--- example for CLoad::Load(int) 
#include <Arrays\List.mqh> 
//--- 
void OnStart() 
  { 
   int    file_handle; 
   CList *list=new CList; 
   //--- 
   if(list!=NULL) 
     { 
      printf("Object create error"); 
      return; 
     } 
   //--- open file 
   file_handle=FileOpen("MyFile.bin",FILE_READ|FILE_BIN|FILE_ANSI); 
   if(file_handle>=0) 
     { 
      if(!list.Load(file_handle)) 
        { 
         //--- file load error 
         printf("File load: Error %d!",GetLastError()); 
         delete list; 
         FileClose(file_handle); 
         //--- 
         return; 
        } 
      FileClose(file_handle); 
     } 
   //--- use list elements 
   //--- . . . 
   //--- delete list 
   delete list; 
  } 

```
