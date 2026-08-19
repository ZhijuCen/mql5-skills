# CiGator

CiGator is a class intended for using the Gator Oscillator technical indicator.

### Description

CiGator class provides the creation, setup, and access to the data of the Gator Oscillator indicator.

### Declaration

```
   class CiGator: public CIndicator

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
                       CiGator

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| JawPeriod | Returns the averaging period for the Jaws line |
| JawShift | Returns the horizontal shift of the Jaws line |
| TeethPeriod | Returns the averaging period for the Teeth line |
| TeethShift | Returns the horizontal shift of the Teeth line |
| LipsPeriod | Returns the averaging period for the Lips line |
| LipsShift | Returns the horizontal shift of the Lips line |
| MaMethod | Returns the averaging method |
| Applied | Returns the price type or handle to apply |
| Create Methods |  |
| Create | Creates the indicator |
| Data Access Methods |  |
| Upper | Returns the data of the upper buffer |
| Lower | Returns the data of the lower buffer |
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
