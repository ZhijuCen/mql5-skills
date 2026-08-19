# OnCalculate

The function is called in the indicators when the [Calculate](/en/docs/runtime/event_fire#calculate) event occurs for processing price data changes. There are two function types. Only one of them can be used within a single indicator.

Calculation based on data array

```
int  OnCalculate(
   const int        rates_total,       // price[] array size
   const int        prev_calculated,   // number of handled bars at the previous call
   const int        begin,             // index number in the price[] array meaningful data starts from
   const double&    price[]            // array of values for calculation
   );

```

Calculations based on the current timeframe timeseries

```
int  OnCalculate(
   const int        rates_total,       // size of input time series
   const int        prev_calculated,   // number of handled bars at the previous call
   const datetime&  time[],            // Time array
   const double&    open[],            // Open array
   const double&    high[],            // High array
   const double&    low[],             // Low array
   const double&    close[],           // Close array
   const long&      tick_volume[],     // Tick Volume array
   const long&      volume[],          // Real Volume array
   const int&       spread[]           // Spread array
   );

```

Parameters

rates_total

[in]  Size of the price[] array or input series available to the indicator for calculation. In the second function type, the parameter value corresponds to the number of bars on the chart it is launched at.

prev_calculated

[in] Contains the value returned by the OnCalculate() function during the previous call. It is designed to skip the bars that have not changed since the previous launch of this function.

begin

[in]  Index value in the price[] array meaningful data starts from. It allows you to skip missing or initial data, for which there are no correct values.

price[]

[in]  Array of values for calculations. One of the price [timeseries](/en/docs/series) or a calculated indicator buffer can be passed as the price[] array. Type of data passed for calculation can be defined using the [_AppliedTo](/en/docs/predefined/_appliedto) predefined variable.

time{}

[in]  Array with bar open time values.

open[]

[in]  Array with Open price values.

high[]

[in]  Array with High price values.

low[]

[in]  Array with Low price values.

close[]

[in]  Array with Close price values.

tick_volume[]

[in]  Array with tick volume values.

volume[]

[in]  Array with trade volume values.

spread[]

[in]  Array with spread values for bars.

Return Value

int type value to be passed as the prev_calculated parameter during the next function call.

Note

If the OnCalculate() function is equal to zero, no indicator values are shown in the DataWindow of the client terminal.

If the price data have been changed since the last call of the OnCalculate() function (a deeper history has been loaded or gaps in the history have been filled), the value of the prev_calculated input parameter is set to zero by the terminal itself.

To define the indexing direction in the time[], open[], high[], low[], close[], tick_volume[], volume[] and spread[] arrays, call the [ArrayGetAsSeries()](/en/docs/array/arraygetasseries) function. In order not to depend on defaults, call the [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function for the arrays to work with.

When using the first function type, a necessary timeseries or indicator is selected by a user as the price[] array in the Parameters tab when launching the indicator. To do this, specify the necessary element in the drop-down list of the ["Apply to"](/en/docs/basis/function/events#oncalculate2) field.

To get [custom indicator](/en/docs/customind) values from other mql5 programs, the [iCustom()](/en/docs/indicators/icustom) function is used. It returns the indicator handle for subsequent operations. It is also possible to specify the required price [] array or the handle of another indicator. This parameter should be passed the last in the list of input variables of a custom indicator.

It is necessary to use the connection between the value returned by the OnCalculate() function and the prev_calculated second input parameter. When calling the function, the prev_calculated parameter contains the value returned by the OnCalculate() function during the previous call. This makes it possible to implement resource-saving algorithms for calculating a custom indicator in order to avoid repetitive calculations for the bars that have not changed since the previous launch of this function.

Sample indicator

```
//+------------------------------------------------------------------+
//|                                           OnCalculate_Sample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Sample Momentum indicator calculation"
 
//---- indicator settings
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
#property indicator_type1   DRAW_LINE
#property indicator_color1  Blue
//---- inputs
input int MomentumPeriod=14; // Calculation period
//---- indicator buffer
double    MomentumBuffer[];
//--- global variable for storing calculation period
int       IntPeriod;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- check the input parameter
   if(MomentumPeriod<0)
     {
      IntPeriod=14;
      Print("Period parameter has an incorrect value. The following value is to be used for calculations ",IntPeriod);
     }
   else
      IntPeriod=MomentumPeriod;
//---- buffers  
   SetIndexBuffer(0,MomentumBuffer,INDICATOR_DATA);
//---- indicator name to be displayed in DataWindow and subwindow
   IndicatorSetString(INDICATOR_SHORTNAME,"Momentum"+"("+string(IntPeriod)+")");
//--- set index of the bar the drawing starts from
   PlotIndexSetInteger(0,PLOT_DRAW_BEGIN,IntPeriod-1);
//--- set 0.0 as an empty value that is not drawn
   PlotIndexSetDouble(0,PLOT_EMPTY_VALUE,0.0);
//--- indicator accuracy to be displayed
   IndicatorSetInteger(INDICATOR_DIGITS,2);
  }
//+------------------------------------------------------------------+
//|  Momentum indicator calculation                                  |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,     // price[] array size 
                const int prev_calculated, // number of previously handled bars
                const int begin,           // where significant data start from 
                const double &price[])     // value array for handling
  {
//--- initial position for calculations
   int StartCalcPosition=(IntPeriod-1)+begin;
//---- if calculation data is insufficient
   if(rates_total<StartCalcPosition)
      return(0);  // exit with a zero value - the indicator is not calculated
//--- correct draw begin
   if(begin>0)
      PlotIndexSetInteger(0,PLOT_DRAW_BEGIN,StartCalcPosition+(IntPeriod-1));
//--- start calculations, define the starting position
   int pos=prev_calculated-1;
   if(pos<StartCalcPosition)
      pos=begin+IntPeriod;
//--- main calculation loop
   for(int i=pos;i<rates_total && !IsStopped();i++)
      MomentumBuffer[i]=price[i]*100/price[i-IntPeriod];
//--- OnCalculate execution is complete. Return the new prev_calculated value for the subsequent call
   return(rates_total);
  }

```

See also

[ArrayGetAsSeries](/en/docs/array/arraygetasseries), [ArraySetAsSeries](/en/docs/array/arraysetasseries), [iCustom](/en/docs/indicators/icustom), [Event handling functions](/en/docs/basis/function/events), [Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire), [Access to timeseries and indicators](/en/docs/series)
