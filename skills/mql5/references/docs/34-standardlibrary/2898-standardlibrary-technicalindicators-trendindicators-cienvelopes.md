# CiEnvelopes

CiEnvelopes is a class intended for using the Envelopes technical indicator.

### Description

CiEnvelopes class provides the creation, configuration, and access to the data of the Envelopes indicator.

### Declaration

```
   class CiEnvelopes: public CIndicator

```

### Title

```
   #include <Indicators\Trend.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
                   CIndicator
                       CiEnvelopes

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| MaPeriod | Returns the averaging period |
| MaShift | Returns the horizontal shift |
| MaMethod | Returns the averaging method |
| Deviation | Returns the deviation |
| Applied | Returns the price type or handle to apply |
| Create |  |
| Create | Creates the indicator |
| Data Access |  |
| Upper | Returns the buffer data of the upper line |
| Lower | Returns the buffer data of the lower line |
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
