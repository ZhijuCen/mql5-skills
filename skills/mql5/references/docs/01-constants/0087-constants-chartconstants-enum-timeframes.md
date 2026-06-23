# Chart Timeframes

All predefined timeframes of charts have unique identifiers. The PERIOD_CURRENT identifier means the current period of a chart, at which a mql5-program is running.

ENUM_TIMEFRAMES

| ID | Description |
| --- | --- |
| PERIOD_CURRENT | Current timeframe |
| PERIOD_M1 | 1 minute |
| PERIOD_M2 | 2 minutes |
| PERIOD_M3 | 3 minutes |
| PERIOD_M4 | 4 minutes |
| PERIOD_M5 | 5 minutes |
| PERIOD_M6 | 6 minutes |
| PERIOD_M10 | 10 minutes |
| PERIOD_M12 | 12 minutes |
| PERIOD_M15 | 15 minutes |
| PERIOD_M20 | 20 minutes |
| PERIOD_M30 | 30 minutes |
| PERIOD_H1 | 1 hour |
| PERIOD_H2 | 2 hours |
| PERIOD_H3 | 3 hours |
| PERIOD_H4 | 4 hours |
| PERIOD_H6 | 6 hours |
| PERIOD_H8 | 8 hours |
| PERIOD_H12 | 12 hours |
| PERIOD_D1 | 1 day |
| PERIOD_W1 | 1 week |
| PERIOD_MN1 | 1 month |

Example:

```
   string chart_name="test_Object_Chart";
   Print("Let's try to create a Chart object with the name ",chart_name);
//--- If such an object does not exist - create it
   if(ObjectFind(0,chart_name)<0)ObjectCreate(0,chart_name,OBJ_CHART,0,0,0,0,0);
//--- Define symbol
   ObjectSetString(0,chart_name,OBJPROP_SYMBOL,"EURUSD");
//--- Set X coordinate of the anchor point
   ObjectSetInteger(0,chart_name,OBJPROP_XDISTANCE,100);
//--- Set Y coordinate of the anchor point
   ObjectSetInteger(0,chart_name,OBJPROP_YDISTANCE,100);
//--- Set the width of chart
   ObjectSetInteger(0,chart_name,OBJPROP_XSIZE,400);
//--- Set the height
   ObjectSetInteger(0,chart_name,OBJPROP_YSIZE,300);
//--- Set the timeframe
   ObjectSetInteger(0,chart_name,OBJPROP_PERIOD,PERIOD_D1);
//--- Set scale (from 0 to 5)
   ObjectSetDouble(0,chart_name,OBJPROP_SCALE,4);
//--- Disable selection by a mouse
   ObjectSetInteger(0,chart_name,OBJPROP_SELECTABLE,false);

```

### Timeseries identifiers  #

The identifiers of timeseries are used in the [iHighest()](/en/docs/series/ihighest) and [iLowest()](/en/docs/series/ilowest) functions. They can be equal to a value the enumeration

ENUM_SERIESMODE

| Identifier | Description |
| --- | --- |
| MODE_OPEN | Opening price |
| MODE_LOW | Low price |
| MODE_HIGH | High price |
| MODE_CLOSE | Close price |
| MODE_VOLUME | Tick volume |
| MODE_REAL_VOLUME | Real volume |
| MODE_SPREAD | Spread |

See also

[PeriodSeconds](/en/docs/common/periodseconds), [Period](/en/docs/check/period), [Date and Time](/en/docs/dateandtime), [Visibility of objects](/en/docs/constants/objectconstants/visible)
