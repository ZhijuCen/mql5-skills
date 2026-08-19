# TrailingStopLong

It modifies parameters of the opened long position.

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

[in]  Take Profit price.

Return Value

true - trade operation has been executed, otherwise - false.

Note

The function modifies parameters of the opened long position (PositionModify(...) method of CTrade class object).

Implementation

```
//+------------------------------------------------------------------+
//| Trailing stop/profit long position                               |
//| INPUT:  sl - new stop loss,                                      |
//|         tp - new take profit.                                    |
//| OUTPUT: true-if trade operation successful, false otherwise.     |
//| REMARK: no.                                                      |
//+------------------------------------------------------------------+
bool CExpert::TrailingStopLong(double sl,double tp)
  {
   return(m_trade.PositionModify(m_symbol.Name(),sl,tp));
  }

```
