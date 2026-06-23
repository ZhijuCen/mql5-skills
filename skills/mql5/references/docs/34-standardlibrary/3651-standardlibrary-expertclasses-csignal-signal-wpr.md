# Signals of the Oscillator Williams Percent Range

This module of signals is based on the market models of the oscillator [Williams Percent Range](https://www.metatrader5.com/en/terminal/help/indicators/oscillators/wpr). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | Reverse behind the oversold level  — the oscillator turned upwards and its value at the analyzed bar is behind the oversold level (default value is -80). 
 
 
   
 
 Divergence  — the first analyzed bottom of the oscillator is higher than the previous one, and the corresponding price bottom is lower than the previous one. |
| For selling | Reverse behind the overbought level  — the oscillator turned downwards and its value at the analyzed bar is behind the overbought level (default value is -20). 
 
 
   
 
 Divergence  — the first analyzed peak of the oscillator is lower than the previous one, and the corresponding price peak is higher than the previous peak. |
| No objections to buying | Value of the oscillator grows at the analyzed bar. |
| No objections to selling | Value of the oscillator falls at the analyzed bar. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

Remember that the oscillator Williams Percent Range has a reversed scale. Its maximum value is -100, and minimum is 0.

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodWPR | Period of calculation of the oscillator. |
