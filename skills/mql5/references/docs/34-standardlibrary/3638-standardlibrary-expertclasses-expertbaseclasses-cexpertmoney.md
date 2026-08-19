# CExpertMoney

CExpertMoney is a base class for money and risk management algorithms.

### Description

CExpertMoney is a base class for implementation of money and risk management classes.

### Declaration

```
   class CExpertMoney : public CObject

```

### Title

```
   #include <Expert\ExpertMoney.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertMoney
Direct descendants
CMoneyFixedLot, CMoneyFixedMargin, CMoneyFixedRisk, CMoneyNone, CMoneySizeOptimized

```

### Class Methods by Groups

| Access to Protected Data |  |
| --- | --- |
| Percent | Sets the value of "Risk percent" parameter |
| Initialization |  |
| virtual  ValidationSettings | Checks the settings |
| Checking Trading Conditions |  |
| virtual  CheckOpenLong | Gets the volume for a long position |
| virtual  CheckOpenShort | Gets the volume for a short position |
| virtual  CheckReverse | Gets the volume for a reverse of the position |
| virtual  CheckClose | Checks conditions to close an opened position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |
