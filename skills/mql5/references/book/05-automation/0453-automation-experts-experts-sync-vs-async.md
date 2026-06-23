# Synchronous and asynchronous requests

Before going into details, let's remind you that each MQL program is executed in its own thread, and therefore parallel asynchronous processing of transactions (and other events) is only possible due to the fact that another MQL program would be doing it. At the same time, it is necessary to ensure information exchange between programs. We already know a couple of ways to do this: [global variables](/en/book/common/globals) of the terminal and [files](/en/book/common/files). In Part 7 of the book, we will explore other features such as [graphical resources](/en/book/advanced/resources) and [databases](/en/book/advanced/sqlite).

Indeed, imagine that an Expert Advisor similar to TradeTransactions.mq5 runs in parallel with the trading Expert Advisor and saves the received transactions (not necessarily all fields, but only selective ones that affect decision-making) in global variables. Then the Expert Advisor could check the global variables immediately after sending the next request and read the results from them without leaving the current function. Moreover, it does not need its own OnTradeTransaction handler.

However, it is not easy to organize the running of a third-party Expert Advisor. From the technical point of view, this could be done by creating a [chart object](/en/book/applications/objects/objects_chart) and applying a [template](/en/book/applications/charts/charts_tpl) with a predefined transaction monitor Expert Advisor. But there is an easier way. The point is that events of OnTradeTransaction are translated not only into Expert Advisor but also into indicators. In turn, an indicator is the most easily launched type of MQL program: it is enough to call [iCustom](/en/book/applications/indicators_use/indicators_icustom).

In addition, the use of the indicator gives one more nice bonus: it can describe the indicator buffer available from external programs via CopyBuffer, and arrange a ring buffer in it for storing transactions coming from the terminal (request results). Thus, there is no need to mess with global variables.

Attention! The OnTradeTransaction event is not generated for indicators in the tester, so you can only check the operation of the Expert Advisor-indicator pair online.

Let's call this indicator TradeTransactionRelay.mq5 and describe one buffer in it. It could be made invisible because it will write data that cannot be rendered, but we left it visible to prove the concept.

```
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
   
double Buffer[];
   
void OnInit()
{
   SetIndexBuffer(0, Buffer, INDICATOR_DATA);
}

```

The OnCalculate handler is empty.

```
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const int begin,
                const double &price[])
{
   return rates_total;
}

```

In the code, we need a ready [converter](/en/book/common/maths/maths_nan) from double to ulong and vice versa, since buffer cells can corrupt large ulong values if they are written there using a simple typecast (see [Real numbers](/en/book/basis/builtin_types/float_numbers)).

```
#include <MQL5Book/ConverterT.mqh>
Converter<ulong,double> cnv;

```

Here is the OnTradeTransaction function.

```
#defineFIELD_NUM6// the most important fields in MqlTradeResult
   
void OnTradeTransaction(const MqlTradeTransaction &transaction,
   const MqlTradeRequest &request,
   const MqlTradeResult &result)
{
   if(transaction.type == TRADE_TRANSACTION_REQUEST)
   {
      ArraySetAsSeries(Buffer, true);
      
      // store FIELD_NUM result fields into consecutive buffer cells
      const int offset = (int)((result.request_id * FIELD_NUM)
         % (Bars(_Symbol, _Period) / FIELD_NUM * FIELD_NUM));
      Buffer[offset + 1] = result.retcode;
      Buffer[offset + 2] = cnv[result.deal];
      Buffer[offset + 3] = cnv[result.order];
      Buffer[offset + 4] = result.volume;
      Buffer[offset + 5] = result.price;
      // this assignment must come last,
      // because it is the result ready flag
      Buffer[offset + 0] = result.request_id;
   }
}

```

We decided to keep only the six most important fields of the MqlTradeResult structure. If desired, you can extend the mechanism to the entire structure, but to transfer the string field comment you will need an array of characters for which you will have to reserve quite a lot of elements.

