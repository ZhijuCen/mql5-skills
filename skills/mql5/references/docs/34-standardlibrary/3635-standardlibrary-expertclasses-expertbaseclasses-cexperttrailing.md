# CExpertTrailing

CExpertTrailing is a base class for trailing algorithms, it does nothing but provides the interfaces.

How to use it:

1. Prepare an algorithm for trailing;  

2. Create your own trailing class inherited from CExpertTrailing class;  

3. Override the virtual methods in your class with your own algorithms.

You can find an examples of trailing classes in the Expert\Trailing\ folder.

### Description

CExpertTrailing is a base class for implementation of trailing stop algorithms.

### Declaration

```
   class CExpertTrailing : public CExpertBase

```

### Title

```
   #include <Expert\ExpertTrailing.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertTrailing
Direct descendants
CTrailingFixedPips, CTrailingMA, CTrailingNone, CTrailingPSAR

```

### Class Methods by Groups

| Checking of Trailing Stop Conditions |  |
| --- | --- |
| virtual  CheckTrailingStopLong | Checks conditions to modify parameters of the long position |
| virtual  CheckTrailingStopShort | Checks conditions to modify parameters of the short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  ValidationSettings ,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |

###
