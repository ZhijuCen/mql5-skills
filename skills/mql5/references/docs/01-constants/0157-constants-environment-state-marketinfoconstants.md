# Symbol Properties

To obtain the current market information there are several functions: [SymbolInfoInteger()](/en/docs/marketinformation/symbolinfointeger), [SymbolInfoDouble()](/en/docs/marketinformation/symbolinfodouble) and [SymbolInfoString()](/en/docs/marketinformation/symbolinfostring). The first parameter is the symbol name, the values of the second function parameter can be one of the identifiers of ENUM_SYMBOL_INFO_INTEGER, ENUM_SYMBOL_INFO_DOUBLE and ENUM_SYMBOL_INFO_STRING.

For function [SymbolInfoInteger()](/en/docs/marketinformation/symbolinfointeger)

ENUM_SYMBOL_INFO_INTEGER

| Identifier | Description | Type |
| --- | --- | --- |
| SYMBOL_SUBSCRIPTION_DELAY | Symbol data arrives with a delay. The property can be requested only for symbols selected in MarketWatch (SYMBOL_SELECT = true). The  ERR_MARKET_NOT_SELECTED  (4302) error is generated for other symbols | bool |
| SYMBOL_SECTOR | The sector of the economy to which the asset belongs | ENUM_SYMBOL_SECTOR |
| SYMBOL_INDUSTRY | The industry or the economy branch to which the symbol belongs | ENUM_SYMBOL_INDUSTRY |
| SYMBOL_CUSTOM | It is a custom symbol – the symbol has been created synthetically based on other symbols from the Market Watch and/or external data sources | bool |
| SYMBOL_BACKGROUND_COLOR | The color of the background used for the symbol in Market Watch | color |
| SYMBOL_CHART_MODE | The price type used for generating symbols bars, i.e. Bid or Last | ENUM_SYMBOL_CHART_MODE |
| SYMBOL_EXIST | Symbol with this name exists | bool |
| SYMBOL_SELECT | Symbol is selected in Market Watch | bool |
| SYMBOL_VISIBLE | Symbol is visible in Market Watch. 
   
 Some symbols (mostly, these are cross rates required for calculation of margin requirements or profits in deposit currency) are selected automatically, but may not be visible in Market Watch. To be displayed such symbols have to be explicitly selected. | bool |
| SYMBOL_SESSION_DEALS | Number of deals in the current session | long |
| SYMBOL_SESSION_BUY_ORDERS | Number of Buy orders at the moment | long |
| SYMBOL_SESSION_SELL_ORDERS | Number of Sell orders at the moment | long |
| SYMBOL_VOLUME | Volume of the last deal | long |
| SYMBOL_VOLUMEHIGH | Maximal day volume | long |
| SYMBOL_VOLUMELOW | Minimal day volume | long |
| SYMBOL_TIME | Time of the last quote | datetime |
| SYMBOL_TIME_MSC | Time of the last quote in milliseconds since 1970.01.01 | long |
| SYMBOL_DIGITS | Digits after a decimal point | int |
| SYMBOL_SPREAD_FLOAT | Indication of a floating spread | bool |
| SYMBOL_SPREAD | Spread value in points | int |
| SYMBOL_TICKS_BOOKDEPTH | Maximal number of requests shown in  Depth of Market . For symbols that have no queue of requests, the value is equal to zero. | int |
| SYMBOL_TRADE_CALC_MODE | Contract price calculation mode | ENUM_SYMBOL_CALC_MODE |
| SYMBOL_TRADE_MODE | Order execution type | ENUM_SYMBOL_TRADE_MODE |
| SYMBOL_START_TIME | Date of the symbol trade beginning (usually used for futures) | datetime |
| SYMBOL_EXPIRATION_TIME | Date of the symbol trade end (usually used for futures) | datetime |
| SYMBOL_TRADE_STOPS_LEVEL | Minimal indention in points from the current close price to place Stop orders | int |
| SYMBOL_TRADE_FREEZE_LEVEL | Distance to freeze trade operations in points | int |
| SYMBOL_TRADE_EXEMODE | Deal execution mode | ENUM_SYMBOL_TRADE_EXECUTION |
| SYMBOL_SWAP_MODE | Swap calculation model | ENUM_SYMBOL_SWAP_MODE |
| SYMBOL_SWAP_ROLLOVER3DAYS | The day of week to charge 3-day swap rollover | ENUM_DAY_OF_WEEK |
| SYMBOL_MARGIN_HEDGED_USE_LEG | Calculating hedging margin using the larger leg (Buy or Sell) | bool |
| SYMBOL_EXPIRATION_MODE | Flags of allowed order  expiration modes | int |
| SYMBOL_FILLING_MODE | Flags of allowed order  filling modes | int |
| SYMBOL_ORDER_MODE | Flags of allowed  order types | int |
| SYMBOL_ORDER_GTC_MODE | Expiration of Stop Loss and Take Profit orders, if SYMBOL_EXPIRATION_MODE= SYMBOL_EXPIRATION_GTC  (Good till canceled) | ENUM_SYMBOL_ORDER_GTC_MODE |
| SYMBOL_OPTION_MODE | Option type | ENUM_SYMBOL_OPTION_MODE |
| SYMBOL_OPTION_RIGHT | Option right (Call/Put) | ENUM_SYMBOL_OPTION_RIGHT |

For function [SymbolInfoDouble()](/en/docs/marketinformation/symbolinfodouble)

ENUM_SYMBOL_INFO_DOUBLE

