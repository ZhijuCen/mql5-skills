# CheckTrailingStopLong

Checks Trailing Stop conditions of a long position.

```
virtual bool  CheckTrailingStopLong(
   CPositionInfo*  position,     // pointer
   double&         sl,           // reference to Stop Loss
   double&         tp            // reference to Take Profit
   )

```

Parameters

position

[in]  Pointer to [CPositionInfo](/en/docs/standardlibrary/tradeclasses/cpositioninfo) object.

sl

[in][out]  Reference to variable for Stop Loss price.

tp

[in][out]  Reference to variable for Take Profit price.

Return Value

true - conditions are satisfied, otherwise - false.

Note

If Stop Loss level is equal to 0, the condition is not fulfilled (exit). If position already has Stop Loss price, its value is assumed as a base price, otherwise the position open price is assumed as a base price. If the current Bid price is higher than base price+stop loss level, it suggests to set new Stop Loss price. In this case, If position already has Take Profit price, it suggests to set new Take Profit price equal to Bid price+take profit level.
