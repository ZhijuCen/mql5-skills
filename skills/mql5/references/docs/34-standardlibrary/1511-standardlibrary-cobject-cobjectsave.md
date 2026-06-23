# Save

Saves list element data in a file.

```
virtual bool  Save(
   int  file_handle      // File handle
   )

```

Parameters

file_handle

[in]  Handle of the binary file opened earlier using the FileOpen () function

Return Value

true - successfully completed, false - error.

Note

Save(int) method in CObject class always returns 'true' and does not perform any action. If you want to save the data of a derived class in a file, the Save(int) method should be implemented.

Example:

```
//--- example for CObject::Save(int)
#include <Object.mqh>
//---
void OnStart()
  {
   int    file_handle;
   CObject *object=new CObject;
   //---
   if(object!=NULL)
     {
      printf("Object create error");
      return;
     }
   //--- set objects data
   //--- . . .
   //--- open file
   file_handle=FileOpen("MyFile.bin",FILE_WRITE|FILE_BIN|FILE_ANSI);
   if(file_handle>=0)
     {
      if(!object.Save(file_handle))
        {
         //--- file save error
         printf("File save: Error %d!",GetLastError());
         delete object;
         FileClose(file_handle);
         //---
         return;
        }
      FileClose(file_handle);
     }
   delete object;
  }

```
