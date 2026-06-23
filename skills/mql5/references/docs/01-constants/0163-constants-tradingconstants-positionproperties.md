# Position Properties

Execution of [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions) results in the opening of a position, changing of its volume and/or direction, or its disappearance. Trade operations are conducted based on [orders](/en/docs/constants/tradingconstants/orderproperties), sent by the [OrderSend()](/en/docs/trading/ordersend) function in the form of [trade requests](/en/docs/constants/structures/mqltraderequest). For each financial [security](/en/docs/constants/environment_state/marketinfoconstants) (symbol) only one open position is possible. A position has a set of properties available for reading by the PositionGet...() functions.

For the function [PositionGetInteger()](/en/docs/trading/positiongetinteger)

ENUM_POSITION_PROPERTY_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| POSITION_TICKET | Position ticket. Unique number assigned to each newly opened position. It usually matches the ticket of an order used to open the position except when the ticket is changed as a result of service operations on the server, for example, when charging swaps with position re-opening. To find an order used to open a position, apply the POSITION_IDENTIFIER property. 
   
 POSITION_TICKET  value corresponds to  MqlTradeRequest::position . | long |
| POSITION_TIME | Position open time | datetime |
| POSITION_TIME_MSC | Position opening time in milliseconds since 01.01.1970 | long |
| POSITION_TIME_UPDATE | Position changing time | datetime |
| POSITION_TIME_UPDATE_MSC | Position changing time in milliseconds since 01.01.1970 | long |
| POSITION_TYPE | Position type | ENUM_POSITION_TYPE |
| POSITION_MAGIC | Position magic number (see  ORDER_MAGIC ) | long |
| POSITION_IDENTIFIER | Position identifier is a unique number assigned to each re-opened position. It does not change throughout its life cycle and corresponds to the ticket of an order used to open a position. 
   
 Position identifier is specified in each order (ORDER_POSITION_ID) and deal (DEAL_POSITION_ID) used to open, modify, or close it. Use this property to search for orders and deals related to the position. 
   
 When reversing a position in netting mode (using a single in/out trade), POSITION_IDENTIFIER does not change. However, POSITION_TICKET is replaced with the ticket of the order that led to the reversal. Position reversal is not provided in hedging mode. | long |
| POSITION_REASON | The reason for opening a position | ENUM_POSITION_REASON |

For the function [PositionGetDouble()](/en/docs/trading/positiongetdouble)

ENUM_POSITION_PROPERTY_DOUBLE

| Identifier | Description | Type |
| --- | --- | --- |
| POSITION_VOLUME | Position volume | double |
| POSITION_PRICE_OPEN | Position open price | double |
| POSITION_SL | Stop Loss level of opened position | double |
| POSITION_TP | Take Profit level of opened position | double |
| POSITION_PRICE_CURRENT | Current price of the position symbol | double |
| POSITION_SWAP | Cumulative swap | double |
| POSITION_PROFIT | Current profit | double |

For the function [PositionGetString()](/en/docs/trading/positiongetstring)

ENUM_POSITION_PROPERTY_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| POSITION_SYMBOL | Symbol of the position | string |
| POSITION_COMMENT | Position comment | string |
| POSITION_EXTERNAL_ID | Position identifier in an external trading system (on the Exchange) | string |

Direction of an open position (buy or sell) is defined by the value from the ENUM_POSITION_TYPE enumeration. In order to obtain the type of an open position use the [PositionGetInteger()](/en/docs/trading/positiongetinteger) function with the POSITION_TYPE modifier.

ENUM_POSITION_TYPE

| Identifier | Description |
| --- | --- |
| POSITION_TYPE_BUY | Buy |
| POSITION_TYPE_SELL | Sell |

The reason for opening a position is contained in the POSITION_REASON property. A position can be opened as a result of activation of an order placed from a desktop terminal, a mobile application, by an Expert Advisor, etc. Possible values of POSITION_REASON are described in the ENUM_POSITION_REASON enumeration.

ENUM_POSITION_REASON

| Identifier | Description |
| --- | --- |
| POSITION_REASON_CLIENT | The position was opened as a result of activation of an order placed from a desktop terminal |
| POSITION_REASON_MOBILE | The position was opened as a result of activation of an order placed from a mobile application |
| POSITION_REASON_WEB | The position was opened as a result of activation of an order placed from the web platform |
| POSITION_REASON_EXPERT | The position was opened as a result of activation of an order placed from an MQL5 program, i.e. an Expert Advisor or a script |
