# OpenLong

Opens a long position.

```
virtual bool  OpenLong(
   double    price,    // price
   double    sl,       // Stop Loss
   double    tp        // Take Profit
   )

```

Parameters

price

[in]  Market entry price.

sl

[in]  Stop Loss price.

tp

[in]  Take Profit price.

Return Value

true - trade operation has been executed, otherwise - false.

Note

It gets trading volume ([LotOpenLong(...)](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertlotopenlong) method) and opens a long position (Buy() method of Trade object) if trading volume is not equal to 0.

Implementation

```
//+------------------------------------------------------------------+
//| Long position open or limit/stop order set                       |
//| INPUT:  price - price,                                           |
//|         sl    - stop loss,                                       |
//|         tp    - take profit.                                     |
//| OUTPUT: true-if trade operation processed, false otherwise.      |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::OpenLong(double price,double sl,double tp)
  {
   if(price==EMPTY_VALUE) return(false);
//--- get lot for open
   double lot=LotOpenLong(price,sl);
//--- check lot for open
   if(lot==0.0) return(false);
//---
   return(m_trade.Buy(lot,price,sl,tp));
  }

```
