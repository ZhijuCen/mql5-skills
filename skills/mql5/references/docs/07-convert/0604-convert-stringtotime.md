# StringToTime

Transforms the string containing time and/or date in the "yyyy.mm.dd [hh:mi]" format into the datetime type number.

```
datetime  StringToTime(
   const string  time_string      // date string
   );

```

Parameters

time_string

[in]  String in one of the specified formats:

- "yyyy.mm.dd [hh:mi]"
- "yyyy.mm.dd [hh:mi:ss]"
- "yyyymmdd [hh:mi:ss]"
- "yyyymmdd [hhmiss]"
- "yyyy/mm/dd [hh:mi:ss]"
- "yyyy-mm-dd [hh:mi:ss]"

Return Value

[datetime](/en/docs/basis/types/integer/datetime) type value containing the number of seconds elapsed since 01.01.1970.

Note

Any sequence of space and tabulation characters between date and time is considered to be a single space to avoid additional processing of the time_string before calling StringToTime().

Example:

```
//--- input parameters
input group    "The date can be entered in any of the formats:"
input group    "yyyy.mm.dd [hh:mi], yyyy.mm.dd [hh:mi:ss]"
input group    "yyyymmdd [hh:mi:ss], yyyymmdd [hhmiss]"
input group    "yyyy/mm/dd [hh:mi:ss], yyyy-mm-dd [hh:mi:ss]"
input string   InpDateStr;    // Please enter the date here as a string
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- convert the time entered in the inputs as a string into a datetime value
   datetime time=StringToTime(InpDateStr);
//--- display the entered string and the obtained time in the journal
   PrintFormat("Date entered as a string in the form '%s' is converted to datetime in the form '%s'",
               InpDateStr, TimeToString(time, TIME_DATE|TIME_MINUTES|TIME_SECONDS));
//--- create a vertical line on the received date-time and shift the chart to this location
   if(CreateVLine(time))
      ChartNavigateToTime(time);
   /*
   result:
   Date entered as a string in the form '' is converted to datetime in the form '1970.01.01 00:00:00'
   Date entered as a string in the form '2024' is converted to datetime in the form '2024.02.24 20:24:00'
   Date entered as a string in the form '202400' is converted to datetime in the form '2024.02.24 20:24:00'
   Date entered as a string in the form '20240000' is converted to datetime in the form '2024.02.24 00:00:00'
   Date entered as a string in the form '2024022410' is converted to datetime in the form '2030.09.06 00:00:00'
   Date entered as a string in the form '20240224 10' is converted to datetime in the form '2024.02.24 10:00:00'
   Date entered as a string in the form '20240224 01' is converted to datetime in the form '2024.02.24 01:00:00'
   Date entered as a string in the form '20240224 0030' is converted to datetime in the form '2024.02.24 23:00:00'
   Date entered as a string in the form '20240224 0100' is converted to datetime in the form '2024.02.24 01:00:00'
   */
  }
//+------------------------------------------------------------------+
//| Create a vertical line object                                    |
//+------------------------------------------------------------------+
bool CreateVLine(const datetime line_time)
  {
   ResetLastError();
 
   string name=MQLInfoString(MQL_PROGRAM_NAME)+"_VLINE";
   if(!ObjectCreate(0, name, OBJ_VLINE, 0, line_time, 0))
     {
      Print("ObjectCreate() failed. Error code: ", GetLastError());
      return(false);
     }
   ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, true);
 
   return(true);
  }
//+------------------------------------------------------------------+
//| Shift the chart to the specified bar opening time                |
//+------------------------------------------------------------------+
bool ChartNavigateToTime(const datetime time)
  {
   ChartSetInteger(0, CHART_AUTOSCROLL, false);
   ResetLastError();
 
   int bar=iBarShift(_Symbol, PERIOD_CURRENT, time);
   if(bar<0)
     {
      PrintFormat("%s: iBarShift() failed. Error code: %d", __FUNCTION__, GetLastError());
      return(false);
     }
 
   long first=0;
   if(!ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0, first))
     {
      PrintFormat("%s: ChartGetInteger() failed. Error code: %d", __FUNCTION__, GetLastError());
      return(false);
     }
 
   return(ChartNavigate(0, CHART_CURRENT_POS, (int)first-bar));
  }

```

See also

[TimeToString](/en/docs/convert/timetostring), [TimeToStruct](/en/docs/dateandtime/timetostruct)
