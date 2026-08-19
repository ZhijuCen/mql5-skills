# CTrade

CTrade is a class for easy access to the trade functions.

### Description

CTrade class provides easy access to the trade functions.

### Declaration

```
   class CTrade : public CObject

```

### Title

```
   #include <Trade\Trade.mqh>

```

```
Inheritance hierarchy
   CObject
       CTrade
Direct descendants
CExpertTrade

```

### Class methods by groups

| Setting parameters |  |
| --- | --- |
| LogLevel | Sets logging level |
| SetExpertMagicNumber | Sets the expert ID |
| SetDeviationInPoints | Sets the allowed deviation |
| SetTypeFilling | Sets filling type of the order |
| SetTypeFillingBySymbol | Sets filling type of the order according to the specified symbol settings |
| SetAsyncMode | Sets asynchronous mode for trade operations |
| SetMarginMode | Sets margin calculation mode in accordance with the current account settings |
| Operations with orders |  |
| OrderOpen | Places a pending order with specified parameters |
| OrderModify | Modifies the pending order parameters |
| OrderDelete | Deletes a pending order |
| Operations with positions |  |
| PositionOpen | Opens a position with specified parameters |
| PositionModify | Modifies position parameters by the specified symbol or position ticket |
| PositionClose | Closes a position for the specified symbol |
| PositionClosePartial | Partially closes a position on a specified symbol or having a specified ticket |
| PositionCloseBy | Closes a position with the specified ticket by an opposite position |
| Additional methods |  |
| Buy | Opens a long position with specified parameters |
| Sell | Opens a short position with specified parameters |
| BuyLimit | Places a pending order of the Buy Limit type with specified parameters |
| BuyStop | Places a pending order of the Buy Stop type with specified parameters |
| SellLimit | Places a pending order of the Sell Limit type with specified parameters |
| SellStop | Places a pending order of the Sell Stop type with specified parameters |
| Access to the last request parameters |  |
| Request | Gets the copy of the last request structure |
| RequestAction | Gets the trade operation type |
| RequestActionDescription | Gets the trade operation type as string |
| RequestMagic | Gets the magic number of the Expert Advisor |
| RequestOrder | Gets the order ticket used in the last request |
| RequestSymbol | Gets the name of the symbol used in the last request |
| RequestVolume | Gets the trade volume (in lots) used in the last request |
| RequestPrice | Gets the price used in the last request |
| RequestStopLimit | Gets the price of  pending order of Stop Limit type used in the last request |
| RequestSL | Gets the Stop Loss price of the order used in the last request |
| RequestTP | Gets the Take Profit price of the order used in the last request |
| RequestDeviation | Gets the maximum allowable price deviation of the order used in the last request |
| RequestType | Gets the type of the order used in the last request |
| RequestTypeDescription | Gets the type of the order (as string) used in the last request |
| RequestTypeFilling | Gets the filling type of the order used in the last request |
| RequestTypeFillingDescription | Gets the filling type of the order (as string) used in the last request |
| RequestTypeTime | Gets the validity period of the order used in the last request |
| RequestTypeTimeDescription | Gets the validity period of the order (as string) used in the last request |
| RequestExpiration | Gets the expiration time of the order used in the last request |
| RequestComment | Gets the comment of the order used in the last request |
| RequestPosition | Gets position ticket |
| RequestPositionBy | Gets opposite position ticket |
| Access to the last request checking results |  |
| CheckResult | Gets the copy of the structure of the last request check result. |
| CheckResultRetcode | Gets the value of the retcode field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultRetcodeDescription | Gets the string description of the retcode field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultBalance | Gets the value of the balance field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultEquity | Gets the value of the equity field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultProfit | Gets the value of the floating profit after executing a trading operation. |
| CheckResultMargin | Gets the value of the margin field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultMarginFree | Gets the value of the margin_free field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultMarginLevel | Gets the value of the margin_level field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| CheckResultComment | Gets the value of the comment field of  MqlTradeCheckResult  type, filled while checking the request correctness |
| Access to the last request execution results |  |
| Result | Gets the copy of the structure of the last request result |
| ResultRetcode | Gets the code of request result |
| ResultRetcodeDescription | Gets the code of request result as a string |
| ResultDeal | Gets the deal ticket |
| ResultOrder | Gets the order ticket |
| ResultVolume | Gets the volume of deal or order |
| ResultPrice | Gets the price, confirmed by broker |
| ResultBid | Gets the current bid price (the requote) |
| ResultAsk | Gets the current ask price (the requote) |
| ResultComment | Gets the broker comment |
| Auxiliary methods |  |
| PrintRequest | Prints the last request parameters into journal |
| PrintResult | Prints the results of the last request into journal |
| FormatRequest | Prepares the formatted string with last request parameters |
| FormatRequestResult | Prepares the formatted string with results of the last request execution |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
