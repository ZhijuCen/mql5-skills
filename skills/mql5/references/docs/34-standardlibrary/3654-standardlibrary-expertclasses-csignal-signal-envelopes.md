# Signals of the Indicator Envelopes

This module of signals is based on the market models of the indicator [Envelopes](https://www.metatrader5.com/en/terminal/help/indicators/trend_indicators/envelopes). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | The price is near the lower line of the indicator at the analyzed bar. 
 
 
   
 
 The price crossed the upper line of the indicator at the analyzed bar. |
| For selling | The price is near the upper line of the indicator at the analyzed bar. 
 
 
   
 
 The price crossed the lower line of the indicator at the analyzed bar. |
| No objections to buying | No signals. |
| No objections to selling | No signals. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodMA | Period of calculation of the indicator. |
| Shift | Shift of the indicator along the time axis (in bars). |
| Method | Method of averaging . |
| Applied | A  price series  used for calculation of the indicator. |
| Deviation | Deviation of the envelope borders from the center line (MA) in percentage terms. |
