# CheckDeleteOrderLong

It checks conditions to delete Buy Limit/Stop order.

```
virtual bool  CheckDeleteOrderLong()

```

Return Value

true - trade operation has been executed, otherwise - false.

Note

It checks the order expiration time. It checks conditions to delete the Buy Limit/Stop order (CheckCloseLong(...) method of Signal class object) and deletes the order if condition is satisfied ([DeleteOrderLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertdeleteorderlong) method).

Implementation

```
//+------------------------------------------------------------------+
//| Check for delete long limit/stop order                           |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckDeleteOrderLong()
  {
   double price;
//--- check the possibility of deleting the long order
   if(m_expiration!=0 && TimeCurrent()>m_expiration)
     {
      m_expiration=0;
      return(DeleteOrderLong());
     }
   if(m_signal.CheckCloseLong(price))
      return(DeleteOrderLong());
//--- return without operations
   return(false);
  }

```
