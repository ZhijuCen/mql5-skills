# ChartClose

Closes the specified chart.

```
bool  ChartClose(
   long  chart_id=0      // Chart ID
   );

```

Parameters

chart_id=0

[in]  Chart ID. 0 means the current chart.

Return Value

If successful, returns true, otherwise false.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- open a new chart with the same symbol and period as the current one
   long chart_id=ChartOpen(_Symbol, _Period);
   if(chart_id==0)
     {
      Print("ChartOpen() failed. Error ", GetLastError());
      return;
     }
 
//--- print open chart parameters in the journal
   PrintFormat("A new chart of the %s symbol has been opened with a period of %s and ChartID %I64u",
               _Symbol, StringSubstr(EnumToString(_Period), 7), chart_id);
 
//--- wait two seconds and close the newly opened chart
   PrintFormat("Waiting 3 seconds before closing a newly opened chart with ID %I64d ...", chart_id);
   Sleep(3000);
   ResetLastError();
   if(!ChartClose(chart_id))
     {
      Print("ChartClose() failed. Error ", GetLastError());
      return;
     }
 
//--- print successful chart closure message in the journal
   PrintFormat("The chart with ID %I64d was successfully closed", chart_id);
   /*
   result:
   A new chart of the GBPUSD symbol has been opened with a period of M1 and ChartID 133346697706632016
   Waiting 3 seconds before closing a newly opened chart with ID 133346697706632016 ...
   The chart with ID 133346697706632016 was successfully closed
   */
  }

```
