# TrailingOrderLong

It modifies parameters of Buy Limit/Stop trailing order.

```
virtual bool  TrailingOrderLong(
   double    delta    // delta
   )

```

Parameters

delta

[in]  Price delta.

Return Value

true - trade operation has been executed, otherwise - false.

Note

It modifies parameters of Buy Limit/Stop trailing order (OrderModify(...) method of CTrade class object).

Implementation

```
//+------------------------------------------------------------------+
//| Trailing long limit/stop order                                   |
//| INPUT:  delta - price change.                                    |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::TrailingOrderLong(double delta)
  {
   ulong  ticket=m_order.Ticket();
   double price =m_order.PriceOpen()-delta;
   double sl    =m_order.StopLoss()-delta;
   double tp    =m_order.TakeProfit()-delta;
//--- modifying the long order
   return(m_trade.OrderModify(ticket,price,sl,tp,m_order.TypeTime(),m_order.TimeExpiration()));
  }

```
