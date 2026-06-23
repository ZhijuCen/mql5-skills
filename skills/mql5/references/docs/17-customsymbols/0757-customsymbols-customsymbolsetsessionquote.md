# CustomSymbolSetSessionQuote

Sets the start and end time of the specified quotation session for the specified symbol and week day.

```
bool  CustomSymbolSetSessionQuote(
   const string      symbol_name,         // symbol name
   ENUM_DAY_OF_WEEK  day_of_week,         // week day
   uint              session_index,       // session index
   datetime          from,                // session start time
   datetime          to                   // session end time
   );

```

Parameters

symbol_name

[in]  Custom symbol name.

ENUM_DAY_OF_WEEK

[in]  Week day, value from the [ENUM_DAY_OF_WEEK](/en/docs/constants/environment_state/marketinfoconstants#enum_day_of_week) enumeration.

uint

[in]  Index of the session, for which start and end times are to be set. Session indexing starts from 0.

from

[in]  Session start time in seconds from 00:00, data value in the variable is ignored.

to

[in]  Session end time in seconds from 00:00, data value in the variable is ignored.

Return Value

true – success, otherwise – false. To get information about the error, call the [GetLastError()](/en/docs/check/getlasterror) function.

Note

If the session with the specified session_index already exists, the function simply edits the beginning and end of the session.

If zero start and end parameters have been passed for the session (from=0 and to=0), the appropriate session with the session_index is deleted, while the session indexing is shifted downwards.

Sessions can be added only sequentially. In other words, you can add session_index=1 only if the session with the index 0 already exists. If this rule is broken, a new session is not created, while the function itself returns 'false'.

Example:

```
//+------------------------------------------------------------------+
//|                                  CustomSymbolSetSessionQuote.mq5 |
//|                                  Copyright 2024, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#define   CUSTOM_SYMBOL_NAME     Symbol()+".C"           // custom symbol name
#define   CUSTOM_SYMBOL_PATH     "Forex"                 // name of the group, in which a symbol is to be created
#define   CUSTOM_SYMBOL_ORIGIN   Symbol()                // name of a symbol a custom one is to be based on
 
#define   SESSION_0_FROM         D'1970.01.01 00:15:00'  // session 0 start time
#define   SESSION_0_TO           D'1970.01.01 11:59:00'  // session 0 end time
#define   SESSION_1_FROM         D'1970.01.01 12:15:00'  // session 1 start time
#define   SESSION_1_TO           D'1970.01.01 23:59:00'  // session 1 end time
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the error code when creating a custom symbol
   int create=CreateCustomSymbol(CUSTOM_SYMBOL_NAME, CUSTOM_SYMBOL_PATH, CUSTOM_SYMBOL_ORIGIN);
   
//--- if the error code is not 0 (successful symbol creation) and not 5304 (symbol has already been created) - leave
   if(create!=0 && create!=5304)
      return;
    
//--- print the header with the base symbol and session index and 
//--- in a loop by day of the week from Mon to Fri, print the start and end times of each quote session in the journal 
   for(int session=0; session<2; session++)
     {
      PrintFormat("Quote session %d of '%s' symbol from which the custom '%s' was created", session, CUSTOM_SYMBOL_ORIGIN, CUSTOM_SYMBOL_NAME); 
      for(int day_of_week=MONDAY; day_of_week<SATURDAY; day_of_week++) 
         SymbolInfoSessionQuotePrint(CUSTOM_SYMBOL_ORIGIN, (ENUM_DAY_OF_WEEK)day_of_week, session);     
     }
     
//--- in a loop by two sessions
   bool res=true;
   for(int session=0; session<2; session++)
     {
      datetime from = SESSION_0_FROM;
      datetime to   = SESSION_0_TO;
      if(session>0)
        {
         from = SESSION_1_FROM;
         to   = SESSION_1_TO;
        }
      //--- set the quote sessions time for a custom symbol of each day of the week
      ResetLastError();
      for(int day_of_week=MONDAY; day_of_week<SATURDAY; day_of_week++)
         res &=CustomSymbolSetSessionQuote(CUSTOM_SYMBOL_NAME, (ENUM_DAY_OF_WEEK)day_of_week, session, from, to);
     }
 
//--- if there was an error when setting any of the sessions, display an appropriate message in the journal
   if(!res)
      Print("CustomSymbolSetSessionQuote() failed. Error ", GetLastError());
   
//--- print the header with the custom symbol and session index and 
//--- in a loop by day of the week from Mon to Fri, print the start and end times of each quote session in the journal 
   for(int session=0; session<2; session++)
     {
      PrintFormat("Quote session %d of custom symbol '%s' based on '%s'", session, CUSTOM_SYMBOL_NAME, CUSTOM_SYMBOL_ORIGIN); 
      for(int day_of_week=MONDAY; day_of_week<SATURDAY; day_of_week++) 
         SymbolInfoSessionQuotePrint(CUSTOM_SYMBOL_NAME, (ENUM_DAY_OF_WEEK)day_of_week, session);     
     }
     
//--- display a hint about the script termination keys on the chart comment
   Comment(StringFormat("Press 'Esc' to exit or 'Del' to delete the '%s' symbol and exit", CUSTOM_SYMBOL_NAME));
//--- wait for pressing the Esc or Del keys to exit in an endless loop
   while(!IsStopped() && TerminalInfoInteger(TERMINAL_KEYSTATE_ESCAPE)==0)
     {
      Sleep(16);
      //--- when pressing Del, delete the created custom symbol
      if(TerminalInfoInteger(TERMINAL_KEYSTATE_DELETE)<0)
        {
         if(DeleteCustomSymbol(CUSTOM_SYMBOL_NAME))
            PrintFormat("Custom symbol '%s' deleted successfully", CUSTOM_SYMBOL_NAME);
         break;
        }
     }
//--- clear the chart before exiting
   Comment("");
   /*
   result:
   Quote session 0 of 'EURUSD' symbol from which the custom 'EURUSD.C' was created
   - Monday     00:15 - 23:55
   - Tuesday    00:15 - 23:55
   - Wednesday  00:15 - 23:55
   - Thursday   00:15 - 23:55
   - Friday     00:15 - 23:55
   Quote session 1 of 'EURUSD' symbol from which the custom 'EURUSD.C' was created
   - Monday     Session not set
   - Tuesday    Session not set
   - Wednesday  Session not set
   - Thursday   Session not set
   - Friday     Session not set
   Quote session 0 of custom symbol 'EURUSD.C' based on 'EURUSD'
   - Monday     00:15 - 11:59
   - Tuesday    00:15 - 11:59
   - Wednesday  00:15 - 11:59
   - Thursday   00:15 - 11:59
   - Friday     00:15 - 11:59
   Quote session 1 of custom symbol 'EURUSD.C' based on 'EURUSD'
   - Monday     12:15 - 23:59
   - Tuesday    12:15 - 23:59
   - Wednesday  12:15 - 23:59
   - Thursday   12:15 - 23:59
   - Friday     12:15 - 23:59
   */
  }
//+------------------------------------------------------------------+
//| Create a custom symbol, return an error code                     |
//+------------------------------------------------------------------+
int CreateCustomSymbol(const string symbol_name, const string symbol_path, const string symbol_origin=NULL)
  {
//--- define the name of a symbol a custom one is to be based on
   string origin=(symbol_origin==NULL ? Symbol() : symbol_origin);
   
//--- if failed to create a custom symbol and this is not error 5304, report this in the journal
   ResetLastError();
   int error=0;
   if(!CustomSymbolCreate(symbol_name, symbol_path, origin))
     {
      error=GetLastError();
      if(error!=5304)
         PrintFormat("CustomSymbolCreate(%s, %s, %s) failed. Error %d", symbol_name, symbol_path, origin, error);
     }
//--- successful
   return(error);
  }
//+------------------------------------------------------------------+
//| Remove a custom symbol                                           |
//+------------------------------------------------------------------+
bool DeleteCustomSymbol(const string symbol_name)
  {
//--- hide the symbol from the Market Watch window
   ResetLastError();
   if(!SymbolSelect(symbol_name, false))
     {
      PrintFormat("SymbolSelect(%s, false) failed. Error %d", GetLastError());
      return(false);
     }
      
//--- if failed to delete a custom symbol, report this in the journal and return 'false'
   ResetLastError();
   if(!CustomSymbolDelete(symbol_name))
     {
      PrintFormat("CustomSymbolDelete(%s) failed. Error %d", symbol_name, GetLastError());
      return(false);
     }
//--- successful
   return(true);
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
    
//--- create the week day name from the enumeration constant 
   string week_day=EnumToString(day_of_week); 
   if(week_day.Lower()) 
      week_day.SetChar(0, ushort(week_day.GetChar(0)-32)); 
  
//--- get data from the quotation session by symbol and day of the week 
   if(!SymbolInfoSessionQuote(symbol, day_of_week, session_index, date_from, date_to)) 
     { 
      int err=GetLastError();
      string message=(err==4307 ? StringFormat("- %-10s Session not set", week_day) : 
                      StringFormat("SymbolInfoSessionQuote(%s, %s, session %d) failed. Error %d", symbol, week_day, session_index, GetLastError()));
      Print(message); 
      return; 
     } 
      
//--- send data for the specified quote session to the journal 
   PrintFormat("- %-10s %s - %s", week_day, TimeToString(date_from, TIME_MINUTES), TimeToString(date_to, TIME_MINUTES)); 
  }

```

See also

[SymbolInfoSessionQuote](/en/docs/marketinformation/symbolinfosessionquote), [Symbol info](/en/docs/constants/environment_state/marketinfoconstants), [TimeToStruct](/en/docs/dateandtime/timetostruct), [Date structure](/en/docs/constants/structures/mqldatetime)
