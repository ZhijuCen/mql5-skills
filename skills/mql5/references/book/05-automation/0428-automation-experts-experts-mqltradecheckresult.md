# MqlTradeCheckResult structure

Before sending a request for a trading operation to the trade server, it is recommended to check that it is completed without formal errors. The check is carried out by the [OrderCheck](/en/book/automation/experts/experts_ordercheck) function, to which we pass the request in the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure and the receiving variable of the MqlTradeCheckResult structure type.

In addition to the correctness of the request, the structure enables the evaluation of the account state after the execution of a trading operation, in particular, the balance, funds, and margin.

```
struct MqlTradeCheckResult 
{ 
   uint   retcode;      // Response code
   double balance;      // Balance after the transaction
   double equity;       // Equity after the transaction
   double profit;       // Floating profit
   double margin;       // Margin requirements
   double margin_free;  // Free margin
   double margin_level; // Margin level
   string comment;      // Comment to the response code (description of the error)
};

```

The following table describes the fields.

| Field | Description |
| --- | --- |
| retcode | Assumed return code |
| balance | The value of the balance, which will be observed after the execution of the trade operation |
| equity | The value of own funds, which will be observed after the execution of the trade operation |
| profit | The value of the floating profit, which will be observed after the execution of the trade operation |
| margin | Total locked margin after a trade |
| margin_free | The volume of free own funds that will remain after the execution of the trade operation |
| margin_level | The margin level that will be set after the execution of a trade operation |
| comment | Comment on the response code, description of the error |

In the structure which is filled by calling OrderCheck, the retcode field will contain a result code from among those that the platform supports for processing real trade requests and puts in a similar retcode field of the [MqlTradeResult](/en/book/automation/experts/experts_mqltraderesult) structure after calling trading functions OrderSend and OrderSendAsync.

Return code constants are presented in [MQL5 documentation](https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes). For their more visual output to the log when debugging Expert Advisors, the applied enumeration TRADE_RETCODE was defined in the file TradeRetcode.mqh. All elements in it have identifiers that match the built-in constants but without the common "TRADE_RETCODE_" prefix. For example,

```
enum TRADE_RETCODE
{
   OK_0           = 0,      // no standard constant
   REQUOTE        = 10004,  // TRADE_RETCODE_REQUOTE
   REJECT         = 10006,  // TRADE_RETCODE_REJECT
   CANCEL         = 10007,  // TRADE_RETCODE_CANCEL
   PLACED         = 10008,  // TRADE_RETCODE_PLACED
   DONE           = 10009,  // TRADE_RETCODE_DONE
   DONE_PARTIAL   = 10010,  // TRADE_RETCODE_DONE_PARTIAL
   ERROR          = 10011,  // TRADE_RETCODE_ERROR
   TIMEOUT        = 10012,  // TRADE_RETCODE_TIMEOUT
   INVALID        = 10013,  // TRADE_RETCODE_INVALID
   INVALID_VOLUME = 10014,  // TRADE_RETCODE_INVALID_VOLUME
   INVALID_PRICE  = 10015,  // TRADE_RETCODE_INVALID_PRICE
   INVALID_STOPS  = 10016,  // TRADE_RETCODE_INVALID_STOPS
   TRADE_DISABLED = 10017,  // TRADE_RETCODE_TRADE_DISABLED
   MARKET_CLOSED  = 10018,  // TRADE_RETCODE_MARKET_CLOSED
   ...
};
   
#define TRCSTR(X) EnumToString((TRADE_RETCODE)(X))

```

So, the use of TRCSTR(r.retcode), where r is a structure, will provide a minimal description of the numeric code.

We will consider an example of applying a macro and analyzing a structure in the next section about the [OrderCheck](/en/book/automation/experts/experts_ordercheck) function.
