# Signals of the Oscillator Bulls Power

This module of signals is based on the market models of the oscillator [Bulls Power](https://www.metatrader5.com/en/terminal/help/indicators/oscillators/bulls). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | No signals for buying. |
| For selling | Reverse  — the oscillator turned downwards and its value at the analyzed bar is above 0. 
 
 
   
 
 Divergence  — the first analyzed peak of the oscillator is lower than the previous one, and the corresponding price peak is higher than the previous peak. In addition, the oscillator must not fall below the zero level. |
| No objections to buying | No signals. |
| No objections to selling | Value of the oscillator is greater than 0. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodBulls | Period of calculation of the oscillator. |
