# CalendarValueHistoryByEvent

Get the array of values for all events in a specified time range by an event ID.

```
int  CalendarValueHistoryByEvent(
   ulong              event_id,          // event ID 
   MqlCalendarValue&  values[],          // array for value descriptions 
   datetime           datetime_from,     // left border of a time range
   datetime           datetime_to=0      // right border of a time range
   );

```

Parameters

event_id

[in]  Event ID.

values[]

[out]  [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) type array for receiving event values. See the [example of handling calendar events](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue_sample).

datetime_from

[in]  Initial date of a time range events are selected from by a specified ID, while datetime_from < datetime_to.

datetime_to=0

[in]  End date of a time range events are selected from by a specified ID. If the datetime_to is not set (or is 0), all event values beginning from the specified datetime_from date in the Calendar database are returned (including the values of future events).

Return Value

If successful, return the number of available values in the 'values' array, otherwise -1. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),

- 4004 – ERR_NOT_ENOUGH_MEMORY (not enough memory for executing a request),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded),

- 5400 – ERR_CALENDAR_MORE_DATA (array size is insufficient for receiving descriptions of all values, only the ones that managed to fit in were received),

- errors of failed execution of [ArrayResize()](/en/docs/array/arrayresize)

The MqlCalendarValue structure provides methods for checking and setting values from the actual_value, forecast_value, prev_value and revised_prev_value fields. If no value is specified, the field stores LONG_MIN (-9223372036854775808).

Please note that the values stored in these field are multiplied by one million. It means that when you receive values in MqlCalendarValue using functions [CalendarValueById](/en/docs/calendar/calendarcountrybyid), [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarValueLastByEvent](/en/docs/calendar/calendarvaluelastbyevent) and [CalendarValueLast](/en/docs/calendar/calendarvaluelast), you should check if the field values are equal to LONG_MIN; if a value is specified in a field, then you should divide the value by 1,000,000 in order to get the value. Another method to get the values is to check and to get values using the functions of the MqlCalendarValue structure.

Note

All functions for working with the economic calendar use the trade server time ([TimeTradeServer](/en/docs/dateandtime/timetradeserver)). This means that the time in the [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) structure and the time inputs in the [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent)/[CalendarValueHistory](/en/docs/calendar/calendarvaluehistory) functions are set in a trade server timezone, rather than a user's local time.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- country code for EU (ISO 3166-1 Alpha-2)
   string EU_code="EU";
//--- get EU events
   MqlCalendarEvent events[];
   int events_count=CalendarEventByCountry(EU_code,events);
//--- display EU events in the Journal
   if(events_count>0)
     {
      PrintFormat("EU events: %d",events_count);
      //--- reduce the event list, 10 events are sufficient for analysis
      ArrayResize(events,10);
      ArrayPrint(events);
     }
//--- see that the "ECB Interest Rate Decision" event has event_id=999010007
   ulong event_id=events[6].id;        // the event's ID may change in the Calendar, so be sure to verify
   string event_name=events[6].name;   // name of a Calendar event
   PrintFormat("Get values for event_name=%s event_id=%d",event_name,event_id);
//--- get all values of the "ECB Interest Rate Decision" event
   MqlCalendarValue values[];
//--- set the boundaries of the interval we take the events from
   datetime date_from=0;           // take all events from the beginning of the available history
   datetime date_to=D'01.01.2016'; // take events not older than 2016
   if(CalendarValueHistoryByEvent(event_id,values,date_from,date_to))
     {
      PrintFormat("Received values for %s: %d",
                  event_name,ArraySize(values));
      //--- reduce the value list, 10 events are sufficient for analysis
      ArrayResize(values,10);
      ArrayPrint(values);
     }
   else
     {
      PrintFormat("Error! Failed to get values for event_id=%d",event_id);
      PrintFormat("Error code: %d",GetLastError());
     }
  }
//---
/*
  Result:
  EU events: 56
            [id] [type] [sector] [frequency] [time_mode] [country_id] [unit] [importance] [multiplier] [digits]                                        [source_url]                                 [event_code]                                    [name] [reserv
   [0] 999010001      0        5           0           0          999      0            2            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-non-monetary-policy-meeting"            "ECB Non-monetary Policy Meeting"                
   [1] 999010002      0        5           0           0          999      0            2            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-monetary-policy-meeting-accounts"       "ECB Monetary Policy Meeting Accounts"           
   [2] 999010003      0        5           0           0          999      0            3            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-monetary-policy-press-conference"       "ECB Monetary Policy Press Conference"           
   [3] 999010004      0        5           0           0          999      0            3            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-president-draghi-speech"                "ECB President Draghi Speech"                    
   [4] 999010005      0        5           0           0          999      0            2            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-vice-president-vitor-constancio-speech" "ECB Vice President Constancio Speech"           
   [5] 999010006      1        5           0           0          999      1            3            0        2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-deposit-rate-decision"                  "ECB Deposit Facility Rate Decision"             
   [6] 999010007      1        5           0           0          999      1            3            0        2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-interest-rate-decision"                 "ECB Interest Rate Decision"                     
   [7] 999010008      0        5           0           0          999      0            2            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-economic-bulletin"                      "ECB Economic Bulletin"                          
   [8] 999010009      1        5           0           0          999      2            2            3        3 "https://www.ecb.europa.eu/home/html/index.en.html" "targeted-ltro"                              "ECB Targeted LTRO"                              
   [9] 999010010      0        5           0           0          999      0            2            0        0 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-executive-board-member-praet-speech"    "ECB Executive Board Member Praet Speech"        
  Get values for event_name=ECB Interest Rate Decision event_id=999010007
  Received ECB Interest Rate Decision event values: 102
       [id] [event_id]              [time]            [period] [revision] [actual_value] [prev_value] [revised_prev_value]     [forecast_value] [impact_type] [reserved]
   [0] 2776  999010007 2007.03.08 11:45:00 1970.01.01 00:00:00          0        3750000      4250000 -9223372036854775808 -9223372036854775808             0          0
   [1] 2777  999010007 2007.05.10 11:45:00 1970.01.01 00:00:00          0        3750000      3750000 -9223372036854775808 -9223372036854775808             0          0
   [2] 2778  999010007 2007.06.06 11:45:00 1970.01.01 00:00:00          0        4000000      3750000 -9223372036854775808 -9223372036854775808             0          0
   [3] 2779  999010007 2007.07.05 11:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [4] 2780  999010007 2007.08.02 11:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [5] 2781  999010007 2007.09.06 11:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [6] 2782  999010007 2007.10.04 11:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [7] 2783  999010007 2007.11.08 12:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [8] 2784  999010007 2007.12.06 12:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
   [9] 2785  999010007 2008.01.10 12:45:00 1970.01.01 00:00:00          0        4000000      4000000 -9223372036854775808 -9223372036854775808             0          0
*/

```

See also

[CalendarCountries](/en/docs/calendar/calendarcountries), [CalendarEventByCountry](/en/docs/calendar/calendareventbycountry), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarEventById](/en/docs/calendar/calendareventbyid), [CalendarValueById](/en/docs/calendar/calendarvaluebyid)
