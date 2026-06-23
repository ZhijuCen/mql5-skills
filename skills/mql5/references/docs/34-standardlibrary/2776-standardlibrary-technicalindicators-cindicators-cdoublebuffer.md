# CDoubleBuffer

CDoubleBuffer is a base class for simplified access to data buffers of double type.

### Description

The CDoubleBuffer class provides a simplified access to the data of the buffer of double type.

### Declaration

```
   class CDoubleBuffer: public CArrayDouble

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
Direct descendants
CCloseBuffer, CHighBuffer, CIndicatorBuffer, CLowBuffer, COpenBuffer

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
| Methods inherited from class CArrayDouble 
 Delta ,  Type ,  Save ,  Load ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  AddArray ,  Insert ,  InsertArray ,  InsertArray ,  AssignArray ,  AssignArray ,  At , operator,  Minimum ,  Maximum ,  Update ,  Shift ,  Delete ,  DeleteRange ,  CompareArray ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast ,  SearchLinear |
