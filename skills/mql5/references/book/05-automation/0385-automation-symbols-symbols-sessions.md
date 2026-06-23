# Schedules of trading and quoting sessions

A little later, in further chapters, we will discuss the MQL5 API functions that allow us to automate trading operations. But first, we should study the technical features of the platform, which determine the success of calling these APIs. In particular, some restrictions are imposed by the specifications of financial instruments. In this chapter, we will gradually consider their programmatic analysis in full, and we will start with such an item as sessions.

When trading financial instruments, it should be taken into account that many international markets, such as stock exchanges, have predetermined opening hours, and information and trading are available only during these hours. Despite the fact that the terminal is constantly connected to the broker's server, an attempt to make a deal outside the working schedule will fail. In this regard, for each symbol, the terminal stores a schedule of sessions, that is, the time periods within a day when certain actions can be performed.

As you know, there are two main types of sessions: quoting and trading. During the quoting session, the terminal receives (may receive) current quotes. During the trading session, it is allowed to send trade orders and make deals. During the day, there may be several sessions of each type, with breaks (for example, morning and evening). It is obvious that the duration of the quoting sessions is greater than or equal to the trading ones.

In any case, session times, that is, opening and closing hours, are translated by the terminal from the local time zone of the exchange to the broker's time zone (server time).

The MQL5 API allows you to find out the quoting and trading sessions of each instrument using the SymbolInfoSessionQuote and SymbolInfoSessionTrade functions. In particular, this important information allows the program to check whether the market is currently open before sending a trade request to the server. Thus, we prevent the inevitable erroneous result and avoid unnecessary server loads. Keep in mind that in the case of massive erroneous requests to the server due to an incorrectly implemented MQL program, the server may begin to "ignore" your terminal, refusing to execute subsequent commands (even correct ones) for some time.

bool SymbolInfoSessionQuote(const string symbol, ENUM_DAY_OF_WEEK dayOfWeek, uint sessionIndex, datetime &from, datetime &to)

bool SymbolInfoSessionTrade(const string symbol, ENUM_DAY_OF_WEEK dayOfWeek, uint sessionIndex, datetime &from, datetime &to)

The functions work in the same way. For a given symbol and day of the week dayOfWeek, they fill in the from and to parameters passed by reference with the opening and closing times of the session with sessionIndex. Session indexing starts from 0. The ENUM_DAY_OF_WEEK structure was described in the section [Enumerations](/en/book/basis/builtin_types/enums).

There are no separate functions for querying the number of sessions: instead, we should be calling SymbolInfoSessionQuote andSymbolInfoSessionTrade with increasing index sessionIndex, until the function returns an error flag (false). When a session with the specified number exists, and the output arguments from and to received correct values, the functions return a success indicator (true).

According to the MQL5 documentation, in the received values of from and to of type datetime, the date should be ignored and only the time should be considered. This is because the information is an intraday schedule. However, there is an important exception to this rule.

Since the market is potentially open 24 hours a day, as in the case of Forex, or an exchange on the other side of the world, where daytime business hours coincide with the change of dates in your broker's "timezone", the end of sessions can have a time equal to or greater than 24 hours. For example, if the start of Forex sessions is 00:00, then the end is 24:00. However, from the point of view of the datetime type, 24 hours is 00 hours 00 minutes the very next day.

The situation becomes more confusing for those exchanges, where the schedule is shifted relative to your broker's time zone by several hours in such a way that the session starts on one day and ends on another. Because of this, the to variable registers not only time but also an extra day that cannot be ignored, because otherwise intraday time from will be more than intraday time to (for example, a session can last from 21:00 today to 8:00 tomorrow, that is, 21 > 8). In this case, the check for the occurrence of the current time inside the session ("time x is greater than the start and less than the end") will turn out to be incorrect (for example, the condition x >= 21 && x < 8 is not fulfilled for x = 23, although the session is actually active).

Thus, we come to the conclusion that it is impossible to ignore the date in the from/to parameters, and this point should be taken into account in the algorithms (see example).

