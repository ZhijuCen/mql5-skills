# Order Properties

Requests to execute trade operations are formalized as orders. Each order has a variety of properties for reading. Information on them can be obtained using functions OrderGet...() and HistoryOrderGet...().

For functions [OrderGetInteger()](/en/docs/trading/ordergetinteger) and [HistoryOrderGetInteger()](/en/docs/trading/historyordergetinteger)

ENUM_ORDER_PROPERTY_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| ORDER_TICKET | Order ticket. Unique number assigned to each order | long |
| ORDER_TIME_SETUP | Order setup time | datetime |
| ORDER_TYPE | Order type | ENUM_ORDER_TYPE |
| ORDER_STATE | Order state | ENUM_ORDER_STATE |
| ORDER_TIME_EXPIRATION | Order expiration time | datetime |
| ORDER_TIME_DONE | Order execution or cancellation time | datetime |
| ORDER_TIME_SETUP_MSC | The time of placing an order for execution in milliseconds since 01.01.1970 | long |
| ORDER_TIME_DONE_MSC | Order execution/cancellation time in milliseconds since 01.01.1970 | long |
| ORDER_TYPE_FILLING | Order filling type | ENUM_ORDER_TYPE_FILLING |
| ORDER_TYPE_TIME | Order lifetime | ENUM_ORDER_TYPE_TIME |
| ORDER_MAGIC | ID of an Expert Advisor that has placed the order (designed to ensure that each Expert Advisor places its own unique number) | long |
| ORDER_REASON | The reason or source for placing an order | ENUM_ORDER_REASON |
| ORDER_POSITION_ID | Position identifier  that is set to an order as soon as it is executed. Each executed order results in a  deal  that opens or modifies an already existing position. The identifier of exactly this position is set to the executed order at this moment. | long |
| ORDER_POSITION_BY_ID | Identifier of an opposite position used for closing by order  ORDER_TYPE_CLOSE_BY | long |

For functions [OrderGetDouble()](/en/docs/trading/ordergetdouble) and [HistoryOrderGetDouble()](/en/docs/trading/historyordergetdouble)

ENUM_ORDER_PROPERTY_DOUBLE

| Identifier | Description | Type |
| --- | --- | --- |
| ORDER_VOLUME_INITIAL | Order initial volume | double |
| ORDER_VOLUME_CURRENT | Order current volume | double |
| ORDER_PRICE_OPEN | Price specified in the order | double |
| ORDER_SL | Stop Loss value | double |
| ORDER_TP | Take Profit value | double |
| ORDER_PRICE_CURRENT | The current price of the order symbol | double |
| ORDER_PRICE_STOPLIMIT | The Limit order price for the StopLimit order | double |

For functions [OrderGetString()](/en/docs/trading/ordergetstring) and [HistoryOrderGetString()](/en/docs/trading/historyordergetstring)

ENUM_ORDER_PROPERTY_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| ORDER_SYMBOL | Symbol of the order | string |
| ORDER_COMMENT | Order comment | string |
| ORDER_EXTERNAL_ID | Order identifier in an external trading system (on the Exchange) | string |

When sending a trade request using the [OrderSend()](/en/docs/trading/ordersend) function, some operations require the indication of the order type. The order type is specified in the type field of the special structure [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest), and can accept values of the ENUM_ORDER_TYPE enumeration.

ENUM_ORDER_TYPE

| Identifier | Description |
| --- | --- |
| ORDER_TYPE_BUY | Market Buy order |
| ORDER_TYPE_SELL | Market Sell order |
| ORDER_TYPE_BUY_LIMIT | Buy Limit pending order |
| ORDER_TYPE_SELL_LIMIT | Sell Limit pending order |
| ORDER_TYPE_BUY_STOP | Buy Stop pending order |
| ORDER_TYPE_SELL_STOP | Sell Stop pending order |
| ORDER_TYPE_BUY_STOP_LIMIT | Upon reaching the order price, a pending Buy Limit order is placed at the StopLimit price |
| ORDER_TYPE_SELL_STOP_LIMIT | Upon reaching the order price, a pending Sell Limit order is placed at the StopLimit price |
| ORDER_TYPE_CLOSE_BY | Order to close a position by an opposite one |

Each order has a status that describes its state. To obtain information, use [OrderGetInteger()](/en/docs/trading/ordergetinteger) or [HistoryOrderGetInteger()](/en/docs/trading/historyordergetinteger) with the ORDER_STATE modifier. Allowed values are stored in the ENUM_ORDER_STATE enumeration.

