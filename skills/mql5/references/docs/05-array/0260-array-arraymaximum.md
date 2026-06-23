# ArrayMaximum

Searches for the largest element in the first dimension of a multidimensional numeric array.

```
int  ArrayMaximum(
   const void&   array[],             // array for search
   int           start=0,             // index to start checking with
   int           count=WHOLE_ARRAY    // number of checked elements
   );

```

Parameters

array[]

[in]  A numeric array, in which search is made.

start=0

[in]  Index to start checking with.

count=WHOLE_ARRAY

[in]  Number of elements for search. By default, searches in the entire array (count=[WHOLE_ARRAY](/en/docs/constants/namedconstants/otherconstants)).

Return Value

The function returns an index of a found element taking into account the array [serial](/en/docs/array/arraygetasseries). In case of failure it returns -1.

Note

The [AS_SERIES](/en/docs/array/arraygetasseries) flag value is taken into account while searching for a maximum.

Functions ArrayMaximum and ArrayMinimum accept any-dimensional arrays as a parameter. However, searching is always applied to the first (zero) dimension.

Example:

```
#property description "The indicator displays larger timeframe's candlesticks on the current one."
//--- indicator settings
#property indicator_chart_window
#property indicator_buffers 16
#property indicator_plots   8
//---- plot 1
#property indicator_label1  "BearBody"
#property indicator_color1  clrSeaGreen,clrSeaGreen
//---- plot 2
#property indicator_label2  "BearBodyEnd"
#property indicator_color2  clrSeaGreen,clrSeaGreen
//---- plot 3
#property indicator_label3  "BearShadow"
#property indicator_color3  clrSalmon,clrSalmon
//---- plot 4
#property indicator_label4  "BearShadowEnd"
#property indicator_color4  clrSalmon,clrSalmon
//---- plot 5
#property indicator_label5  "BullBody"
#property indicator_color5  clrOlive,clrOlive
//---- plot 6
#property indicator_label6  "BullBodyEnd"
#property indicator_color6  clrOlive,clrOlive
//---- plot 7
#property indicator_label7  "BullShadow"
#property indicator_color7  clrSkyBlue,clrSkyBlue
//---- plot 8
#property indicator_label8  "BullShadowEnd"
#property indicator_color8  clrSkyBlue,clrSkyBlue
//--- predefined constant
#define INDICATOR_EMPTY_VALUE 0.0
//--- input parameters
input ENUM_TIMEFRAMES InpPeriod=PERIOD_H4;              // Time frame for the indicator calculation
input datetime        InpDateStart=D'2013.01.01 00:00'; // Analysis start date
//--- indicator buffers for bearish candlesticks
double   ExtBearBodyFirst[];
double   ExtBearBodySecond[];
double   ExtBearBodyEndFirst[];
double   ExtBearBodyEndSecond[];
double   ExtBearShadowFirst[];
double   ExtBearShadowSecond[];
double   ExtBearShadowEndFirst[];
double   ExtBearShadowEndSecond[];
//--- indicator buffers for bullish candlesticks
double   ExtBullBodyFirst[];
double   ExtBullBodySecond[];
double   ExtBullBodyEndFirst[];
double   ExtBullBodyEndSecond[];
double   ExtBullShadowFirst[];
double   ExtBullShadowSecond[];
double   ExtBullShadowEndFirst[];
double   ExtBullShadowEndSecond[];
//--- global variables
datetime ExtTimeBuff[];      // larger time frame's time buffer
int      ExtSize=0;          // time buffer size
int      ExtCount=0;         // index inside time buffer
int      ExtStartPos=0;      // initial position for the indicator calculation
bool     ExtStartFlag=true;  // auxiliary flag for receiving the initial position
datetime ExtCurrentTime[1];  // last time of the larger time frame's bar generation
datetime ExtLastTime;        // last time from the larger time frame, for which the calculation is performed
bool     ExtBearFlag=true;   // flag for defining the order of writing the data to bearish indicator buffers
bool     ExtBullFlag=true;   // flag for defining the order of writing the data to bullish indicator buffers
int      ExtIndexMax=0;      // index of the maximum element in the array
int      ExtIndexMin=0;      // index of the minimum element in the array
int      ExtDirectionFlag=0; // price movement direction for the current candlestick
//--- shift between the candlestick's open and close price for correct drawing
const double ExtEmptyBodySize=0.2*SymbolInfoDouble(Symbol(),SYMBOL_POINT);
//+------------------------------------------------------------------+
//| Filling the basic part of the candlestick                        |
//+------------------------------------------------------------------+
void FillCandleMain(const double &open[],const double &close[],
                    const double &high[],const double &low[],
                    const int start,const int last,const int fill_index,
                    int &index_max,int &index_min)
  {
//--- find the index of the maximum and minimum elements in the arrays
   index_max=ArrayMaximum(high,ExtStartPos,last-start+1); // maximum in High
   index_min=ArrayMinimum(low,ExtStartPos,last-start+1);  // minimum in Low
//--- define how many bars from the current time frame are to be filled out
   int count=fill_index-start+1;
//--- if the close price at the first bar exceeds the one at the last bar, the candlestick is bearish
   if(open[start]>close[last])
     {
      //--- if the candlestick has been bullish before that, clear the values of bullish indicator buffers
      if(ExtDirectionFlag!=-1)
         ClearCandle(ExtBullBodyFirst,ExtBullBodySecond,ExtBullShadowFirst,ExtBullShadowSecond,start,count);
      //--- bearish candlestick
      ExtDirectionFlag=-1;
      //--- generate the candlestick
      FormCandleMain(ExtBearBodyFirst,ExtBearBodySecond,ExtBearShadowFirst,ExtBearShadowSecond,open[start],
                     close[last],high[index_max],low[index_min],start,count,ExtBearFlag);
      //--- exit the function
      return;
     }
//--- if the close price at the first bar is less than the one at the last bar, the candlestick is bullish
   if(open[start]<close[last])
     {
      //--- if the candlestick has been bearish before that, clear the values of bearish indicator buffers
      if(ExtDirectionFlag!=1)
         ClearCandle(ExtBearBodyFirst,ExtBearBodySecond,ExtBearShadowFirst,ExtBearShadowSecond,start,count);
      //--- bullish candlestick
      ExtDirectionFlag=1;
      //--- generate the candlestick
      FormCandleMain(ExtBullBodyFirst,ExtBullBodySecond,ExtBullShadowFirst,ExtBullShadowSecond,close[last],
                     open[start],high[index_max],low[index_min],start,count,ExtBullFlag);
      //--- exit the function             
      return;
     }
//--- if you are in this part of the function, the open price at the first bar is equal to
//--- the close price at the last bar; such candlestick is considered bearish
//--- if the candlestick has been bullish before that, clear the values of bullish indicator buffers
   if(ExtDirectionFlag!=-1)
      ClearCandle(ExtBullBodyFirst,ExtBullBodySecond,ExtBullShadowFirst,ExtBullShadowSecond,start,count);
//--- bearish candlestick
   ExtDirectionFlag=-1;
//--- if close and open prices are equal, use the shift for correct display
   if(high[index_max]!=low[index_min])
      FormCandleMain(ExtBearBodyFirst,ExtBearBodySecond,ExtBearShadowFirst,ExtBearShadowSecond,open[start],
                     open[start]-ExtEmptyBodySize,high[index_max],low[index_min],start,count,ExtBearFlag);
   else
      FormCandleMain(ExtBearBodyFirst,ExtBearBodySecond,ExtBearShadowFirst,ExtBearShadowSecond,
                     open[start],open[start]-ExtEmptyBodySize,high[index_max],
                     high[index_max]-ExtEmptyBodySize,start,count,ExtBearFlag);
  }
//+------------------------------------------------------------------+
//| Fill out the end of the candlestick                              |
//+------------------------------------------------------------------+
void FillCandleEnd(const double &open[],const double &close[],
                   const double &high[],const double &low[],
                   const int start,const int last,const int fill_index,
                   const int index_max,const int index_min)
  {
//--- do not draw in case of a single bar
   if(last-start==0)
      return;
//--- if the close price at the first bar exceeds the one at the last bar, the candlestick is bearish
   if(open[start]>close[last])
     {
      //--- generate the end of the candlestick
      FormCandleEnd(ExtBearBodyEndFirst,ExtBearBodyEndSecond,ExtBearShadowEndFirst,ExtBearShadowEndSecond,
                    open[start],close[last],high[index_max],low[index_min],fill_index,ExtBearFlag);
      //--- exit the function
      return;
     }
//--- if the close price at the first bar is less than the one at the last bar, the candlestick is bullish
   if(open[start]<close[last])
     {
      //--- generate the end of the candlestick
      FormCandleEnd(ExtBullBodyEndFirst,ExtBullBodyEndSecond,ExtBullShadowEndFirst,ExtBullShadowEndSecond,
                    close[last],open[start],high[index_max],low[index_min],fill_index,ExtBullFlag);
      //--- exit the function
      return;
     }
//--- if you are in this part of the function, the open price at the first bar is equal to
//--- the close price at the last bar; such candlestick is considered bearish
//--- generate the end of the candlestick
   if(high[index_max]!=low[index_min])
      FormCandleEnd(ExtBearBodyEndFirst,ExtBearBodyEndSecond,ExtBearShadowEndFirst,ExtBearShadowEndSecond,open[start],
                    open[start]-ExtEmptyBodySize,high[index_max],low[index_min],fill_index,ExtBearFlag);
   else
      FormCandleEnd(ExtBearBodyEndFirst,ExtBearBodyEndSecond,ExtBearShadowEndFirst,ExtBearShadowEndSecond,open[start],
                    open[start]-ExtEmptyBodySize,high[index_max],high[index_max]-ExtEmptyBodySize,fill_index,ExtBearFlag);
  }
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- check the indicator period
   if(!CheckPeriod((int)Period(),(int)InpPeriod))
      return(INIT_PARAMETERS_INCORRECT);
//--- display price data in the foreground
   ChartSetInteger(0,CHART_FOREGROUND,0,1);
//--- binding indicator buffers
   SetIndexBuffer(0,ExtBearBodyFirst);
   SetIndexBuffer(1,ExtBearBodySecond);
   SetIndexBuffer(2,ExtBearBodyEndFirst);
   SetIndexBuffer(3,ExtBearBodyEndSecond);
   SetIndexBuffer(4,ExtBearShadowFirst);
   SetIndexBuffer(5,ExtBearShadowSecond);
   SetIndexBuffer(6,ExtBearShadowEndFirst);
   SetIndexBuffer(7,ExtBearShadowEndSecond);
   SetIndexBuffer(8,ExtBullBodyFirst);
   SetIndexBuffer(9,ExtBullBodySecond);
   SetIndexBuffer(10,ExtBullBodyEndFirst);
   SetIndexBuffer(11,ExtBullBodyEndSecond);
   SetIndexBuffer(12,ExtBullShadowFirst);
   SetIndexBuffer(13,ExtBullShadowSecond);
   SetIndexBuffer(14,ExtBullShadowEndFirst);
   SetIndexBuffer(15,ExtBullShadowEndSecond);
//--- set some property values for creating the indicator
   for(int i=0;i<8;i++)
     {
      PlotIndexSetInteger(i,PLOT_DRAW_TYPE,DRAW_FILLING); // graphical construction type
      PlotIndexSetInteger(i,PLOT_LINE_STYLE,STYLE_SOLID); // drawing line style
      PlotIndexSetInteger(i,PLOT_LINE_WIDTH,1);           // drawing line width
     }
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
//--- in case there are no calculated bars yet
   if(prev_calculated==0)
     {
      //--- receive larger time frame's bars arrival time
      if(!GetTimeData())
         return(0);
     }
//--- set direct indexing
   ArraySetAsSeries(time,false);
   ArraySetAsSeries(high,false);
   ArraySetAsSeries(low,false);
   ArraySetAsSeries(open,false);
   ArraySetAsSeries(close,false);
//--- start variable for calculation of bars
   int start=prev_calculated;
//--- if the bar is generated, recalculate the indicator value on it
   if(start!=0 && start==rates_total)
      start--;
//--- the loop for calculating the indicator values
   for(int i=start;i<rates_total;i++)
     {
      //--- fill i elements of the indicator buffers by empty values
      FillIndicatorBuffers(i);
      //--- perform calculation for bars starting from InpDateStart date
      if(time[i]>=InpDateStart)
        {
         //--- define position, from which the values are to be displayed, for the first time
         if(ExtStartFlag)
           {
            //--- store the number of the initial bar
            ExtStartPos=i;
            //--- define the first date from the larger time frame exceeding time[i]
            while(time[i]>=ExtTimeBuff[ExtCount])
               if(ExtCount<ExtSize-1)
                  ExtCount++;
            //--- change the value of the flag in order not to run into this block again
            ExtStartFlag=false;
           }
         //--- check if there are still any elements in the array
         if(ExtCount<ExtSize)
           {
            //--- wait for the current time frame's value to reach the larger time frame's one
            if(time[i]>=ExtTimeBuff[ExtCount])
              {
               //--- draw the main part of the candlestick (without filling out the area between the last and penultimate bar)
               FillCandleMain(open,close,high,low,ExtStartPos,i-1,i-2,ExtIndexMax,ExtIndexMin);
               //--- fill out the end of the candlestick (the area between the last and the penultimate bar)
               FillCandleEnd(open,close,high,low,ExtStartPos,i-1,i-1,ExtIndexMax,ExtIndexMin);
               //--- shift the initial position for drawing the next candlestick
               ExtStartPos=i;
               //--- increase the array counter
               ExtCount++;
              }
            else
               continue;
           }
         else
           {
            //--- reset the array values
            ResetLastError();
            //--- receive the last date from the larger time frame
            if(CopyTime(Symbol(),InpPeriod,0,1,ExtCurrentTime)==-1)
              {
               Print("Data copy error, code = ",GetLastError());
               return(0);
              }
            //--- if the new date is later, stop generating the candlestick
            if(ExtCurrentTime[0]>ExtLastTime)
              {
               //--- clear the area between the last and penultimate bars in the main indicator buffers
               ClearEndOfBodyMain(i-1);
               //--- fill out the area using auxiliary indicator buffers
               FillCandleEnd(open,close,high,low,ExtStartPos,i-1,i-1,ExtIndexMax,ExtIndexMin);
               //--- shift the initial position for drawing the next candlestick
               ExtStartPos=i;
               //--- reset price direction flag
               ExtDirectionFlag=0;
               //--- store the new last date
               ExtLastTime=ExtCurrentTime[0];
              }
            else
              {
               //--- generate the candlestick
               FillCandleMain(open,close,high,low,ExtStartPos,i,i,ExtIndexMax,ExtIndexMin);
              }
           }
        }
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Check correctness of the specified indicator period              |
//+------------------------------------------------------------------+
bool CheckPeriod(int current_period,int high_period)
  {
//--- the indicator period should exceed the timeframe on which it is displayed
   if(current_period>=high_period)
     {
      Print("Error! The value of the indicator period should exceed the value of the current time frame!");
      return(false);
     }
//--- if the indicator period is one week or month, the period is correct
   if(high_period>32768)
      return(true);
//--- convert period values to minutes
   if(high_period>30)
      high_period=(high_period-16384)*60;
   if(current_period>30)
      current_period=(current_period-16384)*60;
//--- the indicator period should be multiple of the time frame it is displayed on
   if(high_period%current_period!=0)
     {
      Print("Error! The value of the indicator period should be multiple of the value of the current time frame!");
      return(false);
     }
//--- the indicator period should exceed the time frame it is displayed on 3 or more times
   if(high_period/current_period<3)
     {
      Print("Error! The indicator period should exceed the current time frame 3 or more times!");
      return(false);
     }
//--- the indicator period is correct for the current time frame
   return(true);
  }
//+------------------------------------------------------------------+
//| Receive time data from the larger time frame                     |
//+------------------------------------------------------------------+
bool GetTimeData(void)
  {
//--- reset the error value
   ResetLastError();
//--- copy all data for the current time
   if(CopyTime(Symbol(),InpPeriod,InpDateStart,TimeCurrent(),ExtTimeBuff)==-1)
     {
      //--- receive the error code
      int code=GetLastError();
      //--- print out the error message
      PrintFormat("Data copy error! %s",code==4401
                  ? "History is still being uploaded!"
                  : "Code = "+IntegerToString(code));
      //--- return false to make a repeated attempt to download data
      return(false);
     }
//--- receive the array size
   ExtSize=ArraySize(ExtTimeBuff);
//--- set the loop index for the array to zero
   ExtCount=0;
//--- set the current candlestick's position on the time frame to zero
   ExtStartPos=0;
   ExtStartFlag=true;
//--- store the last time value from the larger time frame
   ExtLastTime=ExtTimeBuff[ExtSize-1];
//--- successful execution
   return(true);
  }
//+--------------------------------------------------------------------------+
//| Function forms the main part of the candlestick. Depending on the flag's |
//| value, the function defines what data and arrays are                     |
//| to be used for correct display.                                          |
//+--------------------------------------------------------------------------+
void FormCandleMain(double &body_fst[],double &body_snd[],
                    double &shadow_fst[],double &shadow_snd[],
                    const double fst_value,const double snd_value,
                    const double fst_extremum,const double snd_extremum,
                    const int start,const int count,const bool flag)
  {
//--- check the flag's value
   if(flag)
     {
      //--- generate the candlestick's body
      FormMain(body_fst,body_snd,fst_value,snd_value,start,count);
      //--- generate the candlestick's shadow
      FormMain(shadow_fst,shadow_snd,fst_extremum,snd_extremum,start,count);
     }
   else
     {
      //--- generate the candlestick's body
      FormMain(body_fst,body_snd,snd_value,fst_value,start,count);
      //--- generate the candlestick's shadow
      FormMain(shadow_fst,shadow_snd,snd_extremum,fst_extremum,start,count);
     }
  }
//+-------------------------------------------------------------------------------+
//| The function forms the end of the candlestick. Depending on the flag's value, |
//| the function defines what data and arrays are                                 |
//| to be used for correct display.                                               |
//+-------------------------------------------------------------------------------+
void FormCandleEnd(double &body_fst[],double &body_snd[],
                   double &shadow_fst[],double &shadow_snd[],
                   const double fst_value,const double snd_value,
                   const double fst_extremum,const double snd_extremum,
                   const int end,bool &flag)
  {
//--- check the flag's value
   if(flag)
     {
      //--- generate the end of the candlestick's body
      FormEnd(body_fst,body_snd,fst_value,snd_value,end);
      //--- generate the end of the candlestick's shadow
      FormEnd(shadow_fst,shadow_snd,fst_extremum,snd_extremum,end);
      //--- change the flag's value to the opposite one
      flag=false;
     }
   else
     {
      //--- generate the end of the candlestick's body
      FormEnd(body_fst,body_snd,snd_value,fst_value,end);
      //--- generate the end of the candlestick's shadow
      FormEnd(shadow_fst,shadow_snd,snd_extremum,fst_extremum,end);
      //--- change the flag's value to the opposite one
      flag=true;
     }
  }
//+---------------------------------------------------------------------------------+
//| Clear the end of the candlestick (the area between the last and the penultimate |
//| bar)                                                                            |
//+---------------------------------------------------------------------------------+
void ClearEndOfBodyMain(const int ind)
  {
   ClearCandle(ExtBearBodyFirst,ExtBearBodySecond,ExtBearShadowFirst,ExtBearShadowSecond,ind,1);
   ClearCandle(ExtBullBodyFirst,ExtBullBodySecond,ExtBullShadowFirst,ExtBullShadowSecond,ind,1);
  }
//+--------------------------------------------------------------------------+
//| Clear the candlestick                                                    |
//+--------------------------------------------------------------------------+
void ClearCandle(double &body_fst[],double &body_snd[],double &shadow_fst[],
                 double &shadow_snd[],const int start,const int count)
  {
//--- check
   if(count!=0)
     {
      //--- fill indicator buffers with empty values
      ArrayFill(body_fst,start,count,INDICATOR_EMPTY_VALUE);
      ArrayFill(body_snd,start,count,INDICATOR_EMPTY_VALUE);
      ArrayFill(shadow_fst,start,count,INDICATOR_EMPTY_VALUE);
      ArrayFill(shadow_snd,start,count,INDICATOR_EMPTY_VALUE);
     }
  }
//+--------------------------------------------------------------------------+
//| Generate the main part of the candlestick                                |
//+--------------------------------------------------------------------------+
void FormMain(double &fst[],double &snd[],const double fst_value,
              const double snd_value,const int start,const int count)
  {
//--- check
   if(count!=0)
     {
      //--- fill indicator buffers with values
      ArrayFill(fst,start,count,fst_value);
      ArrayFill(snd,start,count,snd_value);
     }
  }
//+-----------------------------------------------------------------------------+
//| Generate the end of the candlestick                                         |
//+-----------------------------------------------------------------------------+
void FormEnd(double &fst[],double &snd[],const double fst_value,
             const double snd_value,const int last)
  {
//--- fill indicator buffers with values
   ArrayFill(fst,last-1,2,fst_value);
   ArrayFill(snd,last-1,2,snd_value);
  }
//+------------------------------------------------------------------+
//| Fill i element of the indicator buffers by empty values          |
//+------------------------------------------------------------------+
void FillIndicatorBuffers(const int i)
  {
//--- set an empty value in the cell of the indicator buffers
   ExtBearBodyFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBearBodySecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBearShadowFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBearShadowSecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBearBodyEndFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBearBodyEndSecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBearShadowEndFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBearShadowEndSecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBullBodyFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBullBodySecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBullShadowFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBullShadowSecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBullBodyEndFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBullBodyEndSecond[i]=INDICATOR_EMPTY_VALUE;
   ExtBullShadowEndFirst[i]=INDICATOR_EMPTY_VALUE;
   ExtBullShadowEndSecond[i]=INDICATOR_EMPTY_VALUE;
  }

```
