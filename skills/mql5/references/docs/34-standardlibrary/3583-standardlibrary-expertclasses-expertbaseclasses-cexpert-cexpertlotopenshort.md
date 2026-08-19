# LotOpenShort

Gets trade volume for sell operation.

```
double  LotOpenShort(
   double    price,   // price
   double    sl       // Stop Loss
   )

```

Parameters

price

[in]  Market entry price.

sl

[in]  Stop Loss price.

Return Value

Trade volume (in lots) for sell operation.

Note

It gets trade volume for sell operation (CheckOpenShort(...) method of money management object).

Implementation

```
//+------------------------------------------------------------------+
//| Method of getting the lot for open short position.               |
//| INPUT:  price - price,                                           |
//|         sl    - stop loss.                                       |
//| OUTPUT: lot for open.                                            |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
double CExpert::LotOpenShort(double price,double sl)
  {
   return(m_money.CheckOpenShort(price,sl));
  }

```
