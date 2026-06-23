# FileReadFloat

Reads the single-precision floating point number (float) from the current position of the binary file.

```
float  FileReadFloat(
   int  file_handle    // File handle
   );

```

Parameters

file_handle

[in]  File descriptor returned by [FileOpen()](/en/docs/files/fileopen).

Return Value

The value of float type.

Note

For more details about the error, call [GetLastError()](/en/docs/check/getlasterror).

Example (the file obtained after executing the example for [FileWriteFloat](/en/docs/files/filewritefloat) function is used here)

```
//+------------------------------------------------------------------+
//|                                           Demo_FileReadFloat.mq5 |
//|                        Copyright 2013, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2013, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   1
//---- plot Label1
#property indicator_label1  "CloseLine"
#property indicator_type1   DRAW_COLOR_LINE
#property indicator_color1  clrRed,clrBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2
//--- parameters for data reading
input string InpFileName="Close.bin"; // file name
input string InpDirectoryName="Data"; // directory name
//--- global variables
int      ind=0;
int      size=0;
double   close_buff[];
datetime time_buff[];
//--- indicator buffers
double   buff[];
double   color_buff[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
   int def_size=100;
//--- allocate memory for the arrays
   ArrayResize(close_buff,def_size);
   ArrayResize(time_buff,def_size);
//--- open the file
   ResetLastError();
   int file_handle=FileOpen(InpDirectoryName+"//"+InpFileName,FILE_READ|FILE_BIN);
   if(file_handle!=INVALID_HANDLE)
     {
      PrintFormat("%s file is available for reading",InpFileName);
      PrintFormat("File path: %s\\Files\\",TerminalInfoString(TERMINAL_DATA_PATH));
      //--- read data from the file
      while(!FileIsEnding(file_handle))
        {
         //--- read time and price values
         time_buff[size]=(datetime)FileReadDouble(file_handle);
         close_buff[size]=(double)FileReadFloat(file_handle);
         size++;
         //--- increase the array sizes if they are overflown
         if(size==def_size)
           {
            def_size+=100;
            ArrayResize(close_buff,def_size);
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
//--- bind the arrays to the indicator buffers
   SetIndexBuffer(0,buff,INDICATOR_DATA);
   SetIndexBuffer(1,color_buff,INDICATOR_COLOR_INDEX);
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
//--- the loop for the bars that have not been handled yet
   for(int i=prev_calculated;i<rates_total;i++)
     {
      //--- 0 by default
      buff[i]=0;
      color_buff[i]=0; // red color by default
      //--- check if any data is still present
      if(ind<size)
        {
         for(int j=ind;j<size;j++)
           {
            //--- if the dates coincide, the value from the file is used
            if(time[i]==time_buff[j])
              {
               //--- receive the price
               buff[i]=close_buff[j];
               //--- if the current price exceeds the previous one, the color is blue
               if(buff[i-1]>buff[i])
                  color_buff[i]=1;
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

[Real types (double, float)](/en/docs/basis/types/double), [FileReadDouble](/en/docs/files/filereaddouble), [FileWriteFloat](/en/docs/files/filewritefloat)
