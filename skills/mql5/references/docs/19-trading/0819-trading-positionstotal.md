# PositionsTotal

Returns the number of open positions.

```
int  PositionsTotal();

```

Return Value

Value of [int](/en/docs/basis/types/integer/integertypes) type.

Note

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get and print the number of open positions on the account in the journal
   int total=PositionsTotal();
   Print("Number of open positions on account: ", total);
   /*
   result:
   Number of open positions on account: 2
   */
  }

```

See also

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionSelect()](/en/docs/trading/positionselect), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
