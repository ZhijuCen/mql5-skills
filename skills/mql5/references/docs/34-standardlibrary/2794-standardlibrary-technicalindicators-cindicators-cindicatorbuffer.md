# CIndicatorBuffer

CIndicatorBuffer is a class for simplified access to the data of the indicator's buffer.

### Description

CIndicatorBuffer class provides the simplified access to the data buffer of technical indicator.

### Declaration

```
   class CIndicatorBuffer: public CDoubleBuffer

```

### Title

```
   #include <Indicators\Indicator.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayDouble
               CDoubleBuffer
                   CIndicatorBuffer

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Offset | Gets/sets offset of the buffer |
| Name | Gets/sets buffer name |
| Data Access |  |
| At | Gets buffer's element |
| Data Update |  |
| Refresh | Updates the buffer |
| RefreshCurrent | Updates only the current value |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayDouble 
 Delta ,  Type ,  Save ,  Load ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  AddArray ,  Insert ,  InsertArray ,  InsertArray ,  AssignArray ,  AssignArray ,  At , operator,  Minimum ,  Maximum ,  Update ,  Shift ,  Delete ,  DeleteRange ,  CompareArray ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast ,  SearchLinear |
| Methods inherited from class CDoubleBuffer 
 Size ,  At ,  SetSymbolPeriod |
