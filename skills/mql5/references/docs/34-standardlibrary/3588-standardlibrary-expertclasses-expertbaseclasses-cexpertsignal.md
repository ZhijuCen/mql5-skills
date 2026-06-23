# CExpertSignal

CExpertSignal is a base class for trading signals, it does nothing (except [CheckReverseLong()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal/cexpertsignalcheckreverselong) and [CheckReverseShort()](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal/cexpertsignalcheckreverseshort) methods) but provides the interfaces.

How to use it:

1. Prepare an algorithm for trading signals;  

2. Create your own trading signal class, inherited from CExpertSignal class;  

3. Override the virtual methods in your class with your own algorithms.

You can find an examples of trading signal classes in the Expert\Signal\ folder.

### Description

CExpertSignal is a base class for implementation of trading signal algorithms.

### Declaration

```
   class CExpertSignal : public CExpertBase

```

### Title

```
   #include <Expert\ExpertSignal.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
           CExpertSignal
Direct descendants
CSignalAC, CSignalAMA, CSignalAO, CSignalBearsPower, CSignalBullsPower, CSignalCCI, CSignalDeM, CSignalDEMA, CSignalEnvelopes, CSignalFrAMA, CSignalRSI, CSignalRVI, CSignalSAR, CSignalStoch, CSignalTEMA, CSignalTriX, CSignalWPR

```

### Class Methods by Groups

| Initialization |  |
| --- | --- |
| virtual  InitIndicators | Initializes indicators and timeseries |
| virtual  ValidationSettings | Checks the object settings |
| virtual  AddFilter | Adds a filter to combined signal |
| Access to Protected Data |  |
| BasePrice | Sets base price level |
| UsedSeries | Gets the flags of timeseries used |
| Parameters Setting |  |
| Weight | Sets the value of "Weight" parameter |
| PatternsUsage | Sets the value of "PatternsUsage" parameter |
| General | Sets the value of "General" parameter |
| Ignore | Sets the value of "Ignore" parameter |
| Invert | Sets the value of "Invert" parameter |
| ThresholdOpen | Sets the value of "ThresholdOpen" parameter |
| ThresholdClose | Sets the value of "ThresholdClose" parameter |
| PriceLevel | Sets the value of "PriceLevel" parameter |
| StopLevel | Sets the value of "StopLevel" parameter |
| TakeLevel | Sets the value of "TakeLevel" parameter |
| Expiration | Sets the value of "Expiration" parameter |
| Magic | Sets the value of "Magic" parameter |
| Checking Trading Conditions |  |
| virtual  CheckOpenLong | Checks conditions to open long position |
| virtual  CheckCloseLong | Checks conditions to close long position |
| virtual  CheckOpenShort | Checks conditions to open short position |
| virtual  CheckCloseShort | Checks conditions to close short position |
| virtual  CheckReverseLong | Checks conditions of long position reversal |
| virtual  CheckReverseShort | Checks conditions of short position reversal |
| Trade Parameters Setting |  |
| virtual  OpenLongParams | Sets parameters for long position opening |
| virtual  OpenShortParams | Sets parameters for short position opening |
| virtual  CloseLongParams | Sets parameters for long position closing |
| virtual  CloseShortParams | Sets parameters for short position closing |
| Checking of Order Trailing Conditions |  |
| virtual  CheckTrailingOrderLong | Checks conditions to modify parameters of Buy Pending order |
| virtual  CheckTrailingOrderShort | Checks conditions to modify parameters of Sell Pending order |
| Methods to Check Formation of Market Orders |  |
| virtual  LongCondition | Gets the result of checking buy conditions |
| virtual  ShortCondition | Gets the result of checking sell conditions |
| virtual  Direction | Gets the "weighted" direction of price |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Save ,  Load ,  Type ,  Compare |
| --- |
| Methods inherited from class CExpertBase 
 InitPhase ,  TrendType ,  UsedSeries ,  EveryTick ,  Open ,  High ,  Low ,  Close ,  Spread ,  Time ,  TickVolume ,  RealVolume ,  Init ,  Symbol ,  Period ,  Magic , SetMarginMode,  SetPriceSeries ,  SetOtherSeries |
