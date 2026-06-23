# Price Constants

Calculations of technical indicators require price values and/or values of volumes, on which calculations will be performed. There are 7 predefined identifiers from the ENUM_APPLIED_PRICE enumeration, used to specify the desired price base for calculations.

ENUM_APPLIED_PRICE

| ID | Description |
| --- | --- |
| PRICE_CLOSE | Close price |
| PRICE_OPEN | Open price |
| PRICE_HIGH | The maximum price for the period |
| PRICE_LOW | The minimum price for the period |
| PRICE_MEDIAN | Median price, (high + low)/2 |
| PRICE_TYPICAL | Typical price, (high + low + close)/3 |
| PRICE_WEIGHTED | Average price, (high + low + close + close)/4 |

If the volume is used in calculations, it's necessary to specify one of the two values from the ENUM_APPLIED_VOLUME enumeration.

ENUM_APPLIED_VOLUME

| ID | Description |
| --- | --- |
| VOLUME_TICK | Tick volume |
| VOLUME_REAL | Trade volume |

The [iStochastic()](/en/docs/indicators/istochastic) technical Indicator can be calculated in two ways using:

- either only Close prices;
- or High and Low prices.

To select a necessary variant for calculation, specify one of the values of the ENUM_STO_PRICE enumeration.

ENUM_STO_PRICE

| ID | Description |
| --- | --- |
| STO_LOWHIGH | Calculation is based on Low/High prices |
| STO_CLOSECLOSE | Calculation is based on Close/Close prices |

If a technical indicator uses for calculations price data, type of which is set by ENUM_APPLIED_PRICE, then handle of any indicator (built in the terminal or written by a user) can be used as the input price series. In this case, values of the zero buffer of the indicator will be used for calculations. This makes it easy to build values of one indicator using values of another indicator. The handle of a custom indicator is created by calling the [iCustom()](/en/docs/indicators/icustom) function.

Example:

```
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   2
//--- input parameters
input int      RSIperiod=14;         // Period for calculating the RSI
input int      Smooth=8;             // Smoothing period RSI
input ENUM_MA_METHOD meth=MODE_SMMA; // Method of smoothing
//---- plot RSI
#property indicator_label1  "RSI"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//---- plot RSI_Smoothed
#property indicator_label2  "RSI_Smoothed"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrNavy
#property indicator_style2  STYLE_SOLID
#property indicator_width2  1
//--- indicator buffers
double         RSIBuffer[];          // Here we store the values of RSI
double         RSI_SmoothedBuffer[]; // Here will be smoothed values of RSI
int            RSIhandle;            // Handle to the RSI indicator
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,RSIBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,RSI_SmoothedBuffer,INDICATOR_DATA);
   IndicatorSetString(INDICATOR_SHORTNAME,"iRSI");
   IndicatorSetInteger(INDICATOR_DIGITS,2);
//--- 
   RSIhandle=iRSI(NULL,0,RSIperiod,PRICE_CLOSE);
//---
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                 const int prev_calculated,
                 const int begin,
                 const double &price[]
                 )
 
  {
//---  Reset the value of the last error
   ResetLastError();
//--- Get RSI indicator data in an array RSIBuffer []
   int copied=CopyBuffer(RSIhandle,0,0,rates_total,RSIBuffer);
   if(copied<=0)
     {
      Print("Unable to copy the values of the indicator RSI. Error = ",
            GetLastError(),",  copied =",copied);
      return(0);
     }
//--- Create the indicator of average values using values of RSI
   int RSI_MA_handle=iMA(NULL,0,Smooth,0,meth,RSIhandle);
   copied=CopyBuffer(RSI_MA_handle,0,0,rates_total,RSI_SmoothedBuffer);
   if(copied<=0)
     {
      Print("Unable to copy the smoothed indicator of RSI. Error = ",
            GetLastError(),",  copied =",copied);
      return(0);
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```
