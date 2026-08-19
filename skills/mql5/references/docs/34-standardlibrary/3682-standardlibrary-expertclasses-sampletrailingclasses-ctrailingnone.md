# CTrailingNone

CTrailingNone is a stub class. This class should be used at initialization of trailing object in CExpert class if your strategy does not use Trailing Stop.

### Description

CTrailingNone class does not implement any Trailing Stop algorithm. The methods of checking Trailing Stop conditions always return false.

### Declaration

```
class CTrailingNone: public CExpertTrailing

```

### Title

```
   #include <Expert\Trailing\TrailingNone.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertTrailing
               CTrailingNone

```

### Class Methods by Groups

| Check Trailing Methods |  |
| --- | --- |
| virtual  CheckTrailingStopLong | A stub method for checking Trailing Stop conditions of a long position |
| virtual  CheckTrailingStopShort | A stub method for checking Trailing Stop conditions of a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  ValidationSettings ,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |
| Methods inherited from class CExpertTrailing 
 CheckTrailingStopLong ,  CheckTrailingStopShort |
