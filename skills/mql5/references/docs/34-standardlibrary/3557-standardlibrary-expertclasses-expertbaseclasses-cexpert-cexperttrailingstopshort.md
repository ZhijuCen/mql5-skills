# TrailingStopShort

It modifies parameters of the opened short position.

```
virtual bool  TrailingStopLong(
   double    sl,    // Stop Loss
   double    tp,    // Take Profit
   )

```

Parameters

sl

[in]  Stop Loss price.

tp

[in]  Take Profit price.

Return Value

true - trade operation has been executed, otherwise - false.

Note

The function modifies parameters of the opened short position (PositionModify(...) method of CTrade class object).

Implementation

```
//+------------------------------------------------------------------+
//| Trailing stop/profit short position                              |
//| INPUT:  sl - new stop loss,                                      |
//|         tp - new take profit.                                    |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::TrailingStopShort(double sl,double tp)
  {
   return(m_trade.PositionModify(m_symbol.Name(),sl,tp));
  }

```
