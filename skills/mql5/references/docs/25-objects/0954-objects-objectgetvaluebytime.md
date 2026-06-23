# ObjectGetValueByTime

The function returns the price value for the specified time value of the specified object.

```
double  ObjectGetValueByTime(
   long      chart_id,     // chart identifier
   string    name,         // object name
   datetime  time,         // Time
   int       line_id       // Line number
   );

```

Parameters

chart_id

[in]  Chart identifier. 0 means the current chart.

name

[in]  Name of the object.

time

[in]  Time value.

line_id

[in]  Line ID.

Return Value

The price value for the specified time value of the specified object.

Note

The function uses a synchronous call, which means that the function waits for the execution of all commands that have been enqueued for this chart prior to its call, that is why this function can be time consuming. This feature should be taken into account when working with a large number of objects on a chart.

An object can have several values in one price coordinate, therefore it is necessary to specify the line number. This function applies only to the following objects:

- Trendline (OBJ_TREND)
- Trendline by angle (OBJ_TRENDBYANGLE)
- Gann line (OBJ_GANNLINE)
- Equidistant channel (OBJ_CHANNEL) - 2 lines
- Linear regression channel (OBJ_REGRESSION) - 3 lines
- Standard deviation channel (OBJ_STDDEVCHANNEL) - 3 lines
- Arrowed line (OBJ_ARROWED_LINE)

Example:

