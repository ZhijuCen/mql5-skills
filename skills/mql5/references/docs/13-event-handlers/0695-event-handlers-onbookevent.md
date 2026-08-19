# OnBookEvent

The function is called in indicators and EAs when the [BookEvent](/en/docs/runtime/event_fire#bookevent) event occurs. It is meant for handling Depth of Market changes.

```
void  OnBookEvent(
   const string&  symbol         // symbol
   );

```

Parameters

symbol

[in]  Name of a symbol the [BookEvent](/en/docs/runtime/event_fire#bookevent) has arrived for

Return Value

No return value

Note

To get the BookEvent events for any symbol, simply subscribe to receive them for this symbol using the [MarketBookAdd()](/en/docs/marketinformation/symbolinfosessiontrade) function. To cancel subscription for receiving the BookEvent for a certain symbol, call the [MarketBookRelease()](/en/docs/marketinformation/marketbookrelease) function.

The BookEvent broadcasts within the entire chart. This means that if one application on a chart subscribes to the BookEvent using the MarketBookAdd function, all other indicators and EAs launched on the same chart and having the OnBookEvent() handler receive this event as well. Therefore, it is necessary to analyze a symbol name passed to the OnBookEvent() handler as the symbol parameter.

Separate BookEvent counters sorted by symbols are provided for all applications running on the same chart. This means that each chart may have multiple subscriptions to different symbols, and a counter is provided for each symbol. Subscribing and unsubscribing from BookEvent changes the subscription counter for specified symbols only within one chart. In other words, there may be two adjacent charts to the BookEvent for the same symbol but different subscription counter values.

The initial subscription counter value is zero. At each [MarketBookAdd()](/en/docs/marketinformation/symbolinfosessiontrade) call, the subscription counter for a specified symbol on the chart is increased by one (chart symbol and symbol in MarketBookAdd() do not have to match). When calling [MarketBookRelease()](/en/docs/marketinformation/marketbookrelease), the counter of subscriptions for a specified symbol within the chart is decreased by one. The BookEvent events for any symbol are broadcast within the chart till the counter is equal to zero. Therefore, it is important that each MQL5 program that contains [MarketBookAdd ()](/en/docs/marketinformation/symbolinfosessiontrade) calls correctly unsubscribes from getting events for each symbol using [MarketBookRelease ()](/en/docs/marketinformation/marketbookrelease) at the end of its work. To achieve this, the number of [MarketBookAdd()](/en/docs/marketinformation/symbolinfosessiontrade) and  [MarketBookRelease()](/en/docs/marketinformation/marketbookrelease) calls should be even for each call during the entire MQL5 program lifetime. Using flags or custom subscription counters within the program allows you to safely work with BookEvent events and prevents disabling subscriptions for getting this event in third-party programs within the same chart.

[BookEvent](/en/docs/runtime/event_fire#bookevent) events are never skipped and are always placed into a queue even if handling the previous BookEvent handling is not over yet.

Example

```
//+------------------------------------------------------------------+
//|                                           OnBookEvent_Sample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com/en/articles/2635"
#property version   "1.00"
#property description "Example of measuring the market depth refresh rate using OnBookEvent()"
#property description "The code is taken from the article https://www.mql5.com/en/articles/2635"
//--- input parameters
input ulong ExtCollectTime   =30;  // test time in seconds
input ulong ExtSkipFirstTicks=10;  // number of ticks skipped at start
//--- flag of subscription to BookEvent events
bool book_subscribed=false;
//--- array for accepting requests from the market depth
MqlBookInfo  book[];
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- show the start
   Comment(StringFormat("Waiting for the first %I64u ticks to arrive",ExtSkipFirstTicks));
   PrintFormat("Waiting for the first %I64u ticks to arrive",ExtSkipFirstTicks);
//--- enable market depth broadcast
   if(MarketBookAdd(_Symbol))
     {
      book_subscribed=true;
      PrintFormat("%s: MarketBookAdd(%s) function returned true",__FUNCTION__,_Symbol);
     }
   else
      PrintFormat("%s: MarketBookAdd(%s) function returned false! GetLastError()=%d",__FUNCTION__,_Symbol,GetLastError());
//--- successful initialization
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Deinitialize expert                                              |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- display deinitialization reason code
   Print(__FUNCTION__,": Deinitialization reason code = ",reason);  
//--- cancel subscription for getting market depth events
   if(book_subscribed)
     {
      if(!MarketBookRelease(_Symbol))
         PrintFormat("%s: MarketBookRelease(%s) returned false! GetLastError()=%d",_Symbol,GetLastError());
      else
         book_subscribed=false;
     }
//--- 
  }
//+------------------------------------------------------------------+
//| BookEvent function                                               |
//+------------------------------------------------------------------+
void OnBookEvent(const string &symbol)
  {
   static ulong starttime=0;             // test start time
   static ulong tickcounter=0;           // market depth update counter
//--- work with depth market events only if we subscribed to them ourselves
   if(!book_subscribed)
      return;
//--- count updates only for a certain symbol
   if(symbol!=_Symbol)
      return;
//--- skip first ticks to clear the queue and to prepare
   tickcounter++;
   if(tickcounter<ExtSkipFirstTicks)
      return;
//--- remember the start time
   if(tickcounter==ExtSkipFirstTicks) 
      starttime=GetMicrosecondCount();
//--- request for the market depth data
   MarketBookGet(symbol,book);
//--- when to stop?  
   ulong endtime=GetMicrosecondCount()-starttime;
   ulong ticks  =1+tickcounter-ExtSkipFirstTicks;
// how much time has passed in microseconds since the start of the test?
   if(endtime>ExtCollectTime*1000*1000) 
     {
      PrintFormat("%I64u ticks for %.1f seconds: %.1f ticks/sec ",ticks,endtime/1000.0/1000.0,ticks*1000.0*1000.0/endtime);
      ExpertRemove();
      return;
     }
//--- display the counters in the comment field
   if(endtime>0)
      Comment(StringFormat("%I64u ticks for %.1f seconds: %.1f ticks/sec ",ticks,endtime/1000.0/1000.0,ticks*1000.0*1000.0/endtime));
  }

```

See also

[MarketBookAdd](/en/docs/marketinformation/marketbookadd), [MarketBookRelease](/en/docs/marketinformation/marketbookrelease), [MarketBookGet](/en/docs/marketinformation/marketbookget), [OnTrade](/en/docs/event_handlers/ontrade), [OnTradeTransaction](/en/docs/event_handlers/ontradetransaction), [OnTick](/en/docs/event_handlers/ontick), [Event handling functions](/en/docs/basis/function/events), [Program running](/en/docs/runtime/running), [Client terminal events](/en/docs/runtime/event_fire)
