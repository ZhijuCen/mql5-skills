# int _AppliedTo

The _AppliedTo variable allows finding out the type of data, used for indicator calculation:

| Data type | Meaning | Description of data used for indicator calculation. |
| --- | --- | --- |
| — | 0 | The indicator uses the second  OnCalculate()  call form - the data for calculation are not specified by a certain buffer or data array |
| Close | 1 | Close prices |
| Open | 2 | Open prices |
| High | 3 | High prices |
| Low | 4 | Low prices |
| Median Price (HL/2) | 5 | Median price = (High+Low)/2 |
| Typical Price (HLC/3) | 6 | Typical price = (High+Low+Close)/3 |
| Weighted Price (HLCC/4) | 7 | Weighted price = (Open+High+Low+Close)/4 |
| Previous Indicator's Data | 8 | Data of the indicator, which was launched on the chart before this indicator |
| First Indicator's Data | 9 | Data of the indicator, which was launched first on the chart |
| Indicator handle | 10+ | Data of the indicator, which was passed to the  iCustom()  function using the indicator handle. The  _AppliedTo  value contains the indicator handle |

Example:

```
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,Label1Buffer,INDICATOR_DATA);
// Getting the type of data used for indicator calculation
   Print("_AppliedTo=",_AppliedTo);
   Print(getIndicatorDataDescription(_AppliedTo));
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Description of data used for indicator calculation               |
//+------------------------------------------------------------------+
string getIndicatorDataDescription(int data_id)
  {
   string descr="";
   switch(data_id)
     {
      case(0):descr="It's first type of OnCalculate() - no data buffer";
         break;
      case(1):descr="Indicator calculates on Close price";
         break;
      case(2):descr="Indicator calculates on Open price";
         break;
      case(3):descr="Indicator calculates on High price";
         break;
      case(4):descr="Indicator calculates on Low price";
         break;
      case(5):descr="Indicator calculates on Median Price (HL/2)";
         break;
      case(6):descr="Indicator calculates on Typical Price (HLC/3)";
         break;
      case(7):descr="Indicator calculates on Weighted Price (HLCC/4)";
         break;
      case(8):descr="Indicator calculates Previous Indicator's data";
         break;
      case(9):descr="Indicator calculates on First Indicator's data";
         break;
      default: descr="Indicator calculates on data of indicator with handle="+string(data_id);
         break;
     }
//---
   return descr;
  }

```

See also

[ENUM_APPLIED_PRICE](/en/docs/constants/indicatorconstants/prices#enum_applied_price_enum)
