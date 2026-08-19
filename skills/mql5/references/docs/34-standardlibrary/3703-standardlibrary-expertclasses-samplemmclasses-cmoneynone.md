# CMoneyNone

CMoneyNone is a class with implementation of the "absence" of money and risk management.

### Description

CMoneyNone class implements trading with minimal allowed lot.

### Declaration

```
   class CMoneyNone: public CExpertMoney

```

### Title

```
   #include <Expert\Money\MoneyNone.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertMoney
               CMoneyNone

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| virtual  ValidationSettings | Checks the settings |
| Money and Risk Management Methods |  |
| virtual  CheckOpenLong | Gets trade volume for a long position |
| virtual  CheckOpenShort | Gets trade volume for a short position |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries ,  InitIndicators |
| Methods inherited from class CExpertMoney 
 Percent ,  CheckReverse ,  CheckClose |

###