ENUM_ORDER_STATE

| Identifier | Description |
| --- | --- |
| ORDER_STATE_STARTED | Order checked, but not yet accepted by broker |
| ORDER_STATE_PLACED | Order accepted |
| ORDER_STATE_CANCELED | Order canceled by client |
| ORDER_STATE_PARTIAL | Order partially executed |
| ORDER_STATE_FILLED | Order fully executed |
| ORDER_STATE_REJECTED | Order rejected |
| ORDER_STATE_EXPIRED | Order expired |
| ORDER_STATE_REQUEST_ADD | Order is being registered (placing to the trading system) |
| ORDER_STATE_REQUEST_MODIFY | Order is being modified (changing its parameters) |
| ORDER_STATE_REQUEST_CANCEL | Order is being deleted (deleting from the trading system) |

When sending a trade request for execution at the current time (time in force), the price and the required buy/sell volume should be specified. Also, keep in mind that financial markets provide no guarantee that the entire requested volume is available for a certain financial instrument at the desired price. Therefore, trading operations in real time are regulated using the price and volume execution modes. The modes, or execution policies, define the rules for cases when the price has changed or the requested volume cannot be completely fulfilled at the moment.

Price execution mode can be obtained from the [SYMBOL_TRADE_EXEMODE](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_trade_execution) symbol property containing the combination of flags from the  [ENUM_SYMBOL_TRADE_EXECUTION](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_trade_execution) enumeration.

| Execution mode | Description | The value in  ENUM_SYMBOL_TRADE_EXECUTION |
| --- | --- | --- |
| Execution mode 
   
 (Request Execution) | Executing a market order at the price previously received from the broker. 
   
 Prices for a certain market order are requested from the broker before the order is sent. Upon receiving the prices, order execution at the given price can be either confirmed or rejected. | SYMBOL_TRADE_EXECUTION_REQUEST |
| Instant Execution 
   
 (Instant Execution) | Executing a market order at the specified price immediately. 
   
 When sending a trade request to be executed, the platform automatically adds the current prices to the order. 
 
 If the broker accepts the price, the order is executed. 
 If the broker does not accept the requested price, a "Requote" is sent — the broker returns prices, at which this order can be executed. | SYMBOL_TRADE_EXECUTION_INSTANT |
| Market Execution 
   
 (Market Execution) | A broker makes a decision about the order execution price without any additional discussion with the trader. 
   
 Sending the order in such a mode means advance consent to its execution at this price. | SYMBOL_TRADE_EXECUTION_MARKET |
| Exchange Execution 
   
 (Exchange Execution) | Trade operations are executed at the prices of the current market offers. | SYMBOL_TRADE_EXECUTION_EXCHANGE |

Volume filling policy is specified in the [ORDER_TYPE_FILLING](/en/docs/constants/tradingconstants/orderproperties) order property and may contain only the values from the ENUM_ORDER_TYPE_FILLING enumeration

| Fill policy | Description | The value in  ENUM_ORDER_TYPE_FILLING |
| --- | --- | --- |
| Fill or Kill | An order can be executed in the specified volume only. 
   
 If the necessary amount of a financial instrument is currently unavailable in the market, the order will not be executed. 
   
 The desired volume can be made up of several available offers. 
   
 The possibility of using FOK orders is determined at the trade server. | ORDER_FILLING_FOK |
| Immediate or Cancel | A trader agrees to execute a deal with the volume maximally available in the market within that indicated in the order. 
   
 If the request cannot be filled completely, an order with the available volume will be executed, and the remaining volume will be canceled. 
   
 The possibility of using IOC orders is determined at the trade server. | ORDER_FILLING_IOC |
| Passive (Book or Cancel) | The BoC order assumes that the order can only be placed in the Depth of Market and cannot be immediately executed. If the order can be executed immediately when placed, then it is canceled. 
   
 In fact, the BOC policy guarantees that the price of the placed order will be worse than the current market. BoC orders are used to implement passive trading, so that the order is not executed immediately when placed and does not affect current liquidity. 
   
 Only limit and stop limit orders are supported (ORDER_TYPE_BUY_LIMIT, ORDER_TYPE_SELL_LIMIT, ORDER_TYPE_BUY_STOP_LIMIT, ORDER_TYPE_SELL_STOP_LIMIT). | ORDER_FILLING_BOC |
