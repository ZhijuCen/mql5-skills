# iStochastic

The function returns the handle of the Stochastic Oscillator indicator.

```
int  iStochastic(
   string           symbol,          // symbol name
   ENUM_TIMEFRAMES  period,          // period
   int              Kperiod,         // K-period (number of bars for calculations)
   int              Dperiod,         // D-period (period of first smoothing)
   int              slowing,         // final smoothing
   ENUM_MA_METHOD   ma_method,       // type of smoothing
   ENUM_STO_PRICE   price_field      // stochastic calculation method
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

Kperiod

[in]  Averaging period (bars count) for the %K line calculation.

Dperiod

[in]  Averaging period (bars count) for the %D line calculation.

slowing

[in]  Slowing value.

ma_method

[in]  Type of averaging. Can be any of the [ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method) values.

price_field

[in]  Parameter of price selection for calculations. Can be one of the [ENUM_STO_PRICE](/en/docs/constants/indicatorconstants/prices#enum_sto_price_enum) values.

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Note

The buffer numbers: 0 - MAIN_LINE, 1 - SIGNAL_LINE.

Example:

```
//+------------------------------------------------------------------+
//|                                             Demo_iStochastic.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iStochastic technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
#property description "All the other parameters are similar to the standard Stochastic Oscillator."
 
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   2
//--- the Stochastic plot
#property indicator_label1  "Stochastic"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrLightSeaGreen
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- the Signal plot
#property indicator_label2  "Signal"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrRed
#property indicator_style2  STYLE_SOLID
#property indicator_width2  1
//--- set limit of the indicator values
#property indicator_minimum 0
#property indicator_maximum 100
//--- horizontal levels in the indicator window
#property indicator_level1  -100.0
#property indicator_level2  100.0
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iStochastic,       // use iStochastic
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iStochastic;     // type of the function 
input int                  Kperiod=5;                 // the K period (the number of bars for calculation)
input int                  Dperiod=3;                 // the D period (the period of primary smoothing)
input int                  slowing=3;                 // period of final smoothing      
input ENUM_MA_METHOD       ma_method=MODE_SMA;        // type of smoothing   
input ENUM_STO_PRICE       price_field=STO_LOWHIGH;   // method of calculation of the Stochastic
input string               symbol=" ";                // symbol 
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;     // timeframe
//--- indicator buffers
double         StochasticBuffer[];
double         SignalBuffer[];
//--- variable for storing the handle of the iStochastic indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- we will keep the number of values in the Stochastic Oscillator indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of arrays to indicator buffers
   SetIndexBuffer(0,StochasticBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,SignalBuffer,INDICATOR_DATA);
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
   if(type==Call_iStochastic)
      handle=iStochastic(name,period,Kperiod,Dperiod,slowing,ma_method,price_field);
   else
     {
      //--- fill the structure with parameters of the indicator     
      MqlParam pars[5];
      //--- the K period for calculations
      pars[0].type=TYPE_INT;
      pars[0].integer_value=Kperiod;
      //--- the D period for primary smoothing
      pars[1].type=TYPE_INT;
      pars[1].integer_value=Dperiod;
      //--- the K period for final smoothing
      pars[2].type=TYPE_INT;
      pars[2].integer_value=slowing;
      //--- type of smoothing
      pars[3].type=TYPE_INT;
      pars[3].integer_value=ma_method;
      //--- method of calculation of the Stochastic
      pars[4].type=TYPE_INT;
      pars[4].integer_value=price_field;
      handle=IndicatorCreate(name,period,IND_STOCHASTIC,5,pars);
     }
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create handle of the iStochastic indicator for the symbol %s/%s, error code %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Stochastic Oscillator indicator is calculated for
   short_name=StringFormat("iStochastic(%s/%s, %d, %d, %d, %s, %s)",name,EnumToString(period),
                           Kperiod,Dperiod,slowing,EnumToString(ma_method),EnumToString(price_field));
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
//--- number of values copied from the iStochastic indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iStochastic indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the StochasticBuffer array is greater than the number of values in the iStochastic indicator for symbol/period, then we don't copy everything 
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
//--- fill the arrays with values of the iStochastic indicator
//--- if FillArraysFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArraysFromBuffers(StochasticBuffer,SignalBuffer,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Stochastic Oscillator indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iStochastic indicator         |
//+------------------------------------------------------------------+
bool FillArraysFromBuffers(double &main_buffer[],    // indicator buffer of Stochastic Oscillator values
                           double &signal_buffer[],  // indicator buffer of the signal line
                           int ind_handle,           // handle of the iStochastic indicator
                           int amount                // number of copied values
                           )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the StochasticBuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,MAIN_LINE,0,amount,main_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iStochastic indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
//--- fill a part of the SignalBuffer array with values from the indicator buffer that has index 1
   if(CopyBuffer(ind_handle,SIGNAL_LINE,0,amount,signal_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iStochastic indicator, error code %d",GetLastError());
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
