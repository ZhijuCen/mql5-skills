# ArraySort

Sorts the values in the first dimension of a multidimensional numeric array in the ascending order.

```
bool  ArraySort(
   void&  array[]      // array for sorting
   );

```

Parameters

array[]

[in][out]  Numeric array for sorting.

Return Value

The function returns true on success, otherwise  - false.

Note

An array is always sorted in the ascending order irrespective of the  [AS_SERIES](/en/docs/array/arraygetasseries) flag value.

Functions ArraySort and ArrayBSearch accept any-dimensional arrays as a parameter. However, searching and sorting are always applied to the first (zero) dimension.

Example:

```
#property description "The indicator analyzes data for the last month and draws all candlesticks with small"
#property description "and large tick volumes. The tick volume array is sorted out"
#property description "to define such candlesticks. The candlesticks having the volumes comprising the first InpSmallVolume"
#property description "per cent of the array are considered small. The candlesticks having the tick volumes comprising "
#property description "the last InpBigVolume per cent of the array are considered large."
//--- indicator settings
#property indicator_chart_window
#property indicator_buffers 5
#property indicator_plots   1
//--- plot
#property indicator_label1  "VolumeFactor"
#property indicator_type1   DRAW_COLOR_CANDLES
#property indicator_color1  clrDodgerBlue,clrOrange
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2
//--- predefined constant
#define INDICATOR_EMPTY_VALUE 0.0
//--- input parameters
input int InpSmallVolume=15; // Percentage value of small volumes (<50)
input int InpBigVolume=20;   // Percentage value of large volumes (<50)
//--- analysis start time (will be shifted)
datetime ExtStartTime;
//--- indicator buffers
double   ExtOpenBuff[];
double   ExtHighBuff[];
double   ExtLowBuff[];
double   ExtCloseBuff[];
double   ExtColorBuff[];
//--- volume boundary values for displaying the candlesticks
long     ExtLeftBorder=0;
long     ExtRightBorder=0;
//+------------------------------------------------------------------+
//| Receive border values for tick volumes                           |
//+------------------------------------------------------------------+
bool GetVolumeBorders(void)
  {
//--- variables
   datetime stop_time;  // copy end time
   long     buff[];     // buffer for copying
//--- end time is the current one
   stop_time=TimeCurrent();
//--- start time is one month earlier from the current one
   ExtStartTime=GetStartTime(stop_time);
//--- receive the values of tick volumes
   ResetLastError();
   if(CopyTickVolume(Symbol(),Period(),ExtStartTime,stop_time,buff)==-1)
     {
      //--- failed to receive the data, return false to launch recalculation command
      PrintFormat("Failed to receive tick volume values. Error code = %d",GetLastError());
      return(false);
     }
//--- calculate array size
   int size=ArraySize(buff);
//--- sort out the array
   ArraySort(buff);
//--- define the values of the left and right border for tick volumes
   ExtLeftBorder=buff[size*InpSmallVolume/100];
   ExtRightBorder=buff[(size-1)*(100-InpBigVolume)/100];
//--- successful execution
   return(true);
  }
//+------------------------------------------------------------------+
//| Receive the data that is one month less than the passed one      |
//+------------------------------------------------------------------+
datetime GetStartTime(const datetime stop_time)
  {
//--- convert end time into MqlDateTime type structure variable
   MqlDateTime temp;
   TimeToStruct(stop_time,temp);
//--- receive the data that is one month less
   if(temp.mon>1)
      temp.mon-=1;  // the current month is not the first one in the year, therefore, the number of the previous one is one less
   else
     {
      temp.mon=12;  // the current month is the first in the year, therefore, the number of the previous one is 12,
      temp.year-=1; // while the year number is one less
     }
//--- day number will not exceed 28
   if(temp.day>28)
      temp.day=28;
//--- return the obtained date
   return(StructToTime(temp));
  }
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- check if input parameters satisfy the conditions
   if(InpSmallVolume<0 || InpSmallVolume>=50 || InpBigVolume<0 || InpBigVolume>=50)
     {
      Print("Incorrect input parameters");
      return(INIT_PARAMETERS_INCORRECT);
     }
//--- indicator buffers mapping
   SetIndexBuffer(0,ExtOpenBuff);
   SetIndexBuffer(1,ExtHighBuff);
   SetIndexBuffer(2,ExtLowBuff);
   SetIndexBuffer(3,ExtCloseBuff);
   SetIndexBuffer(4,ExtColorBuff,INDICATOR_COLOR_INDEX);
//--- set the value that will not be displayed
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,INDICATOR_EMPTY_VALUE);
//--- set labels for indicator buffers
   PlotIndexSetString(0,PLOT_LABEL,"Open;High;Low;Close");
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
//--- check if unhandled bars are still present
   if(prev_calculated<rates_total)
     {
      //--- receive new values of the right and left borders for volumes
      if(!GetVolumeBorders())
         return(0);
     }
//--- start variable for bar calculation
   int start=prev_calculated;
//--- work at the last bar if the indicator values have already been calculated at the previous tick
   if(start>0)
      start--;
//--- set direct indexing in time series
   ArraySetAsSeries(time,false);
   ArraySetAsSeries(open,false);
   ArraySetAsSeries(high,false);
   ArraySetAsSeries(low,false);
   ArraySetAsSeries(close,false);
   ArraySetAsSeries(tick_volume,false);
//--- the loop of calculation of the indicator values
   for(int i=start;i<rates_total;i++)
     {
      //--- fill out candlesticks starting from the initial date
      if(ExtStartTime<=time[i])
        {
         //--- if the value is not less than the right border, fill out the candlestick
         if(tick_volume[i]>=ExtRightBorder)
           {
            //--- receive data for drawing the candlestick
            ExtOpenBuff[i]=open[i];
            ExtHighBuff[i]=high[i];
            ExtLowBuff[i]=low[i];
            ExtCloseBuff[i]=close[i];
            //--- DodgerBlue color
            ExtColorBuff[i]=0;
            //--- continue the loop
            continue;
           }
         //--- fill out the candlestick if the value does not exceed the left border
         if(tick_volume[i]<=ExtLeftBorder)
           {
            //--- receive data for drawing the candlestick
            ExtOpenBuff[i]=open[i];
            ExtHighBuff[i]=high[i];
            ExtLowBuff[i]=low[i];
            ExtCloseBuff[i]=close[i];
            //--- Orange color
            ExtColorBuff[i]=1;
            //--- continue the loop
            continue;
           }
        }
      //--- set empty values for bars that have not been included in the calculation
      ExtOpenBuff[i]=INDICATOR_EMPTY_VALUE;
      ExtHighBuff[i]=INDICATOR_EMPTY_VALUE;
      ExtLowBuff[i]=INDICATOR_EMPTY_VALUE;
      ExtCloseBuff[i]=INDICATOR_EMPTY_VALUE;
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```

See also

[ArrayBsearch](/en/docs/array/arraybsearch)
