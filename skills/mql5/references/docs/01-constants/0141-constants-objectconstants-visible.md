# Visibility of Objects

The combination of object visibility flags determines chart timeframes, where the object is visible. To set/get the value of the OBJPROP_TIMEFRAMES property, you can use functions [ObjectSetInteger()](/en/docs/objects/objectsetinteger)/[ObjectGetInteger()](/en/docs/objects/objectgetinteger).

| ID | Value | Description |
| --- | --- | --- |
| OBJ_NO_PERIODS | 0 | The object is not drawn in all timeframes |
| OBJ_PERIOD_M1 | 0x00000001 | The object is drawn in 1-minute chart |
| OBJ_PERIOD_M2 | 0x00000002 | The object is drawn in 2-minute chart |
| OBJ_PERIOD_M3 | 0x00000004 | The object is drawn in 3-minute chart |
| OBJ_PERIOD_M4 | 0x00000008 | The object is drawn in 4-minute chart |
| OBJ_PERIOD_M5 | 0x00000010 | The object is drawn in 5-minute chart |
| OBJ_PERIOD_M6 | 0x00000020 | The object is drawn in 6-minute chart |
| OBJ_PERIOD_M10 | 0x00000040 | The object is drawn in 10-minute chart |
| OBJ_PERIOD_M12 | 0x00000080 | The object is drawn in 12-minute chart |
| OBJ_PERIOD_M15 | 0x00000100 | The object is drawn in 15-minute chart |
| OBJ_PERIOD_M20 | 0x00000200 | The object is drawn in 20-minute chart |
| OBJ_PERIOD_M30 | 0x00000400 | The object is drawn in 30-minute chart |
| OBJ_PERIOD_H1 | 0x00000800 | The object is drawn in 1-hour chart |
| OBJ_PERIOD_H2 | 0x00001000 | The object is drawn in 2-hour chart |
| OBJ_PERIOD_H3 | 0x00002000 | The object is drawn in 3-hour chart |
| OBJ_PERIOD_H4 | 0x00004000 | The object is drawn in 4-hour chart |
| OBJ_PERIOD_H6 | 0x00008000 | The object is drawn in 6-hour chart |
| OBJ_PERIOD_H8 | 0x00010000 | The object is drawn in 8-hour chart |
| OBJ_PERIOD_H12 | 0x00020000 | The object is drawn in 12-hour chart |
| OBJ_PERIOD_D1 | 0x00040000 | The object is drawn in day charts |
| OBJ_PERIOD_W1 | 0x00080000 | The object is drawn in week charts |
| OBJ_PERIOD_MN1 | 0x00100000 | The object is drawn in month charts |
| OBJ_ALL_PERIODS | 0x001fffff | The object is drawn in all timeframes |

Visibility flags can be combined using the symbol "|", for example, the combination of flags OBJ_PERIOD_M10|OBJ_PERIOD_H4 means that the object will be visible on the 10-minute and 4-hour timeframes.

Example:

```
void OnStart()
  {
//---
   string highlevel="PreviousDayHigh";
   string lowlevel="PreviousDayLow";
   double prevHigh;           // The previous day High
   double prevLow;            // The previous day Low
   double highs[],lows[];     // Arrays for High and Low
 
//--- Reset the last error
   ResetLastError();
//--- Get the last 2 High values on the daily timeframe
   int highsgot=CopyHigh(Symbol(),PERIOD_D1,0,2,highs);
   if(highsgot>0) // If copying was successful
     {
      Print("High prices for the last 2 days were obtained successfully");
      prevHigh=highs[0]; // The previous day High
      Print("prevHigh = ",prevHigh);
      if(ObjectFind(0,highlevel)<0) // Object with the name highlevel not found
        {
         ObjectCreate(0,highlevel,OBJ_HLINE,0,0,0); // Create the Horizontal Line object
        }
      //--- Set value for the price level for the line highlevel
      ObjectSetDouble(0,highlevel,OBJPROP_PRICE,0,prevHigh);
      //--- Set the visibility only PERIOD_M10 and PERIOD_H4
      ObjectSetInteger(0,highlevel,OBJPROP_TIMEFRAMES,OBJ_PERIOD_M10|OBJ_PERIOD_H4);
     }
   else
     {
      Print("Could not get High prices over the past 2 days, Error = ",GetLastError());
     }
 
//--- Reset the last error
   ResetLastError();
//--- Get the 2 days values Low on the daily timeframe
   int lowsgot=CopyLow(Symbol(),PERIOD_D1,0,2,lows);
   if(lowsgot>0) // If copying was successful
     {
      Print("Low prices for the last 2 days were obtained successfully");
      prevLow=lows[0]; // The previous day Low
      Print("prevLow = ",prevLow);
      if(ObjectFind(0,lowlevel)<0) // Object with the name lowlevel not found
        {
         ObjectCreate(0,lowlevel,OBJ_HLINE,0,0,0); // Create the Horizontal Line object
        }
      //--- Set value for the price level for the line lowlevel
      ObjectSetDouble(0,lowlevel,OBJPROP_PRICE,0,prevLow);
      //--- Set the visibility only PERIOD_M10 and PERIOD_H4
      ObjectSetInteger(0,lowlevel,OBJPROP_TIMEFRAMES,OBJ_PERIOD_M10|OBJ_PERIOD_H4);
     }
   else Print("Could not get Low prices for the last 2 days, Error = ",GetLastError());
 
   ChartRedraw(0); // redraw the chart forcibly
  }

```

See also

[PeriodSeconds](/en/docs/common/periodseconds), [Period](/en/docs/check/period), [Chart timeframes](/en/docs/constants/chartconstants/enum_timeframes), [Date and Time](/en/docs/dateandtime)
