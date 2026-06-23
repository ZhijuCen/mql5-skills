# CiAO

CiAO is a class intended for using the Awesome Oscillator technical indicator.

### Description

CiAO class provides the creation, setup, and access to the data of the Awesome Oscillator indicator.

### Declaration

```
   class CiAO: public CIndicator

```

### Title

```
   #include <Indicators\BillWilliams.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
                   CIndicator
                       CiAO

```

### Class Methods by Groups

| Create |  |
| --- | --- |
| Create | Creates the indicator |
| Data Access |  |
| Main | Returns the buffer element |
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