To demonstrate the capabilities of the functions, let's return to an example of the script EnvPermissions.mq5 which was presented in the [Permissions](/en/book/common/environment/env_permissions) section. One of the types of permissions (or restrictions, if you like) refers specifically to the availability of trading. Earlier, the script took into account the terminal settings (TERMINAL_TRADE_ALLOWED) and the settings of a specific MQL program (MQL_TRADE_ALLOWED). Now we can add to it session checks to determine the trading permissions that are valid at a given moment for a particular symbol.

The new version of the script is called SymbolPermissions.mq5. It is also not final: in one of the following chapters, we will study the limitations imposed by the [trading account](/en/book/automation/account/account_limits_and_restrictions) settings.

Recall that the script implements the class Permissions, which provides a centralized description of all types of permissions/restrictions applicable to MQL programs. Among other things, the class has methods for checking the availability of trading: isTradeEnabled and isTradeOnSymbolEnabled. The first of these relates to global permissions and will remain almost unchanged:

```
class Permissions
{
public:
   static bool isTradeEnabled(const string symbol = NULL, const datetime now = 0)
   {
      return TerminalInfoInteger(TERMINAL_TRADE_ALLOWED)
          && MQLInfoInteger(MQL_TRADE_ALLOWED)
          && isTradeOnSymbolEnabled(symbol == NULL ? _Symbol : symbol, now);
   }
   ...

```

After checking the properties of the terminal and the MQL program, the script proceeds to isTradeOnSymbolEnabled where the symbol specification is analyzed. Previously, this method was practically empty.

In addition to the working symbol passed in the symbol parameter, the isTradeOnSymbolEnabled function receives the current time (now) and the required trading mode (mode). We will discuss the latter in more detail in the following sections (see [Trading permissions](/en/book/automation/symbols/symbols_trade_mode)). For now, let's just note that the default value of SYMBOL_TRADE_MODE_FULL gives maximum freedom (all trading operations are allowed).

```
   static bool isTradeOnSymbolEnabled(string symbol, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      // checking sessions
      bool found = now == 0;
      if(!found)
      {
         const static ulong day = 60 * 60 * 24;
         const ulong time = (ulong)now % day;
         datetime from, to;
         int i = 0;
         
         ENUM_DAY_OF_WEEK d = TimeDayOfWeek(now);
         
         while(!found && SymbolInfoSessionTrade(symbol, d, i++, from, to))
         {
            found = time >= (ulong)from && time < (ulong)to;
         }
      }
      // checking the trading mode for the symbol
      return found && (SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) == mode);
   }

```

If the now time is not specified (it is equal to 0 by default), we consider that we are not interested in sessions. This means that the found variable with an indication that a suitable session has been found (that is, a session containing the given time) is immediately set to true. But if the now parameter is specified, the function gets into the trading session analysis block.

To extract time without taking into account the date from the values of the datetime type, we describe the day constant equal to the number of seconds in a day. An expression like now % day will return the remainder of dividing the full date and time by the duration of one day, which will give only the time (the most significant digits in datetime will be null).

The TimeDayOfWeek function returns the day of the week for the given datetime value. It is located in the MQL5Book/DateTime.mqh header file which we have already used before (see [Date and time](/en/book/common/conversions/conversions_datetime)).

Further in the while loop, we call the SymbolInfoSessionTrade function while constantly incrementing the session index i until a suitable session is found or the function returns false (no more sessions). Thus, the program can get a complete list of sessions by day of the week, similar to what is displayed in the terminal in the symbol Specifications window.

Obviously, a suitable session is the one that contains the specified time value between the session beginning from and end to times. It is here that we take into account the problem associated with the possible round-the-clock trading: from and to are compared against time "as is", without discarding the day (from % day or to % day).

Once found becomes equal to true, we exit the loop. Otherwise, the loop will end when the allowed number of sessions is exceeded (function SymbolInfoSessionTrade will return false) and a suitable session will never be found.

If, according to the session schedule, trading is now allowed, we additionally check the trading mode for the symbol ([SYMBOL_TRADE_MODE](/en/book/automation/symbols/symbols_trade_mode)). For example, symbol trading can be completely prohibited ("indicative") or be in the "only closing positions" mode.

