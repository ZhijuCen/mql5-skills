# Deleting a pending order

Deletion of a pending order is performed at the program level using the TRADE_ACTION_REMOVE operation: this constant should be assigned to the action field of the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure before calling one of the versions of the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function. The only required field in addition to action is order to specify the ticket of the order to be deleted.

The remove method in MqlTradeRequestSync application structure from the MqlTradeSync.mqh file is pretty basic.

```
struct MqlTradeRequestSync: public MqlTradeRequest
{
   ...
   bool remove(const ulong ticket)
   {
      if(!OrderSelect(ticket)) return false;
      action = TRADE_ACTION_REMOVE;
      order = ticket;
      ZeroMemory(result);
      return OrderSend(this, result);
   }

```

Checking the fact of deleting an order is traditionally done in the completed method.

```
   bool completed()
   {
      ...
      else if(action == TRADE_ACTION_REMOVE)
      {
         result.order = order;
         return result.removed(timeout);
      }
      ...
   }

```

Waiting for the actual removal of the order is performed in the removed method of the MqlTradeResultSync structure.

```
struct MqlTradeResultSync: public MqlTradeResult
{
   ...
   bool removed(const ulong msc = 1000)
   {
      if(retcode != TRADE_RETCODE_DONE)
      {
         return false;
      }
   
      if(!wait(orderRemoved, msc))
      {
         Print("Order removal timeout: #=" + (string)order);
         return false;
      }
      
      return true;
   }
   
   static bool orderRemoved(MqlTradeResultSync &ref)
   {
      return !OrderSelect(ref.order) && HistoryOrderSelect(ref.order);
   }

```

An example of the Expert Advisor (PendingOrderDelete.mq5) demonstrating the removal of an order we will build almost entirely based on PendingOrderSend.mq5. This is due to the fact that it is easier to guarantee the existence of an order before deletion. Thus, immediately after the launch, the Expert Advisor will create a new order with the specified parameters. The order will then be deleted in the OnDeinit handler. If you change the Expert Advisor input parameters, the symbol, or the chart timeframe, the old order will also be deleted, and a new one will be created.

The OwnOrder global variable has been added to store the order ticket. It is filled as a result of the PlaceOrder call (the function itself is unchanged).

```
ulong OwnOrder = 0;
   
void OnTimer()
{
   // execute the code once for the current parameters
   EventKillTimer();
   
   const string symbol = StringLen(Symbol) == 0 ? _Symbol : Symbol;
   OwnOrder = PlaceOrder((ENUM_ORDER_TYPE)Type, symbol, Volume,
      Distance2SLTP, Expiration, Until, Magic, Comment);
}

```

Here is a simple deletion function RemoveOrder, which creates the request object and sequentially calls the remove and completed methods for it.

```
void OnDeinit(const int)
{
   if(OwnOrder != 0)
   {
      RemoveOrder(OwnOrder);
   }
}
   
void RemoveOrder(const ulong ticket)
{
   MqlTradeRequestSync request;
   if(request.remove(ticket) && request.completed())
   {
      Print("OK order removed");
   }
   Print(TU::StringOf(request));
   Print(TU::StringOf(request.result));
}

```

The following log shows the entries that appeared as a result of placing the Expert Advisor on the EURUSD chart, after which the symbol was switched to XAUUSD, and then the Expert Advisor was deleted.

```
(EURUSD,H1)        Autodetected daily range: 0.0094
(EURUSD,H1)        OK order placed: #=1284920879
(EURUSD,H1)        TRADE_ACTION_PENDING, EURUSD, ORDER_TYPE_BUY_STOP, V=0.01, ORDER_FILLING_FOK, »
                » @ 1.11011, ORDER_TIME_GTC, M=1234567890
(EURUSD,H1)        DONE, #=1284920879, V=0.01, Request executed, Req=1
(EURUSD,H1)        OK order removed
(EURUSD,H1)        TRADE_ACTION_REMOVE, EURUSD, ORDER_TYPE_BUY, ORDER_FILLING_FOK, #=1284920879
(EURUSD,H1)        DONE, #=1284920879, Request executed, Req=2
(XAUUSD,H1)        Autodetected daily range: 47.45
(XAUUSD,H1)        OK order placed: #=1284921672
(XAUUSD,H1)        TRADE_ACTION_PENDING, XAUUSD, ORDER_TYPE_BUY_STOP, V=0.01, ORDER_FILLING_FOK, »
                » @ 1956.68, ORDER_TIME_GTC, M=1234567890
(XAUUSD,H1)        DONE, #=1284921672, V=0.01, Request executed, Req=3
(XAUUSD,H1)        OK order removed
(XAUUSD,H1)        TRADE_ACTION_REMOVE, XAUUSD, ORDER_TYPE_BUY, ORDER_FILLING_FOK, #=1284921672
(XAUUSD,H1)        DONE, #=1284921672, Request executed, Req=4

```

We will look at another example of deleting orders to implement the "One Cancel Other" (OCO) strategy in the [OnTrade](/en/book/automation/experts/experts_ontrade) events section.
