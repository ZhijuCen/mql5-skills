# CiMACD

CiMACD is a class intended for using the Moving Averages Convergence-Divergence technical indicator.

### Description

CiMACD class provides the creation, setup, and access to the data of the Moving Averages Convergence-Divergence indicator.

### Declaration

```
   class CiMACD: public CIndicator

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
                       CiMACD

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| FastEmaPeriod | Returns the averaging period of the fast EMA |
| SlowEmaPeriod | Returns the averaging period of the slow EMA |
| SignalPeriod | Returns the averaging period of the signal line |
| Applied | Returns the price type or handle to apply |
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
