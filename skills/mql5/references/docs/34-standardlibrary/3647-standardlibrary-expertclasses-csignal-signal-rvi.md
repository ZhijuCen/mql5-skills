# Signals of the Oscillator Relative Vigor Index

This module of signals is based on the market models of the oscillator [Relative Vigor Index](https://www.metatrader5.com/en/terminal/help/indicators/oscillators/rvi). The mechanism of making trade decisions based on signals obtained from the modules is described in a [separate section](/en/docs/standardlibrary/expertclasses/csignal#mechanism).

## Conditions of Generation of Signals

Below you can find the description of conditions when the module passes a signal to an Expert Advisor.

| Signal Type | Description of Conditions |
| --- | --- |
| For buying | Crossing of the main and signal line  — the main line is above the signal line at the analyzed bar and below the signal line at the previous one. |
| For selling | Crossing of the main and signal line  — the main line is below the signal line at the analyzed bar and above the signal line at the previous one. |
| No objections to buying | Value of the oscillator grows at the analyzed bar. |
| No objections to selling | Value of the oscillator falls at the analyzed bar. |

Note

Depending on the mode of operation of an Expert Advisor ("Every tick" or "Open prices only") an analyzed bar is either the current bar (with index 0), or the last formed bar (with index 1).

## Adjustable Parameters

This module has the following adjustable parameters:

| Parameter | Description |
| --- | --- |
| Weight | Weight of signal of the module in the interval 0 to 1. |
| PeriodRVI | Period of calculation of the oscillator. |
