# Load

Loads object parameters from file.

```
virtual bool  Load(
   int  file_handle      // file handle
   )

```

Parameters

file_handle

[in]  handle of file previously opened using the FileOpen(...) function.

Return Value

true - success, false - error.

Example:

```
//--- example for CChartObjectArrow::Load  
#include <ChartObjects\ChartObjectsArrows.mqh>  
//---  
void OnStart()  
  {  
   int               file_handle;  
   CChartObjectArrow arrow;  
//--- open file  
   file_handle=FileOpen("MyFile.bin",FILE_READ|FILE_BIN|FILE_ANSI);  
   if(file_handle>=0)  
     {  
      if(!arrow.Load(file_handle))  
        {  
         //--- file load error  
         printf("File load: Error %d!",GetLastError());  
         FileClose(file_handle);  
         //---  
         return;  
        }  
      FileClose(file_handle);  
     }  
//--- use arrow  
//--- . . .  
  }  

```
