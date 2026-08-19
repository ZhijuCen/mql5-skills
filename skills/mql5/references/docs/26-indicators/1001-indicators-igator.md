# iGator

The function returns the handle of the Gator indicator. The Oscillator shows the difference between the blue and red lines of Alligator (upper histogram) and difference between red and green lines (lower histogram).

```
int  iGator(
   string              symbol,            // symbol name
   ENUM_TIMEFRAMES     period,            // period
   int                 jaw_period,        // period for the calculation of the jaws
   int                 jaw_shift,         // jaws horizontal shift
   int                 teeth_period,      // period for the calculation of the teeth
   int                 teeth_shift,       // teeth horizontal shift
   int                 lips_period,       // period for the calculation of the lips
   int                 lips_shift,        // lips horizontal shift
   ENUM_MA_METHOD      ma_method,         // type of smoothing
   ENUM_APPLIED_PRICE  applied_price      // type of price or handle
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

jaw_period

[in]  Averaging period for the blue line (Alligator's Jaw).

jaw_shift

[in] The shift of the blue line relative to the price chart. It isn't directly connected with the visual shift of the indicator histogram.

teeth_period

[in]   Averaging period for the red line (Alligator's Teeth).

teeth_shift

[in] The shift of the red line relative to the price chart. It isn't directly connected with the visual shift of the indicator histogram.

lips_period

[in]  Averaging period for the green line (Alligator's lips).

lips_shift

[in] The shift of the green line relative to the price charts. It isn't directly connected with the visual shift of the indicator histogram.

ma_method

[in]  Smoothing type. Can be one of the values of [ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method).

applied_price

[in]  The price used. Can be any of the price constants [ENUM_APPLIED_PRICE](/en/docs/constants/indicatorconstants/prices#enum_applied_price_enum) or a handle of another indicator.

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Note

Buffer numbers: 0 - UPPER_HISTOGRAM, 1 - color buffer of the upper histogram, 2 - LOWER_HISTOGRAM, 3 - color buffer of the lower histogram.

Example:

```
//+------------------------------------------------------------------+
//|                                                  Demo_iGator.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iGator technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
#property description "All other parameters are as in a standard Gator Oscillator."
 
#property indicator_separate_window
#property indicator_buffers 4
#property indicator_plots   2
//--- drawing GatorUp
#property indicator_label1  "GatorUp"
#property indicator_type1   DRAW_COLOR_HISTOGRAM
#property indicator_color1  clrGreen, clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- drawing GatorDown
#property indicator_label2  "GatorDown"
#property indicator_type2   DRAW_COLOR_HISTOGRAM
#property indicator_color2  clrGreen, clrRed
#property indicator_style2  STYLE_SOLID
#property indicator_width2  1
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iGator,            // use iGator
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iGator;       // type of the function 
input string               symbol=" ";             // symbol
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;  // timeframe
input int                  jaw_period=13;          // period of the Jaw line
input int                  jaw_shift=8;            // shift of the Jaw line
input int                  teeth_period=8;         // period of the Teeth line
input int                  teeth_shift=5;          // shift of the Teeth line
input int                  lips_period=5;          // period of the Lips line
input int                  lips_shift=3;           // shift of the Lips line
input ENUM_MA_METHOD       MA_method=MODE_SMMA;    // method of averaging of the Alligator lines
input ENUM_APPLIED_PRICE   applied_price=PRICE_MEDIAN;// type of price used for calculation of Alligator
//--- indicator buffers
double         GatorUpBuffer[];
double         GatorUpColors[];
double         GatorDownBuffer[];
double         GatorDownColors[];
//--- variable for storing the handle of the iGator indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- shift values for the upper and lower histograms
int shift;
//--- we will keep the number of values in the Gator Oscillator indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of arrays to indicator buffers
   SetIndexBuffer(0,GatorUpBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,GatorUpColors,INDICATOR_COLOR_INDEX);
   SetIndexBuffer(2,GatorDownBuffer,INDICATOR_DATA);
   SetIndexBuffer(3,GatorDownColors,INDICATOR_COLOR_INDEX);
/*
  All the shifts specified in the parameters refer to the Alligator indicator on the basis which the Gator Oscillator is drawn!
  That's is why they don't move the Gator indicator itself, but they move the Alligator lines,
  which values are used for calculation of the Gator Oscillator!
*/
//--- let's calculate the shift for the upper and lower histograms, that is equal to the difference between the Jaw line and the Teeth line
   shift=MathMin(jaw_shift,teeth_shift);
   PlotIndexSetInteger(0,PLOT_SHIFT,shift);
