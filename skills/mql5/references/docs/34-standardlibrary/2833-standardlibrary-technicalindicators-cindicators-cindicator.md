# CIndicator

CIndicator is a base class for technical indicator classes of the MQL5 standard library.

### Description

The CIndicator class provides the simplified access for all of its descendants to general MQL5 API technical indicator functions.

### Declaration

```
   class CIndicator: public CSeries

```

### Title

```
   #include <Indicators\Indicator.mqh>

```

```
Inheritance hierarchy
   CObject
       CArray
           CArrayObj
               CSeries
                   CIndicator
Direct descendants
CiAC, CiAD, CiADX, CiADXWilder, CiAlligator, CiAMA, CiAO, CiATR, CiBands, CiBearsPower, CiBullsPower, CiBWMFI, CiCCI, CiChaikin, CiCustom, CiDEMA, CiDeMarker, CiEnvelopes, CiForce, CiFractals, CiFrAMA, CiGator, CiIchimoku, CiMA, CiMACD, CiMFI, CiMomentum, CiOBV, CiOsMA, CiRSI, CiRVI, CiSAR, CiStdDev, CiStochastic, CiTEMA, CiTriX, CiVIDyA, CiVolumes, CiWPR

```

### Class Methods by Groups

| Attributes |  |
| --- | --- |
| Handle | Gets the indicator's handle. |
| Status | Gets the status of the indicator. |
| FullRelease | Sets a flag to release the handle. |
| Creation |  |
| Create | Creates the indicator |
| BufferResize | Sets the new buffer sizes |
| Data Access |  |
| GetData | Copies the data from the indicator buffer |
| Data Update Methods |  |
| Refresh | Updates the indicator data |
| Finding Min/Max Values |  |
| Minimum | Gets the index of minimal value in a specified range. |
| MinValue | Gets the minimal value in a specified range. |
| Maximum | Gets the index of maximal value in a specified range. |
| MaxValue | Gets the maximal value in a specified range. |
| Conversion of Enumerations |  |
| MethodDescription | Converts  ENUM_MA_METHOD  into a string |
| PriceDescription | Converts  ENUM_APPLIED_PRICE  into a string |
| VolumeDescription | Converts  ENUM_APPLIED_VOLUME  into a string |
| Working with chart |  |
| AddToChart | Adds an indicator to the chart |
| DeleteFromChart | Deletes an indicator from the chart |

| Methods inherited from class CObject 
 Prev, Prev, Next, Next,  Compare |
| --- |
| Methods inherited from class CArray 
 Step ,  Step ,  Total ,  Available ,  Max ,  IsSorted ,  SortMode ,  Clear ,  Sort |
| Methods inherited from class CArrayObj 
 FreeMode ,  FreeMode ,  Type ,  Save ,  Load ,  CreateElement ,  Reserve ,  Resize ,  Shutdown ,  Add ,  AddArray ,  Insert ,  InsertArray ,  AssignArray ,  At ,  Update ,  Shift ,  Detach ,  Delete ,  DeleteRange ,  Clear ,  CompareArray ,  InsertSort ,  Search ,  SearchGreat ,  SearchLess ,  SearchGreatOrEqual ,  SearchLessOrEqual ,  SearchFirst ,  SearchLast |
| Methods inherited from class CSeries 
 Name ,  BuffersTotal ,  BufferSize ,  Timeframe ,  Symbol ,  Period ,  PeriodDescription ,  RefreshCurrent |
