# FileReadStruct

The function reads contents into a structure passed as a parameter from a binary-file, starting with the current position of the file pointer.

```
uint  FileReadStruct(
   int          file_handle,        // file handle
   const void&  struct_object,      // target structure to which the contents are read
   int          size=-1             // structure size in bytes
   );

```

Parameters

file_handle

[in] File descriptor of an open bin-file.

struct_object

[out]  The object of this structure. The structure should not contain strings, [dynamic arrays](/en/docs/basis/types/dynamic_array) or [virtual functions](/en/docs/basis/oop/virtual).

size=-1

[in]  Number of bytes that should be read. If size is not specified or the indicated value is greater than the size of the structure, the exact size of the specified structure is used.

Return Value

If successful the function returns the number of bytes read. File pointer is moved by the same number of bytes.

Example (the file obtained after using the example for [FileWriteStruct](/en/docs/files/filewritestruct) function is used here)

```
//+------------------------------------------------------------------+
//|                                          Demo_FileReadStruct.mq5 |
//|                        Copyright 2013, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2013, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 4
#property indicator_plots   1
//---- plot Label1
#property indicator_label1  "Candles"
#property indicator_type1   DRAW_CANDLES
#property indicator_color1  clrOrange
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
#property indicator_separate_window
//--- parameters for receiving data
input string  InpFileName="EURUSD.txt"; // file name
input string  InpDirectoryName="Data";  // directory name
//+------------------------------------------------------------------+
//| Structure for storing candlestick data                           |
//+------------------------------------------------------------------+
struct candlesticks
  {
   double            open;  // open price
   double            close; // close price
   double            high;  // high price
   double            low;   // low price
   datetime          date;  // date
  };
//--- indicator buffers
double       open_buff[];
double       close_buff[];
double       high_buff[];
double       low_buff[];
//--- global variables
candlesticks cand_buff[];
int          size=0;
int          ind=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
   int default_size=100;
   ArrayResize(cand_buff,default_size);
//--- open the file
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_BIN|FILE_COMMON);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for reading",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_COMMONDATA_PATH));
      //--- read data from the file
      while(!FileIsEnding(file_handle))
        {
         //--- write data to the array
         FileReadStruct(file_handle,cand_buff[size]);
         size++;
         //--- check if the array is overflown
         if(size==default_size)
           {
            //--- increase the array size
            default_size+=100;
            ArrayResize(cand_buff,default_size);
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
//--- indicator buffers mapping
   SetIndexBuffer(0,open_buff,INDICATOR_DATA);
   SetIndexBuffer(1,high_buff,INDICATOR_DATA);
   SetIndexBuffer(2,low_buff,INDICATOR_DATA);
   SetIndexBuffer(3,close_buff,INDICATOR_DATA);
//--- empty value
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
//--- the loop for the candlesticks that have not been handled yet
   for(int i=prev_calculated;i<rates_total;i++)
     {
      //--- 0 by default
      open_buff[i]=0;
      close_buff[i]=0;
      high_buff[i]=0;
      low_buff[i]=0;
      //--- check if any data is still present
      if(ind<size)
        {
         for(int j=ind;j<size;j++)
           {
            //--- if dates coincide, the value from the file is used
            if(time[i]==cand_buff[j].date)
              {
               open_buff[i]=cand_buff[j].open;
               close_buff[i]=cand_buff[j].close;
               high_buff[i]=cand_buff[j].high;
               low_buff[i]=cand_buff[j].low;
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

[Structures and classes](/en/docs/basis/types/classes), [FileWriteStruct](/en/docs/files/filewritestruct)
