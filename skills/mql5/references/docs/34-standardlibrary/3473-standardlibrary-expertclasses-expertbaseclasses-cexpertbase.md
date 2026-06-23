# CExpertBase

CExpertBase is a base class for the [CExpert](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert) class and all auxiliary trading strategy classes.

### Description

CExpertBase provides the data and methods, which are common to all objects of the Expert Advisor.

### Declaration

```
   class CExpertBase : public CObject

```

### Title

```
   #include <Expert\ExpertBase.mqh>

```

```
Inheritance hierarchy
   CObject
       CExpertBase
Direct descendants
CExpert, CExpertMoney, CExpertSignal, CExpertTrailing

```

### Class Methods by Groups

### Public Methods:

| Initialization |  |
| --- | --- |
| virtual  Init | Initializes the object |
| virtual  ValidationSettings | Checks the settings |
| Parameters |  |
| Symbol | Sets the symbol |
| Period | Sets the timeframe |
| Magic | Sets the Expert Advisor ID |
| Indicators and Timeseries |  |
| virtual  SetPriceSeries | Sets pointers to external timeseries (price series) |
| virtual  SetOtherSeries | Sets pointers to external timeseries (non-price series) |
| virtual  InitIndicators | Initializes the indicators and timeseries |
| Access to Protected Data |  |
| InitPhase | Gets the current phase of object initialization |
| TrendType | Sets trend type |
| UsedSeries | Gets bitmask of timeseries used |
| EveryTick | Sets the "Every tick" flag |
| Access to Timeseries |  |
| Open | Gets the element of the Open timeseries by index |
| High | Gets the element of the High timeseries by index |
| Low | Gets the element of the Low timeseries by index |
| Close | Gets the element of the Close timeseries by index |
| Spread | Gets the element of the Spread timeseries by index |
| Time | Gets the element of the Time timeseries by index |
| TickVolume | Gets the element of the TickVolume timeseries by index |
| RealVolume | Gets the element of the RealVolume timeseries by index |

### Protected Methods:

| Initialization of Timeseries |  |
| --- | --- |
| InitOpen | Open timeseries initialization method |
| InitHigh | High timeseries initialization method |
| InitLow | Low timeseries initialization method |
| InitClose | Close timeseries initialization method |
| InitSpread | Spread timeseries initialization method |
| InitTime | Time timeseries initialization method |
| InitTickVolume | TickVolume timeseries initialization method |
| InitRealVolume | RealVolume timeseries initialization method |
| Service Methods |  |
| virtual  PriceLevelUnit | Gets the price level unit |
| virtual  StartIndex | Gets the index of starting bar to analyze |
| virtual  CompareMagic | Compares the Expert Advisor ID with the specified value |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
