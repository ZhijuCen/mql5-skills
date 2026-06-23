# Getting event records by country or currency

Specific events of various kinds are queried in the calendar for a given range of dates and filtered by country or currency.

int CalendarValueHistory(MqlCalendarValue &values[], datetime from, datetime to = 0,  

   const string country = NULL, const string currency = NULL)

The CalendarValueHistory function fills the values array passed by reference with calendar entries in the time range between from and to. Both parameters may include date and time. Value from is included in the interval, but value to is not. In other words, the function selects calendar entries (structuresMqlCalendarValue), in which the following compound condition is met for the time property: from <= time < to.

The start time from must be specified, while the end time to is optional: if it is omitted or equal to 0, all future events are copied to the array.

Time to there should be larger than from, except when it is 0. A special combination for querying all available events (both past and future) is when from and to are both 0.

If the receiving array is dynamic, memory will be automatically allocated for it. If the array is of a fixed size, the number of entries copied will be no more than the size of the array.

The country and currency parameters allow you to set an additional filtering of records by country or currency. The country parameter accepts a two-letter ISO 3166-1 alpha-2 country code (for example. "DE", "FR", "EU"), and the currency parameter accepts a three-letter currency designation (for example, "EUR", "CNY").

The default value NULL or an empty string "" in any of the parameters is equivalent to the absence of the corresponding filter.

If both filters are specified, only the values of those events are selected for which both conditions — country and currency — are satisfied simultaneously. This can come in handy if the calendar includes countries with multiple currencies, each of which also has circulation in several countries. There are no such events in the calendar at the moment. To get the events in the Eurozone countries, it is enough to specify the code of a particular country or "EU", and the currency "EUR" will be assumed.

The function returns the number of elements copied and can set an error code. In particular, if the request timeout from the server is exceeded, in _LastError we get error 5401 (ERR_CALENDAR_TIMEOUT). If the fixed array does not fit all the records, the code will be equal to 5400 (ERR_CALENDAR_MORE_DATA), but the array will be filled. When allocating memory for a dynamic array, error 4004 (ERR_NOT_ENOUGH_MEMORY) is potentially possible.

Attention! The order of the elements in an array can be different from chronological. You have to sort records by time.

Using the CalendarValueHistory function, we could query upcoming events like this:

```
   MqlCalendarValue values[];
   if(CalendarValueHistory(values, TimeCurrent()))
   {
      ArrayPrint(values);
   }

```

However, with this code, we will get a table with insufficient information, where the event names, importance, and currency codes will be hidden behind the event ID in the MqlCalendarValue::event_id field and, indirectly, behind the country identifier in the MqlCalendarEvent::country_id field. To make the output of information more user-friendly, you should request a description of the event by the event code, take the country code from this description, and get its attributes. Let's show it in the example script CalendarForDates.mq5.

In the input parameters, we will provide the ability to enter the country code and currency for filtering. By default, events for the European Union are requested.

```
input string CountryCode = "EU";
input string Currency = "";

```

The date range of the events will automatically count for some time back and forth. This "some time" will also be left to the user to choose from three options: a day, a week, or a month.

```
#define DAY_LONG   60 * 60 * 24
#define WEEK_LONG  DAY_LONG * 7
#define MONTH_LONG DAY_LONG * 30
#define YEAR_LONG  MONTH_LONG * 12
   
enum ENUM_CALENDAR_SCOPE
{
   SCOPE_DAY = DAY_LONG,
   SCOPE_WEEK = WEEK_LONG,
   SCOPE_MONTH = MONTH_LONG,
   SCOPE_YEAR = YEAR_LONG,
};
   
input ENUM_CALENDAR_SCOPE Scope = SCOPE_DAY;

```

Let's define our structure MqlCalendarRecord, derivative of MqlCalendarValue, and add fields to it for a convenient presentation of attributes that will be filled in by links (identifiers) from dependent structures.

```
struct MqlCalendarRecord: public MqlCalendarValue
{
   static const string importances[];
   
   string importance;
   string name;
   string currency;
   string code;
   double actual, previous, revised, forecast;
   ...
};
   
static const string MqlCalendarRecord::importances[] = {"None", "Low", "Medium", "High"};

```

Among the added fields there are lines with importance (one of the values of the static array importances), the name of the event, country, and currency, as well as four values in the double format. This actually means duplication of information for the sake of visual presentation when printing. Later we will prepare a more advanced "wrapper" for the calendar.

To fill the object, we will need a parametric constructor that takes the original structure MqlCalendarValue. After all the inherited fields are implicitly copied into the new object by the operator '=', we call the specially prepared extend method.

