# FileClose

Close the file previously opened by [FileOpen()](/en/docs/files/fileopen).

```
void  FileClose(
   int  file_handle      // File handle
   );

```

Parameters

file_handle

[in]  File descriptor returned by FileOpen().

Return Value

No value returned.

Example:

```
//--- show the window of input parameters when launching the script
#property script_show_inputs
//--- input parameters
input string InpFileName="file.txt";    // file name
input string InpDirectoryName="Data";   // directory name
input int    InpEncodingType=FILE_ANSI; // ANSI=32 or UNICODE=64
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- print the path to the file we are going to use
   PrintFormat("Working %s\\Files\\ folder",TerminalInfoString(TERMINAL_DATA_PATH));
//--- reset the error value
   ResetLastError();
//--- open the file for reading (if the file does not exist, the error will occur)
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_TXT|InpEncodingType);
   if(file_handle!=INVALID_HANDLE)
     {
      //--- print the file contents
      while(!FileIsEnding(file_handle))
         Print(FileReadString(file_handle));
      //--- close the file
      FileClose(file_handle);
     }
   else
      PrintFormat("Error, code = %d",GetLastError());
  }

```
