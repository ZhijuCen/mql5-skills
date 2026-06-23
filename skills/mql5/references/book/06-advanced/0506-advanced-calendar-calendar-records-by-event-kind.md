# Getting event records of a specific type

If necessary, an MQL program has the ability to request events of a specific type: to do this, it is enough to know the event identifier in advance, for example, using the CalendarEventByCountry or CalendarEventByCurrency functions which were presented in the section [Querying event types by country and currency](/en/book/advanced/calendar/calendar_event_kinds_by_country_currency).

int CalendarValueHistoryByEvent(ulong id, MqlCalendarValue &values[], datetime from, datetime to = 0)

The CalendarValueHistoryByEvent function fills the array passed by reference with records of events of a specific type indicated by the id identifier. Parameters from and to allow you to limit the range of dates in which events are searched.

If an optional parameter to is not specified, all calendar entries will be placed in the array, starting from the from time and further into the future. To query all the past events, set from to 0. If both from and to parameters are 0, all history and scheduled events will be returned. In all other cases, when to is not equal to 0, it must be greater than from.

The values array can be dynamic (then the function will automatically expand or reduce it according to the amount of data) or of fixed size (then only a part that fits will be copied into the array).

The function returns the number of copied elements.

As an example, consider the script CalendarStatsByEvent.mq5, which calculates the statistics (frequency of occurrence) of events of different types for a given country or currency in a given time range.

The analysis conditions are specified in the input variables.

```
input string CountryOrCurrency = "EU";
input ENUM_CALENDAR_SCOPE Scope = SCOPE_YEAR;

```

Depending on the length of the CountryOrCurrency string, it is interpreted as a country code (2 characters) or currency code (3 characters).

To collect statistics, we will declare a structure; its fields will store the identifier and name of the event type, its importance, and the counter of such events.

```
struct CalendarEventStats
{
   static const string importances[];
   ulong id;
   string name;
   string importance;
   int count;
};
   
static const string CalendarEventStats::importances[] = {"None", "Low", "Medium", "High"};

```

In the OnStart function, we first request all kinds of events using the CalendarEventByCountry or CalendarEventByCurrency function to the specified depth of history and into the future, and then, in a loop through the event descriptions received in the events array, we call CalendarValueHistoryByEvent for each event ID. In this application, we are not interested in the contents of the values array, as we just need to know their count.

```
void OnStart()
{
   MqlCalendarEvent events[];
   MqlCalendarValue values[];
   CalendarEventStats stats[];
   
   const datetime from = TimeCurrent() - Scope;
   const datetime to = TimeCurrent() + Scope;
   
   if(StringLen(CountryOrCurrency) == 2)
   {
      PRTF(CalendarEventByCountry(CountryOrCurrency, events));
   }
   else
   {
      PRTF(CalendarEventByCurrency(CountryOrCurrency, events));
   }
   
   for(int i = 0; i < ArraySize(events); ++i)
   {
      if(CalendarValueHistoryByEvent(events[i].id, values, from, to))
      {
         CalendarEventStats event = {events[i].id, events[i].name,
            CalendarEventStats::importances[events[i].importance], ArraySize(values)};
         PUSH(stats, event);
      }
   }
   
   SORT_STRUCT(CalendarEventStats, stats, count);
   ArrayReverse(stats);
   ArrayPrint(stats);
}

```

Upon successful function call, we fill the CalendarEventStats structure and add it to the array of structures stats. Next, we sort the structure in the way we already know (the SORT_STRUCT macro is described in the section [Comparing, sorting, and searching in arrays](/en/book/common/arrays/arrays_compare_sort_search)).

Running the script with default settings generates something like this in the log (abbreviated).

```
CalendarEventByCountry(CountryOrCurrency,events)=82 / ok
          [id]                                                [name] [importance] [count]
[ 0] 999520001 "CFTC EUR Non-Commercial Net Positions"               "Low"             79
[ 1] 999010029 "ECB President Lagarde Speech"                        "High"            69
[ 2] 999010035 "ECB Executive Board Member Elderson Speech"          "Medium"          37
[ 3] 999030027 "Core CPI"                                            "Low"             36
[ 4] 999030026 "CPI"                                                 "Low"             36
[ 5] 999030025 "CPI excl. Energy and Unprocessed Food y/y"           "Low"             36
[ 6] 999030024 "CPI excl. Energy and Unprocessed Food m/m"           "Low"             36
[ 7] 999030010 "Core CPI m/m"                                        "Medium"          36
[ 8] 999030013 "CPI y/y"                                             "Low"             36
[ 9] 999030012 "Core CPI y/y"                                        "Low"             36
[10] 999040006 "Consumer Confidence Index"                           "Low"             36
[11] 999030011 "CPI m/m"                                             "Medium"          36
...
[65] 999010008 "ECB Economic Bulletin"                               "Medium"           8
[66] 999030023 "Wage Costs y/y"                                      "Medium"           6
[67] 999030009 "Labour Cost Index"                                   "Low"              6
[68] 999010025 "ECB Bank Lending Survey"                             "Low"              6
[69] 999010030 "ECB Supervisory Board Member af Jochnick Speech"     "Medium"           4
[70] 999010022 "ECB Supervisory Board Member Hakkarainen Speech"     "Medium"           3
[71] 999010028 "ECB Financial Stability Review"                      "Medium"           3
[72] 999010009 "ECB Targeted LTRO"                                   "Medium"           2
[73] 999010036 "ECB Supervisory Board Member Tuominen Speech"        "Medium"           1
 

```

Please note that a total of 82 types of events were received, however, in the statistics array, we had only 74. This is because the CalendarValueHistoryByEvent function returns false (failure) and zero error code in _LastError if there were no events of any kind in the specified date range. In the above test, there are 8 such entries that theoretically exist but were never encountered within the year.
