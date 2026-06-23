# ExpertRemove

The function stops an [Expert Advisor](/en/docs/mql5_guide#expert) and unloads it from a chart.

```
void  ExpertRemove();

```

Return Value

No return value.

Note

The Expert Advisor is not stopped immediately as you call ExpertRemove(); just a flag to stop the EA operation is set. That is, any next event won't be processed, [OnDeinit()](/en/docs/event_handlers/ondeinit) will be called and the Expert Advisor will be unloaded and removed from the chart.

Calling [ExpertRemove()](/en/docs/common/expertremove) in the strategy tester inside the [OnInit()](/en/docs/event_handlers/oninit) handler cancels testing on the current set of parameters. Such completion is considered an initialization error.

When calling [ExpertRemove()](/en/docs/common/expertremove) in the strategy tester after [successful initialization](/en/docs/event_handlers/oninit) of an EA, a test is completed normally with the call of [OnDeinit()](/en/docs/event_handlers/ondeinit) and [OnTester()](/en/docs/event_handlers/ontester). In this case, the entire trading statistics and an [optimization criterion](https://www.metatrader5.com/en/terminal/help/algotrading/optimization_types#criterion) value are obtained.

Example:

```
//+------------------------------------------------------------------+
//|                                            Test_ExpertRemove.mq5 |
//|                        Copyright 2009, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2009, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
input int ticks_to_close=20;// number of ticks before EA unload
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- 
   Print(TimeCurrent(),": " ,__FUNCTION__," reason code = ",reason);
//--- "clear" comment
   Comment("");
//---
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   static int tick_counter=0;
//---
   tick_counter++;
   Comment("\nBefore unloading expert advisor ",__FILE__," left",
           (ticks_to_close-tick_counter)," ticks");
//--- before
   if(tick_counter>=ticks_to_close)
     {
      ExpertRemove();
      Print(TimeCurrent(),": ",__FUNCTION__," expert advisor will be unloaded");
     }
   Print("tick_counter =",tick_counter);
//---
  }
//+------------------------------------------------------------------+

```

See also

[Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire)
