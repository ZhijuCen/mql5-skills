# CMoneyFixedRisk

CMoneyFixedRisk is a class with implementation of money management algorithm with fixed predefined risk.

### Description

CMoneyFixedRisk class implements the money management algorithm with fixed predefined risk.

### Declaration

```
   class CMoneyFixedRisk: public CExpertMoney

```

### Title

```
   #include <Expert\Money\MoneyFixedRisk.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertMoney
               CMoneyFixedRisk

```

### Class Methods by Groups

| Money and Risk Management Methods |  |
| --- | --- |
| virtual  CheckOpenLong | Gets trade volume for a long position |
| virtual  CheckOpenShort | Gets trade volume for a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |
| Methods inherited from class CExpertMoney 
 Percent ,  ValidationSettings ,  CheckReverse |

###
