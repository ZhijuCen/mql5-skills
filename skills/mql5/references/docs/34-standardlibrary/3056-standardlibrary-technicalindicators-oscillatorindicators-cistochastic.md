# CiStochastic

CiStochastic is a class intended for using the Stochastic Oscillator technical indicator.

### Description

CiStochastic class provides the creation, setup, and access to the data of the Stochastic Oscillator indicator.

### Declaration

```
   class CiStochastic: public CIndicator

```

### Title

```
   #include <Indicators\Oscilators.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
                   CIndicator
                       CiStochastic

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Kperiod | Returns the averaging period for the %K line |
| Dperiod | Returns the averaging period for the %D line |
| Slowing | Returns the slowing period |
| MaMethod | Returns the averaging method |
| PriceField | Price type (Low/High or Close/Close) to apply |
| Create |  |
| Create | Creates the indicator |
| Data Access |  |
| Main | Returns the buffer data of the main line |
| Signal | Returns the buffer data of the signal line |
| Input/output |  |
| virtual  Type | Virtual identification method |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
| Methods inherited from class CSeries 
 Name ,  BuffersTotal ,  BufferSize ,  Timeframe ,  Symbol ,  Period ,  PeriodDescription ,  RefreshCurrent |
| Methods inherited from class CIndicator 
 Handle ,  Status ,  FullRelease , Redrawer,  Create ,  BufferResize ,  BarsCalculated ,  GetData ,  GetData ,  GetData ,  GetData ,  Minimum ,  MinValue ,  Maximum ,  MaxValue ,  Refresh ,  AddToChart ,  DeleteFromChart ,  MethodDescription ,  PriceDescription ,  VolumeDescription |