Thus, each result now occupies six consecutive buffer cells. The index of the first cell of these six is determined based on the request ID: this number is simply multiplied by 6. Since there can be many requests, the entry works on the principle of a ring buffer, i.e., the resulting index is normalized by dividing with remainder ('%') by the size of the indicator buffer, which is the number of bars rounded up to 6. When the request numbers exceed the size, the record will go in a circle from the initial elements.

Since the numbering of bars is affected by the formation of new bars, it is recommended to put the indicator on large timeframes, such as D1. Then only at the beginning of the day is it likely (yet rather unlikely) the situation when the numbering of bars in the indicator will shift directly during the processing of the next transaction, and then the results recorded by the indicator will not be read by the Expert Advisor (one transaction may be missed).

The indicator is ready. Now let's start implementing a new modification of the test Expert Advisor OrderSendTransaction3.mq5 (hooray, this is its latest version). Let's describe the handle variable for the indicator handle and create the indicator in OnInit.

```
int handle = 0;
   
int OnInit()
{
   ...
   const static string indicator = "MQL5Book/p6/TradeTransactionRelay";
   handle = iCustom(_Symbol, PERIOD_D1, indicator);
   if(handle == INVALID_HANDLE)
   {
      Alert("Can't start indicator ", indicator);
      return INIT_FAILED;
   }
   return INIT_SUCCEEDED;
}

```

To read query results from the indicator buffer, let's prepare a helper function AwaitAsync. As its first parameter, it receives a reference to the MqlTradeRequestSync structure. If successful, the results obtained from the indicator buffer with handle will be written to this structure. The identifier of the request we are interested in should already be in the nested structure, in the result.request_id field. Of course, here we must read the data according to the same principle, that is, in six bars.

```
#define FIELD_NUM   6  // the most important fields in MqlTradeResult
#define TIMEOUT  1000  // 1 second
   
bool AwaitAsync(MqlTradeRequestSync &r, const int _handle)
{
   Converter<ulong,double> cnv;
   const int offset = (int)((r.result.request_id * FIELD_NUM)
      % (Bars(_Symbol, _Period) / FIELD_NUM * FIELD_NUM));
   const uint start = GetTickCount();
   // wait for results or timeout
   while(!IsStopped() && GetTickCount() - start < TIMEOUT)
   {
      double array[];
      if((CopyBuffer(_handle, 0, offset, FIELD_NUM, array)) == FIELD_NUM)
      {
         ArraySetAsSeries(array, true);
         // when request_id is found, fill other fields with results
         if((uint)MathRound(array[0]) == r.result.request_id)
         {
            r.result.retcode = (uint)MathRound(array[1]);
            r.result.deal = cnv[array[2]];
            r.result.order = cnv[array[3]];
            r.result.volume = array[4];
            r.result.price = array[5];
            PrintFormat("Got Req=%d at %d ms",
               r.result.request_id, GetTickCount() - start);
            Print(TU::StringOf(r.result));
            return true;
         }
      }
   }
   Print("Timeout for: ");
   Print(TU::StringOf(r));
   return false;
}

```

Now that we have this function, let's write a trading algorithm in an asynchronous-synchronous style: as a direct sequence of steps, each of which waits for the previous one to be ready due to notifications from the parallel indicator program while remaining inside one function.

```
void OnTimer()
{
   EventKillTimer();
   
   MqlTradeRequestSync::AsyncEnabled = true;
   
   MqlTradeRequestSync request;
   request.magic = Magic;
   request.deviation = Deviation;
   
   const double volume = Volume == 0 ?
      SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN) : Volume;
   ...

```

Step 1.

```
   Print("Start trade");
   ResetLastError();
   if((bool)(Type == MARKET_BUY ? request.buy(volume) : request.sell(volume)))
   {
      Print("OK Open?");
   }
   
   if(!(AwaitAsync(request, handle) && request.completed()))
   {
      Print("Failed Open");
      return;
   }
   ...

```

Step 2.

```
   Print("SL/TP modification");
   ...
   if(request.adjust(SL, TP))
   {
      Print("OK Adjust?");
   }
   
   if(!(AwaitAsync(request, handle) && request.completed()))
   {
      Print("Failed Adjust");
   }

```

Step 3.

