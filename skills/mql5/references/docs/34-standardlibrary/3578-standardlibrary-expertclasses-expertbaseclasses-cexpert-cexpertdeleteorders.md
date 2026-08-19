# DeleteOrders

Deletes all orders.

```
virtual bool  DeleteOrders()

```

Return Value

true - trade operation has been executed, otherwise - false.

Note

It deletes all orders ([DeleteOrder()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertdeleteorder) for all orders).

Implementation

```
//+------------------------------------------------------------------+
//| Delete all limit/stop orders                                     |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::DeleteOrders()
  {
   bool result=false;
   int  total=OrdersTotal();
//---
   for(int i=total-1;i>=0;i--)
     {
      if(m_order.Select(OrderGetTicket(i)))
        {
         if(m_order.Symbol()!=m_symbol.Name()) continue;
         result|=DeleteOrder();
        }
     }
//---
   return(result);
  }

```
