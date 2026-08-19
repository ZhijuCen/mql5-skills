# Signals of the Indicator Accelerator Oscillator

This module is based on the market models of the indicator [Accelerator Oscillator](https://www.metatrader5.com/en/terminal/help/indicators/bw_indicators/ao). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | The indicator value is above 0 and it rises at the analyzed and at the previous bars. 
 
 
   
 
 The indicator value is below 0 and it rises at the analyzed and at the previous bars. |
| For selling | The indicator value is below 0 and it falls at the analyzed and at the previous bars. 
 
 
   
 
 The indicator value is above 0 and it falls at the analyzed and at the two previous bars. |
| No objections to buying | The indicator value grows at the analyzed bar. |
| No objections to selling | The indicator value falls at the analyzed bar. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only"), an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
