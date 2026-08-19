# CTrailingMA

CTrailingMA is a class with implementation of Trailing Stop algorithm based on the values of moving average indicator.

### Description

CTrailingMA class implements Trailing Stop algorithm based on the values of moving average indicator of the previous (completed) bar.

### Declaration

```
class CTrailingMA: public CExpertTrailing

```

### Title

```
   #include <Expert\Trailing\TrailingMA.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertTrailing
               CTrailingMA

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| Period | Sets period of moving average |
| Shift | Sets shift of moving average |
| Method | Sets smoothing method of moving average |
| Applied | Sets applied price of moving average |
| virtual  InitIndicators | Initializes indicators and timeseries |
| virtual  ValidationSettings | Checks the settings |
| Check Trailing Methods |  |
| virtual  CheckTrailingStopLong | Check Trailing Stop conditions of a long position |
| virtual  CheckTrailingStopShort | Check Trailing Stop conditions of a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries |
