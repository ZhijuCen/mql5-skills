# FileWriteFloat

The function writes the value of the float parameter to a bin-file, starting from the current position of the file pointer.

```
uint  FileWriteFloat(
   int    file_handle,     // File handle
   float  value            // Value to be written
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

value

[in] The value of float type.

Return Value

If successful the function returns the number of bytes written (in this case [sizeof](/en/docs/basis/operations/other#sizeof)(float)=4). The file pointer is shifted by the same number of bytes.

Example:

```
//+------------------------------------------------------------------+
//|                                          Demo_FileWriteFloat.mq5 |
//|                        Copyright 2013, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2013, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- show the window of input parameters when launching the script
#property script_show_inputs
//--- parameters for receiving data from the terminal
input string          InpSymbolName="EURUSD";           // currency pair
input ENUM_TIMEFRAMES InpSymbolPeriod=PERIOD_M15;       // time frame
input datetime        InpDateStart=D'2013.01.01 00:00'; // data copying start date
//--- parameters for writing data to the file
input string          InpFileName="Close.bin"; // file name
input string          InpDirectoryName="Data"; // directory name
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   datetime date_finish=TimeCurrent();
   double   close_buff[];
   datetime time_buff[];
   int      size;
//--- reset the error value
   ResetLastError();
//--- copy the close price for each bar
   if(CopyClose(InpSymbolName,InpSymbolPeriod,InpDateStart,date_finish,close_buff)==-1)
     {
      PrintFormat("Failed to copy close price values. Error code = %d",GetLastError());
      return;
     }
//--- copy the time for each bar
   if(CopyTime(InpSymbolName,InpSymbolPeriod,InpDateStart,date_finish,time_buff)==-1)
     {
      PrintFormat("Failed to copy the time values. Error code = %d",GetLastError());
      return;
     }
//--- receive the buffer size
   size=ArraySize(close_buff);
//--- open the file for writing the values (if the file is absent, it will be created automatically)
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_WRITE|FILE_BIN);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is open for writing",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_DATA_PATH));
      //--- write close prices' time and values to the file
      for(int i=0;i<size;i++)
        {
         FileWriteDouble(file_handle,(double)time_buff[i]);
         FileWriteFloat(file_handle,(float)close_buff[i]);
        }
      //--- close the file
      FileClose(file_handle);
      PrintFormat("Data is written, %s file is closed",InpFileName);
     }
   else
      PrintFormat("Failed to open %s file, Error code = %d",InpFileName,GetLastError());
  }

```

See also

[Real types (double, float)](/en/docs/basis/types/double), [FileWriteDouble](/en/docs/files/filewritedouble)
