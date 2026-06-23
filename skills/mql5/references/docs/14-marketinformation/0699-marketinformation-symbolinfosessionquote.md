# SymbolInfoSessionQuote

Allows receiving time of beginning and end of the specified quoting sessions for a specified symbol and day of week.

```
bool  SymbolInfoSessionQuote(
   string            name,                // symbol name
   ENUM_DAY_OF_WEEK  day_of_week,         // day of the week
   uint              session_index,       // session index
   datetime&         from,                // time of the session beginning
   datetime&         to                   // time of the session end
   );

```

Parameters

name

[in]  Symbol name.

ENUM_DAY_OF_WEEK

[in]  Day of the week, value of enumeration [ENUM_DAY_OF_WEEK](/en/docs/constants/environment_state/marketinfoconstants#enum_day_of_week).

uint

[in]  Ordinal number of a session, whose beginning and end time we want to receive. Indexing of sessions starts with 0.

from

[out]  Session beginning time in seconds from 00 hours 00 minutes, in the returned value date should be ignored.

to

[out]  Session end time in seconds from 00 hours 00 minutes, in the returned value date should be ignored.

Return Value

If data for the specified session, symbol and day of the week are received, returns true, otherwise returns false.

Example:

```
#define SYMBOL_NAME   Symbol()
#define SESSION_INDEX 0
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- print the header with a symbol and SESSION_INDEX and
//--- in a loop by day of the week from Mon to Fri, print the start and end times of the quote session in the journal
   PrintFormat("Symbol %s, Quote session %d:", SYMBOL_NAME, SESSION_INDEX);
   for(int i=MONDAY; i<SATURDAY; i++)
      SymbolInfoSessionQuotePrint(SYMBOL_NAME, (ENUM_DAY_OF_WEEK)i, SESSION_INDEX);
   /*
   result:
   Symbol RU000A103661, Quote session 0:
   - Monday     06:45 - 00:00
   - Tuesday    06:45 - 00:00
   - Wednesday  06:45 - 00:00
   - Thursday   06:45 - 00:00
   - Friday     06:45 - 00:00
   */
  }
//+------------------------------------------------------------------+
//| Send the start and end times of the specified quote session      |
//| for the specified symbol and day of the week to the journal      |
//+------------------------------------------------------------------+
void SymbolInfoSessionQuotePrint(const string symbol, const ENUM_DAY_OF_WEEK day_of_week, const uint session_index)
  {
//--- declare variables to record the beginning and end of the quote session
   datetime date_from;  // session start time
   datetime date_to;    // session end time
   
//--- get data from the quotation session by symbol and day of the week
   if(!SymbolInfoSessionQuote(symbol, day_of_week, session_index, date_from, date_to))
     {
      Print("SymbolInfoSessionQuote() failed. Error ", GetLastError());
      return;
     }
     
//--- create the week day name from the enumeration constant
   string week_day=EnumToString(day_of_week);
   if(week_day.Lower())
      week_day.SetChar(0, ushort(week_day.GetChar(0)-32));
 
//--- send data for the specified quote session to the journal
   PrintFormat("- %-10s %s - %s", week_day, TimeToString(date_from, TIME_MINUTES), TimeToString(date_to, TIME_MINUTES));
  }

```

See also

[Symbol Properties](/en/docs/constants/environment_state/marketinfoconstants), [TimeToStruct](/en/docs/dateandtime/timetostruct), [Data Structures](/en/docs/constants/structures/mqldatetime)
