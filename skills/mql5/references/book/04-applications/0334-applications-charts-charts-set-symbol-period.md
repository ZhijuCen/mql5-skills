# Switching symbol and timeframe

Sometimes an MQL program needs to switch the current symbol or timeframe of a chart. In particular, this is a familiar functionality for many multicurrency, multitimeframe trading panels or trading history analyzing utilities. For this purpose, the MQL5 API provides the ChartSetSymbolPeriod function.

You can also use this function to initiate the recalculation of the entire chart, including the indicators located on it. You can simply specify the current symbol and timeframe as parameters. This technique can be useful for indicators that could not be fully calculated on the first call of OnCalculate, and wait for the loading of third-party data (other symbols, ticks, or indicators). Also, changing the symbol/timeframe leads to the reinitialization of the Expert Advisors attached to the chart. The script (if it is executed periodically in a cycle) will completely disappear from the chart during this procedure (it will be unloaded from the old symbol/timeframe combination but will not be loaded automatically for the new combination).

bool ChartSetSymbolPeriod(long chartId, string symbol, ENUM_TIMEFRAMES timeframe)

The function changes the symbol and timeframe of the specified chart with the chartId identifier to the values of the corresponding parameters: symbol and timeframe. 0 in the chartId parameter means the current chart, NULL in the symbol parameter is the current character, and 0 in the timeframe parameter is the current timeframe.

Changes take effect asynchronously, that is, the function only sends a command to the terminal and does not wait for its execution. The command is added to the chart's message queue and is executed only after all previous commands have been processed.

The function returns true in case of successful placement of the command in the chart queue or false in case of problems. Information about the error can be found in _LastError.

We have seen examples of using the function to update several indicators, in particular:

- IndDeltaVolume.mq5 (see [Waiting for data and managing visibility](/en/book/applications/indicators_make/indicators_wait_none))
- IndUnityPercent.mq5 (see [Multicurrency and multitimeframe indicators](/en/book/applications/indicators_make/indicators_multisymbol))
- UseWPRMTF.mq5 (see [Support for multiple symbols and timeframes](/en/book/applications/indicators_use/indicators_multitimeframe))
- UseM1MA.mq5 (see [Using built-in indicators](/en/book/applications/indicators_use/indicators_standard_use))
- UseDemoAllLoop.mq5 (see [Deleting indicator instances](/en/book/applications/indicators_use/indicators_indicatorrelease))
- IndSubChart.mq5 (see [Chart display modes](/en/book/applications/charts/charts_mode))
