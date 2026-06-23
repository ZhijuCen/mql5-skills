# CiSpread

CiSpread is a class designed for access to spreads of the bars in the history.

### Description

CiSpread class provides an access to spread historical data.

### Declaration

```
   class CiSpread: public CSeries

```

### Title

```
   #include <Indicators\TimeSeries.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
                   CiSpread

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates a timeseries |
| BufferResize | Sets a series buffer size |
| Data Access |  |
| GetData | Gets the series data |
| Data Update |  |
| Refresh | Updates the series data |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Type ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
| Methods inherited from class CSeries 
 Name ,  BuffersTotal ,  BufferSize ,  Timeframe ,  Symbol ,  Period ,  PeriodDescription ,  RefreshCurrent |
