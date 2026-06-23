# CTrailingFixedPips

CTrailingFixedPips is a class with implementation of Trailing Stop algorithm based on fixed points trailing.

CTrailingFixedPips class implements the following algorithm of trailing open positions: If Stop Loss level is equal to zero, Stop Loss order modification condition is considered unfulfilled, therefore there is no suggestion to change a position's Stop Loss. Otherwise, the check of whether the price has moved in favorable direction is performed.

If a position has a Stop Loss order, it checks the minimal allowed Stop Loss distance to the current price. If the position has no Stop Loss level, the distance between the current and open prices is checked. If the distance exceeds Stop Loss level, the system suggests to set a new Stop Loss price.

If Stop Loss modification condition is fulfilled and Take Profit is not equal to zero, the system suggests setting a new Take Profit price.

If Expert Advisor class has been [initialized](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertinit) with the flag every_tick=false, it will perform all operations (trading, trailing, etc) only at the new bar on a working symbol and timeframe. In this case, setting Take Profit order allows you to close position when the price moves in the position direction before a new bar appears.

### Description

CTrailingFixedPips implements the Trailing Stop algorithm at a specified "distance" from the current price (in points).

### Declaration

```
class CTrailingFixedPips: public CExpertTrailing

```

### Title

```
   #include <Expert\Trailing\CTrailingFixedPips.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertTrailing
               CTrailingFixedPips

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| StopLevel | Sets the value of Stop Loss level |
| ProfitLevel | Sets the value of Take Profit level |
| virtual  ValidationSettings | Checks the settings |
| Check Trailing Methods |  |
| virtual  CheckTrailingStopLong | Check Trailing Stop conditions of a long position |
| virtual  CheckTrailingStopShort | Check Trailing Stop conditions of a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |
