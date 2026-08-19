# CopyTicks

The function receives ticks in the [MqlTick](/en/docs/constants/structures/mqltick) format into ticks_array. In this case, ticks are indexed from the past to the present, i.e. the 0 indexed tick is the oldest one in the array. For tick analysis, check the flags field, which shows what exactly has changed in the tick.

```
int  CopyTicks(
   string           symbol_name,           // Symbol name
   MqlTick&         ticks_array[],         // Tick receiving array
   uint             flags=COPY_TICKS_ALL,  // The flag that determines the type of received ticks
   ulong            from=0,                // The date from which you want to request ticks
   uint             count=0                // The number of ticks that you want to receive
   );

```

Parameters

symbol_name

[in]  Symbol.

ticks_array

[out]  An array of the [MqlTick](/en/docs/constants/structures/mqltick) type for receiving ticks.

flags

[in]  A flag to define the type of the requested ticks. COPY_TICKS_INFO – ticks with Bid and/or Ask changes, COPY_TICKS_TRADE – ticks with changes in Last and Volume, COPY_TICKS_ALL – all ticks. For any type of request, the values of the previous tick are added to the remaining fields of the MqlTick structure.

from

[in]   The date from which you want to request ticks. In milliseconds since 1970.01.01. If from=0, the last count ticks will be returned.

count

[in]  The number of requested ticks. If the 'from' and 'count' parameters are not specified, all available recent ticks (but not more than 2000) will be written to ticks_array[].

Returned value

The number of copied tick or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

The CopyTicks() function allows requesting and analyzing all received ticks. The first call of CopyTicks() initiates synchronization of the symbol's tick database stored on the hard disk. If the local database does not provide all the requested ticks, then missing ticks will be automatically downloaded from the trade server. Ticks beginning with the from date specified in CopyTicks() till the current moment will be synchronized. After that, all ticks arriving for this symbol will be added to the tick database thus keeping it in the synchronized state.

If the from and count parameters are not specified, all available recent ticks (but not more than 2000) will be written to ticks_array[]. The flags parameter allows specifying the type of required ticks.

COPY_TICKS_INFO – ticks with Bid and/or Ask price changes are returned. Data of other fields will also be added. For example, if only the Bid has changed, the ask and volume fields will be filled with last known values. To find out exactly what has changed, analyze the flags field, which will have the value of TICK_FLAG_BID and/or TICK_FLAG_ASK. If a tick has zero values of the Bid and Ask prices, and the flags show that these data have changed (flags=TICK_FLAG_BID|TICK_FLAG_ASK), this means that the order book (Market Depth) is empty. In other words, there are no buy and sell orders.

COPY_TICKS_TRADE – ticks with the Last price and volume changes are returned. Data of other fields will also be added, i.e. last known values of Bid and Ask will be specified in the appropriate fields. To find out exactly what has changed, analyze the flags field, which will have the TICK_FLAG_LAST and TICK_FLAG_VOLUME value.

COPY_TICKS_ALL – all ticks with any change are returned. Unchanged fields will be filled with last known values.

Call of CopyTicks() with the COPY_TICKS_ALL flag immediately returns all ticks from the request interval, while calls in other modes require some time to process and select ticks, therefore they do not provide significant speed advantage.

When requesting ticks (either COPY_TICKS_INFO or COPY_TICKS_TRADE), every tick contains full price information as of the time of the tick (bid, ask, last and volume). This feature is provided for an easier analysis of the trade state at the time of each tick, so there is no need to request a deep tick history and search for the values of other fields.

In indicators, the CopyTicks() function returns the result: when called from an indicator, CopyTick() immediately returns all available ticks of a symbol, and will launch synchronization of the tick database, if available data is not enough. All indicators in one symbol operate in one common thread, so the indicator cannot wait for the completion of synchronization. After synchronization, CopyTicks() will return all requested ticks during the next call. In indicators, the [OnCalculate()](/en/docs/event_handlers/oncalculate) function is called after the arrival of each tick.

CopyTicks() can wait for the result for 45 seconds in Expert Advisors and scripts: as distinct from indicators, every Expert Advisor and script operate in a separate thread, and therefore can wait 45 seconds till the completion of synchronization. If the required amount of ticks fails to be synchronized during this time, CopyTicks() will return available ticks by timeout and will continue synchronization. [OnTick()](/en/docs/event_handlers/ontick) in Expert Advisor is not a handler of every tick, it only notifies an Expert Advisor about changes in the market. It can be a batch of changes: the terminal can simultaneously make a few ticks, but OnTick() will be called only once to notify the EA of the latest market state.

The rate of data return: the terminal stores in the fast access cache 4,096 last ticks for each instrument (65,536 ticks for symbols with a running Market Depth). If requested ticks for the current trading session are beyond the cache, CopyTicks() calls the ticks stored in the terminal memory. These requests require more time for execution. The slowest requests are those requesting ticks for other days, since the data is read from the disk in this case.

