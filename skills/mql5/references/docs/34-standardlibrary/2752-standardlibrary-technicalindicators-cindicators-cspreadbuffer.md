# CSpreadBuffer

CSpreadBuffer is a class for simplified access to spreads of the bars in the history.

### Description

The CSpreadBuffer class provides a simplified access to spreads of the bars in the history.

### Declaration

```
   class CSpreadBuffer: public CArrayInt

```

### Title

```
   #include <Indicators\TimeSeries.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayInt
               CSpreadBuffer

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Size | Sets buffer size |
| Settings |  |
| SetSymbolPeriod | Sets symbol and period |
| Data Access |  |
| At | Gets the buffer element |
| Data Update |  |
| virtual  Refresh | Updates the buffer |
| virtual  RefreshCurrent | Updates the current value |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayInt 
 Type ,  Save ,  Load ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  AddArray ,  Insert ,  InsertArray ,  InsertArray ,  AssignArray ,  AssignArray ,  At , operator, Minimum, Maximum,  Update ,  Shift ,  Delete ,  DeleteRange ,  CompareArray ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast ,  SearchLinear |