```
   MqlCalendarRecord() { }
   
   MqlCalendarRecord(const MqlCalendarValue &value)
   {
      this = value;
      extend();
   }

```

In the extend method, we get the description of the event by its identifier. Then, based on the country identifier from the event description, we get a structure with country attributes. After that, we can fill in the first half of the added fields from the received structures MqlCalendarEvent and MqlCalendarCountry.

```
   void extend()
   {
      MqlCalendarEvent event;
      CalendarEventById(event_id, event);
      
      MqlCalendarCountry country;
      CalendarCountryById(event.country_id, country);
      
      importance = importances[event.importance];
      name = event.name;
      currency = country.currency;
      code = country.code;
      
      MqlCalendarValue value = this;
      
      actual = value.GetActualValue();
      previous = value.GetPreviousValue();
      revised = value.GetRevisedValue();
      forecast = value.GetForecastValue();
   }

```

Next, we called the built-in Get methods for filling four fields of type double with financial indicators.

Now we can use the new structure in the main OnStart handler.

```
void OnStart()
{
   MqlCalendarValue values[];
   MqlCalendarRecord records[];
   datetime from = TimeCurrent() - Scope;
   datetime to = TimeCurrent() + Scope;
   if(PRTF(CalendarValueHistory(values, from, to, CountryCode, Currency)))
   {
      for(int i = 0; i < ArraySize(values); ++i)
      {
         PUSH(records, MqlCalendarRecord(values[i]));
      }
      Print("Near past and future calendar records (extended): ");
      ArrayPrint(records);
   }
}

```

Here the array of standard MqlCalendarValue structures is filled by calling CalendarValueHistory for the current conditions set in the input parameters. Next, all elements are transferred to the MqlCalendarRecord array. Moreover, while objects are being created, they are expanded with additional information. Finally, the array of events is output to the log.

The log entries are coming quite long. First, let's show the left half, which is exactly what we would see if we printed an array of standard MqlCalendarValue structures.

```
CalendarValueHistory(values,from,to,CountryCode,Currency)=6 / ok
Near past and future calendar records (extended): 
      [id] [event_id]              [time]            [period] [revision] [actual_value]         [prev_value] [revised_prev_value]     [forecast_value] [impact_type]
[0] 162723  999020003 2022.06.23 03:00:00 1970.01.01 00:00:00    0 -9223372036854775808 -9223372036854775808 -9223372036854775808 -9223372036854775808             0
[1] 162724  999020003 2022.06.24 03:00:00 1970.01.01 00:00:00    0 -9223372036854775808 -9223372036854775808 -9223372036854775808 -9223372036854775808             0
[2] 168518  999010034 2022.06.24 11:00:00 1970.01.01 00:00:00    0 -9223372036854775808 -9223372036854775808 -9223372036854775808 -9223372036854775808             0
[3] 168515  999010031 2022.06.24 13:10:00 1970.01.01 00:00:00    0 -9223372036854775808 -9223372036854775808 -9223372036854775808 -9223372036854775808             0
[4] 168509  999010014 2022.06.24 14:30:00 1970.01.01 00:00:00    0 -9223372036854775808 -9223372036854775808 -9223372036854775808 -9223372036854775808             0
[5] 161014  999520001 2022.06.24 22:30:00 2022.06.21 00:00:00    0 -9223372036854775808             -6000000 -9223372036854775808 -9223372036854775808             0
 

```

Here is the second half with the "decoding" of names, importance, and meanings.

```
CalendarValueHistory(values,from,to,CountryCode,Currency)=6 / ok
Near past and future calendar records (extended):
     [importance]                                                [name] [currency] [code] [actual] [previous] [revised] [forecast]
[0]  "High"       "EU Leaders Summit"                                   "EUR"      "EU"        nan        nan       nan        nan
[1]  "High"       "EU Leaders Summit"                                   "EUR"      "EU"        nan        nan       nan        nan
[2]  "Medium"     "ECB Supervisory Board Member McCaul Speech"          "EUR"      "EU"        nan        nan       nan        nan
[3]  "Medium"     "ECB Supervisory Board Member Fernandez-Bollo Speech" "EUR"      "EU"        nan        nan       nan        nan
[4]  "Medium"     "ECB Vice President de Guindos Speech"                "EUR"      "EU"        nan        nan       nan        nan
[5]  "Low"        "CFTC EUR Non-Commercial Net Positions"               "EUR"      "EU"        nan   -6.00000       nan        nan
 

```