```
   Print("Close down");
   if(request.close(request.result.position))
   {
      Print("OK Close?");
   }
   
   if(!(AwaitAsync(request, handle) && request.completed()))
   {
      Print("Failed Close");
   }
   
   Print("Finish");
}

```

Please note that the completed method calls are now done not after sending the request but after the result is received by the AwaitAsync function.

Otherwise, everything is very similar to the first version of this algorithm, but now it is built on asynchronous function calls and reacts to asynchronous events.

It probably doesn't seem significant in this particular example of a chain of manipulations on a single position. However, we can use the same technique to send and control a batch of orders. And then the benefits will become obvious. After a moment, we will demonstrate this with the help of a grid Expert Advisor and at the same time compare the performance of two functions: OrderSend and OrderSendAsync.

But right now, as we complete the series of OrderSendTransaction Expert Advisors, let's run the latest version and see in the log the regular, linear execution of all steps.

```
Start trade
OK Open?
Got Req=1 at 62 ms
DONE, D=1282677007, #=1300045365, V=0.01, @ 1.10564, Bid=1.10564, Ask=1.10564, Order placed, Req=1
Waiting for position for deal D=1282677007
SL/TP modification
OK Adjust?
Got Req=2 at 63 ms
DONE, Order placed, Req=2
Close down
OK Close?
Got Req=3 at 78 ms
DONE, D=1282677008, #=1300045366, V=0.01, @ 1.10564, Bid=1.10564, Ask=1.10564, Order placed, Req=3
Finish

```

Timing with response delays can significantly depend on the server, time of day, and symbol. Of course, part of the time here is spent not on a trade request with confirmation but on the execution of the CopyBuffer function. According to our observations, it takes no more than 16 ms (within one cycle of a standard system timer, those who wish can profile programs using high-precision timers GetMicrosecondCount).

Ignore the difference between the status (DONE) and the string description ("Order placed"). The fact is that the comment (as well as the ask/bid fields) remains in the structure from the moment it is sent by the OrderSendAsync function, and the final status in the retcode field is written by our AwaitAsync function. It is important for us that in the structure with the results, the ticket numbers (deal and order), exercise price (price) and volume (volume) are up-to-date.

Based on the earlier considered example of OrderSendTransaction3.mq5, let's create a new version of the grid Expert Advisor PendingOrderGrid3.mq5 (the previous version is provided in the section [Functions for reading position properties](/en/book/automation/experts/experts_positionget_funcs)). It will be able to set a complete grid of orders in synchronous or asynchronous mode, at the user's choice. We will also detect the times of setting the full grid for comparison.

The mode is controlled by the input variable EnableAsyncSetup. The handle variable is allocated for the indicator handle.

```
input bool EnableAsyncSetup = false;
   
int handle;

```

During initialization, in the case of asynchronous mode, we create an instance of the TradeTransactionRelay indicator.

```
int OnInit()
{
   ...
   if(EnableAsyncSetup)
   {
      const uint start = GetTickCount();
      const static string indicator = "MQL5Book/p6/TradeTransactionRelay";
      handle = iCustom(_Symbol, PERIOD_D1, indicator);
      if(handle == INVALID_HANDLE)
      {
         Alert("Can't start indicator ", indicator);
         return INIT_FAILED;
      }
      PrintFormat("Started in %d ms", GetTickCount() - start);
   }
   ...
}

```

In order to simplify coding, we have replaced the two-dimensional request array with a one-dimensional one in the SetupGrid function.

```
uint SetupGrid()
{
   ...                                  // prev:
   MqlTradeRequestSyncLog request[];    // MqlTradeRequestSyncLog request[][2];
   ArrayResize(request, GridSize * 2);  // ArrayResize(request, GridSize);
   ...
}

```

Further in the loop through the array, instead request[i][1] type calls we use the addressing request[i * 2 + 1].

This small transformation was required for the following reasons. Since we use this array of structures for queries when creating the grid, and we need to wait for all the results, the AwaitAsync function should now take as its first parameter a reference to an array. A one-dimensional array is easier to handle.

For each request, its offset in the indicator buffer is calculated in accordance with its request_id: all offsets are placed into the offset array. As request confirmations are received, the corresponding elements of the array are marked as processed by writing the value of -1 there. The number of executed requests is counted in the done variable. When it equals the size of the array, the entire grid is ready.

