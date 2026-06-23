# Request validation: OrderCheck

To perform any trading operation, the MQL program must first fill the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure with the necessary data. Before sending it to the server using trading functions, it makes sense to check it for formal correctness and evaluate the consequences of the request, in particular, the amount of margin that will be required and the remaining free funds. This check is performed by the OrderCheck function.

bool OrderCheck(const MqlTradeRequest &request, MqlTradeCheckResult &result)

If there are not enough funds if the parameters are filled incorrectly, the function returns false. In addition, the function also reacts with a refusal when the trading is disabled, both in the terminal as a whole and for a specific program. For the error code check the retcode field of the result structure.

Successful check of structure request and the trading environment ends with the status true, however, this does not guarantee that the requested operation will certainly succeed if it is repeated using the functions OrderSend or OrderSendAsync. Trading conditions may change between calls or the broker on the server may have settings applied for a specific external trading system that cannot be satisfied in the formal verification algorithm that is performed by OrderCheck.

To obtain a description of the expected financial result, you should analyze the fields of the structure result.

Unlike the [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin) function which calculates the estimated margin required for only one proposed position or order, OrderCheck takes into account, albeit in a simplified mode, the general state of the trading account. So it fills the margin field in the MqlTradeCheckResult structure and other related fields (margin_free, margin_level) with cumulative variables that will be formed after the execution of the order. For example, if a position is already open for any instrument at the time of the OrderCheck call and the request being checked increases the position, the margin field will reflect the amount of deposit, including previous margin liabilities. If the new order contains an operation in the opposite direction, the margin will not increase (in reality, it should decrease, because a position should be closed completely on a netting account and the hedging margin should be applied for opposite positions on a hedging account; however, the function does not perform such accurate calculations).

First of all, OrderCheck is useful for programmers at the initial stage of getting acquainted with the trading API in order to experiment with requests without sending them to the server.

Let's test the performance of the fOrderCheck unction using a simple non-trading Expert Advisor CustomOrderCheck.mq5. We made it an Expert Advisor and not a script for ease of use: this way it will remain on the chart after being launched with the current settings, which can be easily edited by changing individual input parameters. With a script, we would have to start over by setting the fields each time from the default values.

To run the check, let's set a timer in OnInit.

```
void OnInit()
{
   // initiate pending execution
   EventSetTimer(1);
}

```

As for the timer handler, the main algorithm will be implemented there. At the very beginning we cancel the timer since we need the code to be executed once, and then wait for the user to change the parameters.

```
void OnTimer()
{
   // execute the code once and wait for new user settings
   EventKillTimer();
   ...
}

```

The Expert Advisor's input parameters completely repeat the set of fields of the trade request structure.

```
input ENUM_TRADE_REQUEST_ACTIONS Action = TRADE_ACTION_DEAL;
input ulong Magic;
input ulong Order;
input string Symbol;    // Symbol (empty = current _Symbol)
input double Volume;    // Volume (0 = minimal lot)
input double Price;     // Price (0 = current Ask)
input double StopLimit;
input double SL;
input double TP;
input ulong Deviation;
input ENUM_ORDER_TYPE Type;
input ENUM_ORDER_TYPE_FILLING Filling;
input ENUM_ORDER_TYPE_TIME ExpirationType;
input datetime ExpirationTime;
input string Comment;
input ulong Position;
input ulong PositionBy;

```

Many of them do not affect the check and financial performance but are left so that you can be sure of this.

By default, the state of the variables corresponds to the request to open a position with the minimum lot of the current instrument. In particular, the Type parameter without explicit initialization will get the value of 0, which is equal to the ORDER_TYPE_BUY member of the ENUM_ORDER_TYPE structure. In the Action parameter, we specified an explicit initialization because 0 does not correspond to any element of the ENUM_TRADE_REQUEST_ACTIONS enumeration (the first element of TRADE_ACTION_DEAL is 1).

```
void OnTimer()
{
   ...
   // initialize structures with zeros
   MqlTradeRequest request = {};
   MqlTradeCheckResult result = {};
   
   // default values
   const bool kindOfBuy = (Type & 1) == 0;
   const string symbol = StringLen(Symbol) == 0 ? _Symbol : Symbol;
   const double volume = Volume == 0 ?
      SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN) : Volume;
   const double price = Price == 0 ?
      SymbolInfoDouble(symbol, kindOfBuy ? SYMBOL_ASK : SYMBOL_BID) : Price;
   ...

```

Let's fill in the structure. Real robots usually only need to assign a few fields, but since this test is generic, we must ensure that any parameters that the user enters are passed.

```
   request.action = Action;
   request.magic = Magic;
   request.order = Order;
   request.symbol = symbol;
   request.volume = volume;
   request.price = price;
   request.stoplimit = StopLimit;
   request.sl = SL;
   request.tp = TP;
   request.deviation = Deviation;
   request.type = Type;
   request.type_filling = Filling;
   request.type_time = ExpirationType;
   request.expiration = ExpirationTime;
   request.comment = Comment;
   request.position = Position;
   request.position_by = PositionBy;
   ...

```

