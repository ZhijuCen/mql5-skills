# CMoneySizeOptimized

CMoneySizeOptimized is a class with implementation of money and risk management algorithm depending on results of the previous deals.

### Description

CMoneySizeOptimized implements the market entry algorithm with the lot size depending on results of the previous deals.

### Declaration

```
   class CMoneySizeOptimized: public CExpertMoney

```

### Title

```
   #include <Expert\Money\MoneySizeOptimized.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertMoney
               CMoneySizeOptimized

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| DecreaseFactor | Sets the parameter value |
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
