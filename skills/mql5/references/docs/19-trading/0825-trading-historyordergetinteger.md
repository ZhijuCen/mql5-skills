# HistoryOrderGetInteger

Returns the requested property of an order. The order property must be of datetime, int type. There are 2 variants of the function.

1. Immediately returns the property value.

```
long  HistoryOrderGetInteger(
   ulong                        ticket_number,     // Ticket
   ENUM_ORDER_PROPERTY_INTEGER  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  HistoryOrderGetInteger(
   ulong                        ticket_number,     // Ticket
   ENUM_ORDER_PROPERTY_INTEGER  property_id,       // Property identifier
   long&                        long_var           // Here we accept the property value
   );

```

Parameters

ticket_number

[in]  Order ticket.

property_id

[in]  Identifier of the order property. The value can be one of the values of the [ENUM_ORDER_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer) enumeration.

long_var

[out]  Variable of the long type that accepts the value of the requested property.

Return Value

Value of the [long](/en/docs/basis/types/integer/integertypes#long) type.

Note

Do not confuse orders of a trading history with current [pending orders](/en/docs/trading/orderstotal) that appear on the "Trade" tab of the "Toolbox" bar. The list of [orders](/en/docs/constants/tradingconstants/orderproperties) that were canceled or have led to a transaction, can be viewed in the "History" tab of "Toolbox" of the client terminal.

Example:

```
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//--- receive the last order's ticket from week's trading history
   ulong last_order=GetLastOrderTicket();
   if(HistoryOrderSelect(last_order))
     {
      //--- time of placing an order in milliseconds since 01.01.1970
      long time_setup_msc=HistoryOrderGetInteger(last_order,ORDER_TIME_SETUP_MSC);
      PrintFormat("Order #%d ORDER_TIME_SETUP_MSC=%i64 => %s",
                  last_order,time_setup_msc,TimeToString(time_setup_msc/1000));
      //--- order execution/cancellation time in milliseconds since 01.01.1970
      long  time_done_msc=HistoryOrderGetInteger(last_order,ORDER_TIME_DONE_MSC);
      PrintFormat("Order #%d ORDER_TIME_DONE_MSC=%i64 => %s",
                  last_order,time_done_msc,TimeToString(time_done_msc/1000));
     }
   else // notify on failure
      PrintFormat("HistoryOrderSelect() failed for #%d. Eror code=%d",
                  last_order,GetLastError());
 
//---
  }
//+------------------------------------------------------------------+
//| Returns the last order ticket in history or -1                   |
//+------------------------------------------------------------------+
ulong GetLastOrderTicket()
  {
//--- request history for the last 7 days
   if(!GetTradeHistory(7))
     {
      //--- notify on unsuccessful call and return -1
      Print(__FUNCTION__," HistorySelect() returned false");
      return -1;
     }
//--- 
   ulong first_order,last_order,orders=HistoryOrdersTotal();
//--- work with orders if there are any
   if(orders>0)
     {
      Print("Orders = ",orders);
      first_order=HistoryOrderGetTicket(0);
      PrintFormat("first_order = %d",first_order);
      if(orders>1)
        {
         last_order=HistoryOrderGetTicket((int)orders-1);
         PrintFormat("last_order = %d",last_order);
         return last_order;
        }
      return first_order;
     }
//--- no order found, return -1
   return -1;
  }
//+--------------------------------------------------------------------------+
//| Requests history for the last days and returns false in case of failure  |
//+--------------------------------------------------------------------------+
bool GetTradeHistory(int days)
  {
//--- set a week period to request trade history
   datetime to=TimeCurrent();
   datetime from=to-days*PeriodSeconds(PERIOD_D1);
   ResetLastError();
//--- make a request and check the result
   if(!HistorySelect(from,to))
     {
      Print(__FUNCTION__," HistorySelect=false. Error code=",GetLastError());
      return false;
     }
//--- history received successfully
   return true;
  }

```

See also

[HistorySelect()](/en/docs/trading/historyselect), [HistoryOrdersTotal()](/en/docs/trading/historyorderstotal), [HistoryOrderSelect()](/en/docs/trading/historyorderselect), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
