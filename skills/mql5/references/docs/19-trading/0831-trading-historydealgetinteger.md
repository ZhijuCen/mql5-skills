# HistoryDealGetInteger

Returns the requested property of a deal. The deal property must be of the datetime, int type. There are 2 variants of the function.

1. Immediately returns the property value.

```
long  HistoryDealGetInteger(
   ulong                       ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_INTEGER  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  HistoryDealGetInteger(
   ulong                       ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_INTEGER  property_id,       // Property identifier
   long&                       long_var           // Here we accept the property value
   );

```

Parameters

ticket_number

[in]  Trade ticket.

property_id

[in]  Identifier of the deal property. The value can be one of the values of the [ENUM_DEAL_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/dealproperties#enum_deal_property_integer) enumeration.

long_var

[out]  Variable of the long type that accepts the value of the requested property.

Return Value

Value of the [long](/en/docs/basis/types/integer/integertypes#long) type.

Note

Do not confuse [orders](/en/docs/constants/tradingconstants/orderproperties), [deals](/en/docs/constants/tradingconstants/dealproperties) and [positions](/en/docs/constants/tradingconstants/positionproperties). Each deal is the result of the execution of an order, each position is the summary result of one or more deals.

Example:

```
//+------------------------------------------------------------------+
//| Trade function                                                   |
//+------------------------------------------------------------------+
void OnTrade()
  {
//--- receive the last deal's ticket from week's trading history
   ulong last_deal=GetLastDealTicket();
   if(HistoryDealSelect(last_deal))
     {
      //--- time of deal execution in milliseconds since 01.01.1970
      long deal_time_msc=HistoryDealGetInteger(last_deal,DEAL_TIME_MSC);
      PrintFormat("Deal #%d DEAL_TIME_MSC=%i64 => %s",
                  last_deal,deal_time_msc,TimeToString(deal_time_msc/1000));
     }
   else
      PrintFormat("HistoryDealSelect() failed for #%d. Eror code=%d",
                  last_deal,GetLastError());
//---
  }
//+------------------------------------------------------------------+
//| Returns the last deal ticket in history or -1                    |
//+------------------------------------------------------------------+
ulong GetLastDealTicket()
  {
//--- request history for the last 7 days
   if(!GetTradeHistory(7))
     {
      //--- notify on unsuccessful call and return -1
      Print(__FUNCTION__," HistorySelect() returned false");
      return -1;
     }
//--- 
   ulong first_deal,last_deal,deals=HistoryDealsTotal();
//--- work with orders if there are any
   if(deals>0)
     {
      Print("Deals = ",deals);
      first_deal=HistoryDealGetTicket(0);
      PrintFormat("first_deal = %d",first_deal);
      if(deals>1)
        {
         last_deal=HistoryDealGetTicket((int)deals-1);
         PrintFormat("last_deal = %d",last_deal);
         return last_deal;
        }
      return first_deal;
     }
//--- no deal found, return -1
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

[HistoryDealsTotal()](/en/docs/trading/historydealstotal), [HistorySelect()](/en/docs/trading/historyselect), [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket),  [Deal Properties](/en/docs/constants/tradingconstants/dealproperties)
