# CalendarEventByCountry

Get the array of descriptions of all events available in the Calendar by a specified country code.

```
int  CalendarEventByCountry(
   string               country_code,     // country code name (ISO 3166-1 alpha-2)
   MqlCalendarEvent&    events[]          // variable for receiving the description array
   );

```

Parameters

country_code

[in]  Country code name (ISO 3166-1 alpha-2)

events[]

[out]  [MqlCalendarEvent](/en/docs/constants/structures/mqlcalendar#mqlcalendarevent) type array for receiving descriptions of all events for a specified country.

Return Value

Number of received descriptions. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),
- 4004 – ERR_NOT_ENOUGH_MEMORY (not enough memory for executing a request),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded),
- errors of failed execution of [ArrayResize()](/en/docs/array/arrayresize)

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
      ArrayPrint(events);
     }
//---
  }
/*
  Result:
  EU events: 56
             [id] [type]  [country_id] [unit] [importance] [multiplier] [digits] [event_code]                                     
   [ 0] 999010001      0          999      0            2            0        0  "ECB Non-monetary Policy Meeting"   
   [ 1] 999010002      0          999      0            2            0        0  "ECB Monetary Policy Meeting Account
   [ 2] 999010003      0          999      0            3            0        0  "ECB Monetary Policy Press Conferenc
   [ 3] 999010004      0          999      0            3            0        0  "ECB President Draghi Speech"       
   [ 4] 999010005      0          999      0            2            0        0  "ECB Vice President Constancio Speec
   [ 5] 999010006      1          999      1            3            0        2  "ECB Deposit Facility Rate Decision"
   [ 6] 999010007      1          999      1            3            0        2  "ECB Interest Rate Decision"        
   [ 7] 999010008      0          999      0            2            0        0  "ECB Economic Bulletin"             
   [ 8] 999010009      1          999      2            2            3        3  "ECB Targeted LTRO"                 
   [ 9] 999010010      0          999      0            2            0        0  "ECB Executive Board Member Praet Sp
   [10] 999010011      0          999      0            2            0        0  "ECB Executive Board Member Mersch S   
   ...
 
*/

```

See also

[CalendarCountries](/en/docs/calendar/calendarcountries), [CalendarCountryById](/en/docs/calendar/calendarcountrybyid)
