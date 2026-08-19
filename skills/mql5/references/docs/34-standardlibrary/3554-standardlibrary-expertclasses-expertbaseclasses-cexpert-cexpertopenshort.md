# OpenShort

Opens a short position.

```
virtual bool  OpenShort(
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

It gets trading volume ([LotOpenShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertlotopenshort) method) and opens a short position (by calling Sell method of Trade object) if trading volume is not equal to 0.

Implementation

```
//+------------------------------------------------------------------+
//| Short position open or limit/stop order set                      |
//| INPUT:  price - price,                                           |
//|         sl    - stop loss,                                       |
//|         tp    - take profit.                                     |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::OpenShort(double price,double sl,double tp)
  {
   if(price==EMPTY_VALUE) return(false);
//--- get lot for open
   double lot=LotOpenShort(price,sl);
//--- check lot for open
   if(lot==0.0) return(false);
//---
   return(m_trade.Sell(lot,price,sl,tp));
  }

```
