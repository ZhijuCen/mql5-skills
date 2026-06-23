# Save

Saves object parameters to file.

```
virtual bool  Save(
   int  file_handle      // file handle
   )

```

Parameters

file_handle

[in]  handle of file opened previously using the FileOpen(...) function.

Return Value

true - successful, false - error.

Example:

```
//--- example for CChartObjectArrow::Save  
#include <ChartObjects\ChartObjectsArrows.mqh>  
//---  
void OnStart()  
  {  
   int               file_handle;  
   CChartObjectArrow arrow;  
//--- set object parameters  
   double price=SymbolInfoDouble(Symbol(),SYMBOL_BID);  
   if(!arrow.Create(0,"Arrow",0,TimeCurrent(),price,181))  
     {  
      //--- arrow create error  
      printf("Arrow create: Error %d!",GetLastError());  
      //---  
      return;  
     }     
//--- open file  
   file_handle=FileOpen("MyFile.bin",FILE_WRITE|FILE_BIN|FILE_ANSI);  
   if(file_handle>=0)  
     {  
      if(!arrow.Save(file_handle))  
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
