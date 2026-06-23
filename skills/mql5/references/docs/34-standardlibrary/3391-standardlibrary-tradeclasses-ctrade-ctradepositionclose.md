# PositionClose

Closes a position by the specified symbol.

```
bool  PositionClose(
   const string  symbol,                  // symbol
   ulong         deviation=ULONG_MAX      // deviation
   )

```

Closes a position with the specified ticket.

```
bool  PositionClose(
   const ulong   ticket,                  // position ticket
   ulong         deviation=ULONG_MAX      // deviation
   )

```

Parameters

symbol

[in]  Name of trade instrument, by which it is intended to close position.

ticket

[in]  Ticket of a closed position.

deviation=[ULONG_MAX](/en/docs/constants/namedconstants/typeconstants)

[in] Maximal deviation from the current price (in points).

Return Value

true - successful check of the basic structures, otherwise - false.

Note

Successful completion of the PositionClose(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of trade request (trade server return code) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode).

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol. In this case, PositionClose will close a position with the lowest ticket.
