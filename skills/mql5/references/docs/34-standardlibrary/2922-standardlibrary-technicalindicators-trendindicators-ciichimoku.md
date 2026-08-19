# CiIchimoku

CiIchimoku is a class intended for using the Ichimoku Kinko Hyo technical indicator.

### Description

CiIchimoku class provides the creation, setup, and access to the data of the Ichimoku Kinko Hyo indicator.

### Declaration

```
   class CiIchimoku: public CIndicator

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
                       CiIchimoku

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| TenkanSenPeriod | Returns the TenkanSen period |
| KijunSenPeriod | Returns the KijunSen period |
| SenkouSpanBPeriod | Returns the SenkouSpanB period |
| Create |  |
| Create | Creates the indicator |
| Data Access |  |
| TenkanSen | Returns the buffer element of the TenkanSen line |
| KijunSen | Returns the buffer element of the KijunSen line |
| SenkouSpanA | Returns the buffer element of the SenkouSpanA line |
| SenkouSpanB | Returns the buffer element of the SenkouSpanB line |
| ChinkouSpan | Returns the buffer element of the ChikouSpan line |
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