```
bool AwaitAsync(MqlTradeRequestSyncLog &r[], const int _handle)
{
   Converter<ulong,double> cnv;
   int offset[];
   const int n = ArraySize(r);
   int done = 0;
   ArrayResize(offset, n);
   
   for(int i = 0; i < n; ++i)
   {
      offset[i] = (int)((r[i].result.request_id * FIELD_NUM)
         % (Bars(_Symbol, _Period) / FIELD_NUM * FIELD_NUM));
   }
   
   const uint start = GetTickCount();
   while(!IsStopped() && done < n && GetTickCount() - start < TIMEOUT)
   for(int i = 0; i < n; ++i)
   {
      if(offset[i] == -1) continue; // skip empty elements
      double array[];
      if((CopyBuffer(_handle, 0, offset[i], FIELD_NUM, array)) == FIELD_NUM)
      {
         ArraySetAsSeries(array, true);
         if((uint)MathRound(array[0]) == r[i].result.request_id)
         {
            r[i].result.retcode = (uint)MathRound(array[1]);
            r[i].result.deal = cnv[array[2]];
            r[i].result.order = cnv[array[3]];
            r[i].result.volume = array[4];
            r[i].result.price = array[5];
            PrintFormat("Got Req=%d at %d ms", r[i].result.request_id,
               GetTickCount() - start);
            Print(TU::StringOf(r[i].result));
            offset[i] = -1; // mark processed
            done++;
         }
      }
   }
   return done == n;
}

```

Returning to the SetupGrid function, let's show how AwaitAsync is called after the request sending loop.

```
uint SetupGrid()
{
   ...
   const uint start = GetTickCount();
   for(int i = 0; i < (int)GridSize / 2; ++i)
   {
      // calls of buyLimit/sellStopLimit/sellLimit/buyStopLimit
   }
   
   if(EnableAsyncSetup)
   {
      if(!AwaitAsync(request, handle))
      {
         Print("Timeout");
         return TRADE_RETCODE_ERROR;
      }
   }
   
   PrintFormat("Done %d requests in %d ms (%d ms/request)",
      GridSize * 2, GetTickCount() - start,
      (GetTickCount() - start) / (GridSize * 2));
   ...
}

```

If a timeout occurs when setting the grid (not all requests will receive confirmation within the allotted time), we will return the TRADE_RETCODE_ERROR code, and the Expert Advisor will try to "roll back" what it managed to create.

It's important to note that asynchronous mode is only intended to set up a full grid when we need to send a batch of requests. Otherwise, the synchronous mode will still be used. Therefore, we must set the MqlTradeRequestSync::AsyncEnabled flag to true before the send loop and set it back to false after that. However, please pay attention to the following. Errors can occur inside the loop, due to which it is terminated prematurely, returning the last code from the server. Thus, if we place an asynchronous reset after the loop, there is no guarantee that it will be reset.

To solve this problem, a small AsyncSwitcher class is added to the MqlTradeSync.mqh file. The class controls the enabling and disabling of asynchronous mode from its constructor and destructor. This aligns with the RAII resource management concept discussed in section [File descriptor management](/en/book/common/files/files_handles).

```
class AsyncSwitcher
{
public:
   AsyncSwitcher(const bool enabled = true)
   {
      MqlTradeRequestSync::AsyncEnabled = enabled;
   }
   ~AsyncSwitcher()
   {
      MqlTradeRequestSync::AsyncEnabled = false;
   }
};

```

Now, for the safe temporary activation of the asynchronous mode, we can simply describe the local AsyncSwitcher object in the SetupGrid function. The code will automatically return to the synchronous mode on any exit from the function.

```
uint SetupGrid()
{
   ...
   AsyncSwitcher sync(EnableAsyncSetup);
   ...
   for(int i = 0; i < (int)GridSize / 2; ++i)
   {
      ...
   }
   ...
}

```

The Expert Advisor is ready. Let's try to run it twice: in synchronous and asynchronous modes for a large enough grid (10 levels, grid step 200).

