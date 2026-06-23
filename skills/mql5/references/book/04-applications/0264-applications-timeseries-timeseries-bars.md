# Number of available bars (Bars/iBars)

A shorter way to find out the total number of bars in a timeseries by symbol/period is provided by the functions Bars and iBars (there is no difference between them as iBars is available for compatibility with MQL4).

int Bars(const string symbol, ENUM_TIMEFRAMES timeframe)

int iBars(const string symbol, ENUM_TIMEFRAMES timeframe)

The functions return the number of bars available for the MQL program for the given symbol and period. This value is influenced by the parameter Max. bars in chart in the terminal Options (see the note in the section [Technical features of organization and storage of timeseries](/en/book/applications/timeseries/timeseries_storage_tech)). For example, if a history is downloaded to the terminal, which for a specific timeframe is 20,000 bars, but the limit is set to 10,000 bars in the settings, then the second value will be decisive. Immediately after the launch of the terminal, the functions will return the number of 10,000 bars, but as new bars are formed, it will increase (if free memory allows). In MQL5, this limit can be found by calling [TerminalInfoInteger](/en/book/common/environment/env_bar_lang)(TERMINAL_MAXBARS).

In addition, the Bars function has a second option that allows you to find out the number of bars in the range between two dates.

int Bars(const string symbol, ENUM_TIMEFRAMES timeframe, datetime start, datetime stop)

Such a request queries only those bars, the opening time of which falls within the range from start to stop (inclusive). It doesn't matter in which order start and stop are specified: the function will analyze quotes from a smaller time to a larger one.

If the data for the timeseries with the specified parameters has not yet been generated or synchronized with the trade server by the time the Bars/iBars function is called, the function will return null. In this case, the error attribute in _LastError will also be 0 (there is no error because the data is simply not yet downloaded or ready). After receiving 0, check the synchronization of a specific timeframe using [SeriesInfoInteger](/en/book/applications/timeseries/timeseries_properties)(..., SERIES_SYNCHRONIZED) or the synchronization of the symbol using the special [SymbolIsSynchronized](/en/book/automation/symbols/symbols_sync) function.

Examples of how to work with the functions will be shown in the script SeriesBars.mq5 in the next section, along with the associated iBarShift function.