The above code has some simplifications compared to the final version in the file SymbolPermissions.mq5. It additionally implements a mechanism for marking the source of the restriction that caused the trade to be disabled. All such sources are summarized in the TRADE_RESTRICTIONS enumeration.

```
   enum TRADE_RESTRICTIONS
   {
      TERMINAL_RESTRICTION = 1,
      PROGRAM_RESTRICTION = 2,
      SYMBOL_RESTRICTION = 4,
      SESSION_RESTRICTION = 8,
   };

```

At the moment, the restriction can come from 4 instances: the terminal, the program, the symbol, and the session schedule. We will add more options later.

To register the fact that a constraint was found in the Permissions class, we have the lastFailReasonBitMask variable which allows the collection of a bit mask from the elements of the enumeration using an auxiliary method pass (the bit is set up when the checked condition value is false, and the bit equals false).

```
   static uint lastFailReasonBitMask;
   static bool pass(const bool value, const uint bitflag) 
   {
      if(!value) lastFailReasonBitMask |= bitflag;
      return value;
   }

```

Calling the pass method with a specific flag is done at the appropriate validation steps. For example, the isTradeEnabled method in full looks like this:

```
   static bool isTradeEnabled(const string symbol = NULL, const datetime now = 0)
   {
      lastFailReasonBitMask = 0;
      return pass(TerminalInfoInteger(TERMINAL_TRADE_ALLOWED), TERMINAL_RESTRICTION)
          && pass(MQLInfoInteger(MQL_TRADE_ALLOWED), PROGRAM_RESTRICTION)
          && isTradeOnSymbolEnabled(symbol == NULL ? _Symbol : symbol, now);
   }

```

Due to this, with a negative result of the call TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) or MQLInfoInteger(MQL_TRADE_ALLOWED), either the TERMINAL_RESTRICTION or the PROGRAM_RESTRICTION flag will be set, respectively.

The isTradeOnSymbolEnabled method also sets its own flags when problems are detected, including session flags.

```
   static bool isTradeOnSymbolEnabled(string symbol, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      ...
      return pass(found, SESSION_RESTRICTION)
         && pass(SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) == mode, SYMBOL_RESTRICTION);
   }

```

As a result, the MQL program that is using the query Permissions::isTradeEnabled, after receiving a restriction, may clarify its meaning using the getFailReasonBitMask and explainBitMask methods: the first one returns the mask of set prohibition flags "as is", and the second one forms a user-friendly text description of the restrictions.

```
   static uint getFailReasonBitMask()
   {
      return lastFailReasonBitMask;
   }
   
   static string explainBitMask()
   {
      string result = "";
      for(int i = 0; i < 4; ++i)
      {
         if(((1 << i) & lastFailReasonBitMask) != 0)
         {
            result += EnumToString((TRADE_RESTRICTIONS)(1 << i));
         }
      }
      return result;
   }

```

With the above Permissions class in the OnStart handler, a check is made for the availability of trading for all symbols from the Market Watch (currently,TimeCurrent).

```
void OnStart()
{
   string disabled = "";
   
   const int n = SymbolsTotal(true);
   for(int i = 0; i < n; ++i)
   {
      const string s = SymbolName(i, true);
      if(!Permissions::isTradeEnabled(s, TimeCurrent()))
      {
         disabled += s + "=" + Permissions::explainBitMask() +"\n";
      }
   }
   if(disabled != "")
   {
      Print("Trade is disabled for the following symbols and origins:");
      Print(disabled);
   }
}

```

If trading is prohibited for a certain symbol, we will see an explanation in the log.

```
   Trade is disabled for following symbols and origins:
   USDRUB=SESSION_RESTRICTION
   SP500m=SYMBOL_RESTRICTION

```

In this case, the market is closed for "USDRUB" and trading is disabled for the "SP500m" symbol (more strictly, it does not correspond to the SYMBOL_TRADE_MODE_FULL mode).

It is assumed that when running the script, algorithmic trading was enabled globally in the terminal. Otherwise, we will additionally see TERMINAL_RESTRICTION and PROGRAM_RESTRICTION prohibitions in the log.
