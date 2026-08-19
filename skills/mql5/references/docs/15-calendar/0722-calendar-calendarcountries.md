# CalendarCountries

Get the array of country names available in the Calendar.

```
int  CalendarCountries(
   MqlCalendarCountry&  countries[]         // array for receiving a list of Calendar countries' descriptions
   );

```

Parameters

countries[]

[out]  An array of [MqlCalendarCountry](/en/docs/constants/structures/mqlcalendar#mqlcalendarcountry) type for receiving all Calendar countries' descriptions.

Return Value

Number of received descriptions. To get information about an error, call the [GetLastError()](/en/docs/check/getlasterror) function. Possible errors:

- 4001 – ERR_INTERNAL_ERROR  (general runtime error),
- 5401 – ERR_CALENDAR_TIMEOUT (request time limit exceeded),
- 5400 – ERR_CALENDAR_MORE_DATA (array size is insufficient for receiving descriptions of all countries, only the ones that managed to fit in were received).

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the list of countries from the economic calendar
   MqlCalendarCountry countries[];
   int count=CalendarCountries(countries);
//--- display the array in the Journal
   if(count>0)
      ArrayPrint(countries);
   else
      PrintFormat("CalendarCountries() returned 0! Error %d",GetLastError());
/*
  Result:
        [id]           [name] [code] [currency] [currency_symbol]       [url_name] [reserved]
   [ 0]    0 "Worldwide"      "WW"   "ALL"      ""                "worldwide"               0
   [ 1]  999 "European Union" "EU"   "EUR"      "€"               "european-union"          0
   [ 2]  840 "United States"  "US"   "USD"      "$"               "united-states"           0
   [ 3]  124 "Canada"         "CA"   "CAD"      "$"               "canada"                  0
   [ 4]   36 "Australia"      "AU"   "AUD"      "$"               "australia"               0
   [ 5]  554 "New Zealand"    "NZ"   "NZD"      "$"               "new-zealand"             0
   [ 6]  392 "Japan"          "JP"   "JPY"      "Ґ"               "japan"                   0
   [ 7]  156 "China"          "CN"   "CNY"      "Ґ"               "china"                   0
   [ 8]  826 "United Kingdom" "GB"   "GBP"      "Ј"               "united-kingdom"          0
   [ 9]  756 "Switzerland"    "CH"   "CHF"      "₣"               "switzerland"             0
   [10]  276 "Germany"        "DE"   "EUR"      "€"               "germany"                 0
   [11]  250 "France"         "FR"   "EUR"      "€"               "france"                  0
   [12]  380 "Italy"          "IT"   "EUR"      "€"               "italy"                   0
   [13]  724 "Spain"          "ES"   "EUR"      "€"               "spain"                   0
   [14]   76 "Brazil"         "BR"   "BRL"      "R$"              "brazil"                  0
   [15]  410 "South Korea"    "KR"   "KRW"      "₩"               "south-korea"             0
*/
  }

```

See also

[CalendarEventByCountry](/en/docs/calendar/calendareventbycountry), [CalendarCountryById](/en/docs/calendar/calendarcountrybyid)
