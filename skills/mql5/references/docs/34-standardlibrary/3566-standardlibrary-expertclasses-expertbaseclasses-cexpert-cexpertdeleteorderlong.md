# DeleteOrderLong

Deletes the Buy Limit/Stop order.

```
virtual bool  DeleteOrderLong()

```

Return Value

true - trade operation has been executed, otherwise - false.

Note

It deletes Buy Limit/Stop order (OrderDelete(...) method of CTrade class object).

Implementation

```
//+------------------------------------------------------------------+
//| Delete long limit/stop order                                     |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::DeleteOrderLong()
  {
   return(m_trade.OrderDelete(m_order.Ticket()));
  }

```
