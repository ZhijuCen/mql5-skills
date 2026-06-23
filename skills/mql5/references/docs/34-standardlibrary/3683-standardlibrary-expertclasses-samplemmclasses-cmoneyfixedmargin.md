# CMoneyFixedMargin

CMoneyFixedMargin is the class designed to implement money management algorithm based on trading with predefined fixed margin.

### Description

CMoneyFixedMargin implements money management algorithm based on trading with predefined fixed margin.

### Declaration

```
   class CMoneyFixedMargin: public CExpertMoney

```

### Title

```
   #include <Expert\Money\MoneyFixedMargin.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertMoney
               CMoneyFixedMargin

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
 Percent ,  ValidationSettings ,  CheckReverse ,  CheckClose |

###
