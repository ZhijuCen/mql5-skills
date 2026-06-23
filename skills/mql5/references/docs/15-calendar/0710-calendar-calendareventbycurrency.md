# CalendarEventByCurrency

Get the array of descriptions of all events available in the Calendar by a specified currency.

```
int  CalendarEventByCurrency(
   const string         currency,     // country currency code name 
   MqlCalendarEvent&    events[]      // variable for receiving the description array
   );

```

Parameters

currency

[in]  Country currency code name.

events[]

[out]  [MqlCalendarEvent](/en/docs/constants/structures/mqlcalendar#mqlcalendarevent) type array for receiving descriptions of all events for a specified currency.

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
//--- declare the array for receiving economic calendar events
      MqlCalendarEvent events[];
//--- get EU currency events      
      int count = CalendarEventByCurrency("EUR",events);
      Print("count = ", count);
//--- 10 events are sufficient for the current example
      if(count>10)
         ArrayResize(events,10);
//--- display events in the Journal        
      ArrayPrint(events);
  }
/*
  Result:
             [id] [type] [country_id] [unit] [importance]                                        [source_url]                                 [event_code]                                    [name] 
   [0] 999010001      0          999      0            2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-non-monetary-policy-meeting"            "ECB Non-monetary Policy Meeting"                
   [1] 999010002      0          999      0            2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-monetary-policy-meeting-accounts"       "ECB Monetary Policy Meeting Accounts"           
   [2] 999010003      0          999      0            3 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-monetary-policy-press-conference"       "ECB Monetary Policy Press Conference"           
   [3] 999010004      0          999      0            3 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-president-draghi-speech"                "ECB President Draghi Speech"                    
   [4] 999010005      0          999      0            2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-vice-president-vitor-constancio-speech" "ECB Vice President Constancio Speech"           
   [5] 999010006      1          999      1            3 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-deposit-rate-decision"                  "ECB Deposit Facility Rate Decision"             
   [6] 999010007      1          999      1            3 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-interest-rate-decision"                 "ECB Interest Rate Decision"                     
   [7] 999010008      0          999      0            2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-economic-bulletin"                      "ECB Economic Bulletin"                          
   [8] 999010009      1          999      2            2 "https://www.ecb.europa.eu/home/html/index.en.html" "targeted-ltro"                              "ECB Targeted LTRO"                              
   [9] 999010010      0          999      0            2 "https://www.ecb.europa.eu/home/html/index.en.html" "ecb-executive-board-member-praet-speech"    "ECB Executive Board Member Praet Speech"        
*/  

```

See also

[CalendarEventById](/en/docs/calendar/calendareventbyid), [CalendarEventByCountry](/en/docs/calendar/calendareventbycountry)