For a grid of 10 levels, we will get 20 queries, so below are some of the logs. First, a synchronous mode was used. Let's clarify that the inscription about the readiness of requests is displayed before messages about the requests because the latter are generated by the structure destructors when the function exits. The processing speed is 51ms per request.

```
Start setup at 1.10379
Done 20 requests in 1030 ms (51 ms/request)
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10200, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978336, V=0.01, Request executed, Req=1
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10200, »
   » X=1.10400, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978337, V=0.01, Request executed, Req=2
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10000, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978343, V=0.01, Request executed, Req=5
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10000, » 
   » X=1.10200, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978344, V=0.01, Request executed, Req=6
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.09800, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978348, V=0.01, Request executed, Req=9
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.09800, »
   » X=1.10000, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978350, V=0.01, Request executed, Req=10
...
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10600, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978339, V=0.01, Request executed, Req=3
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10600, »
   » X=1.10400, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978340, V=0.01, Request executed, Req=4
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10800, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978345, V=0.01, Request executed, Req=7
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10800, »
   » X=1.10600, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978347, V=0.01, Request executed, Req=8
...
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.11400, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978365, V=0.01, Request executed, Req=19
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.11400, »
   » X=1.11200, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300978366, V=0.01, Request executed, Req=20

```

The middle of the grid matched the price of 1.10400. The system assigns numbers to requests in the order in which they are received, and their numbering in the array corresponds to the order in which we place orders: from the central base level, we gradually diverge to the sides. Therefore, do not be surprised that after a pair of 1 and 2 (for the level 1.10200) comes 5 and 6 (1.10000), since 3 and 4 (1.10600) were sent earlier.

In asynchronous mode, destructors are preceded by messages about the readiness of specific requests received in AwaitAsync in real time, and not necessarily in the order in which the requests were sent (for example, the 49th and 50th requests "overtook" the 47th and 48th).

```
Started in 16 ms
Start setup at 1.10356
Got Req=41 at 109 ms
DONE, #=1300979180, V=0.01, Order placed, Req=41
Got Req=42 at 109 ms
DONE, #=1300979181, V=0.01, Order placed, Req=42
Got Req=43 at 125 ms
DONE, #=1300979182, V=0.01, Order placed, Req=43
Got Req=44 at 140 ms
DONE, #=1300979183, V=0.01, Order placed, Req=44
Got Req=45 at 156 ms
DONE, #=1300979184, V=0.01, Order placed, Req=45
Got Req=46 at 172 ms
DONE, #=1300979185, V=0.01, Order placed, Req=46
Got Req=49 at 172 ms
DONE, #=1300979188, V=0.01, Order placed, Req=49
Got Req=50 at 172 ms
DONE, #=1300979189, V=0.01, Order placed, Req=50
Got Req=47 at 172 ms
DONE, #=1300979186, V=0.01, Order placed, Req=47
Got Req=48 at 172 ms
DONE, #=1300979187, V=0.01, Order placed, Req=48
Got Req=51 at 172 ms
DONE, #=1300979190, V=0.01, Order placed, Req=51
Got Req=52 at 203 ms
DONE, #=1300979191, V=0.01, Order placed, Req=52
Got Req=55 at 203 ms
DONE, #=1300979194, V=0.01, Order placed, Req=55
Got Req=56 at 203 ms
DONE, #=1300979195, V=0.01, Order placed, Req=56
Got Req=53 at 203 ms
DONE, #=1300979192, V=0.01, Order placed, Req=53
Got Req=54 at 203 ms
DONE, #=1300979193, V=0.01, Order placed, Req=54
Got Req=57 at 218 ms
DONE, #=1300979196, V=0.01, Order placed, Req=57
Got Req=58 at 218 ms
DONE, #=1300979198, V=0.01, Order placed, Req=58
Got Req=59 at 218 ms
DONE, #=1300979199, V=0.01, Order placed, Req=59
Got Req=60 at 218 ms
DONE, #=1300979200, V=0.01, Order placed, Req=60
Done 20 requests in 234 ms (11 ms/request)
...

```

