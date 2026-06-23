# CTrailingPSAR

CTrailingPSAR is a class with implementation of Trailing Stop algorithm based on the values of Parabolic SAR indicator.

### Description

CTrailingPSAR class implements the Trailing Stop algorithm based on the values of Parabolic SAR indicator of the previous (completed) bar.

### Declaration

```
class CTrailingPSAR: public CExpertTrailing

```

### Title

```
   #include <Expert\Trailing\TrailingParabolicSAR.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertTrailing
               CTrailingPSAR

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| Step | Sets the value of step of Parabolic SAR indicator |
| Maximum | Sets the value of maximum of Parabolic SAR indicator |
| virtual  InitIndicators | Initializes indicators and timeseries |
| Check Trailing Methods |  |
| virtual  CheckTrailingStopLong | Check conditions of trailing stop of a long position |
| virtual  CheckTrailingStopShort | Check conditions of trailing stop of a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  ValidationSettings ,  SetPriceSeries ,  SetOtherSeries |
