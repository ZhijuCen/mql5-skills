# CiTickVolume

CiTickVolume is a class designed for access to tick volumes of the bars in the history.

### Description

CiTickVolume class provides an access to tick volumes of the bars in the history.

### Declaration

```
   class CiTickVolume: public CSeries

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
                   CiTickVolume

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates a timeseries |
| BufferResize | Sets buffer sizes |
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
