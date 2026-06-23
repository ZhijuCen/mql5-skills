# ObjectGetDouble

The function returns the value of the corresponding object property. The object property must be of the [double](/en/docs/basis/types/double) type. There are 2 variants of the function.

1. Immediately returns the property value.

```
double  ObjectGetDouble(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_DOUBLE     prop_id,           // property identifier
   int                             prop_modifier=0    // property modifier, if required
   );

```

2. Returns true or false, depending on the success of the function. If successful, the property value is placed to a receiving variable passed by reference by the last parameter.

```
bool  ObjectGetDouble(
   long                            chart_id,          // chart identifier
   string                          name,              // object name
   ENUM_OBJECT_PROPERTY_DOUBLE     prop_id,           // property identifier
   int                             prop_modifier,     // property modifier
   double&                         double_var         // here we accept the property value
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of the object.

prop_id

[in]  ID of the object property. The value can be one of the values of the [ENUM_OBJECT_PROPERTY_DOUBLE](/en/docs/constants/objectconstants/enum_object_property#enum_object_property_double) enumeration.

prop_modifier

[in]  Modifier of the specified property. For the first variant, the default modifier value is equal to 0. Most properties do not require a modifier.  It denotes the number of the level in [Fibonacci tools](/en/docs/constants/objectconstants/enum_object) and in the graphical object Andrew's pitchfork. The numeration of levels starts from zero.

double_var

[out]  Variable of the double type that received the value of the requested property.

Return Value

Value of the double type for the first calling variant.

For the second variant the function returns true, if this property is maintained and the value has been placed into the double_var variable, otherwise returns false. To read more about the [error](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

The function uses a synchronous call, which means that the function waits for the execution of all commands that have been enqueued for this chart prior to its call, that is why this function can be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   OBJ_NAME   "TestObjectGetDouble"   // Object name
#define   WND        0                       // Chart subwindow
#define   EXT        " (%$)"                 // Format string for displaying price values at levels
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- current chart ID, the chart symbol, and symbol Digits
   long   chart_id= ChartID();
   string symbol  = ChartSymbol(chart_id);
   int    digits  = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   
//--- construct the Fibonacci Levels graphical object at the maximum and minimum prices of the visible chart
   if(!CreateFibo(chart_id))
      return;
      
//--- number of object levels
   int total=(int)ObjectGetInteger(chart_id, OBJ_NAME, OBJPROP_LEVELS);
   double value =0;
   double price0=0;
   double price1=0;
   
//--- anchor point prices
   price0=ObjectGetDouble(chart_id, OBJ_NAME, OBJPROP_PRICE, 0);
   price1=ObjectGetDouble(chart_id, OBJ_NAME, OBJPROP_PRICE, 1);
   
//--- in a loop by the number of object levels
   for(int i=0; i<total; i++)
     {
      //--- get the value set for the current level
      ResetLastError();
      if(!ObjectGetDouble(chart_id, OBJ_NAME, OBJPROP_LEVELVALUE, i, value))
        {
         Print("ObjectGetDouble() failed. Error ", GetLastError());
         return;
        }
      
      //--- get the maximum and minimum prices of the object binding and the distance between them in the price value
      double max=fmax(price0, price1);
      double min=fmin(price0, price1);
      double range=max-min;
      
      //--- calculate the price value for the current level of the object
      double level_price=min+range*value;
      
      //--- set the color for the level so that it is visible on both dark and light backgrounds of the chart
      ObjectSetInteger(chart_id, OBJ_NAME, OBJPROP_LEVELCOLOR, i, clrRed);
      
      //--- set a format string for the level so that its price value is displayed along with the level value
      string level_text=ObjectGetString(chart_id, OBJ_NAME, OBJPROP_LEVELTEXT, i);
      if(StringFind(level_text, EXT)<0)
        {
         level_text+=EXT;
         ObjectSetString(chart_id, OBJ_NAME, OBJPROP_LEVELTEXT, i, level_text);
        }
      
      //--- output the level number and its data - the level value and its price - in the journal
      PrintFormat("Fibo level [%d] value: %.3f,  price: %.*f", i, value, digits, level_price);
     }
   /*
   result:
   Fibo level [0] value: 0.000,  price: 0.61989
   Fibo level [1] value: 0.236,  price: 0.62533
   Fibo level [2] value: 0.382,  price: 0.62869
   Fibo level [3] value: 0.500,  price: 0.63140
   Fibo level [4] value: 0.618,  price: 0.63412
   Fibo level [5] value: 1.000,  price: 0.64292
   Fibo level [6] value: 1.618,  price: 0.65715
   Fibo level [7] value: 2.618,  price: 0.68018
   Fibo level [8] value: 4.236,  price: 0.71745
   */
  }
//+------------------------------------------------------------------+
//| Create the Fibo levels graphical object on the specified chart |
//+------------------------------------------------------------------+
bool CreateFibo(const long chart_id)
  {
//--- draw Fibo levels from the highest to the lowest visible price values on the chart and get them
   double   price_high=0, price_low=0;
   datetime time_high =0, time_low =0;
   
   if(!GetChartExtremums(chart_id, price_high, price_low, time_high, time_low))
      return(false);
 
//--- construct the Fibo Levels object on the found price/time coordinates
   if(!ObjectCreate(chart_id, OBJ_NAME, OBJ_FIBO, WND, time_high, price_high, time_low, price_low))
     {
      PrintFormat("%s: ObjectCreate() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
     
//--- all is well - update the chart and return 'true'
   ChartRedraw();
   return(true);
  }
//+------------------------------------------------------------------+
//| Return the maximum and minimum prices on the chart and their time|
//+------------------------------------------------------------------+
bool GetChartExtremums(const long chart_id, double &price_high, double &price_low, datetime &time_high, datetime &time_low)
  {
//--- reset the variables
   price_high=price_low=0;
   time_high =time_low =0;
//--- chart symbol
   string symbol = ChartSymbol(chart_id);
 
//--- calculate the start of the range of copied timeseries based on the number of the first visible bar and the number of bars on the chart
   int first = (int)ChartGetInteger(chart_id, CHART_FIRST_VISIBLE_BAR);
   int count = (int)ChartGetInteger(chart_id, CHART_VISIBLE_BARS);
   int start = first+1-count;
   
//--- arrays where timeseries are to be copied
   double   array_high[];
   double   array_low[];
   datetime array_time[];
   int      index;
   
//--- copy three timeseries into arrays in the amount of 'count' and starting from 'start'
   ResetLastError();
   if(CopySeries(symbol, PERIOD_CURRENT, start, count, COPY_RATES_TIME|COPY_RATES_HIGH|COPY_RATES_LOW, array_time, array_high, array_low)!=count)
     {
      PrintFormat("%s: CopySeries() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   
//--- look for the maximum price index in the array_high array
   index=ArrayMaximum(array_high);
   if(index<0)
     {
      PrintFormat("%s: ArrayMaximum() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
//--- remember the highest price on the visible chart and the time value of the bar this price is located on
   price_high=array_high[index];
   time_high=array_time[index];
   
//--- look for the minimum price index in the array_low array
   index=ArrayMinimum(array_low);
   if(index<0)
     {
      PrintFormat("%s: ArrayMinimum() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
//--- remember the lowest price on the visible chart and the time value of the bar this price is located on
   price_low=array_low[index];
   time_low=array_time[index];
   
//--- all is fine
   return(true);
  }

```
