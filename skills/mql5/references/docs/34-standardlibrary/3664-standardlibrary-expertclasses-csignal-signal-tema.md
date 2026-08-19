# Signals of the Indicator Triple Exponential Moving Average

This module of signals is based on the market models of the indicator [Triple Exponential Moving Average](https://www.metatrader5.com/en/terminal/help/indicators/trend_indicators/tema). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | The price has crossed the indicator downwards (the Open price of the analyzed bar is above the indicator and the Close price is below the indicator) and the indicator rises (weak signal of a roll-back from the indicator line). 
 
 
   
 
 Moving Average crossover.  The price has crossed the indicator upwards (the Open price of the analyzed bar is below the indicator and the Close price is above the indicator) and the indicator rises (strong signal). 
 
 
   
 
 Formed breakout. The lower shadow of the bar has crossed the indicator (the Open and Close prices of the analyzed bar are above the indicator, and the Low price is below the indicator) and the indicator rises (weak signal of a roll-back from the indicator line). |
| For selling | Failed breakout.  The price has crossed the indicator upwards (the Open price of the analyzed bar is below the indicator and the Close price is above the indicator) and the indicator falls (weak signal of a roll-back from the indicator line). 
 
 
   
 
 Moving Average crossover.  The price has crossed the indicator downwards (the Open price of the analyzed bar is above the indicator and the Close price is below the indicator) and the indicator falls (strong signal). 
 
 
   
 
 Formed breakout.  The upper shadow of the bar has crossed the indicator (the Open and Close prices of the analyzed bar are below the indicator, and the High price is above the indicator) and the indicator falls (weak signal of a roll-back from the indicator line). |
| No objections to buying | The price is above the indicator. |
| No objections to selling | The price is below the indicator. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodMA | Period of averaging of the indicator. |
| Shift | Shift of the indicator along the time axis (in bars). |
| Method | Method of averaging . |
| Applied | A  price series  used for calculation of the indicator. |
