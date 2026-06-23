# Signals of the Indicator Awesome Oscillator

This module of signals is based on the market models of the indicator [Awesome Oscillator](https://www.metatrader5.com/en/terminal/help/indicators/bw_indicators/awesome). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | Saucer  — value of the indicator at the analyzed bar rises, and it fell at the previous bars; at that, both values are above 0. 
 
 
   
 
 Crossing the zero line  — value of the indicator is above 0 at the analyzed bar, and it is below 0 at the previous bar. 
 
 
   
 
 Divergence  — the first analyzed bottom of the indicator is shallower than the previous one, and the corresponding price bottom is deeper than the previous one. In addition, the indicator must not rise above the zero level. |
| For selling | Saucer  — value of the indicator at the analyzed bar falls, and it rose at the previous bars; at that, both values are below 0. 
 
 
   
 
 Crossing the zero line  — value of the indicator is below 0 at the analyzed bar, and it is above 0 at the previous bar. 
 
 
   
 
 Divergence  — the first analyzed peak of the indicator is lower than the previous one, and the corresponding price peak is higher than the previous one. In addition, the indicator must not falls below the zero level. |
| No objections to buying | The indicator value grows at the analyzed bar. |
| No objections to selling | The indicator value falls at the analyzed bar. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