```
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   OBJ_NAME   "TestObjectGetValueByTime" // graphical object name
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- chart ID, symbol
   long   chart_id=ChartID();
   string symbol=ChartSymbol(chart_id);
 
   long bar1=0, bar2=0, visible=0;
//--- get the first bar of the chart visible on the left
   ResetLastError();
   if(!ChartGetInteger(chart_id, CHART_FIRST_VISIBLE_BAR, 0, bar1))
     {
      Print("ChartGetInteger() failed. Error ", GetLastError());
      return;
     }
//--- number of visible bars on the chart
   if(!ChartGetInteger(chart_id, CHART_VISIBLE_BARS, 0, visible))
     {
      Print("ChartGetInteger() failed. Error ", GetLastError());
      return;
     }
 
//--- adjust the obtained values and calculate the index of the first bar visible on the right
   bar1-=1;
   visible-=2;
   bar2=bar1-visible;
 
//--- build an equidistant channel from the High of the left visible bar to the Low of the right one
   if(!CreateChannel(chart_id, (int)bar1, (int)bar2))
      return;
   
   int digits=(int)SymbolInfoInteger(symbol,SYMBOL_DIGITS);
   
//--- in a loop from the left visible bar to the right visible bar on the chart
//--- get the price value for the loop bar time of each equidistant channel line.
//--- display the received price for each line in the journal
   for(int i=(int)bar1; i>=bar2 && !IsStopped(); i--)
     {
      datetime time=GetTime(symbol, i);
      if(time==0)
         continue;
      
      string time_str=TimeToString(time);
      double value0=ObjectGetValueByTime(chart_id, OBJ_NAME, time, 0);
      double value1=ObjectGetValueByTime(chart_id, OBJ_NAME, time, 1);
      string idx=StringFormat("%03d", i);
      PrintFormat("[%s] For time %s the price value at 0 line of the object: %.*f, at line 1: %.*f",
                  idx, TimeToString(time), digits, value0, digits, value1);
     }
   
//--- wait 5 seconds and clean up
   Sleep(5000);
   ObjectDelete(chart_id, OBJ_NAME);
   ChartRedraw(chart_id);
   /*
   result:
   [114] For time 2025.01.02 05:00 the price value at 0 line of the object: 1.03732, at line 1: 1.03393
   [113] For time 2025.01.02 05:30 the price value at 0 line of the object: 1.03694, at line 1: 1.03355
   [112] For time 2025.01.02 06:00 the price value at 0 line of the object: 1.03657, at line 1: 1.03318
   [111] For time 2025.01.02 06:30 the price value at 0 line of the object: 1.03619, at line 1: 1.03280
   [110] For time 2025.01.02 07:00 the price value at 0 line of the object: 1.03581, at line 1: 1.03242
   [109] For time 2025.01.02 07:30 the price value at 0 line of the object: 1.03544, at line 1: 1.03205
   [108] For time 2025.01.02 08:00 the price value at 0 line of the object: 1.03506, at line 1: 1.03167
   [107] For time 2025.01.02 08:30 the price value at 0 line of the object: 1.03468, at line 1: 1.03129
   [106] For time 2025.01.02 09:00 the price value at 0 line of the object: 1.03431, at line 1: 1.03092
   [105] For time 2025.01.02 09:30 the price value at 0 line of the object: 1.03393, at line 1: 1.03054
   [104] For time 2025.01.02 10:00 the price value at 0 line of the object: 1.03355, at line 1: 1.03016
   [103] For time 2025.01.02 10:30 the price value at 0 line of the object: 1.03318, at line 1: 1.02979
   [102] For time 2025.01.02 11:00 the price value at 0 line of the object: 1.03280, at line 1: 1.02941
   [101] For time 2025.01.02 11:30 the price value at 0 line of the object: 1.03242, at line 1: 1.02903
   [100] For time 2025.01.02 12:00 the price value at 0 line of the object: 1.03205, at line 1: 1.02866
   [099] For time 2025.01.02 12:30 the price value at 0 line of the object: 1.03167, at line 1: 1.02828
   [098] For time 2025.01.02 13:00 the price value at 0 line of the object: 1.03129, at line 1: 1.02790
   [097] For time 2025.01.02 13:30 the price value at 0 line of the object: 1.03092, at line 1: 1.02753
   [096] For time 2025.01.02 14:00 the price value at 0 line of the object: 1.03054, at line 1: 1.02715
   [095] For time 2025.01.02 14:30 the price value at 0 line of the object: 1.03016, at line 1: 1.02677
   [094] For time 2025.01.02 15:00 the price value at 0 line of the object: 1.02979, at line 1: 1.02640
   [093] For time 2025.01.02 15:30 the price value at 0 line of the object: 1.02941, at line 1: 1.02602
   [092] For time 2025.01.02 16:00 the price value at 0 line of the object: 1.02903, at line 1: 1.02564
   [091] For time 2025.01.02 16:30 the price value at 0 line of the object: 1.02866, at line 1: 1.02527
   [090] For time 2025.01.02 17:00 the price value at 0 line of the object: 1.02828, at line 1: 1.02489
   [089] For time 2025.01.02 17:30 the price value at 0 line of the object: 1.02790, at line 1: 1.02451
   [088] For time 2025.01.02 18:00 the price value at 0 line of the object: 1.02753, at line 1: 1.02414
   [087] For time 2025.01.02 18:30 the price value at 0 line of the object: 1.02715, at line 1: 1.02376
   [086] For time 2025.01.02 19:00 the price value at 0 line of the object: 1.02677, at line 1: 1.02338
   [085] For time 2025.01.02 19:30 the price value at 0 line of the object: 1.02640, at line 1: 1.02301
   [084] For time 2025.01.02 20:00 the price value at 0 line of the object: 1.02602, at line 1: 1.02263
   */
  }
//+------------------------------------------------------------------+
//| Return the time of the bar specified by index                    |
//+------------------------------------------------------------------+
datetime GetTime(const string symbol_name, const int index)
  {
   if(index<0)
      return(0);
   datetime array[1];
   ResetLastError();
   if(CopyTime(symbol_name, PERIOD_CURRENT, index, 1, array)!=1)
     {
      PrintFormat("%s: CopyTime() failed. Error %d",__FUNCTION__, GetLastError());
      return(0);
     }
   return(array[0]);
  }
//+--------------------------------------------------------------------------------------------+
//| Construct an equidistant channel from the High of the left bar to the Low of the right bar |
//+--------------------------------------------------------------------------------------------+
bool CreateChannel(const long chart_id, const int bar1, const int bar2)
  {
   long     visible=0;
   datetime time1 =0, time2 =0;
   double   price1=0, price2=0;
 
//--- chart symbol
   string symbol=ChartSymbol(chart_id);
   
//--- get the time of the first bar visible on the left of the chart
   ResetLastError();
   datetime time_array[1];
   if(CopyTime(symbol, PERIOD_CURRENT, (int)bar1, 1, time_array)!=1)
     {
      PrintFormat("%s: CopyTime() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   time1=time_array[0];
   
//--- get the time of the first bar of the chart visible on the right
   if(CopyTime(symbol, PERIOD_CURRENT, (int)bar2, 1, time_array)!=1)
     {
      PrintFormat("%s: CopyTime() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   time2=time_array[0];
   
//--- get the High price of the first bar visible on the left of the chart
   double price_array[];
   if(CopyHigh(symbol, PERIOD_CURRENT, (int)bar1, 1, price_array)!=1)
     {
      PrintFormat("%s: CopyHigh() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   price1=price_array[0];
   
//--- get the Low price of the first bar visible on the right of the chart
   if(CopyLow(symbol, PERIOD_CURRENT, (int)bar2, 1, price_array)!=1)
     {
      PrintFormat("%s: CopyLow() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
   price2=price_array[0];
   
//--- calculate the price range of the chart in points
//--- for an equidistant channel, the distance of the second line will be 1/3 of the price range
   double range=price1-price2;
   double distance=range*0.3;
   
//--- at the calculated coordinates, create a graphical object - an equidistant channel
   if(!ObjectCreate(chart_id, OBJ_NAME, OBJ_CHANNEL, 0, time1, price1, time2, price2, time1, price1-distance))
     {
      PrintFormat("%s: ObjectCreate() failed. Error %d",__FUNCTION__, GetLastError());
      return(false);
     }
     
//--- update the chart and return 'true'
   ChartRedraw(chart_id);
   return(true);
  }

```

See also

[Object Types](/en/docs/constants/objectconstants/enum_object)
