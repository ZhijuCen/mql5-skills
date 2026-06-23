# CiATR

# CiATR is a class intended for using the Average True Range technical indicator.

### Description

CiATR class provides the creation, setup, and access to the data of the Average True Range indicator.

### Declaration

```
   class CiATR: public CIndicator

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
                       CiATR

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| MaPeriod | Returns the averaging period |
| Create |  |
| Create | Creates the indicator |
| Data Access |  |
| Main | Returns the buffer data |
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
