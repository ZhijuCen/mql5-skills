# CExpert

CExpert is a base class for trading strategies.

It already has some elementary trading "skills". It has built-in algorithms for working with time series and indicators and a set of virtual methods for trading strategy.

How to use it:

1. Prepare an algorithm of the strategy;  

2. Create your own class, inherited from CExpert class;  

3. Override the virtual methods in your class with your own algorithms.

### Description

The CExpert class is a set of virtual methods for implementation of trading strategies.

### Note

A position is recognized as belonging to an Expert Advisor and managed by it based on the pair of properties m_symbol and m_magic. In the "hedging" mode, multiple positions can be opened for the same symbol, therefore the m_magic value is important.

### Declaration

```
   class CExpert : public CExpertBase

```

### Title

```
   #include <Expert\Expert.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpert

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| Init | Class instance initialization method |
| virtual  InitSignal | Initializes Trading Signal object |
| virtual  InitTrailing | Initializes Trailing Stop object |
| virtual  InitMoney | Initializes Money Management object |
| virtual  InitTrade | Initializes Trade object |
| virtual  ValidationSettings | Checks the settings |
| virtual  InitIndicators | Initializes indicators and timeseries |
| virtual  InitParameters | Expert Advisor parameters initialization method |
| virtual  Deinit | Class instance deinitialization method |
| virtual  DeinitSignal | Deinitializes Trading Signal object |
| virtual  DeinitTrailing | Deinitializes Trailing Stop object |
| virtual  DeinitMoney | Deinitializes Money Management object |
| virtual  DeinitTrade | Deinitializes Trade object |
| virtual  DeinitIndicators | Deinitializes indicators and timeseries |
| Parameters |  |
| Magic | Sets the Expert Advisor ID |
| MaxOrders | Gets/sets the maximum amount of allowed orders |
| OnTickProcess | Sets a flag to proceed the "OnTick" event |
| OnTradeProcess | Sets a flag to proceed the "OnTrade" event |
| OnTimerProcess | Sets a flag to proceed the "OnTimer" event |
| OnChartEventProcess | Sets a flag to proceed the "OnChartEvent" event |
| OnBookEventProcess | Sets a flag to proceed the "OnBookEvent" event |
| Event Processing Methods |  |
| OnTick | OnTick event handler |
| OnTrade | OnTrade event handler |
| OnTimer | OnTimer event handler |
| OnChartEvent | OnChartEvent event handler |
| OnBookEvent | OnBookEvent event handler |
| Update Methods |  |
| Refresh | Updates all data |
| Processing |  |
| Processing | Main processing algorithm |
| Market Entry Methods |  |
| CheckOpen | Checks position opening conditions |
| CheckOpenLong | Checks conditions to open long position |
| CheckOpenShort | Checks conditions to open short position |
| OpenLong | Opens a long position |
| OpenShort | Opens a short position |
| Market Exit Methods |  |
| CheckClose | Checks conditions to close current position |
| CheckCloseLong | Checks conditions to close long position |
| CheckCloseShort | Checks conditions to close short position |
| CloseAll | Closes the opened position and deletes all orders |
| Close | Closes the opened position |
| CloseLong | Closes the long position |
| CloseShort | Closes the short position |
| Position Reverse Methods |  |
| CheckReverse | Checks conditions to reverse opened position |
| CheckReverseLong | Checks conditions to reverse long position |
| CheckReverseShort | Checks conditions to reverse short position |
| ReverseLong | Performs reverse operation of long position |
| ReverseShort | Performs reverse operation of short position |
| Position/Order Trailing Methods |  |
| CheckTrailingStop | Checks conditions to modify position parameters |
| CheckTrailingStopLong | Checks Trailing Stop conditions of long position |
| CheckTrailingStopShort | Checks Trailing Stop conditions of short position |
| TrailingStopLong | Performs Trailing Stop for long position |
| TrailingStopShort | Performs Trailing Stop for short position |
| CheckTrailingOrderLong | Checks Trailing Stop conditions of Buy Limit/Stop order |
| CheckTrailingOrderShort | Checks Trailing Stop conditions of Sell Limit/Stop order |
| TrailingOrderLong | Performs Trailing Stop for Buy Limit/Stop order |
| TrailingOrderShort | Performs Trailing Stop for Sell Limit/Stop order |
| Order Delete Methods |  |
| CheckDeleteOrderLong | Checks conditions to delete Buy order |
| CheckDeleteOrderShort | Checks conditions to delete Sell order |
| DeleteOrders | Deletes all orders |
| DeleteOrder | Deletes Stop/Limit order |
| DeleteOrderLong | Deletes Buy Limit/Stop order |
| DeleteOrderShort | Deletes Sell Limit/Stop order |
| Trade Volume Methods |  |
| LotOpenLong | Gets trade volume for buy operation |
| LotOpenShort | Gets trade volume for sell operation |
| LotReverse | Gets trade volume for position reverse operation |
| Trade History Methods |  |
| PrepareHistoryDate | Sets starting date for trade history tracking |
| HistoryPoint | Creates a checkpoint of trade history (saves number of positions, orders, deals and historical orders) |
| CheckTradeState | Compares the current state with the saved one and calls the corresponding event handler |
| Event flags |  |
| WaitEvent | Sets the trading event waiting flag |
| NoWaitEvent | Resets the trading event waiting flag |
| Trade Event Processing Methods |  |
| TradeEventPositionStopTake | Event handler of the "Position Stop Loss/Take Profit triggered" event |
| TradeEventOrderTriggered | Event handler of the "Pending Order Triggered" event |
| TradeEventPositionOpened | Event handler of the "Position Opened" event |
| TradeEventPositionVolumeChanged | Event handler of the "Position Volume Changed" event |
| TradeEventPositionModified | Event handler of the "Position Modified" event |
| TradeEventPositionClosed | Event handler of the "Position Closed" event |
| TradeEventOrderPlaced | Event handler of the "Pending Order Placed" event |
| TradeEventOrderModified | Event handler of the "Pending Order Modified" event |
| TradeEventOrderDeleted | Event handler of the "Pending Order Deleted" event |
| TradeEventNotIdentified | Event handler of the non-identified event |
| Service methods |  |
| TimeframeAdd | Adds a timeframe to track |
| TimeframesFlags | Forms timeframe flags |
| SelectPosition | Selects a position to work with |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries |
