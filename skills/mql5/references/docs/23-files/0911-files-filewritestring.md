# FileWriteString

The function writes the value of a string-type parameter into a BIN, CSV or TXT file starting from the current position of the file pointer. When writing to a CSV or TXT file: if there is a symbol in the string '\n' (LF) without previous character '\r' (CR), then before '\n' the missing '\r' is added.

```
uint  FileWriteString(
   int           file_handle,    // File handle
   const string  text_string,    // string to write
   int           length=-1       // number of symbols
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

text_string

[in]  String.

length=-1

[in] The number of characters that you want to write. This option is needed for writing a string into a BIN file. If the size is not specified, then the entire string without the trailer 0 is written. If you specify a size smaller than the length of the string, then a part of the string without the trailer 0 is written. If you specify a size greater than the length of the string, the string is filled by the appropriate number of zeros. For files of CSV and TXT type, this parameter is ignored and the string is written entirely.

Return Value

If successful the function returns the number of bytes written. The file pointer is shifted by the same number of bytes.

Note

Note that when writing to a file opened by the FILE_UNICODE [flag](/en/docs/constants/io_constants/fileflags) (or without a flag FILE_ANSI), then the number of bytes written will be twice as large as the number of string characters written. When recording to a file opened with the FILE_ANSI flag, the number of bytes written will coincide with the number of string characters written.

Example:

```
//+------------------------------------------------------------------+
//|                                         Demo_FileWriteString.mq5 |
//|                        Copyright 2013, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2013, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
//--- show the window of input parameters when launching the script
#property script_show_inputs
//--- parameters for receiving data from the terminal
input string             InpSymbolName="EURUSD";           // currency pair
input ENUM_TIMEFRAMES    InpSymbolPeriod=PERIOD_H1;        // time frame
input int                InpMAPeriod=14;                   // MA period
input ENUM_APPLIED_PRICE InpAppliedPrice=PRICE_CLOSE;      // price type
input datetime           InpDateStart=D'2013.01.01 00:00'; // data copying start date
//--- parameters for writing data to the file
input string             InpFileName="RSI.csv";   // file name
input string             InpDirectoryName="Data"; // directory name
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   datetime date_finish; // data copying end date
   double   rsi_buff[];  // array of indicator values
   datetime date_buff[]; // array of the indicator dates
   int      rsi_size=0;  // size of the indicator arrays
//--- end time is the current one
   date_finish=TimeCurrent();
//--- receive RSI indicator handle
   ResetLastError();
   int rsi_handle=iRSI(InpSymbolName,InpSymbolPeriod,InpMAPeriod,InpAppliedPrice);
   if(rsi_handle==INVALID_HANDLE)
     {
      //--- failed to receive the indicator handle
      PrintFormat("Error when receiving indicator handle. Error code = %d",GetLastError());
      return;
     }
//--- being in the loop, until the indicator calculates all its values
   while(BarsCalculated(rsi_handle)==-1)
      Sleep(10); // a pause to allow the indicator to calculate all its values
//--- copy the indicator values for a certain period of time
   ResetLastError();
   if(CopyBuffer(rsi_handle,0,InpDateStart,date_finish,rsi_buff)==-1)
     {
      PrintFormat("Failed to copy indicator values. Error code = %d",GetLastError());
      return;
     }
//--- copy the appropriate time for the indicator values
   ResetLastError();
   if(CopyTime(InpSymbolName,InpSymbolPeriod,InpDateStart,date_finish,date_buff)==-1)
     {
      PrintFormat("Failed to copy time values. Error code = %d",GetLastError());
      return;
     }
//--- free the memory occupied by the indicator
   IndicatorRelease(rsi_handle);
//--- receive the buffer size
   rsi_size=ArraySize(rsi_buff);
//--- open the file for writing the indicator values (if the file is absent, it will be created automatically)
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_WRITE|FILE_CSV|FILE_ANSI);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for writing",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_DATA_PATH));
      //--- prepare additional variables
      string str="";
      bool   is_formed=false;
      //--- write dates of forming overbought and oversold areas
      for(int i=0;i<rsi_size;i++)
        {
         //--- check the indicator values
         if(rsi_buff[i]>=70 || rsi_buff[i]<=30)
           {
            //--- if the value is the first one in this area
            if(!is_formed)
              {
               //--- add the value and the date
               str=(string)rsi_buff[i]+"\t"+(string)date_buff[i];
               is_formed=true;
              }
            else
               str+="\t"+(string)rsi_buff[i]+"\t"+(string)date_buff[i];
            //--- move to the next loop iteration
            continue;
           }
         //--- check the flag
         if(is_formed)
           {
            //--- the string is formed, write it to the file
            FileWriteString(file_handle,str+"\r\n");
            is_formed=false;
           }
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

[String Type](/en/docs/basis/types/stringconst), [StringFormat](/en/docs/convert/stringformat)
