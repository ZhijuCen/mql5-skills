# LotOpenLong

Gets trade volume for buy operation.

```
double  LotOpenLong(
   double    price,   // price
   double    sl       // Stop Loss
   )

```

Parameters

price

[in]  Market entry price.

sl

[in]  Stop Loss price.

Return Value

Trade volume (in lots) for buy operation.

Note

It gets trade volume for buy operation (CheckOpenLong(...) method of money management object).

Implementation

```
//+------------------------------------------------------------------+
//| Method of getting the lot for open long position.                |
//| INPUT:  price - price,                                           |
//|         sl    - stop loss.                                       |
//| OUTPUT: lot for open.                                            |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
double CExpert::LotOpenLong(double price,double sl)
  {
   return(m_money.CheckOpenLong(price,sl));
  }

```
