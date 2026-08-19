# OrdersTotal

Returns the number of current orders.

```
int  OrdersTotal();

```

Return Value

Value of the [int](/en/docs/basis/types/integer/integertypes) type.

Note

Do not confuse current [pending orders](/en/docs/constants/tradingconstants/orderproperties) with positions, which are also displayed on the "Trade" tab of the "Toolbox" of the client terminal. An order is a request to conduct a [transaction](/en/docs/constants/tradingconstants/enum_trade_request_actions), while a position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties).

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get and print in the journal the number of active pending orders on the account
   int total=OrdersTotal();
   Print("Number of active pending orders on the account: ", total);
   /*
   result:
   Number of active pending orders on the account: 2
   */
  }

```

See also

[OrderSelect()](/en/docs/trading/orderselect), [OrderGetTicket()](/en/docs/trading/ordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