| Identifier | Description | Type |
| --- | --- | --- |
| SYMBOL_BID | Bid - best sell offer | double |
| SYMBOL_BIDHIGH | Maximal Bid of the day | double |
| SYMBOL_BIDLOW | Minimal Bid of the day | double |
| SYMBOL_ASK | Ask - best buy offer | double |
| SYMBOL_ASKHIGH | Maximal Ask of the day | double |
| SYMBOL_ASKLOW | Minimal Ask of the day | double |
| SYMBOL_LAST | Price of the last deal | double |
| SYMBOL_LASTHIGH | Maximal Last of the day | double |
| SYMBOL_LASTLOW | Minimal Last of the day | double |
| SYMBOL_VOLUME_REAL | Volume of the last deal | double |
| SYMBOL_VOLUMEHIGH_REAL | Maximum Volume of the day | double |
| SYMBOL_VOLUMELOW_REAL | Minimum Volume of the day | double |
| SYMBOL_OPTION_STRIKE | The strike price of an option. The price at which an option buyer can buy (in a Call option) or sell (in a Put option) the underlying asset, and the option seller is obliged to sell or buy the appropriate amount of the underlying asset. | double |
| SYMBOL_POINT | Symbol point value | double |
| SYMBOL_TRADE_TICK_VALUE | Value of SYMBOL_TRADE_TICK_VALUE_PROFIT | double |
| SYMBOL_TRADE_TICK_VALUE_PROFIT | Calculated tick price for a profitable position | double |
| SYMBOL_TRADE_TICK_VALUE_LOSS | Calculated tick price for a losing position | double |
| SYMBOL_TRADE_TICK_SIZE | Minimal price change | double |
| SYMBOL_TRADE_CONTRACT_SIZE | Trade contract size | double |
| SYMBOL_TRADE_ACCRUED_INTEREST | Accrued interest  – accumulated coupon interest, i.e. part of the coupon interest calculated in proportion to the number of days since the coupon bond issuance or the last coupon interest payment | double |
| SYMBOL_TRADE_FACE_VALUE | Face value  – initial bond value set by the issuer | double |
| SYMBOL_TRADE_LIQUIDITY_RATE | Liquidity Rate is the share of the asset that can be used for the margin. | double |
| SYMBOL_VOLUME_MIN | Minimal volume for a deal | double |
| SYMBOL_VOLUME_MAX | Maximal volume for a deal | double |
| SYMBOL_VOLUME_STEP | Minimal volume change step for deal execution | double |
| SYMBOL_VOLUME_LIMIT | Maximum allowed aggregate volume of an open position and pending orders in one direction (buy or sell) for the symbol. For example, with the limitation of 5 lots, you can have an open buy position with the volume of 5 lots and place a pending order Sell Limit with the volume of 5 lots. But in this case you cannot place a Buy Limit pending order (since the total volume in one direction will exceed the limitation) or place Sell Limit with the volume more than 5 lots. | double |
| SYMBOL_SWAP_LONG | Long swap value | double |
| SYMBOL_SWAP_SHORT | Short swap value | double |
| SYMBOL_SWAP_SUNDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from SUNDAY to the next day. There following values are supported: 
 
 0 – no swap is charged 
 1 – single swap 
 3 – triple swap | double |
| SYMBOL_SWAP_MONDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Monday to Tuesday | double |
| SYMBOL_SWAP_TUESDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Tuesday to Wednesday | double |
| SYMBOL_SWAP_WEDNESDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Wednesday to Thursday | double |
| SYMBOL_SWAP_THURSDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Thursday to Friday | double |
| SYMBOL_SWAP_FRIDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Friday to Saturday | double |
| SYMBOL_SWAP_SATURDAY | Swap calculation ratio (SYMBOL_SWAP_LONG or SYMBOL_SWAP_SHORT) for overnight positions rolled over from Saturday to Sunday | double |
| SYMBOL_MARGIN_INITIAL | Initial margin means the amount in the margin currency required for opening a position with the volume of one lot. It is used for checking a client's assets when he or she enters the market. 
   
 The  SymbolInfoMarginRate()  function provides data on the amount of charged margin depending on the order type and direction. | double |
| SYMBOL_MARGIN_MAINTENANCE | The maintenance margin. If it is set, it sets the margin amount in the margin currency of the symbol, charged from one lot. It is used for checking a client's assets when his/her account state changes. If the maintenance margin is equal to 0, the initial margin is used. 
   
 The  SymbolInfoMarginRate()  function provides data on the amount of charged margin depending on the order type and direction. | double |
| SYMBOL_SESSION_VOLUME | Summary volume of current session deals | double |
| SYMBOL_SESSION_TURNOVER | Summary turnover of the current session | double |
| SYMBOL_SESSION_INTEREST | Summary open interest | double |
| SYMBOL_SESSION_BUY_ORDERS_VOLUME | Current volume of Buy orders | double |
| SYMBOL_SESSION_SELL_ORDERS_VOLUME | Current volume of Sell orders | double |
| SYMBOL_SESSION_OPEN | Open price of the current session | double |
| SYMBOL_SESSION_CLOSE | Close price of the current session | double |
| SYMBOL_SESSION_AW | Average weighted price of the current session | double |
| SYMBOL_SESSION_PRICE_SETTLEMENT | Settlement price of the current session | double |
| SYMBOL_SESSION_PRICE_LIMIT_MIN | Minimal price of the current session | double |
| SYMBOL_SESSION_PRICE_LIMIT_MAX | Maximal price of the current session | double |
| SYMBOL_MARGIN_HEDGED | Contract size or margin value per one lot of hedged positions (oppositely directed positions of one symbol). Two margin calculation methods are possible for hedged positions. The calculation method is defined by the broker.  
   
 Basic calculation: 
 
 If the initial margin (SYMBOL_MARGIN_INITIAL) is specified for a symbol, the hedged margin is specified as an absolute value (in monetary terms). 
 If the initial margin is not specified (equal to 0), SYMBOL_MARGIN_HEDGED is equal to the size of the contract, that will be used to calculate the margin by the appropriate formula in accordance with the type of the financial instrument ( SYMBOL_TRADE_CALC_MODE ). 
 
   
 Calculation for the largest position: 
 
 The  SYMBOL_MARGIN_HEDGED value is not taken into account. 
 The volume of all short and all long positions of a symbol is calculated. 
 For each direction, a weighted average open price and a weighted average rate of conversion to the deposit currency is calculated. 
 Next, using the appropriate formula chosen in accordance with the symbol type ( SYMBOL_TRADE_CALC_MODE ) the margin is calculated for the short and the long part. 
 The largest one of the values is used as the margin. | double |
