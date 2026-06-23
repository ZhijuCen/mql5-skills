# Deal Properties

A deal is the reflection of the fact of a [trade operation](/en/docs/constants/tradingconstants/enum_trade_request_actions) execution based on an [order](/en/docs/constants/tradingconstants/orderproperties) that contains a trade request. Each trade is described by properties that allow to obtain information about it. In order to read values of properties, functions of the HistoryDealGet...() type are used, that return values from corresponding enumerations.

For the function [HistoryDealGetInteger()](/en/docs/trading/historydealgetinteger)

ENUM_DEAL_PROPERTY_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| DEAL_TICKET | Deal ticket. Unique number assigned to each deal | long |
| DEAL_ORDER | Deal  order number | long |
| DEAL_TIME | Deal time | datetime |
| DEAL_TIME_MSC | The time of a deal execution in milliseconds since 01.01.1970 | long |
| DEAL_TYPE | Deal type | ENUM_DEAL_TYPE |
| DEAL_ENTRY | Deal entry - entry in, entry out, reverse | ENUM_DEAL_ENTRY |
| DEAL_MAGIC | Deal magic number (see  ORDER_MAGIC ) | long |
| DEAL_REASON | The reason or source for deal execution | ENUM_DEAL_REASON |
| DEAL_POSITION_ID | Identifier of a position , in the opening, modification or closing of which this deal took part. Each position has a unique identifier that is assigned to all deals executed for the symbol during the entire lifetime of the position. | long |

For the function [HistoryDealGetDouble()](/en/docs/trading/historydealgetdouble)

ENUM_DEAL_PROPERTY_DOUBLE

| Identifier | Description | Type |
| --- | --- | --- |
| DEAL_VOLUME | Deal volume | double |
| DEAL_PRICE | Deal price | double |
| DEAL_COMMISSION | Deal commission | double |
| DEAL_SWAP | Cumulative swap on close | double |
| DEAL_PROFIT | Deal profit | double |
| DEAL_FEE | Fee for making a deal charged immediately after performing a deal | double |
| DEAL_SL | Stop Loss level 
 
 Entry and reversal deals use the Stop Loss values from the original order based on which the position was opened or reversed 
 Exit deals use the Stop Loss of a position as at the time of position closing | double |
| DEAL_TP | Take Profit level 
 
 Entry and reversal deals use the  Take Profit  values from the original order based on which the position was opened or reversed 
 Exit deals use the  Take Profit  value of a position as at the time of position closing | double |

For the function [HistoryDealGetString()](/en/docs/trading/historydealgetstring)

ENUM_DEAL_PROPERTY_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| DEAL_SYMBOL | Deal symbol | string |
| DEAL_COMMENT | Deal comment | string |
| DEAL_EXTERNAL_ID | Deal identifier in an external trading system (on the Exchange) | string |

Each deal is characterized by a type, allowed values are enumerated in ENUM_DEAL_TYPE. In order to obtain information about the deal type, use the [HistoryDealGetInteger()](/en/docs/trading/historydealgetinteger) function with the DEAL_TYPE modifier.

ENUM_DEAL_TYPE

| Identifier | Description |
| --- | --- |
| DEAL_TYPE_BUY | Buy |
| DEAL_TYPE_SELL | Sell |
| DEAL_TYPE_BALANCE | Balance |
| DEAL_TYPE_CREDIT | Credit |
| DEAL_TYPE_CHARGE | Additional charge |
| DEAL_TYPE_CORRECTION | Correction |
| DEAL_TYPE_BONUS | Bonus |
| DEAL_TYPE_COMMISSION | Additional commission |
| DEAL_TYPE_COMMISSION_DAILY | Daily commission |
| DEAL_TYPE_COMMISSION_MONTHLY | Monthly commission |
| DEAL_TYPE_COMMISSION_AGENT_DAILY | Daily agent commission |
| DEAL_TYPE_COMMISSION_AGENT_MONTHLY | Monthly agent commission |
| DEAL_TYPE_INTEREST | Interest rate |
| DEAL_TYPE_BUY_CANCELED | Canceled buy deal.  There can be a situation when a previously executed buy deal is canceled. In this case, the type of the previously executed deal ( DEAL_TYPE_BUY)  is changed to  DEAL_TYPE_BUY_CANCELED , and its profit/loss is zeroized. Previously obtained profit/loss is charged/withdrawn using a separated balance operation |
| DEAL_TYPE_SELL_CANCELED | Canceled sell deal.  There can be a situation when a previously executed sell deal is canceled. In this case, the type of the previously executed deal ( DEAL_TYPE_SELL)  is changed to  DEAL_TYPE_SELL_CANCELED , and its profit/loss is zeroized. Previously obtained profit/loss is charged/withdrawn using a separated balance operation |
| DEAL_DIVIDEND | Dividend operations |
| DEAL_DIVIDEND_FRANKED | Franked (non-taxable) dividend operations |
| DEAL_TAX | Tax charges |

Deals differ not only in their types set in ENUM_DEAL_TYPE, but also in the way they change positions. This can be a simple position opening, or accumulation of a previously opened position (market entering), position closing by an opposite deal of a corresponding volume (market exiting), or position reversing, if the opposite-direction deal covers the volume of the previously opened position.

All these situations are described by values from the ENUM_DEAL_ENTRY enumeration. In order to receive this information about a deal, use the [HistoryDealGetInteger()](/en/docs/trading/historydealgetinteger) function with the DEAL_ENTRY modifier.

ENUM_DEAL_ENTRY

| Identifier | Description |
| --- | --- |
| DEAL_ENTRY_IN | Entry in |
| DEAL_ENTRY_OUT | Entry out |
| DEAL_ENTRY_INOUT | Reverse |
| DEAL_ENTRY_OUT_BY | Close a position by an opposite one |

The reason for deal execution is contained in the DEAL_REASON property. A deal can be executed as a result of triggering of an order placed from a mobile application or an MQL5 program, as well as as a result of the StopOut event, variation margin calculation, etc. Possible values of DEAL_REASON are described in the ENUM_DEAL_REASON enumeration. For non-trading deals resulting from balance, credit, commission and other operations, DEAL_REASON_CLIENT is indicated as the reason.

ENUM_DEAL_REASON

| Identifier | Description |
| --- | --- |
| DEAL_REASON_CLIENT | The deal was executed as a result of activation of an order placed from a desktop terminal |
| DEAL_REASON_MOBILE | The deal was executed as a result of activation of an order placed from a mobile application |
| DEAL_REASON_WEB | The deal was executed as a result of activation of an order placed from the web platform |
| DEAL_REASON_EXPERT | The deal was executed as a result of activation of an order placed from an MQL5 program, i.e. an Expert Advisor or a script |
| DEAL_REASON_SL | The deal was executed as a result of Stop Loss activation |
| DEAL_REASON_TP | The deal was executed as a result of Take Profit activation |
| DEAL_REASON_SO | The deal was executed as a result of the Stop Out event |
| DEAL_REASON_ROLLOVER | The deal was executed due to a rollover |
| DEAL_REASON_VMARGIN | The deal was executed after charging the variation margin |
| DEAL_REASON_SPLIT | The deal was executed after the split (price reduction) of an instrument, which had an open position during split announcement |
| DEAL_REASON_CORPORATE_ACTION | The deal was executed as a result of a corporate action: merging or renaming a security, transferring a client to another account, etc. |
