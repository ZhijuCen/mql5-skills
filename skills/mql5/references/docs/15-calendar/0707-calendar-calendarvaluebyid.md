# CalendarValueById

Get an event value description by its ID.

```
bool  CalendarValueById(
   ulong                value_id,     // event value ID 
   MqlCalendarValue&    value         // variable for receiving an event value
   );

```

Parameters

value_id

[in]  Event value ID.

value

[out]  [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) type variable for receiving an event description. See the [example of handling calendar events](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue_sample).

Return Value

Returns true if successful, otherwise - false. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),
- 5402 – ERR_CALENDAR_NO_DATA (country is not found),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded).

Note

All functions for working with the economic calendar use the trade server time ([TimeTradeServer](/en/docs/dateandtime/timetradeserver)). This means that the time in the [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) structure and the time inputs in the [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent)/[CalendarValueHistory](/en/docs/calendar/calendarvaluehistory) functions are set in a trade server timezone, rather than a user's local time.

The MqlCalendarValue structure provides methods for checking and setting values from the actual_value, forecast_value, prev_value and revised_prev_value fields. If no value is specified, the field stores LONG_MIN (-9223372036854775808).

Please note that the values stored in these field are multiplied by one million. It means that when you receive values in MqlCalendarValue using functions [CalendarValueById](/en/docs/calendar/calendarcountrybyid), [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarValueLastByEvent](/en/docs/calendar/calendarvaluelastbyevent) and [CalendarValueLast](/en/docs/calendar/calendarvaluelast), you should check if the field values are equal to LONG_MIN; if a value is specified in a field, then you should divide the value by 1,000,000 in order to get the value. Another method to get the values is to check and to get values using the functions of the MqlCalendarValue structure.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- country code for Japan (ISO 3166-1 Alpha-2)
   string japan_code="JP";
//--- set the boundaries of the interval we take the events from
   datetime date_from=D'01.01.2018';  // take all events from 2018
   datetime date_to=0;                // 0 means all known events, including the ones that have not occurred yet    
//--- get the array of the Japan event values
   MqlCalendarValue values[];
   int values_count=CalendarValueHistory(values,date_from,date_to,japan_code);
//--- move along the detected event values
   if(values_count>0)
     {
      PrintFormat("Number of values for Japan events: %d",values_count);
      //--- delete all "empty" values (actual_value==-9223372036854775808)       
      for(int i=values_count-1;i>=0;i--)
        {
         if(values[i].actual_value==-9223372036854775808)
            ArrayRemove(values,i,1);
        }
      PrintFormat("Number of values after deleting empty ones: %d",ArraySize(values));
     }
   else
     {
      PrintFormat("Failed to receive events for the country code %s, error %d",
                  japan_code,GetLastError());
      //--- script early completion
      return;
     }
//--- leave no more than 10 values in the values[] array
   if(ArraySize(values)>10)
     {
      PrintFormat("Reduce the list of values to 10 and display them");
      ArrayRemove(values,0,ArraySize(values)-10);
     }
   ArrayPrint(values);
 
//--- now let's display how to get an event value description based on the known value_id
   for(int i=0;i<ArraySize(values);i++)
     {
      MqlCalendarValue value;
      CalendarValueById(values[i].id,value);
      PrintFormat("%d: value_id=%d value=%d impact=%s",
                  i,values[i].id,value.actual_value,EnumToString(ENUM_CALENDAR_EVENT_IMPACT(value.impact_type)));
     }
//---
  }
/*
  Result:
  Number of values for Japan events: 1734
  Number of values after deleting empty ones: 1017
  Reduce the list of values to 10 and display them
        [id] [event_id]              [time]            [period] [revision] [actual_value] [prev_value] [revised_prev_value] [forecast_value] [impact_type] [reserved]
   [0] 56500  392030004 2019.03.28 23:30:00 2019.03.01 00:00:00          0         900000       600000 -9223372036854775808           500000             1          0
   [1] 56501  392030005 2019.03.28 23:30:00 2019.03.01 00:00:00          0         700000       700000 -9223372036854775808           700000             0          0
   [2] 56502  392030006 2019.03.28 23:30:00 2019.03.01 00:00:00          0        1100000      1100000 -9223372036854775808           900000             1          0
   [3] 56544  392030007 2019.03.28 23:30:00 2019.02.01 00:00:00          0        2300000      2500000 -9223372036854775808          2200000             2          0
   [4] 56556  392050002 2019.03.28 23:30:00 2019.02.01 00:00:00          0        1630000      1630000              1610000          1620000             1          0
   [5] 55887  392020003 2019.03.28 23:50:00 2019.02.01 00:00:00          0         400000       600000 -9223372036854775808          1300000             2          0
   [6] 55888  392020004 2019.03.28 23:50:00 2019.02.01 00:00:00          0       -1800000     -3300000 -9223372036854775808         -2000000             1          0
   [7] 55889  392020002 2019.03.28 23:50:00 2019.02.01 00:00:00          0         200000     -2300000             -1800000           300000             2          0
   [8] 55948  392020006 2019.03.28 23:50:00 2019.02.01 00:00:00          1        1400000     -3400000 -9223372036854775808          -300000             1          0
   [9] 55949  392020007 2019.03.28 23:50:00 2019.02.01 00:00:00          1       -1000000       300000 -9223372036854775808          -100000             2          0
  Display brief data on event values based on value_id
   0: value_id=56500 value=900000 impact=CALENDAR_IMPACT_POSITIVE
   1: value_id=56501 value=700000 impact=CALENDAR_IMPACT_NA
   2: value_id=56502 value=1100000 impact=CALENDAR_IMPACT_POSITIVE
   3: value_id=56544 value=2300000 impact=CALENDAR_IMPACT_NEGATIVE
   4: value_id=56556 value=1630000 impact=CALENDAR_IMPACT_POSITIVE
   5: value_id=55887 value=400000 impact=CALENDAR_IMPACT_NEGATIVE
   6: value_id=55888 value=-1800000 impact=CALENDAR_IMPACT_POSITIVE
   7: value_id=55889 value=200000 impact=CALENDAR_IMPACT_NEGATIVE
   8: value_id=55948 value=1400000 impact=CALENDAR_IMPACT_POSITIVE
   9: value_id=55949 value=-1000000 impact=CALENDAR_IMPACT_NEGATIVE
*/

```

See also

[CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarValueLastByEvent](/en/docs/calendar/calendarvaluelastbyevent), [CalendarValueLast](/en/docs/calendar/calendarvaluelast)
