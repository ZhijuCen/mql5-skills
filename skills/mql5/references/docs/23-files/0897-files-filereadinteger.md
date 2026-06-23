# FileReadInteger

The function reads int, short or char value from the current position of the file pointer depending on the length specified in bytes.

```
int  FileReadInteger(
   int  file_handle,        // File handle
   int  size=INT_VALUE      // Size of an integer in bytes
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

size=INT_VALUE

[in]  Number of bytes (up to 4 inclusive) that should be read. The corresponding constants are provided: CHAR_VALUE = 1, SHORT_VALUE = 2 and INT_VALUE = 4, so the function can read the whole value of char, short or int type.

Return Value

A value of the int type. The result of this function must be explicitly cast to a target type, i.e. to the type of data that you need to read. Since a value of the int type is returned, it can be easily converted to any integer value. The file pointer is shifted by the number of bytes read.

Note

When reading less than 4 bytes, the received result is always positive. If one or two bytes are read, the sign of the number can be determined by explicit casting to type char (1 byte) or short (2 bytes). Getting the sign for a three-byte number is not trivial, since there is no corresponding [underlying type](/en/docs/basis/types/integer).

Example (the file obtained after executing the example for [FileWriteInteger](/en/docs/files/filewriteinteger) function is used here)

```
//+------------------------------------------------------------------+
//|                                         Demo_FileReadInteger.mq5 |
//|                        Copyright 2013, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2013, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
//---- plot Label1
#property indicator_label1  "Trends"
#property indicator_type1   DRAW_SECTION
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- parameters for data reading
input string InpFileName="Trend.bin"; // file name
input string InpDirectoryName="Data"; // directory name
//--- global variables
int      ind=0;
int      size=0;
datetime time_buff[];
//--- indicator buffers
double   buff[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
   int def_size=100;
//--- allocate memory for the array
   ArrayResize(time_buff,def_size);
//--- open the file
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_BIN);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for reading",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_DATA_PATH));
      //--- additional variables
      int    arr_size;
      uchar  arr[];
      //--- read data from the file
      while(!FileIsEnding(file_handle))
        {
         //--- find out how many symbols are used for writing the time
         arr_size=FileReadInteger(file_handle,INT_VALUE);
         ArrayResize(arr,arr_size);
         for(int i=0;i<arr_size;i++)
            arr[i]=(char)FileReadInteger(file_handle,CHAR_VALUE);
         //--- store the time value
         time_buff[size]=StringToTime(CharArrayToString(arr));
         size++;
         //--- increase the sizes of the arrays if they are overflown
         if(size==def_size)
           {
            def_size+=100;
            ArrayResize(time_buff,def_size);
           }
        }
      //--- close the file
      FileClose(file_handle);
      PrintFormat("Data is read, %s file is closed",InpFileName);
     }
   else
     {
      PrintFormat("Failed to open %s file, Error code = %d",InpFileName,GetLastError());
      return(INIT_FAILED);
     }
//--- bind the array to the indicator buffer
   SetIndexBuffer(0,buff,INDICATOR_DATA);
//---- set the indicator values that will not be visible on the chart
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0);
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
   ArraySetAsSeries(time,false);
   ArraySetAsSeries(close,false);
//--- the loop for the bars that have not been handled yet
   for(int i=prev_calculated;i<rates_total;i++)
     {
      //--- 0 by default
      buff[i]=0;
      //--- check if any data is still present
      if(ind<size)
        {
         for(int j=ind;j<size;j++)
           {
            //--- if dates coincide, the value from the file is used
            if(time[i]==time_buff[j])
              {
               //--- receive the price
               buff[i]=close[i];
               //--- increase the counter
               ind=j+1;
               break;
              }
           }
        }
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```

See also

[IntegerToString](/en/docs/convert/integertostring), [StringToInteger](/en/docs/convert/stringtointeger), [Integer types](/en/docs/basis/types/integer), [FileWriteInteger](/en/docs/files/filewriteinteger)
