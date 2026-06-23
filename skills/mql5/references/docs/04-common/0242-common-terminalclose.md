# TerminalClose

The function commands the terminal to complete operation.

```
bool  TerminalClose(
   int ret_code      // closing code of the client terminal
   );

```

Parameters

ret_code

[in]  Return code, returned by the process of the client terminal at the operation completion.

Return Value

The function returns true on success, otherwise  - false.

Note

The TerminalClose() function does not stop the terminal immediately, it just commands the terminal to complete its operation.

The code of an Expert Advisor that called TerminalClose() must have all arrangements for the immediate completion (e.g. all previously opened files must be closed in the normal mode). Call of this function must be followed by the [return operator](/en/docs/basis/operators/return).

The ret_code parameter allows indicating the necessary return code for analyzing reasons of the program termination of the terminal operation when starting it from the command prompt.

Example:

```
//--- input parameters
input int  tiks_before=500; // number of ticks till termination
input int  pips_to_go=15;   // distance in pips 
input int  seconds_st=50;   // number of seconds given to the Expert Advisor
//--- globals
datetime   launch_time;
int        tick_counter=0;
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   Print(__FUNCTION__," reason code = ",reason);
   Comment("");
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   static double first_bid=0.0;
   MqlTick       tick;
   double        distance;
//---
   SymbolInfoTick(_Symbol,tick);
   tick_counter++;
   if(first_bid==0.0)
     {
      launch_time=tick.time;
      first_bid=tick.bid;
      Print("first_bid =",first_bid);
      return;
     }
//--- price distance in pips
   distance=(tick.bid-first_bid)/_Point;
//--- show a notification to track the EA operation
   string comm="From the moment of start:\r\n\x25CF elapsed seconds: "+
               IntegerToString(tick.time-launch_time)+" ;"+
               "\r\n\x25CF ticks received: "+(string)tick_counter+" ;"+
               "\r\n\x25CF price went in points: "+StringFormat("%G",distance);
   Comment(comm);
//--- section for checking condition to close the terminal
   if(tick_counter>=tiks_before)
      TerminalClose(0);    // exit by tick counter
   if(distance>pips_to_go)
      TerminalClose(1);    // go up by the number of pips equal to pips_to_go
   if(distance<-pips_to_go)
      TerminalClose(-1);   // go down by the number of pips equal to pips_to_go
   if(tick.time-launch_time>seconds_st)
      TerminalClose(100);  // termination by timeout
//---
  }

```

See also

[Program running](/en/docs/runtime/running), [Execution errors](/en/docs/runtime/errors), [Reasons for deinitialization](/en/docs/constants/namedconstants/uninit)
