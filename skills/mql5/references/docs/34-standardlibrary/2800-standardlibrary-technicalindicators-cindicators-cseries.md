# CSeries

CSeries is a base class for an access to the timeseries data of the Standard Library.

### Description

CSeries class provides the simplified access to all the MQL5 API general functions related to working with the series data for all its descendants (timeseries and indicator classes).

### Declaration

```
   class CSeries: public CArrayObj

```

### Title

```
   #include <Indicators\Series.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
Direct descendants
CIndicator, CiRealVolume, CiSpread, CiTickVolume, CiTime, CPriceSeries

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Name | Gets the name of timeseries or indicator |
| BuffersTotal | Gets the number of buffers of timeseries or indicator |
| Timeframe | Gets the timeframe flag of timeseries or indicator |
| Symbol | Gets the symbol of timeseries or indicator |
| Period | Gets the period of timeseries or indicator |
| RefreshCurrent | Sets/resets the flag of updating the current data |
| Data Access |  |
| virtual  BufferResize | Sets buffer size of timeseries or indicator |
| Data Update |  |
| virtual  Refresh | Update the data of timeseries or indicator |
| PeriodDescription | Transforms  ENUM_TIMEFRAMES  into a string |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Type ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
