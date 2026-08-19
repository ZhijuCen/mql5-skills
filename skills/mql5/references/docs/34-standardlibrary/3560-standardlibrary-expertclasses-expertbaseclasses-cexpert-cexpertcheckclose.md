# CheckClose

Checks conditions to close position.

```
virtual bool  CheckClose()

```

Return Value

true - trade operation has been executed, otherwise - false.

Note

1. It checks Expert Advisor Stop Out conditions (CheckClose() method of money management object). If condition is satisfied, it closes the position, deletes all orders ([CloseAll()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcloseall)), and exits.
2. It checks conditions to close long or short position ([CheckCloseLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckcloselong) or  [CheckCloseShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckcloseshort) methods) and if position is closed, it deletes all orders ([DeleteOrders()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertdeleteorders) method).

Implementation

```
//+------------------------------------------------------------------+
//| Check for position close or limit/stop order delete              |
//| INPUT:  no.                                                      |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::CheckClose()
  {
   double lot;
//--- position must be selected before call
   if((lot=m_money.CheckClose(GetPointer(m_position)))!=0.0)
      return(CloseAll(lot));
//--- check for position type
   if(m_position.PositionType()==POSITION_TYPE_BUY)
     {
      //--- check the possibility of closing the long position / delete pending orders to buy
      if(CheckCloseLong())
        {
         DeleteOrders();
         return(true);
        }
     }
   else
     {
      //--- check the possibility of closing the short position / delete pending orders to sell
      if(CheckCloseShort())
        {
         DeleteOrders();
         return(true);
        }
     }
//--- return without operations
   return(false);
  }

```
