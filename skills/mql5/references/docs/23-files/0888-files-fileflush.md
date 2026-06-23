# FileFlush

Writes to a disk all data remaining in the input/output file buffer.

```
void  FileFlush(
   int  file_handle      // File handle
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

Return Value

No value returned.

Note

When writing to a file, the data may be actually found there only after some time. To save the data in the file instantly, use FileFlush() function. If the function is not used, part of the data that has not been stored in the disk yet, will be forcibly written there only when the file is closed using FileClose() function.

The function should be used when written data is of a certain value. It should be kept in mind that frequent function call may affect the program operation speed.

Function FileFlush () must be called between the operations of reading from a file and writing to it.

Example:

```
//--- show the window of input parameters when launching the script
#property script_show_inputs
//--- file name for writing
input string InpFileName="example.csv"; // file name
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- reset error value
   ResetLastError();
//--- open the file
   int file_handle=FileOpen(InpFileName,FILE_READ|FILE_WRITE|FILE_CSV);
   if(file_handle!=INVALID_HANDLE)
     {
      //--- write data to the file
      for(int i=0;i<1000;i++)
        {
         //--- call write function
         FileWrite(file_handle,TimeCurrent(),SymbolInfoDouble(Symbol(),SYMBOL_BID),SymbolInfoDouble(Symbol(),SYMBOL_ASK));
         //--- save data on the disk at each 128th iteration
         if((i & 127)==127)
           {
            //--- now, data will be located in the file and will not be lost in case of a critical error
            FileFlush(file_handle);
            PrintFormat("i = %d, OK",i);
           }
         //--- 0.01 second pause
         Sleep(10);
        }
      //--- close the file
      FileClose(file_handle);
     }
   else
      PrintFormat("Error, code = %d",GetLastError());
  }

```

See also

[FileClose](/en/docs/files/fileclose)