| SYMBOL_PRICE_CHANGE | Change of the current price relative to the end of the previous trading day in % | double |
| SYMBOL_PRICE_VOLATILITY | Price volatility in % | double |
| SYMBOL_PRICE_THEORETICAL | Theoretical option price | double |
| SYMBOL_PRICE_DELTA | Option/warrant delta shows the value the option price changes by, when the underlying asset price changes by 1 | double |
| SYMBOL_PRICE_THETA | Option/warrant theta shows the number of points the option price is to lose every day due to a temporary breakup, i.e. when the expiration date approaches | double |
| SYMBOL_PRICE_GAMMA | Option/warrant gamma shows the change rate of delta – how quickly or slowly the option premium changes | double |
| SYMBOL_PRICE_VEGA | Option/warrant vega shows the number of points the option price changes by when the volatility changes by 1% | double |
| SYMBOL_PRICE_RHO | Option/warrant rho reflects the sensitivity of the theoretical option price to the interest rate changing by 1% | double |
| SYMBOL_PRICE_OMEGA | Option/warrant omega. Option elasticity shows a relative percentage change of the option price by the percentage change of the underlying asset price | double |
| SYMBOL_PRICE_SENSITIVITY | Option/warrant sensitivity shows by how many points the price of the option's underlying asset should change so that the price of the option changes by one point | double |

For function [SymbolInfoString()](/en/docs/marketinformation/symbolinfostring)

ENUM_SYMBOL_INFO_STRING

