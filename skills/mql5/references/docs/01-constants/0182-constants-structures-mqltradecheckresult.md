# The Structure of Results of a Trade Request Check (MqlTradeCheckResult)

Before [sending](/en/docs/trading/ordersend) a [request](/en/docs/constants/structures/mqltraderequest) for a [trade operation](/en/docs/constants/tradingconstants/enum_trade_request_actions) to a trade server, it is recommended to check it. The check is performed using the [OrderCheck()](/en/docs/trading/ordercheck) function, to which the checked request and a variable of the MqlTradeCheckResult structure type are passed. The check result will be written to this variable.

```
struct MqlTradeCheckResult
  {
   uint         retcode;             // Reply code
   double       balance;             // Balance after the execution of the deal
   double       equity;              // Equity after the execution of the deal
   double       profit;              // Floating profit
   double       margin;              // Margin requirements
   double       margin_free;         // Free margin
   double       margin_level;        // Margin level
   string       comment;             // Comment to the reply code (description of the error)
  };

```

Description of Fields

| Field | Description |
| --- | --- |
| retcode | Return code |
| balance | Balance value that will be after the execution of the trade operation |
| equity | Equity value that will be after the execution of the trade operation |
| profit | Value of the floating profit that will be after the execution of the trade operation |
| margin | Margin required for the trade operation |
| margin_free | Free margin that will be left after the execution of the trade operation |
| margin_level | Margin level that will be set after the execution of the trade operation |
| comment | Comment to the reply code, error description |

See also

[Trade Request Structure](/en/docs/constants/structures/mqltraderequest), [Structure for Current Prices](/en/docs/constants/structures/mqltick), [OrderSend](/en/docs/trading/ordersend), [OrderCheck](/en/docs/trading/ordercheck)
