# Save

Saves parameters of the object in the file.

```
virtual bool  Save(
   int  file_handle      // file handle
   )

```

Parameters

file_handle

[in]  Handle of the file previously opened using the function FileOpen (...).

Return Value

true - successfully completed, false - error.

Example:

```
//--- example for CChartObject::Save   
#include <ChartObjects\ChartObject.mqh>   
//---   
void OnStart()   
  {   
   int          file_handle;   
   CChartObject object=new CChartObject;   
   //--- set object parameters   
   //--- . . .   
   //--- open file   
   file_handle=FileOpen("MyFile.bin",FILE_WRITE|FILE_BIN|FILE_ANSI);   
   if(file_handle>=0)   
     {   
      if(!object.Save(file_handle))   
        {   
         //--- file save error   
         printf("File save: Error %d!",GetLastError());   
         FileClose(file_handle);   
         //---   
         return;   
        }   
      FileClose(file_handle);   
     }   
  }   

```
