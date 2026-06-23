# CalendarCountryById

Get a country description by its ID.

```
bool  CalendarCountryById(
   const long           country_id,     // country ID
   MqlCalendarCountry&  country         // variable for receiving a country description
   );

```

Parameters

country_id

[in]  Country ID ([ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1)).

country

[out]  [MqlCalendarCountry](/en/docs/constants/structures/mqlcalendar#mqlcalendarcountry) type variable for receiving a country description.

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
//--- get the list of countries from the economic calendar
   MqlCalendarCountry countries[];
   int count=CalendarCountries(countries);
//--- check the result
   if(count==0)
      PrintFormat("CalendarCountries() returned 0! Error %d",GetLastError());
//--- if there are two or more countries
   if(count>=2)
     {
      MqlCalendarCountry country;
      //--- now get a country description by its ID 
      if(CalendarCountryById(countries[1].id, country))
        {
         //--- prepare a country description
         string descr="id = "+IntegerToString(country.id)+"\n";
         descr+=("name = " + country.name+"\n");
         descr+=("code = " + country.code+"\n");
         descr+=("currency = " + country.currency+"\n");
         descr+=("currency_symbol = " + country.currency_symbol+"\n");
         descr+=("url_name = " + country.url_name);         
         //--- display a country description
         Print(descr);
        }
      else
         Print("CalendarCountryById() failed. Error ",GetLastError());
     }
//---
  }
/*
  Result:
   id = 999
   name = European Union
   code = EU
   currency = EUR
   currency_symbol = €
   url_name = european-union
*/

```

See also

[CalendarCountries](/en/docs/calendar/calendarcountries), [CalendarEventByCountry](/en/docs/calendar/calendareventbycountry)
