# CalendarEventById

Get an event description by its ID.

```
bool  CalendarEventById(
   ulong                event_id,     // event ID
   MqlCalendarEvent&    event         // variable for receiving an event description
   );

```

Parameters

event_id

[in]  Event ID.

event

[out]  [MqlCalendarEvent](/en/docs/constants/structures/mqlcalendar#mqlcalendarevent) type variable for receiving an event description.

Return Value

Returns true if successful, otherwise - false. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),
- 5402 – ERR_CALENDAR_NO_DATA (country is not found),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded).

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- country code for Germany (ISO 3166-1 Alpha-2)
   string germany_code="DE";
//--- get Germany events
   MqlCalendarEvent events[];
   int events_count=CalendarEventByCountry(germany_code,events);
//--- display Germany events in the Journal
   if(events_count>0)
     {
      PrintFormat("Germany events: %d",events_count);
      ArrayPrint(events);
     }
   else
     {
      PrintFormat("Failed to receive events for the country code %s, error %d",
                  germany_code,GetLastError());
      //--- script early completion
      return;
     }
//--- get description of the last event from the events[] array
   MqlCalendarEvent event;
   ulong event_id=events[events_count-1].id;
   if(CalendarEventById(event_id,event))
     {
      MqlCalendarCountry country; 
      CalendarCountryById(event.country_id,country);
      PrintFormat("Event description with event_id=%d received",event_id);
      PrintFormat("Country: %s (country code = %d)",country.name,event.country_id);
      PrintFormat("Event name: %s",event.name);
      PrintFormat("Event code: %s",event.event_code);
      PrintFormat("Event importance: %s",EnumToString((ENUM_CALENDAR_EVENT_IMPORTANCE)event.importance));
      PrintFormat("Event type: %s",EnumToString((ENUM_CALENDAR_EVENT_TYPE)event.type));
      PrintFormat("Event sector: %s",EnumToString((ENUM_CALENDAR_EVENT_SECTOR)event.sector));
      PrintFormat("Event frequency: %s",EnumToString((ENUM_CALENDAR_EVENT_FREQUENCY)event.frequency));
      PrintFormat("Event release mode: %s",EnumToString((ENUM_CALENDAR_EVENT_TIMEMODE)event.time_mode));
      PrintFormat("Event measurement unit: %s",EnumToString((ENUM_CALENDAR_EVENT_UNIT)event.unit));
      PrintFormat("Number of decimal places: %d",event.digits);
      PrintFormat("Event multiplier: %s",EnumToString((ENUM_CALENDAR_EVENT_MULTIPLIER)event.multiplier));
      PrintFormat("Source URL: %s",event.source_url);
     }
   else
      PrintFormat("Failed to get event description for event_d=%s, error %d",
                  event_id,GetLastError());
  }
/*
  Result:
  Germany events: 50
             [id] [type] [sector] [frequency] [time_mode] [country_id] [unit] [importance] [multiplier] [digits]                                [source_url]                       [event_code]                             [name] [reserved]
   [ 0] 276010001      1        6           2           0          276      1            1            0        1 "https://www.destatis.de/EN/Homepage.html"  "exports-mm"                       "Exports m/m"                               0
   [ 1] 276010002      1        6           2           0          276      1            1            0        1 "https://www.destatis.de/EN/Homepage.html"  "imports-mm"                       "Imports m/m"                               0
   [ 2] 276010003      1        4           2           0          276      1            1            0        1 "https://www.destatis.de/EN/Homepage.html"  "import-price-index-mm"            "Import Price Index m/m"                    0
   [ 3] 276010004      1        4           2           0          276      1            1            0        1 "https://www.destatis.de/EN/Homepage.html"  "import-price-index-yy"            "Import Price Index y/y"                    0
   ....
   [47] 276500001      1        8           2           0          276      0            2            0        1 "https://www.markiteconomics.com"           "markit-manufacturing-pmi"         "Markit Manufacturing PMI"                  0
   [48] 276500002      1        8           2           0          276      0            2            0        1 "https://www.markiteconomics.com"           "markit-services-pmi"              "Markit Services PMI"                       0
   [49] 276500003      1        8           2           0          276      0            2            0        1 "https://www.markiteconomics.com"           "markit-composite-pmi"             "Markit Composite PMI"                      0
  Event description with event_id=276500003 received
  Country: Germany (country code = 276)
  Event name: Markit Composite PMI
  Event code: markit-composite-pmi
   Event importance: CALENDAR_IMPORTANCE_MODERATE
   Event type: CALENDAR_TYPE_INDICATOR
   Event sector: CALENDAR_SECTOR_BUSINESS
   Event frequency: CALENDAR_FREQUENCY_MONTH
   Event release mode: CALENDAR_TIMEMODE_DATETIME
   Event measurement unit: CALENDAR_UNIT_NONE
  Number of decimal places: 1
   Value multiplier: CALENDAR_MULTIPLIER_NONE
   Source URL: https://www.markiteconomics.com
*/

```

See also

[CalendarEventByCountry](/en/docs/calendar/calendareventbycountry), [CalendarEventByCurrency](/en/docs/calendar/calendareventbycurrency), [CalendarValueById](/en/docs/calendar/calendarvaluebyid)
