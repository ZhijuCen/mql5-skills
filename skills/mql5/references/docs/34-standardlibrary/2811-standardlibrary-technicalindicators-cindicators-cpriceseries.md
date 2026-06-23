# CPriceSeries

CPriceSeries is a base class for access to the price data.

### Description

CSeries class provides the simplified access to MQL5 API general functions for working with price data to all its descendants.

### Declaration

```
   class CPriceSeries: public CSeries

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
                   CPriceSeries
Direct descendants
CiClose, CiHigh, CiLow, CiOpen

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| virtual  BufferResize | Sets size of the series buffer |
| Data Access |  |
| virtual  GetData | Gets the specified series buffer element |
| Data Update |  |
| virtual  Refresh | Updates timeseries data |
| Search for Extreme Values |  |
| virtual  MinIndex | Gets the index of minimal value in the specified range |
| virtual  MinValue | Gets the minimal value in the specified range |
| virtual  MaxIndex | Gets the index of maximal value in the specified range |
| virtual  MaxValue | Gets the maximal value in the specified range |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Type ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
| Methods inherited from class CSeries 
 Name ,  BuffersTotal ,  BufferSize ,  Timeframe ,  Symbol ,  Period ,  PeriodDescription ,  RefreshCurrent |
