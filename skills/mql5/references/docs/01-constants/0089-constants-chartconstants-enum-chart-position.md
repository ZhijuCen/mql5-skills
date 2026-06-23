# Positioning Constants

Three identifiers from the ENUM_CHART_POSITION list are the possible values of the position parameter for the [ChartNavigate()](/en/docs/chart_operations/chartnavigate) function.

ENUM_CHART_POSITION

| ID | Description |
| --- | --- |
| CHART_BEGIN | Chart beginning (the oldest prices) |
| CHART_CURRENT_POS | Current position |
| CHART_END | Chart end (the latest prices) |

Example:

```
   long handle=ChartOpen("EURUSD",PERIOD_H12);
   if(handle!=0)
     {
      ChartSetInteger(handle,CHART_AUTOSCROLL,false);
      ChartSetInteger(handle,CHART_SHIFT,true);
      ChartSetInteger(handle,CHART_MODE,CHART_LINE);
      ResetLastError();
      bool res=ChartNavigate(handle,CHART_END,150);
      if(!res) Print("Navigate failed. Error = ",GetLastError());
      ChartRedraw();
     }

```
