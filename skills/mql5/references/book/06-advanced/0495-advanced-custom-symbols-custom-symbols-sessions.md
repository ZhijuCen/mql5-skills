# Configuring quoting and trading sessions

Two API functions allow setting quoting and trading sessions of a custom instrument. These two concepts were discussed in the section [Schedules of trading and quoting sessions](/en/book/automation/symbols/symbols_sessions).

bool CustomSymbolSetSessionQuote(const string name, ENUM_DAY_OF_WEEK dayOfWeek,  

   uint sessionIndex, datetime from, datetime to)

bool CustomSymbolSetSessionTrade(const string name, ENUM_DAY_OF_WEEK dayOfWeek,  

   uint sessionIndex, datetime from, datetime to)

CustomSymbolSetSessionQuote sets the start and end time of the quoting session specified by number (sessionIndex) for a specific day of the week (dayOfWeek). CustomSymbolSetSessionTrade does the same for trading sessions.

Session numbering starts from 0.

Sessions can only be added sequentially, that is, a session with index 1 can only be added if there already exists a session with index 0. If this rule is violated, a new session will not be created, and the function will return false.

Date values in the from and to parameters are measured in seconds, and from should be less than to. The range is limited to two days, from 0 (00 hours 00 minutes 00 seconds) to 172800 (23 hours 59 minutes 59 seconds the next day). The day change was required in order to be able to specify sessions that begin before midnight and end after midnight. This situation often occurs when the exchange is located on the other side of the world relative to the broker (dealer) servers.

If zero start and end parameters (from = 0 and to = 0) are passed for the sessionIndex session, then it is deleted, and the numbering of the next sessions (if any) is shifted down.

Trading sessions cannot go beyond quoting ones.

For example, we can create a copy of an instrument for a different time zone by shifting the intraday quote time and session schedule for debugging the robot in different conditions, like with any exotic brokers.
