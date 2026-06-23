# CSymbolInfo

CSymbolInfo is a class for easy access to the symbol properties.

### Description

CSymbolInfo class provides access to the symbol properties.

### Declaration

```
   class CSymbolInfo : public CObject

```

### Title

```
   #include <Trade\SymbolInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CSymbolInfo

```

### Class methods by groups

| Controlling |  |
| --- | --- |
| Refresh | Refreshes the symbol data |
| RefreshRates | Refreshes the symbol quotes |
| Properties |  |
| Name | Gets/sets symbol name |
| Select | Gets/sets the "Market Watch" symbol flag |
| IsSynchronized | Checks the symbol synchronization with server |
| Volumes |  |
| Volume | Gets the volume of last deal |
| VolumeHigh | Gets the maximal volume for a day |
| VolumeLow | Gets the minimal volume for a day |
| Miscellaneous |  |
| Time | Gets the time of last quote |
| Spread | Gets the amount of spread (in points) |
| SpreadFloat | Gets the flag of floating spread |
| TicksBookDepth | Gets the depth of ticks saving |
| Levels |  |
| StopsLevel | Gets the minimal indent for orders (in points) |
| FreezeLevel | Gets the distance of freezing trade operations (in points) |
| Bid prices |  |
| Bid | Gets the current Bid price |
| BidHigh | Gets the maximal Bid price for a day |
| BidLow | Gets the minimal Bid price for a day |
| Ask prices |  |
| Ask | Gets the current Ask price |
| AskHigh | Gets the maximal Ask price for a day |
| AskLow | Gets the minimal Ask price for a day |
| Prices |  |
| Last | Gets the current Last price |
| LastHigh | Gets the maximal Last price for a day |
| LastLow | Gets the minimal Last price for a day |
| Trade modes |  |
| TradeCalcMode | Gets the mode of contract cost calculation |
| TradeCalcModeDescription | Gets the mode of contract cost calculation as a string |
| TradeMode | Gets the type of order execution |
| TradeModeDescription | Gets the type of order execution as a string |
| TradeExecution | Gets the trade execution mode |
| TradeExecutionDescription | Gets the execution mode as a string |
| Swaps |  |
| SwapMode | Gets the swap calculation mode |
| SwapModeDescription | Gets the swap calculation mode as a string |
| SwapRollover3days | Gets the day of triple swap charge |
| SwapRollover3daysDescription | Gets the day of triple swap charge as a string |
| Margins and flags |  |
| MarginInitial | Gets the value of initial margin |
| MarginMaintenance | Gets the value of maintenance margin |
| MarginLong | Gets the rate of margin charging for long positions |
| MarginShort | Gets the rate of margin charging for short positions |
| MarginLimit | Gets the rate of margin charging for Limit orders |
| MarginStop | Gets the rate of margin charging for Stop orders |
| MarginStopLimit | Gets the rate of margin charging for StopLimit orders |
| TradeTimeFlags | Gets the flags of allowed expiration modes |
| TradeFillFlags | Gets the flags of allowed filling modes |
| Quantization |  |
| Digits | Gets the number of digits after period |
| Point | Gets the value of one point |
| TickValue | Gets the tick value (minimal change of price) |
| TickValueProfit | Gets the calculated tick price for a profitable position |
| TickValueLoss | Gets the calculated tick price for a losing position |
| TickSize | Gets the minimal change of price |
| Contracts sizes |  |
| ContractSize | Gets the amount of trade contract |
| LotsMin | Gets the minimal volume to close a deal |
| LotsMax | Gets the maximal volume to close a deal |
| LotsStep | Gets the minimal step of volume change to close a deal |
| LotsLimit | Gets the maximal allowed volume of opened position and pending orders (direction insensitive) for one symbol |
| Swaps sizes |  |
| SwapLong | Gets the value of long position swap |
| SwapShort | Gets the value of short position swap |
| Text properties |  |
| CurrencyBase | Gets the name of symbol base currency |
| CurrencyProfit | Gets the profit currency name |
| CurrencyMargin | Gets the margin currency name |
| Bank | Gets the name of current quote source |
| Description | Gets the string description of symbol |
| Path | Gets the path in symbols tree |
| Symbol properties |  |
| SessionDeals | Gets the number of deals in the current session |
| SessionBuyOrders | Gets the number of Buy orders at the moment |
| SessionSellOrders | Gets the number of Sell orders at the moment |
| SessionTurnover | Gets the summary of turnover of the current session |
| SessionInterest | Gets the summary of open interest of the current session |
| SessionBuyOrdersVolume | Gets the current volume of Buy orders |
| SessionSellOrdersVolume | Gets the current volume of Sell orders |
| SessionOpen | Gets the open price of the current session |
| SessionClose | Gets the close price of the current session |
| SessionAW | Gets the average weighted price of the current session |
| SessionPriceSettlement | Gets the settlement price of the current session |
| SessionPriceLimitMin | Gets the minimal price of the current session |
| SessionPriceLimitMax | Gets the maximal price of the current session |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of specified integer type property |
| InfoDouble | Gets the value of specified double type property |
| InfoString | Gets the value of specified string type property |
| Service functions |  |
| NormalizePrice | Returns the value of price, normalized using the symbol properties |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
