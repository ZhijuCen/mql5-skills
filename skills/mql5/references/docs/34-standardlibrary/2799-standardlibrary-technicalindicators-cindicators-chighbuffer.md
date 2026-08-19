# CHighBuffer

CHighBuffer is a class for simplified access to high prices of bars in the history.

### Description

CHighBuffer class provides a simplified access to high prices of bars in the history.

### Declaration

```
   class CHighBuffer: public CDoubleBuffer

```

### Title

```
   #include <Indicators\TimeSeries.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayDouble
               CDoubleBuffer
                   CHighBuffer

```

### Class Methods by Groups

| Data Update |  |
| --- | --- |
| virtual  Refresh | Updates the buffer |
| virtual  RefreshCurrent | Updates the current value |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayDouble 
 Delta ,  Type ,  Save ,  Load ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  AddArray ,  Insert ,  InsertArray ,  InsertArray ,  AssignArray ,  AssignArray ,  At , operator,  Minimum ,  Maximum ,  Update ,  Shift ,  Delete ,  DeleteRange ,  CompareArray ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast ,  SearchLinear |
| Methods inherited from class CDoubleBuffer 
 Size ,  At ,  SetSymbolPeriod |