| Identifier | Description | Type |
| --- | --- | --- |
| SYMBOL_BASIS | The underlying asset of a derivative | string |
| SYMBOL_CATEGORY | The name of the sector or category to which the financial symbol belongs | string |
| SYMBOL_COUNTRY | The country to which the financial symbol belongs | string |
| SYMBOL_SECTOR_NAME | The sector of the economy to which the financial symbol belongs | string |
| SYMBOL_INDUSTRY_NAME | The industry branch or the industry to which the financial symbol belongs | string |
| SYMBOL_CURRENCY_BASE | Basic currency of a symbol | string |
| SYMBOL_CURRENCY_PROFIT | Profit currency | string |
| SYMBOL_CURRENCY_MARGIN | Margin currency | string |
| SYMBOL_BANK | Feeder of the current quote | string |
| SYMBOL_DESCRIPTION | Symbol description | string |
| SYMBOL_EXCHANGE | The name of the exchange in which the financial symbol is traded | string |
| SYMBOL_FORMULA | The formula used for the custom symbol pricing. If the name of a financial symbol used in the formula starts with a digit or contains a special character (">" ", ".", "-", "&", "#" and so on) quotation marks should be used around this symbol name. 
 
 Synthetic symbol: "@ESU19"/EURCAD 
 Calendar spread: "Si-9.13"-"Si-6.13" 
 Euro index: 34.38805726 * pow(EURUSD,0.3155) * pow(EURGBP,0.3056) * pow(EURJPY,0.1891) * pow(EURCHF,0.1113) * pow(EURSEK,0.0785) | string |
| SYMBOL_ISIN | The name of a symbol in the ISIN system (International Securities Identification Number). The International Securities Identification Number is a 12-digit alphanumeric code that uniquely identifies a security. The presence of this symbol property is determined on the side of a trade server. | string |
| SYMBOL_PAGE | The address of the web page containing symbol information. This address will be displayed as a link when viewing symbol properties in the terminal | string |
| SYMBOL_PATH | Path in the symbol tree | string |

A symbol price chart can be based on Bid or Last prices. The price selected for symbol charts also affects the generation and display of bars in the terminal. Possible values of the SYMBOL_CHART_MODE property are described in ENUM_SYMBOL_CHART_MODE

ENUM_SYMBOL_CHART_MODE

| Identifier | Description |
| --- | --- |
| SYMBOL_CHART_MODE_BID | Bars are based on Bid prices |
| SYMBOL_CHART_MODE_LAST | Bars are based on Last prices |

For each symbol several expiration modes of pending orders can be specified. A flag is matched to each mode. Flags can be combined using the operation of logical OR (|), for example, SYMBOL_EXPIRATION_GTC|SYMBOL_EXPIRATION_SPECIFIED. In order to check whether a certain mode is allowed for the symbol, the result of the logical AND (&) should be compared to the mode flag.

If flag SYMBOL_EXPIRATION_SPECIFIED is specified for a symbol, then while sending a pending order, you may specify the moment this pending order is valid till.

| Identifier | Value | Description |
| --- | --- | --- |
| SYMBOL_EXPIRATION_GTC | 1 | The order is valid during the unlimited time period, until it is explicitly canceled |
| SYMBOL_EXPIRATION_DAY | 2 | The order is valid till the end of the day |
| SYMBOL_EXPIRATION_SPECIFIED | 4 | The expiration time is specified in the order |
| SYMBOL_EXPIRATION_SPECIFIED_DAY | 8 | The expiration date is specified in the order |

Example:

```
//+------------------------------------------------------------------+
//| Checks if the specified expiration mode is allowed               |
//+------------------------------------------------------------------+
bool IsExpirationTypeAllowed(string symbol,int exp_type)
  {
//--- Obtain the value of the property that describes allowed expiration modes
   int expiration=(int)SymbolInfoInteger(symbol,SYMBOL_EXPIRATION_MODE);
//--- Return true, if mode exp_type is allowed
   return((expiration&exp_type)==exp_type);
  }

```

If the SYMBOL_EXPIRATION_MODE property is set to SYMBOL_EXPIRATION_GTC (good till canceled), the expiration of pending orders, as well as of Stop Loss/Take Profit orders should be additionally set using the ENUM_SYMBOL_ORDER_GTC_MODE enumeration.

ENUM_SYMBOL_ORDER_GTC_MODE

| Identifier | Description |
| --- | --- |
| SYMBOL_ORDERS_GTC | Pending orders and Stop Loss/Take Profit levels are valid for an unlimited period until their explicit cancellation |
| SYMBOL_ORDERS_DAILY | Orders are valid during one trading day. At the end of the day, all Stop Loss and Take Profit levels, as well as pending orders are deleted. |
| SYMBOL_ORDERS_DAILY_EXCLUDING_STOPS | When a trade day changes, only pending orders are deleted, while Stop Loss and Take Profit levels are preserved. |

When sending an order, we can specify the filling policy of a volume set in the order. The possible volume-based order execution options for each symbol are specified in the table. It is possible to set several modes for each instrument via a combination of flags. The combination of flags is expressed by the logical OR (|) operation, for example SYMBOL_FILLING_FOK|SYMBOL_FILLING_IOC.  To check if a specific mode is allowed for an instrument, compare the logical AND (&) result with the mode flag - [example](/en/docs/constants/environment_state/marketinfoconstants#filling_example).

| Fill policy | ID | Value | Description |
| --- | --- | --- | --- |
| Fill or Kill | SYMBOL_FILLING_FOK | 1 | An order can be executed in the specified volume only. 
   
 If the necessary amount of a financial instrument is currently unavailable in the market, the order will not be executed. The desired volume can be made up of several available offers. 
   
 When sending an order, the  ORDER_FILLING_FOK  filling type should be specified for this policy. 
   
 The possibility of using FOK orders is determined at the trade server. |
| Immediate or Cancel | SYMBOL_FILLING_IOC | 2 | A trader agrees to execute a deal with the volume maximally available in the market within that indicated in the order. If the request cannot be filled completely, an order with the available volume will be executed, and the remaining volume will be canceled. 
   
 When sending an order, the  ORDER_FILLING_IOC  filling type should be specified for this policy. 
   
 The possibility of using IOC orders is determined at the trade server. |
| Passive | SYMBOL_FILLING_BOC | 4 | The BOC (Book-or-Cancel) policy assumes that an order can only be placed in the Depth of Market and cannot be immediately executed. If the order can be executed immediately when placed, then it is canceled. 
   
 In fact, this execution policy can only be specified when the price of the placed order is to be worse than the current market. BoC orders are used to implement passive trading, so that the order is not executed immediately when placed and does not affect current liquidity. 
   
 Only limit and stop limit orders are supported, i.e. the  SYMBOL_ORDER_MODE  flag should contain the SYMBOL_ORDER_LIMIT and/or SYMBOL_ORDER_STOP_LIMIT values. |
| Return | No identifier |  | In case of partial filling, a market or limit order with remaining volume is not canceled but processed further. 
   
 When sending an order, the  ORDER_FILLING_RETURN  filling type should be specified for this policy. 
   
 Return orders are not allowed in the Market Execution mode (market execution — SYMBOL_TRADE_EXECUTION_MARKET). |

When sending a trade request using the [OrderSend()](/en/docs/trading/ordersend) function, the necessary volume execution policy can be set in the type_filling field, namely in the special [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) structure. The values from the [ENUM_ORDER_TYPE_FILLING](/en/docs/constants/tradingconstants/orderproperties#enum_order_type_filling) enumeration are available.  If no filling type is specified, ORDER_FILLING_RETURN is automatically set in the trade request. The ORDER_FILLING_RETURN filling type is enabled in any [execution mode](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_trade_execution) except for "Market execution" (SYMBOL_TRADE_EXECUTION_MARKET).

While sending a trade request for execution at the current time (time in force), we should keep in mind that financial markets provide no guarantee that the entire requested volume is available for a certain financial instrument at the desired price. Therefore, trading operations in real time are regulated using the price and volume execution modes. The modes, or execution policies, define the rules for cases when the price has changed or the requested volume cannot be completely fulfilled at the moment.

| Execution mode | Description | The value in  ENUM_SYMBOL_TRADE_EXECUTION |
| --- | --- | --- |
| Execution mode 
   
 (Request Execution) | Executing a market order at the price previously received from the broker. 
   
 Prices for a certain market order are requested from the broker before the order is sent. Upon receiving the prices, order execution at the given price can be either confirmed or rejected. | SYMBOL_TRADE_EXECUTION_REQUEST |
| Instant Execution | Executing a market order at the specified price immediately. 
   
 When sending a trade request to be executed, the platform automatically adds the current prices to the order. 
 
 If the broker accepts the price, the order is executed. 
 If the broker does not accept the requested price, a "Requote" is sent — the broker returns prices, at which this order can be executed. | SYMBOL_TRADE_EXECUTION_INSTANT |
| Market Execution | A broker makes a decision about the order execution price without any additional discussion with the trader. 
   
 Sending the order in such a mode means advance consent to its execution at this price. | SYMBOL_TRADE_EXECUTION_MARKET |
| Exchange Execution | Trade operations are executed at the prices of the current market offers. | SYMBOL_TRADE_EXECUTION_EXCHANGE |

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

Example:

```
//+------------------------------------------------------------------+
//| check if a given filling mode is allowed                         |
//+------------------------------------------------------------------+
bool IsFillingTypeAllowed(string symbol,int fill_type)
  {
//--- get the value of the property describing the filling mode
   int filling=(int)SymbolInfoInteger(symbol,SYMBOL_FILLING_MODE);
//--- return 'true' if the fill_type mode is allowed
   return((filling&fill_type)==fill_type);
  }

```

When sending a [trade request](/en/docs/constants/structures/mqltraderequest) using OrderSend() function, an order type from [ENUM_ORDER_TYPE enumeration](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) should be specified for some operations. Not all types of orders may be allowed for a specific symbol. [SYMBOL_ORDER_MODE](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_integer) property describes the flags of the allowed order types.

| Identifier | Value | Description |
| --- | --- | --- |
| SYMBOL_ORDER_MARKET | 1 | Market orders are allowed (Buy and Sell) |
| SYMBOL_ORDER_LIMIT | 2 | Limit orders are allowed (Buy Limit and Sell Limit) |
| SYMBOL_ORDER_STOP | 4 | Stop orders are allowed (Buy Stop and Sell Stop) |
| SYMBOL_ORDER_STOP_LIMIT | 8 | Stop-limit orders are allowed (Buy Stop Limit and Sell Stop Limit) |
| SYMBOL_ORDER_SL | 16 | Stop Loss is allowed |
| SYMBOL_ORDER_TP | 32 | Take Profit is allowed |
| SYMBOL_ORDER_CLOSEBY | 64 | Close By operation is allowed, i.e. closing a position by another open position on the same instruments but in the opposite direction. The property is set for accounts with the hedging accounting system ( ACCOUNT_MARGIN_MODE_RETAIL_HEDGING ) |

Example:

```
//+------------------------------------------------------------------+
//| The function prints out order types allowed for a symbol         |
//+------------------------------------------------------------------+
void Check_SYMBOL_ORDER_MODE(string symbol)
  {
//--- receive the value of the property describing allowed order types
   int symbol_order_mode=(int)SymbolInfoInteger(symbol,SYMBOL_ORDER_MODE);
//--- check for market orders (Market Execution)
   if((SYMBOL_ORDER_MARKET&symbol_order_mode)==SYMBOL_ORDER_MARKET)
      Print(symbol+": Market orders are allowed (Buy and Sell)");
//--- check for Limit orders
   if((SYMBOL_ORDER_LIMIT&symbol_order_mode)==SYMBOL_ORDER_LIMIT)
      Print(symbol+": Buy Limit and Sell Limit orders are allowed");
//--- check for Stop orders
   if((SYMBOL_ORDER_STOP&symbol_order_mode)==SYMBOL_ORDER_STOP)
      Print(symbol+": Buy Stop and Sell Stop orders are allowed");
//--- check for Stop Limit orders
   if((SYMBOL_ORDER_STOP_LIMIT&symbol_order_mode)==SYMBOL_ORDER_STOP_LIMIT)
      Print(symbol+": Buy Stop Limit and Sell Stop Limit orders are allowed");
//--- check if placing a Stop Loss orders is allowed
   if((SYMBOL_ORDER_SL&symbol_order_mode)==SYMBOL_ORDER_SL)
      Print(symbol+": Stop Loss orders are allowed");
//--- check if placing a Take Profit orders is allowed
   if((SYMBOL_ORDER_TP&symbol_order_mode)==SYMBOL_ORDER_TP)
      Print(symbol+": Take Profit orders are allowed");
//--- check if closing a position by an opposite one is allowed
   if((SYMBOL_ORDER_TP&symbol_order_mode)==SYMBOL_ORDER_CLOSEBY)
      Print(symbol+": Close by allowed");
//---
  }

```

The ENUM_SYMBOL_CALC_MODE enumeration is used for obtaining information about how the margin requirements for a symbol are calculated.

ENUM_SYMBOL_CALC_MODE

| Identifier | Description | Formula |
| --- | --- | --- |
| SYMBOL_CALC_MODE_FOREX | Forex mode - calculation of profit and margin for Forex | Margin:  Lots *  Contract_Size  /  Leverage  *  Margin_Rate 
   
 Profit:   (close_price - open_price) * Contract_Size*Lots |
| SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE | Forex No Leverage mode – calculation of profit and margin for Forex symbols without taking into account the leverage | Margin:  Lots * Contract_Size * Margin_Rate 
   
 Profit:   (close_price - open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_FUTURES | Futures mode - calculation of margin and profit for futures | Margin: Lots * InitialMargin * Margin_Rate 
   
 Profit:  (close_price - open_price) * TickPrice / TickSize*Lots |
| SYMBOL_CALC_MODE_CFD | CFD mode - calculation of margin and profit for CFD | Margin: Lots * ContractSize * MarketPrice * Margin_Rate 
   
 Profit:  (close_price - open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_CFDINDEX | CFD index mode - calculation of margin and profit for CFD by indexes | Margin: (Lots * ContractSize * MarketPrice) * TickPrice / TickSize * Margin_Rate 
   
 Profit:  (close_price - open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_CFDLEVERAGE | CFD Leverage mode - calculation of margin and profit for CFD at leverage trading | Margin: (Lots * ContractSize * MarketPrice) / Leverage * Margin_Rate 
   
 Profit:  (close_price-open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_EXCH_STOCKS | Exchange mode – calculation of margin and profit for trading securities on a stock exchange | Margin: Lots * ContractSize * LastPrice * Margin_Rate 
   
 Profit:  (close_price - open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_EXCH_FUTURES | Futures mode –  calculation of margin and profit for trading futures contracts on a stock exchange | Margin: Lots * InitialMargin * Margin_Rate or Lots * MaintenanceMargin * Margin_Rate 
   
 Profit:  (close_price - open_price) * Lots * TickPrice / TickSize |
| SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS | FORTS Futures mode –  calculation of margin and profit for trading futures contracts on FORTS. The margin may be reduced by the amount of MarginDiscount deviation according to the following rules: 
 1. If the price of a long position (buy order) is less than the estimated price, MarginDiscount = Lots*((PriceSettle-PriceOrder)*TickPrice/TickSize) 
 2. If the price of a short position (sell order) exceeds the estimated price, MarginDiscount = Lots*((PriceOrder-PriceSettle)*TickPrice/TickSize) 
 where: 
 
 PriceSettle – estimated (clearing) price of the previous session; 
 PriceOrder – average weighted position price or open price set in the order (request); 
 TickPrice – tick price (cost of the price change by one point) 
 TickSize – tick size (minimum price change step) | Margin: Lots * InitialMargin * Margin_Rate or Lots * MaintenanceMargin * Margin_Rate 
   
 Profit:  (close_price - open_price) * Lots * TickPrice / TickSize |
| SYMBOL_CALC_MODE_EXCH_BONDS | Exchange Bonds mode – calculation of margin and profit for trading bonds on a stock exchange | Margin: Lots * ContractSize * FaceValue * open_price * /100 
   
 Profit:  Lots * close_price * FaceValue * Contract_Size  + AccruedInterest * Lots * ContractSize |
| SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX | Exchange MOEX Stocks mode – calculation of margin and profit for trading securities on MOEX | Margin: Lots * ContractSize * LastPrice * Margin_Rate 
   
 Profit:  (close_price - open_price) * Contract_Size * Lots |
| SYMBOL_CALC_MODE_EXCH_BONDS_MOEX | Exchange MOEX Bonds mode – calculation of margin and profit for trading bonds on MOEX | Margin: Lots * ContractSize * FaceValue * open_price * /100 
   
 Profit:  Lots * close_price * FaceValue * Contract_Size  + AccruedInterest * Lots * ContractSize |
| SYMBOL_CALC_MODE_SERV_COLLATERAL | Collateral mode - a symbol is used as a non-tradable asset on a trading account. The market value of an open position is calculated based on the volume, current market price, contract size and liquidity ratio. The value is included into Assets, which are added to Equity. Open positions of such symbols increase the Free Margin amount and are used as additional margin (collateral) for open positions of tradable instruments. | Margin: no 
 Profit:  no 
   
 Market Value: Lots*ContractSize*MarketPrice*LiqudityRate |

There are several symbol trading modes. Information about trading modes of a certain symbol is reflected in the values of enumeration ENUM_SYMBOL_TRADE_MODE.

ENUM_SYMBOL_TRADE_MODE

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_MODE_DISABLED | Trade is disabled for the symbol |
| SYMBOL_TRADE_MODE_LONGONLY | Allowed only long positions |
| SYMBOL_TRADE_MODE_SHORTONLY | Allowed only short positions |
| SYMBOL_TRADE_MODE_CLOSEONLY | Allowed only position close operations |
| SYMBOL_TRADE_MODE_FULL | No trade restrictions |

Possible deal execution modes for a certain symbol are defined in enumeration ENUM_SYMBOL_TRADE_EXECUTION.

ENUM_SYMBOL_TRADE_EXECUTION

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_EXECUTION_REQUEST | Execution by request |
| SYMBOL_TRADE_EXECUTION_INSTANT | Instant execution |
| SYMBOL_TRADE_EXECUTION_MARKET | Market execution |
| SYMBOL_TRADE_EXECUTION_EXCHANGE | Exchange execution |

Methods of swap calculation at position transfer are specified in enumeration ENUM_SYMBOL_SWAP_MODE. The method of swap calculation determines the units of measure of the [SYMBOL_SWAP_LONG](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_double) and [SYMBOL_SWAP_SHORT](/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_info_double) parameters. For example, if swaps are charged in the client deposit currency, then the values of those parameters are specified as an amount of money in the client deposit currency.

ENUM_SYMBOL_SWAP_MODE

| Identifier | Description |
| --- | --- |
| SYMBOL_SWAP_MODE_DISABLED | Swaps disabled (no swaps) |
| SYMBOL_SWAP_MODE_POINTS | Swaps are charged in points |
| SYMBOL_SWAP_MODE_CURRENCY_SYMBOL | Swaps are charged in money in base currency of the symbol |
| SYMBOL_SWAP_MODE_CURRENCY_MARGIN | Swaps are charged in money in margin currency of the symbol |
| SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT | Swaps are charged in money, in client deposit currency |
| SYMBOL_SWAP_MODE_CURRENCY_PROFIT | Swaps are charged in money in profit calculation currency |
| SYMBOL_SWAP_MODE_INTEREST_CURRENT | Swaps are charged as the specified annual interest from the instrument price at calculation of swap (standard bank year is 360 days) |
| SYMBOL_SWAP_MODE_INTEREST_OPEN | Swaps are charged as the specified annual interest from the open price of position (standard bank year is 360 days) |
| SYMBOL_SWAP_MODE_REOPEN_CURRENT | Swaps are charged by reopening positions. At the end of a trading day the position is closed. Next day it is reopened by the close price +/- specified number of points (parameters SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT) |
| SYMBOL_SWAP_MODE_REOPEN_BID | Swaps are charged by reopening positions. At the end of a trading day the position is closed. Next day it is reopened by the current Bid price +/- specified number of points (parameters SYMBOL_SWAP_LONG and SYMBOL_SWAP_SHORT) |

Values of the ENUM_DAY_OF_WEEK enumeration are used for specifying days of week.

ENUM_DAY_OF_WEEK

| Identifier | Description |
| --- | --- |
| SUNDAY | Sunday |
| MONDAY | Monday |
| TUESDAY | Tuesday |
| WEDNESDAY | Wednesday |
| THURSDAY | Thursday |
| FRIDAY | Friday |
| SATURDAY | Saturday |

An option is a contract, which gives the right, but not the obligation, to buy or sell an underlying asset (goods, stocks, futures, etc.) at a specified price on or before a specific date. The following enumerations describe option properties, including the option type and the right arising from it.

ENUM_SYMBOL_OPTION_RIGHT

| Identifier | Description |
| --- | --- |
| SYMBOL_OPTION_RIGHT_CALL | A call option gives you the right to buy an asset at a specified price |
| SYMBOL_OPTION_RIGHT_PUT | A put option gives you the right to sell an asset at a specified price |

ENUM_SYMBOL_OPTION_MODE

| Identifier | Description |
| --- | --- |
| SYMBOL_OPTION_MODE_EUROPEAN | European option may only be exercised on a specified date (expiration, execution date, delivery date) |
| SYMBOL_OPTION_MODE_AMERICAN | American option may be exercised on any trading day or before expiry. The period within which a buyer can exercise the option is specified for it |

Financial instruments are categorized by sectors of the economy. An economic sector is a part of economic activity which has specific characteristics, economic goals, functions and behavior, which allow separating this sector from other parts of the economy. ENUM_SYMBOL_SECTOR lists the economic sectors which a trading instruments can belong to.

ENUM_SYMBOL_SECTOR

| ID | Description |
| --- | --- |
| SECTOR_UNDEFINED | Undefined |
| SECTOR_BASIC_MATERIALS | Basic materials |
| SECTOR_COMMUNICATION_SERVICES | Communication services |
| SECTOR_CONSUMER_CYCLICAL | Consumer cyclical |
| SECTOR_CONSUMER_DEFENSIVE | Consumer defensive |
| SECTOR_CURRENCY | Currencies |
| SECTOR_CURRENCY_CRYPTO | Cryptocurrencies |
| SECTOR_ENERGY | Energy |
| SECTOR_FINANCIAL | Finance |
| SECTOR_HEALTHCARE | Healthcare |
| SECTOR_INDUSTRIALS | Industrials |
| SECTOR_REAL_ESTATE | Real estate |
| SECTOR_TECHNOLOGY | Technology |
| SECTOR_UTILITIES | Utilities |

Each financial instrument can be assigned to a specific type of industry or economy branch. An industry is a branch of an economy that produces a closely related set of raw materials, goods, or services. ENUM_SYMBOL_INDUSTRY lists industries which a trading instrument can belong to.

## ENUM_SYMBOL_INDUSTRY  #

| ID | Description |
| --- | --- |
| INDUSTRY_UNDEFINED | Undefined |
| Basic materials |  |
| INDUSTRY_AGRICULTURAL_INPUTS | Agricultural inputs |
| INDUSTRY_ALUMINIUM | Aluminium |
| INDUSTRY_BUILDING_MATERIALS | Building materials |
| INDUSTRY_CHEMICALS | Chemicals |
| INDUSTRY_COKING_COAL | Coking coal |
| INDUSTRY_COPPER | Copper |
| INDUSTRY_GOLD | Gold |
| INDUSTRY_LUMBER_WOOD | Lumber and wood production |
| INDUSTRY_INDUSTRIAL_METALS | Other industrial metals and mining |
| INDUSTRY_PRECIOUS_METALS | Other precious metals and mining |
| INDUSTRY_PAPER | Paper and paper products |
| INDUSTRY_SILVER | Silver |
| INDUSTRY_SPECIALTY_CHEMICALS | Specialty chemicals |
| INDUSTRY_STEEL | Steel |
| Communication services |  |
| INDUSTRY_ADVERTISING | Advertising agencies |
| INDUSTRY_BROADCASTING | Broadcasting |
| INDUSTRY_GAMING_MULTIMEDIA | Electronic gaming and multimedia |
| INDUSTRY_ENTERTAINMENT | Entertainment |
| INDUSTRY_INTERNET_CONTENT | Internet content and information |
| INDUSTRY_PUBLISHING | Publishing |
| INDUSTRY_TELECOM | Telecom services |
| Consumer cyclical |  |
| INDUSTRY_APPAREL_MANUFACTURING | Apparel manufacturing |
| INDUSTRY_APPAREL_RETAIL | Apparel retail |
| INDUSTRY_AUTO_MANUFACTURERS | Auto manufacturers |
| INDUSTRY_AUTO_PARTS | Auto parts |
| INDUSTRY_AUTO_DEALERSHIP | Auto and truck dealerships |
| INDUSTRY_DEPARTMENT_STORES | Department stores |
| INDUSTRY_FOOTWEAR_ACCESSORIES | Footwear and accessories |
| INDUSTRY_FURNISHINGS | Furnishing, fixtures and appliances |
| INDUSTRY_GAMBLING | Gambling |
| INDUSTRY_HOME_IMPROV_RETAIL | Home improvement retail |
| INDUSTRY_INTERNET_RETAIL | Internet retail |
| INDUSTRY_LEISURE | Leisure |
| INDUSTRY_LODGING | Lodging |
| INDUSTRY_LUXURY_GOODS | Luxury goods |
| INDUSTRY_PACKAGING_CONTAINERS | Packaging and containers |
| INDUSTRY_PERSONAL_SERVICES | Personal services |
| INDUSTRY_RECREATIONAL_VEHICLES | Recreational vehicles |
| INDUSTRY_RESIDENT_CONSTRUCTION | Residential construction |
| INDUSTRY_RESORTS_CASINOS | Resorts and casinos |
| INDUSTRY_RESTAURANTS | Restaurants |
| INDUSTRY_SPECIALTY_RETAIL | Specialty retail |
| INDUSTRY_TEXTILE_MANUFACTURING | Textile manufacturing |
| INDUSTRY_TRAVEL_SERVICES | Travel services |
| Consumer defensive |  |
| INDUSTRY_BEVERAGES_BREWERS | Beverages - Brewers |
| INDUSTRY_BEVERAGES_NON_ALCO | Beverages - Non-alcoholic |
| INDUSTRY_BEVERAGES_WINERIES | Beverages - Wineries and distilleries |
| INDUSTRY_CONFECTIONERS | Confectioners |
| INDUSTRY_DISCOUNT_STORES | Discount stores |
| INDUSTRY_EDUCATION_TRAINIG | Education and training services |
| INDUSTRY_FARM_PRODUCTS | Farm products |
| INDUSTRY_FOOD_DISTRIBUTION | Food distribution |
| INDUSTRY_GROCERY_STORES | Grocery stores |
| INDUSTRY_HOUSEHOLD_PRODUCTS | Household and personal products |
| INDUSTRY_PACKAGED_FOODS | Packaged foods |
| INDUSTRY_TOBACCO | Tobacco |
| Energy |  |
| INDUSTRY_OIL_GAS_DRILLING | Oil and gas drilling |
| INDUSTRY_OIL_GAS_EP | Oil and gas extraction and processing |
| INDUSTRY_OIL_GAS_EQUIPMENT | Oil and gas equipment and services |
| INDUSTRY_OIL_GAS_INTEGRATED | Oil and gas integrated |
| INDUSTRY_OIL_GAS_MIDSTREAM | Oil and gas midstream |
| INDUSTRY_OIL_GAS_REFINING | Oil and gas refining and marketing |
| INDUSTRY_THERMAL_COAL | Thermal coal |
| INDUSTRY_URANIUM | Uranium |
| Finance |  |
| INDUSTRY_EXCHANGE_TRADED_FUND | Exchange traded fund |
| INDUSTRY_ASSETS_MANAGEMENT | Assets management |
| INDUSTRY_BANKS_DIVERSIFIED | Banks - Diversified |
| INDUSTRY_BANKS_REGIONAL | Banks - Regional |
| INDUSTRY_CAPITAL_MARKETS | Capital markets |
| INDUSTRY_CLOSE_END_FUND_DEBT | Closed-End fund - Debt |
| INDUSTRY_CLOSE_END_FUND_EQUITY | Closed-end fund - Equity |
| INDUSTRY_CLOSE_END_FUND_FOREIGN | Closed-end fund - Foreign |
| INDUSTRY_CREDIT_SERVICES | Credit services |
| INDUSTRY_FINANCIAL_CONGLOMERATE | Financial conglomerates |
| INDUSTRY_FINANCIAL_DATA_EXCHANGE | Financial data and stock exchange |
| INDUSTRY_INSURANCE_BROKERS | Insurance brokers |
| INDUSTRY_INSURANCE_DIVERSIFIED | Insurance - Diversified |
| INDUSTRY_INSURANCE_LIFE | Insurance - Life |
| INDUSTRY_INSURANCE_PROPERTY | Insurance - Property and casualty |
| INDUSTRY_INSURANCE_REINSURANCE | Insurance - Reinsurance |
| INDUSTRY_INSURANCE_SPECIALTY | Insurance - Specialty |
| INDUSTRY_MORTGAGE_FINANCE | Mortgage finance |
| INDUSTRY_SHELL_COMPANIES | Shell companies |
| Healthcare |  |
| INDUSTRY_BIOTECHNOLOGY | Biotechnology |
| INDUSTRY_DIAGNOSTICS_RESEARCH | Diagnostics and research |
| INDUSTRY_DRUGS_MANUFACTURERS | Drugs manufacturers - general |
| INDUSTRY_DRUGS_MANUFACTURERS_SPEC | Drugs manufacturers - Specialty and generic |
| INDUSTRY_HEALTHCARE_PLANS | Healthcare plans |
| INDUSTRY_HEALTH_INFORMATION | Health information services |
| INDUSTRY_MEDICAL_FACILITIES | Medical care facilities |
| INDUSTRY_MEDICAL_DEVICES | Medical devices |
| INDUSTRY_MEDICAL_DISTRIBUTION | Medical distribution |
| INDUSTRY_MEDICAL_INSTRUMENTS | Medical instruments and supplies |
| INDUSTRY_PHARM_RETAILERS | Pharmaceutical retailers |
| Industrials |  |
| INDUSTRY_AEROSPACE_DEFENSE | Aerospace and defense |
| INDUSTRY_AIRLINES | Airlines |
| INDUSTRY_AIRPORTS_SERVICES | Airports and air services |
| INDUSTRY_BUILDING_PRODUCTS | Building products and equipment |
| INDUSTRY_BUSINESS_EQUIPMENT | Business equipment and supplies |
| INDUSTRY_CONGLOMERATES | Conglomerates |
| INDUSTRY_CONSULTING_SERVICES | Consulting services |
| INDUSTRY_ELECTRICAL_EQUIPMENT | Electrical equipment and parts |
| INDUSTRY_ENGINEERING_CONSTRUCTION | Engineering and construction |
| INDUSTRY_FARM_HEAVY_MACHINERY | Farm and heavy construction machinery |
| INDUSTRY_INDUSTRIAL_DISTRIBUTION | Industrial distribution |
| INDUSTRY_INFRASTRUCTURE_OPERATIONS | Infrastructure operations |
| INDUSTRY_FREIGHT_LOGISTICS | Integrated freight and logistics |
| INDUSTRY_MARINE_SHIPPING | Marine shipping |
| INDUSTRY_METAL_FABRICATION | Metal fabrication |
| INDUSTRY_POLLUTION_CONTROL | Pollution and treatment controls |
| INDUSTRY_RAILROADS | Railroads |
| INDUSTRY_RENTAL_LEASING | Rental and leasing services |
| INDUSTRY_SECURITY_PROTECTION | Security and protection services |
| INDUSTRY_SPEALITY_BUSINESS_SERVICES | Specialty business services |
| INDUSTRY_SPEALITY_MACHINERY | Specialty industrial machinery |
| INDUSTRY_STUFFING_EMPLOYMENT | Stuffing and employment services |
| INDUSTRY_TOOLS_ACCESSORIES | Tools and accessories |
| INDUSTRY_TRUCKING | Trucking |
| INDUSTRY_WASTE_MANAGEMENT | Waste management |
| Real estate |  |
| INDUSTRY_REAL_ESTATE_DEVELOPMENT | Real estate - Development |
| INDUSTRY_REAL_ESTATE_DIVERSIFIED | Real estate - Diversified |
| INDUSTRY_REAL_ESTATE_SERVICES | Real estate services |
| INDUSTRY_REIT_DIVERSIFIED | REIT - Diversified |
| INDUSTRY_REIT_HEALTCARE | REIT - Healthcase facilities |
| INDUSTRY_REIT_HOTEL_MOTEL | REIT - Hotel and motel |
| INDUSTRY_REIT_INDUSTRIAL | REIT - Industrial |
| INDUSTRY_REIT_MORTAGE | REIT - Mortgage |
| INDUSTRY_REIT_OFFICE | REIT - Office |
| INDUSTRY_REIT_RESIDENTAL | REIT - Residential |
| INDUSTRY_REIT_RETAIL | REIT - Retail |
| INDUSTRY_REIT_SPECIALITY | REIT - Specialty |
| Technology |  |
| INDUSTRY_COMMUNICATION_EQUIPMENT | Communication equipment |
| INDUSTRY_COMPUTER_HARDWARE | Computer hardware |
| INDUSTRY_CONSUMER_ELECTRONICS | Consumer electronics |
| INDUSTRY_ELECTRONIC_COMPONENTS | Electronic components |
| INDUSTRY_ELECTRONIC_DISTRIBUTION | Electronics and computer distribution |
| INDUSTRY_IT_SERVICES | Information technology services |
| INDUSTRY_SCIENTIFIC_INSTRUMENTS | Scientific and technical instruments |
| INDUSTRY_SEMICONDUCTOR_EQUIPMENT | Semiconductor equipment and materials |
| INDUSTRY_SEMICONDUCTORS | Semiconductors |
| INDUSTRY_SOFTWARE_APPLICATION | Software - Application |
| INDUSTRY_SOFTWARE_INFRASTRUCTURE | Software - Infrastructure |
| INDUSTRY_SOLAR | Solar |
| Utilities |  |
| INDUSTRY_UTILITIES_DIVERSIFIED | Utilities - Diversified |
| INDUSTRY_UTILITIES_POWERPRODUCERS | Utilities - Independent power producers |
| INDUSTRY_UTILITIES_RENEWABLE | Utilities - Renewable |
| INDUSTRY_UTILITIES_REGULATED_ELECTRIC | Utilities - Regulated electric |
| INDUSTRY_UTILITIES_REGULATED_GAS | Utilities - Regulated gas |
| INDUSTRY_UTILITIES_REGULATED_WATER | Utilities - Regulated water |
| INDUSTRY_UTILITIES_FIRST | Start of the utilities services types enumeration. Corresponds to INDUSTRY_UTILITIES_DIVERSIFIED. |
| INDUSTRY_UTILITIES_LAST | End of the utilities services types enumeration. Corresponds to INDUSTRY_UTILITIES_REGULATED_WATER. |
