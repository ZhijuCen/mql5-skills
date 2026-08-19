# Load

Loads the parameters of the object from the file.

```
virtual bool  Load(
   int  file_handle      // file handle
   )

```

Parameters

file_handle

[in]  handle of the file previously opened using the function FileOpen (...).

Return Value

true - successfully completed, false - error.

Example:

```
//--- example for CChartObject::Load 
#include <ChartObjects\ChartObject.mqh> 
//--- 
void OnStart()
  {
   int          file_handle;
   CChartObject object;
   //--- open file 
   file_handle=FileOpen("MyFile.bin",FILE_READ|FILE_BIN|FILE_ANSI); 
   if(file_handle>=0) 
     { 
      if(!object.Load(file_handle)) 
        { 
         //--- file load error 
         printf("File load: Error %d!",GetLastError()); 
         FileClose(file_handle); 
         //--- 
         return; 
        } 
      FileClose(file_handle); 
     } 
   //--- use object 
   //--- . . . 
  } 

```