//--- despite the indicator contains two histograms, the same shift is used - this is the implementation of the iGator indicator
   PlotIndexSetInteger(1,PLOT_SHIFT,shift);
 
//--- determine the symbol the indicator is drawn for
   name=symbol;
//--- delete spaces to the right and to the left
   StringTrimRight(name);
   StringTrimLeft(name);
//--- if it results in zero length of the 'name' string
   if(StringLen(name)==0)
     {
      //--- take the symbol of the chart the indicator is attached to
      name=_Symbol;
     }
//--- create handle of the indicator
   if(type==Call_iGator)
      handle=iGator(name,period,jaw_period,jaw_shift,teeth_period,teeth_shift,
                    lips_period,lips_shift,MA_method,applied_price);
   else
     {
      //--- fill the structure with parameters of the indicator
      MqlParam pars[8];
      //--- periods and shifts of the Alligator lines
      pars[0].type=TYPE_INT;
      pars[0].integer_value=jaw_period;
      pars[1].type=TYPE_INT;
      pars[1].integer_value=jaw_shift;
      pars[2].type=TYPE_INT;
      pars[2].integer_value=teeth_period;
      pars[3].type=TYPE_INT;
      pars[3].integer_value=teeth_shift;
      pars[4].type=TYPE_INT;
      pars[4].integer_value=lips_period;
      pars[5].type=TYPE_INT;
      pars[5].integer_value=lips_shift;
      //--- type of smoothing
      pars[6].type=TYPE_INT;
      pars[6].integer_value=MA_method;
      //--- type of price
      pars[7].type=TYPE_INT;
      pars[7].integer_value=applied_price;
      //--- create handle
      handle=IndicatorCreate(name,period,IND_GATOR,8,pars);
     }
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create handle of the iGator indicator for the symbol %s/%s, error code %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Gator Oscillator indicator is calculated for
   short_name=StringFormat("iGator(%s/%s, %d, %d ,%d, %d, %d, %d)",name,EnumToString(period),
                           jaw_period,jaw_shift,teeth_period,teeth_shift,lips_period,lips_shift);
   IndicatorSetString(INDICATOR_SHORTNAME,short_name);
//--- normal initialization of the indicator  
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
//--- number of values copied from the iGator indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iGator indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the GatorUpBuffer array is greater than the number of values in the iGator indicator for symbol/period, then we don't copy everything 
      //--- otherwise, we copy less than the size of indicator buffers
      if(calculated>rates_total) values_to_copy=rates_total;
      else                       values_to_copy=calculated;
     }
   else
     {
      //--- it means that it's not the first time of the indicator calculation, and since the last call of OnCalculate()
      //--- for calculation not more than one bar is added
      values_to_copy=(rates_total-prev_calculated)+1;
     }
//--- fill the arrays with values of the Gator Oscillator indicator
//--- if FillArraysFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArraysFromBuffers(GatorUpBuffer,GatorUpColors,GatorDownBuffer,GatorDownColors,
      shift,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Gator Oscillator indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iGator indicator              |
//+------------------------------------------------------------------+
bool FillArraysFromBuffers(double &ups_buffer[],         // indicator buffer for the upper histogram
                           double &up_color_buffer[],    // indicator buffer for price indexes of the upper histogram
                           double &downs_buffer[],       // indicator buffer for the lower histogram
                           double &downs_color_buffer[], // indicator buffer for price indexes of the lower histogram
                           int u_shift,                  // shift for the upper and lower histogram
                           int ind_handle,               // handle of the iGator indicator
                           int amount                    // number of copied values
                           )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the GatorUpBuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,0,-u_shift,amount,ups_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iGator indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
 
//--- fill a part of the GatorUpColors array with values from the indicator buffer that has index 1
   if(CopyBuffer(ind_handle,1,-u_shift,amount,up_color_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iGator indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
 
//--- fill a part of the GatorDownBuffer array with values from the indicator buffer that has index 2
   if(CopyBuffer(ind_handle,2,-u_shift,amount,downs_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iGator indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
 
//--- fill a part of the GatorDownColors array with values from the indicator buffer that has index 3
   if(CopyBuffer(ind_handle,3,-u_shift,amount,downs_color_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iGator indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
//--- everything is fine
   return(true);
  }
//+------------------------------------------------------------------+
//| Indicator deinitialization function                              |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   if(handle!=INVALID_HANDLE)
      IndicatorRelease(handle);
//--- clear the chart after deleting the indicator
   Comment("");
  }

```