Due to the fact that all requests were executed in parallel, the total send time (234ms) is only slightly more than the time of a single request (here around 100ms, but you will have your own timing). As a result, we got a speed of 11ms per request, which is 5 times faster than with the synchronous method. Since the requests were sent almost simultaneously, we cannot know the execution time of each, and milliseconds indicate the arrival of the result of a particular request from the moment the general start of the group sending.

Further logs, as in the previous case, contain all query and result fields which are printed from structure destructors. The "Order placed" line remained unchanged after OrderSendAsync, since our auxiliary indicator TradeTransactionRelay.mq5 does not publish the MqlTradeResult structure from the TRADE_TRANSACTION_REQUEST message in full.

```
...
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10200, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979180, V=0.01, Order placed, Req=41
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10200, »
   » X=1.10400, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979181, V=0.01, Order placed, Req=42
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10000, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979184, V=0.01, Order placed, Req=45
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10000, »
   » X=1.10200, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979185, V=0.01, Order placed, Req=46
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.09800, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979188, V=0.01, Order placed, Req=49
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.09800, »
   » X=1.10000, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979189, V=0.01, Order placed, Req=50
...
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10600, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979182, V=0.01, Order placed, Req=43
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10600, »
   » X=1.10400, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979183, V=0.01, Order placed, Req=44
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10800, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979186, V=0.01, Order placed, Req=47
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.10800, »
   » X=1.10600, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979187, V=0.01, Order placed, Req=48
...
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_SELL_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.11400, »
   » ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979199, V=0.01, Order placed, Req=59
TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP_LIMIT, V=0.01, ORDER_FILLING_FOK, @ 1.11400, »
   » X=1.11200, ORDER_TIME_GTC, M=1234567890, G[1.10400]
DONE, #=1300979200, V=0.01, Order placed, Req=60

```

Until now, our grid Expert Advisor had a pair of pending orders at each level: limit and stop-limit. To avoid such duplication, we leave only limit orders. This will be the final version of PendingOrderGrid4.mq5, which can also be run in synchronous and asynchronous mode. We will not go into the source code in detail but will only note the main differences from the previous version.

In the SetupGrid function, we need an array of structures of size equal to GridSize and not doubled. The number of requests will also decrease by 2 times: the only methods used for them are buyLimit and sellLimit.

The CheckGrid function checks the integrity of the grid in a different way. Previously, the absence of a paired stop-limit order at the level where there is a limit was considered a mistake. This could happen when a stop-limit order was triggered on the server from a neighboring level. However, this scheme is not capable of restoring the grid if a strong two-way price movement (spike) occurs on one bar: it will knock out not only the original limit orders but also new ones generated from stop-limit ones. Now the algorithm honestly checks the vacant levels on both sides of the current price and creates limit orders there using RepairGridLevel. This helper function previously placed stop-limit orders.

Finally, the OnTradeTransaction handler appeared in PendingOrderGrid4.mq5. The triggering of a pending order will lead to the execution of a deal (and a change in the grid configuration that needs to be corrected), so we control deals by a given symbol and magic. When a transaction is detected, the function CheckGrid is called instantly, in addition to the fact that it is still executed at the beginning of each bar.

```
void OnTradeTransaction(const MqlTradeTransaction &transaction,
   const MqlTradeRequest &,
   const MqlTradeResult &)
{
   if(transaction.type == TRADE_TRANSACTION_DEAL_ADD)
   {
      if(transaction.symbol == _Symbol)
      {
         DealMonitor dm(transaction.deal); // select the deal
         if(dm.get(DEAL_MAGIC) == Magic)
         {
            CheckGrid();
         }
      }
   }
}

```

It should be noted that the presence of OnTradeTransaction is not enough to write Expert Advisors that are resistant to unforeseen external influences. Of course, events allow you to quickly respond to the situation, but we have no guarantee that the Expert Advisor will not be turned off (or go offline) for one reason or another for some time and skip this or that transaction. Therefore the OnTradeTransaction handler should only help speed up the processes that the program can perform without it. In particular, to restore its state correctly after the start.

However, in addition to the OnTradeTransaction event, MQL5 provides another, simpler event: OnTrade.
