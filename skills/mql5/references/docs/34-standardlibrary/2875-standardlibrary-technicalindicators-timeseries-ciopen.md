# CiOpen

CiOpen is a class designed for access to open prices of the bars in the history.

### Description

CiOpen class provides an access to open prices of the bars in the history.

### Declaration

```
   class CiOpen: public CPriceSeries

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
                       CiOpen

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates a series |
| Data Access |  |
| GetData | Gets the series data |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Type ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
| Methods inherited from class CSeries 
 Name ,  BuffersTotal ,  BufferSize ,  Timeframe ,  Symbol ,  Period ,  PeriodDescription ,  RefreshCurrent |
| Methods inherited from class CPriceSeries 
 BufferResize ,  MinIndex ,  MinValue ,  MaxIndex ,  MaxValue ,  GetData ,  Refresh |