Example:

```
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property script_show_inputs
//--- Requesting 100 million ticks to be sure we receive the entire tick history
input int      getticks=100000000; // The number of required ticks
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---  
   int     attempts=0;     // Count of attempts
   bool    success=false;  // The flag of a successful copying of ticks
   MqlTick tick_array[];   // Tick receiving array
   MqlTick lasttick;       // To receive last tick data
   SymbolInfoTick(_Symbol,lasttick);
//--- Make 3 attempts to receive ticks
   while(attempts<3)
     {
      //--- Measuring start time before receiving the ticks
      uint start=GetTickCount();
//--- Requesting the tick history since 1970.01.01 00:00.001 (parameter from=1 ms)
      int received=CopyTicks(_Symbol,tick_array,COPY_TICKS_ALL,1,getticks);
      if(received!=-1)
        {
         //--- Showing information about the number of ticks and spent time
         PrintFormat("%s: received %d ticks in %d ms",_Symbol,received,GetTickCount()-start);
         //--- If the tick history is synchronized, the error code is equal to zero
         if(GetLastError()==0)
           {
            success=true;
            break;
           }
         else
            PrintFormat("%s: Ticks are not synchronized yet, %d ticks received for %d ms. Error=%d",
            _Symbol,received,GetTickCount()-start,_LastError);
        }
      //--- Counting attempts
      attempts++;
      //--- A one-second pause to wait for the end of synchronization of the tick database
      Sleep(1000);
     }
//--- Receiving the requested ticks from the beginning of the tick history failed in three attempts
   if(!success)
     {
      PrintFormat("Error! Failed to receive %d ticks of %s in three attempts",getticks,_Symbol);
      return;
     }
   int ticks=ArraySize(tick_array);
//--- Showing the time of the first tick in the array
   datetime firstticktime=tick_array[ticks-1].time;
   PrintFormat("Last tick time = %s.%03I64u",
               TimeToString(firstticktime,TIME_DATE|TIME_MINUTES|TIME_SECONDS),tick_array[ticks-1].time_msc%1000);
//--- Show the time of the last tick in the array
   datetime lastticktime=tick_array[0].time;
   PrintFormat("First tick time = %s.%03I64u",
               TimeToString(lastticktime,TIME_DATE|TIME_MINUTES|TIME_SECONDS),tick_array[0].time_msc%1000);
 
//---                                                           
   MqlDateTime today;
   datetime current_time=TimeCurrent();                         
   TimeToStruct(current_time,today);                            
   PrintFormat("current_time=%s",TimeToString(current_time));   
   today.hour=0;
   today.min=0;
   today.sec=0;
   datetime startday=StructToTime(today);
   datetime endday=startday+24*60*60;
   if((ticks=CopyTicksRange(_Symbol,tick_array,COPY_TICKS_ALL,startday*1000,endday*1000))==-1) 
     {
      PrintFormat("CopyTicksRange(%s,tick_array,COPY_TICKS_ALL,%s,%s) failed, error %d",       
                  _Symbol,TimeToString(startday),TimeToString(endday),GetLastError());          
      return;                                                                                  
     }
   ticks=MathMax(100,ticks);
//--- Showing the first 100 ticks of the last day
   int counter=0;
   for(int i=0;i<ticks;i++)
     {
      datetime time=tick_array[i].time;
      if((time>=startday) && (time<endday) && counter<100)
        {
         counter++;
         PrintFormat("%d. %s",counter,GetTickDescription(tick_array[i]));
        }
     }
//--- Showing the first 100 deals of the last day
   counter=0;
   for(int i=0;i<ticks;i++)
     {
      datetime time=tick_array[i].time;
      if((time>=startday) && (time<endday) && counter<100)
        {
         if(((tick_array[i].flags&TICK_FLAG_BUY)==TICK_FLAG_BUY) || ((tick_array[i].flags&TICK_FLAG_SELL)==TICK_FLAG_SELL))
           {
            counter++;
            PrintFormat("%d. %s",counter,GetTickDescription(tick_array[i]));
           }
        }
     }
  }
//+------------------------------------------------------------------+
//| Returns the string description of a tick                         |
//+------------------------------------------------------------------+
string GetTickDescription(MqlTick &tick)
  {
   string desc=StringFormat("%s.%03d ",
                            TimeToString(tick.time),tick.time_msc%1000);
//--- Checking flags
   bool buy_tick=((tick.flags&TICK_FLAG_BUY)==TICK_FLAG_BUY);
   bool sell_tick=((tick.flags&TICK_FLAG_SELL)==TICK_FLAG_SELL);
   bool ask_tick=((tick.flags&TICK_FLAG_ASK)==TICK_FLAG_ASK);
   bool bid_tick=((tick.flags&TICK_FLAG_BID)==TICK_FLAG_BID);
   bool last_tick=((tick.flags&TICK_FLAG_LAST)==TICK_FLAG_LAST);
   bool volume_tick=((tick.flags&TICK_FLAG_VOLUME)==TICK_FLAG_VOLUME);
//--- Checking trading flags in a tick first
   if(buy_tick || sell_tick)
     {
      //--- Forming an output for the trading tick
      desc=desc+(buy_tick?StringFormat("Buy Tick: Last=%G Volume=%d ",tick.last,tick.volume):"");
      desc=desc+(sell_tick?StringFormat("Sell Tick: Last=%G Volume=%d ",tick.last,tick.volume):"");
      desc=desc+(ask_tick?StringFormat("Ask=%G ",tick.ask):"");
      desc=desc+(bid_tick?StringFormat("Bid=%G ",tick.ask):"");
      desc=desc+"(Trade tick)";
     }
   else
     {
      //--- Form a different output for an info tick
      desc=desc+(ask_tick?StringFormat("Ask=%G ",tick.ask):"");
      desc=desc+(bid_tick?StringFormat("Bid=%G ",tick.ask):"");
      desc=desc+(last_tick?StringFormat("Last=%G ",tick.last):"");
      desc=desc+(volume_tick?StringFormat("Volume=%d ",tick.volume):"");
      desc=desc+"(Info tick)";
     }
//--- Returning tick description
   return desc;
  }
//+------------------------------------------------------------------+
/* Example of the output
Si-12.16: received 11048387 ticks in 4937 ms
Last tick time = 2016.09.26 18:32:59.775 
First tick time = 2015.06.18 09:45:01.000 
1.  2016.09.26 09:45.249 Ask=65370 Bid=65370 (Info tick)
2.  2016.09.26 09:47.420 Ask=65370 Bid=65370 (Info tick)
3.  2016.09.26 09:50.893 Ask=65370 Bid=65370 (Info tick)
4.  2016.09.26 09:51.827 Ask=65370 Bid=65370 (Info tick)
5.  2016.09.26 09:53.810 Ask=65370 Bid=65370 (Info tick)
6.  2016.09.26 09:54.491 Ask=65370 Bid=65370 (Info tick)
7.  2016.09.26 09:55.913 Ask=65370 Bid=65370 (Info tick)
8.  2016.09.26 09:59.350 Ask=65370 Bid=65370 (Info tick)
9.  2016.09.26 09:59.678 Bid=65370 (Info tick)
10. 2016.09.26 10:00.000 Sell Tick: Last=65367 Volume=3 (Trade tick)
11. 2016.09.26 10:00.000 Sell Tick: Last=65335 Volume=45 (Trade tick)
12. 2016.09.26 10:00.000 Sell Tick: Last=65334 Volume=95 (Trade tick)
13. 2016.09.26 10:00.191 Sell Tick: Last=65319 Volume=1 (Trade tick)
14. 2016.09.26 10:00.191 Sell Tick: Last=65317 Volume=1 (Trade tick)
15. 2016.09.26 10:00.191 Sell Tick: Last=65316 Volume=1 (Trade tick)
16. 2016.09.26 10:00.191 Sell Tick: Last=65316 Volume=10 (Trade tick)
17. 2016.09.26 10:00.191 Sell Tick: Last=65315 Volume=5 (Trade tick)
18. 2016.09.26 10:00.191 Sell Tick: Last=65313 Volume=3 (Trade tick)
19. 2016.09.26 10:00.191 Sell Tick: Last=65307 Volume=25 (Trade tick)
20. 2016.09.26 10:00.191 Sell Tick: Last=65304 Volume=1 (Trade tick)
21. 2016.09.26 10:00.191 Sell Tick: Last=65301 Volume=1 (Trade tick)
22. 2016.09.26 10:00.191 Sell Tick: Last=65301 Volume=10 (Trade tick)
23. 2016.09.26 10:00.191 Sell Tick: Last=65300 Volume=5 (Trade tick)
24. 2016.09.26 10:00.191 Sell Tick: Last=65300 Volume=1 (Trade tick)
25. 2016.09.26 10:00.191 Sell Tick: Last=65300 Volume=6 (Trade tick)
26. 2016.09.26 10:00.191 Sell Tick: Last=65299 Volume=1 (Trade tick)
27. 2016.09.26 10:00.191 Bid=65370 (Info tick)
28. 2016.09.26 10:00.232 Ask=65297 (Info tick)
29. 2016.09.26 10:00.276 Sell Tick: Last=65291 Volume=31 (Trade tick)
30. 2016.09.26 10:00.276 Sell Tick: Last=65290 Volume=1 (Trade tick)
*/

```

See also

[SymbolInfoTick](/en/docs/marketinformation/symbolinfotick), [Structure for Current Prices](/en/docs/constants/structures/mqltick), [OnTick()](/en/docs/event_handlers/ontick)
