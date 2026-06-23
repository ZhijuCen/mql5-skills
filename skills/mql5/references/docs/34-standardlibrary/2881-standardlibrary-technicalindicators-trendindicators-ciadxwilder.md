# CiADXWilder

CiADXWilder is a class intended for using the technical indicator Average Directional Index by Welles Wilder.

### Description

CiADXWilder class provides the creation, configuration, and access to the data of the Average Directional Index by Welles Wilder.

### Declaration

```
   class CiADXWilder: public CIndicator

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
                       CiADXWilder

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| MaPeriod | Returns the averaging period |
| Create |  |
| Create | Creates the indicator |
| Data Access |  |
| Main | Returns the buffer data of the main line |
| Plus | Returns the buffer data of the +DI line |
| Minus | Returns the buffer data of the -DI line |
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