Please note that here we do not normalize prices and lots yet, although it is required in the real program. Thus, this test makes it possible to enter "uneven" values and make sure that they lead to an error. In the following examples, normalization will be enabled.

Then we call OrderCheck and log the request and result structures. We are only interested in the retcode field of the latter, so it is additionally printed with "decryption" as text, macro TRCSTR (TradeRetcode.mqh). You can also analyze a string field comment, but its format may change so that it is more suitable for display to the user.

```
   ResetLastError();
   PRTF(OrderCheck(request, result));
   StructPrint(request, ARRAYPRINT_HEADER);
   Print(TRCSTR(result.retcode));
   StructPrint(result, ARRAYPRINT_HEADER, 2);
   ...

```

The output of structures is provided by a helper function StructPrint which is based on ArrayPrint. Because of this, we will still get a "raw" display of data. In particular, the elements of enumerations are represented by numbers "as is". Later we will develop a function for a more transparent (user-friendly) MqlTradeRequest structure output (see [TradeUtils.mqh](/en/book/automation/experts/experts_ordersend_ordersendasync)).

To facilitate the analysis of the results, at the beginning of the OnTimer function we will display the current state of the account, and at the end, for comparison, we will calculate the margin for a given trading operation using the function OrderCalcMargin.

```
void OnTimer()
{
   PRTF(AccountInfoDouble(ACCOUNT_EQUITY));
   PRTF(AccountInfoDouble(ACCOUNT_PROFIT));
   PRTF(AccountInfoDouble(ACCOUNT_MARGIN));
   PRTF(AccountInfoDouble(ACCOUNT_MARGIN_FREE));
   PRTF(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL));
   ...
   // filling in the structure MqlTradeRequest
   // calling OrderCheck and printing results
   ...
   double margin = 0;
   ResetLastError();
   PRTF(OrderCalcMargin(Type, symbol, volume, price, margin));
   PRTF(margin);
}

```

Below is an example of logs for XAUUSD with default settings.

```
AccountInfoDouble(ACCOUNT_EQUITY)=15565.22 / ok
AccountInfoDouble(ACCOUNT_PROFIT)=0.0 / ok
AccountInfoDouble(ACCOUNT_MARGIN)=0.0 / ok
AccountInfoDouble(ACCOUNT_MARGIN_FREE)=15565.22 / ok
AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)=0.0 / ok
OrderCheck(request,result)=true / ok
[action] [magic] [order] [symbol] [volume] [price] [stoplimit] [sl] [tp] [deviation] [type] »
       1       0       0 "XAUUSD"     0.01 1899.97        0.00 0.00 0.00           0      0 »
 » [type_filling] [type_time]        [expiration] [comment] [position] [position_by] [reserved]
 »             0           0 1970.01.01 00:00:00 ""                 0             0          0
OK_0
[retcode] [balance] [equity] [profit] [margin] [margin_free] [margin_level] [comment] [reserved]
        0  15565.22 15565.22     0.00    19.00      15546.22       81922.21 "Done"             0
OrderCalcMargin(Type,symbol,volume,price,margin)=true / ok
margin=19.0 / ok

```

The next example shows an estimate of the expected increase in margin on the account, where there is already an open position which we are going to double.

```
AccountInfoDouble(ACCOUNT_EQUITY)=9999.540000000001 / ok
AccountInfoDouble(ACCOUNT_PROFIT)=-0.83 / ok
AccountInfoDouble(ACCOUNT_MARGIN)=79.22 / ok
AccountInfoDouble(ACCOUNT_MARGIN_FREE)=9920.32 / ok
AccountInfoDouble(ACCOUNT_MARGIN_LEVEL)=12622.49431961626 / ok
OrderCheck(request,result)=true / ok
[action] [magic] [order]  [symbol] [volume] [price] [stoplimit] [sl] [tp] [deviation] [type] »
       1       0       0 "PLZL.MM"      1.0 12642.0         0.0  0.0  0.0           0      0 »
 » [type_filling] [type_time]        [expiration] [comment] [position] [position_by] [reserved]
 »              0           0 1970.01.01 00:00:00 ""                 0             0          0
OK_0
[retcode] [balance] [equity] [profit] [margin] [margin_free] [margin_level] [comment] [reserved]
        0  10000.87  9999.54    -0.83   158.26       9841.28        6318.43 "Done"             0
OrderCalcMargin(Type,symbol,volume,price,margin)=true / ok
margin=79.04000000000001 / ok

```

Try changing any request parameters and see if the request is successful. Incorrect parameter combinations will cause error codes from the [standard list](https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes), but since there are many more invalid options than reserved ones (the most common errors), the function can often return the generic code TRADE_RETCODE_INVALID (10013). In this regard, it is recommended to implement your own structure checks with a greater degree of diagnostics.

When sending real requests to the server, the same TRADE_RETCODE_INVALID code is used under various unforeseen circumstances, for example, when trying to re-edit an order whose modification operation has already been started (but has not yet been completed) in the external trading system.
