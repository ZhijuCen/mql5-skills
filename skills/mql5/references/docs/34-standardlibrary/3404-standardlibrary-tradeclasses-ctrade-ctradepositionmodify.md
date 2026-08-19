# PositionModify

Modifies the position parameters by specified symbol.

```
bool  PositionModify(
   const string  symbol,     // symbol
   double        sl,         // Stop Loss price
   double        tp          // Take Profit price
   )

```

Modifies position parameters by the specified ticket.

```
bool  PositionModify(
   const ulong   ticket,     // position ticket
   double        sl,         // Stop Loss price 
   double        tp          // Take Profit price
   )

```

Parameters

symbol

[in]  Name of trade instrument, by which it is intended to modify position.

ticket

[in]  Ticket of the position to be modified.

sl

[in] The new price by which the Stop Loss will trigger (or the previous value, if the change is not necessary).

tp

[in] The new price by which the Take Profit will trigger (or the previous value, if the change is not necessary).

Return Value

true - successful check of the basic structures, otherwise - false.

Note

Successful completion of the PositionModify(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of trade request (trade server return code) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode).

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol. In this case, PositionModify will modify the position with the lowest ticket.
