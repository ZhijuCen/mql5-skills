# Signals of the Oscillator Triple Exponential Average

This module of signals is based on the market models of the oscillator [Triple Exponential Average](https://www.metatrader5.com/en/terminal/help/indicators/oscillators/tea). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | Reverse  — the oscillator turned upwards (the oscillator rises at the analyzed bar and falls at the previous one). 
 
 
   
 
 Crossing the zero level  — the main line is above the zero level at the analyzed bar and below the zero level at the previous one. 
 
 
   
 
 Divergence  — the first analyzed bottom of the oscillator is higher than the previous one, and the corresponding price bottom is lower than the previous one. |
| For selling | Reverse  — the oscillator turned downwards (the oscillator falls at the analyzed bar and rises at the previous one). 
 
 
   
 
 Crossing the zero level  — the main line is below the zero level at the analyzed bar and above the zero level at the previous one. 
 
 
   
 
 Divergence  — the first analyzed peak of the oscillator is lower than the previous one, and the corresponding price peak is higher than the previous peak. |
| No objections to buying | Value of the oscillator grows at the analyzed bar. |
| No objections to selling | Value of the oscillator falls at the analyzed bar. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodTriX | Period of calculation of the oscillator. |
| Applied | A  price series  used for calculation of the oscillator. |
