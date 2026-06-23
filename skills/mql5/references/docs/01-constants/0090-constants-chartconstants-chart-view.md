# Chart Representation

Price charts can be displayed in three ways:

- as bars;
- as candlesticks;
- as a line.

The specific way of displaying the price chart is set by the function [ChartSetInteger](/en/docs/chart_operations/chartsetinteger)(chart_handle,[CHART_MODE](/en/docs/constants/chartconstants/enum_chart_property), chart_mode), where chart_mode is one of the values of the ENUM_CHART_MODE enumeration.

ENUM_CHART_MODE

| ID | Description |
| --- | --- |
| CHART_BARS | Display as a sequence of bars |
| CHART_CANDLES | Display as Japanese candlesticks |
| CHART_LINE | Display as a line drawn by Close prices |

To specify the mode of displaying volumes in the price chart the function [ChartSetInteger](/en/docs/chart_operations/chartsetinteger)(chart_handle, [CHART_SHOW_VOLUMES](/en/docs/constants/chartconstants/enum_chart_property), volume_mode) is used, where volume_mode is one of values of the ENUM_CHART_VOLUME_MODE enumeration.

ENUM_CHART_VOLUME_MODE

| ID | Description |
| --- | --- |
| CHART_VOLUME_HIDE | Volumes are not shown |
| CHART_VOLUME_TICK | Tick volumes |
| CHART_VOLUME_REAL | Trade volumes |

Example:

```
//--- Get the handle of the current chart
   long handle=ChartID();
   if(handle>0) // If it succeeded, additionally customize
     {
      //--- Disable autoscroll
      ChartSetInteger(handle,CHART_AUTOSCROLL,false);
      //--- Set the indent of the right border of the chart
      ChartSetInteger(handle,CHART_SHIFT,true);
      //--- Display as candlesticks
      ChartSetInteger(handle,CHART_MODE,CHART_CANDLES);
      //--- Scroll by 100 bars from the beginning of history
      ChartNavigate(handle,CHART_CURRENT_POS,100);
      //--- Set the tick volume display mode
      ChartSetInteger(handle,CHART_SHOW_VOLUMES,CHART_VOLUME_TICK);
     }

```

See also

[ChartOpen](/en/docs/chart_operations/chartopen), [ChartID](/en/docs/chart_operations/chartid)
