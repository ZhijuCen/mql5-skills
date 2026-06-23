# Signals of the Oscillator Bears Power

This module of signals is based on the market models of the oscillator [Bears Power](https://www.metatrader5.com/en/terminal/help/indicators/oscillators/bears). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | Reverse  — the oscillator turned upwards and its value at the analyzed bar is below 0. 
 
 
   
 
 Divergence  — the first analyzed bottom of the oscillator is higher than the previous one, and the corresponding price bottom is lower than the previous one. In addition, the oscillator must not rise above the zero level. |
| For selling | No signals for selling. |
| No objections to buying | Value of the oscillator is less than 0. |
| No objections to selling | No signals. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodBears | Period of calculation of the oscillator. |