| Return | In case of partial filling, an order with remaining volume is not canceled but processed further. 
   
 Return orders are not allowed in the Market Execution mode (market execution — SYMBOL_TRADE_EXECUTION_MARKET). | ORDER_FILLING_RETURN |

When sending a trade request using the [OrderSend()](/en/docs/trading/ordersend) function, the necessary volume execution policy can be set in the type_filling field, namely in the special [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) structure. The values from the ENUM_ORDER_TYPE_FILLING enumeration are available. To get the property value in a specific active/completed order, use the [OrderGetInteger()](/en/docs/trading/ordergetinteger) or [HistoryOrderGetInteger()](/en/docs/trading/historyordergetinteger) function with the ORDER_TYPE_FILLING modifier.

Before sending an order with the current execution time, for the correct setting of the [ORDER_TYPE_FILLING](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer) value (volume execution type), you can use the [SymbolInfoInteger()](/en/docs/marketinformation/symbolinfointeger) function with each financial instrument to get the [SYMBOL_FILLING_MODE](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer) property value, which shows [volume execution types](/en/docs/constants/environment_state/marketinfoconstants#symbol_filling_mode) allowed for the symbol as a combination of flags. The ORDER_FILLING_RETURN filling type is enabled at all times except for the "Market execution" mode (SYMBOL_TRADE_EXECUTION_MARKET).

The use of filling types depending on the execution mode can be shown as the following table:

| Type of Execution\Fill Policy | Fill or Kill (FOK ORDER_FILLING_FOK) | Immediate or Cancel (IOC ORDER_FILLING_IOC) | Return (Return ORDER_FILLING_RETURN) |
| --- | --- | --- | --- |
| Instant Execution 
   
 (SYMBOL_TRADE_EXECUTION_INSTANT) | + (regardless of a symbol setting) | + (regardless of a symbol setting) | + (always) |
| Request Execution 
   
 SYMBOL_TRADE_EXECUTION_REQUEST | + (regardless of a symbol setting) | + (regardless of a symbol setting) | + (always) |
| Market Execution 
   
 SYMBOL_TRADE_EXECUTION_MARKET | + (set in the symbol settings) | + (set in the symbol settings) | - (disabled regardless of the symbol settings) |
| Exchange Execution 
   
 SYMBOL_TRADE_EXECUTION_EXCHANGE | + (set in the symbol settings) | + (set in the symbol settings) | + (always) |

In case of pending orders, the ORDER_FILLING_RETURN filling type should be used regardless of an execution type ([SYMBOL_TRADE_EXEMODE](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_trade_execution)), since such orders are not meant for execution at the time of sending. When using pending orders, a trader agrees in advance that, when conditions for a deal on this order are met, the broker will use the filling type supported by the exchange.

The order validity period can be set in the type_time field of the special structure [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) when sending a trade request using the [OrderSend()](/en/docs/trading/ordersend) function. Values of the ENUM_ORDER_TYPE_TIME enumeration are allowed. To obtain the value of this property use the function [OrderGetInteger()](/en/docs/trading/ordergetinteger) or [HistoryOrderGetInteger()](/en/docs/trading/historyordergetinteger) with the ORDER_TYPE_TIME modifier.

ENUM_ORDER_TYPE_TIME

| Identifier | Description |
| --- | --- |
| ORDER_TIME_GTC | Good till cancel order |
| ORDER_TIME_DAY | Good till current trade day order |
| ORDER_TIME_SPECIFIED | Good till expired order |
| ORDER_TIME_SPECIFIED_DAY | The order will be effective till 23:59:59 of the specified day. If this time is outside a trading session, the order expires in the nearest trading time. |

The reason for order placing is contained in the ORDER_REASON property. An order can be placed by an MQL5 program, from a mobile application, as a result of StopOut, etc. Possible values of ORDER_REASON are described in the ENUM_ORDER_REASON enumeration.

ENUM_ORDER_REASON

| Identifier | Description |
| --- | --- |
| ORDER_REASON_CLIENT | The order was placed from a desktop terminal |
| ORDER_REASON_MOBILE | The order was placed from a mobile application |
| ORDER_REASON_WEB | The order was placed from a web platform |
| ORDER_REASON_EXPERT | The order was placed from an MQL5-program, i.e. by an Expert Advisor or a script |
| ORDER_REASON_SL | The order was placed as a result of Stop Loss activation |
| ORDER_REASON_TP | The order was placed as a result of Take Profit activation |
| ORDER_REASON_SO | The order was placed as a result of the Stop Out event |
