# CalendarValueLastByEvent

Get the array of event values by its ID since the Calendar database status with a specified change_id.

```
int  CalendarValueLastByEvent(
   ulong                event_id,      // event ID 
   ulong&               change_id,     // Calendar change ID 
   MqlCalendarValue&    values[]       // array for value descriptions 
   );

```

Parameters

event_id

[in]  Event ID.

change_id

[in][out]  Change ID.

values[]

[out]  [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) type array for receiving event values. See the [example of handling calendar events](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue_sample).

Return Value

Number of received event values. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),

- 4004 – ERR_NOT_ENOUGH_MEMORY (not enough memory for executing a request),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded),

- 5400 – ERR_CALENDAR_MORE_DATA (array size is insufficient for receiving descriptions of all values, only the ones that managed to fit in were received),

- errors of failed execution of [ArrayResize()](/en/docs/array/arrayresize)

Note

All functions for working with the economic calendar use the trade server time ([TimeTradeServer](/en/docs/dateandtime/timetradeserver)). This means that the time in the [MqlCalendarValue](/en/docs/constants/structures/mqlcalendar#mqlcalendarvalue) structure and the time inputs in the [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent)/[CalendarValueHistory](/en/docs/calendar/calendarvaluehistory) functions are set in a trade server timezone, rather than a user's local time.

If the events[] array of fixed length was passed to the function and there was not enough space to save the entire result, the ERR_CALENDAR_MORE_DATA (5400) error is activated.

If change_id = 0 is passed to the function, the function always returns zero but the current calendar database is returned to change_id.

The function returns the array for a specified news and a new change_id that can be used for subsequent calls of the function to receive the new values of the news. Thus, it is possible to update values for a specified news by calling this function with the last known change_id.

The MqlCalendarValue structure provides methods for checking and setting values from the actual_value, forecast_value, prev_value and revised_prev_value fields. If no value is specified, the field stores LONG_MIN (-9223372036854775808).

Please note that the values stored in these field are multiplied by one million. It means that when you receive values in MqlCalendarValue using functions [CalendarValueById](/en/docs/calendar/calendarcountrybyid), [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarValueLastByEvent](/en/docs/calendar/calendarvaluelastbyevent) and [CalendarValueLast](/en/docs/calendar/calendarvaluelast), you should check if the field values are equal to LONG_MIN; if a value is specified in a field, then you should divide the value by 1,000,000 in order to get the value. Another method to get the values is to check and to get values using the functions of the MqlCalendarValue structure.

The sample EA listening for the Nonfarm payrolls report release:

```
#property description "Example of using the CalendarValueLastByEvent function"
#property description " for tracking the release of the Nonfarm Payrolls report."
#property description "To achieve this, get the current change ID"
#property description " of the Calendar database. Then, use this ID to receive"
#property description " only new events via the timer survey"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(60);
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
 
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//--- Calendar database change ID
   static ulong calendar_change_id=0;
//--- first launch attribute
   static bool first=true;
//--- event ID  
   static ulong event_id=0;
//--- event name  
   static string event_name=NULL;
//--- event value array
   MqlCalendarValue values[];
//--- perform initialization - get the current calendar_change_id
   if(first)
     {
      MqlCalendarEvent events[];
      //--- country code for USA (ISO 3166-1 Alpha-2) 
      string USA_code="US";
      //--- get events for USA    
      int events_count=CalendarEventByCountry(USA_code,events);
      //--- position of a necessary event in the 'events' array
      int event_pos=-1;
      //--- display USA events in the Journal
      if(events_count>0)
        {
         PrintFormat("%s: USA events: %d",__FUNCTION__,events_count);
         for(int i=0;i<events_count;i++)
           {
            string event_name_low=events[i].name;
            //--- change an event name to lower case            
            if(!StringToLower(event_name_low))
              {
               PrintFormat("StringToLower() returned %d error",GetLastError());
               //--- exit the function ahead of time
               return;
              }
            //--- look for the "Nonfarm Payrolls" event            
            if(StringFind(event_name_low,"nonfarm payrolls")!=-1)
              {
               //--- event found, remember its ID
               event_id=events[i].id;
               //--- write the "Nonfarm Payrolls" event name 
               event_name=events[i].name;
               //--- remember the events' position in the 'events[]' array               
               event_pos=i;
               //--- keep in mind that the Calendar features several events containing "nonfarm payrolls" in their names
               PrintFormat("Event \"Nonfarm Payrolls\" found: event_id=%d  event_name=%s",event_id,event_name);
               //--- view all the events by commenting out the 'break' operator to better understand this example
               break;
              }
           }
         //--- reduce the list by deleting events after "Nonfarm Payrolls"
         ArrayRemove(events,event_pos+1);
         //--- leave 9 events before "Nonfarm Payrolls" for more convenient analysis         
         ArrayRemove(events,0,event_pos-9);
         ArrayPrint(events);
        }
      else
        {
         PrintFormat("%s: CalendarEventByCountry(%s) returned 0 events, error code=%d",
                     USA_code,__FUNCTION__,GetLastError());
         //--- operation completed in a failure, try again during the next call of the timer         
         return;
        }
 
      //--- get the Calendar database change ID for the specified event   
      if(CalendarValueLastByEvent(event_id,calendar_change_id,values)>0)
        {
         //--- this code block cannot be executed during the first launch but let's add it anyway
         PrintFormat("%s: Received the Calendar database current ID: change_id=%d",
                     __FUNCTION__,calendar_change_id);
         //--- set the flag and exit before the timer's next event
         first=false;
         return;
        }
      else
        {
         //--- data are not received (this is normal for the first launch), check for an error
         int error_code=GetLastError();
         if(error_code==0)
           {
            PrintFormat("%s: Received the Calendar database current ID: change_id=%d",
                        __FUNCTION__,calendar_change_id);
            //--- set the flag and exit before the timer's next event
            first=false;
            //--- now we have the calendar_change_id value
            return;
           }
         else
           {
            //--- and this is really an error            
            PrintFormat("%s: Failed to get values for event_id=%d",__FUNCTION__,event_id);
            PrintFormat("Error code: %d",error_code);
            //--- operation completed in a failure, try again during the next call of the timer         
            return;
           }
        }
     }
 
//--- we have the last known value of the Calendar change ID (change_id)
   ulong old_change_id=calendar_change_id;
//--- check for a new Nonfarm Payrolls event value
   if(CalendarValueLastByEvent(event_id,calendar_change_id,values)>0)
     {
      PrintFormat("%s: Received new events for \"%s\": %d",
                  __FUNCTION__,event_name,ArraySize(values));
      //--- display data from the 'values' array in the Journal 
      ArrayPrint(values);
      //--- display the values of the previous and new Calendar IDs in the Journal
      PrintFormat("%s: Previous change_id=%d, new change_id=%d",
                  __FUNCTION__,old_change_id,calendar_change_id);
/* 
      write your code that is to handle "Nonfarm Payrolls" data release here
      */
     }
//---     
  }
/*
  Result:
   OnTimer: USA events: 202
  Event "Nonfarm Payrolls" found: event_id=840030016  event_name=Nonfarm Payrolls
            [id] [type] [sector] [frequency] [time_mode] [country_id] [unit] [importance] [multiplier] [digits]          [source_url]                             [event_code]                   [name] [reserved]
   [0] 840030007      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "consumer-price-index-yy"                "CPI y/y"                         0
   [1] 840030008      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "consumer-price-index-ex-food-energy-yy" "Core CPI y/y"                    0
   [2] 840030009      1        4           2           0          840      0            1            0        3 "https://www.bls.gov" "consumer-price-index-nsa"               "CPI n.s.a."                      0
   [3] 840030010      1        4           2           0          840      0            1            0        3 "https://www.bls.gov" "consumer-price-index-ex-food-energy"    "Core CPI"                        0
   [4] 840030011      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "import-price-index-mm"                  "Import Price Index m/m"          0
   [5] 840030012      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "import-price-index-yy"                  "Import Price Index y/y"          0
   [6] 840030013      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "export-price-index-mm"                  "Export Price Index m/m"          0
   [7] 840030014      1        4           2           0          840      1            1            0        1 "https://www.bls.gov" "export-price-index-yy"                  "Export Price Index y/y"          0
   [8] 840030015      1        3           2           0          840      1            2            0        1 "https://www.bls.gov" "unemployment-rate"                      "Unemployment Rate"               0
   [9] 840030016      1        3           2           0          840      4            3            1        0 "https://www.bls.gov" "nonfarm-payrolls"                       "Nonfarm Payrolls"                0
   OnTimer: Received the Calendar database current ID: change_id=33986560
 
*/  

```

See also

[CalendarValueLast](/en/docs/calendar/calendarvaluelast), [CalendarValueHistory](/en/docs/calendar/calendarvaluehistory), [CalendarValueHistoryByEvent](/en/docs/calendar/calendarvaluehistorybyevent), [CalendarValueById](/en/docs/calendar/calendarvaluebyid)
