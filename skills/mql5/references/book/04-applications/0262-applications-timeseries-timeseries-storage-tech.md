# Technical aspects of timeseries organization and storage

Before proceeding to the practical issues of using the MQL5 API functions designed to work with time series, we should consider the technical basics of receiving quote data from the server and storing them in MetaTrader 5.

Before price data is available in the terminal for display on charts and transfer to MQL programs, they are downloaded from the server and prepared in a special way. The mechanism for accessing the server for data does not depend on how the request was initiated — by the user when navigating through the chart or programmatically via the MQL5 language.

The data arrives from the server in a compressed format: these are economically packaged blocks of minute bars, which, however, are not the usual M1 bars.

The data received from the server is automatically unpacked and saved in a special HCC intermediate format. The data for each symbol is written to a separate folder {terminal_dir}/bases/{server_name}/history/{symbol_name}. For example, the data on EURUSD from the MetaQuotes-Demo trading server can be located in the folder C:/Program Files/MetaTrader 5/bases/MetaQuotes-Demo/history/EURUSD/.

The data is written to files with the *.hcc extension: each file stores the data of one-minute bars for a year. For example, the 2021.hcc file in the EURUSD folder contains EURUSD minute bars for 2021. These files are used to prepare price data for all timeframes and are not intended for direct access.

Service files in the HCC format act as a data source for plotting price data for specific timeframes. They are created only at the request of a chart or an MQL program and are saved for further use in files with the *.hc extension.

For each timeframe, data is prepared independently of other timeframes. The rules for data generation and availability are the same for all timeframes, including M1. That is, despite the fact that the unit of data storage in the HCC format is a minute bar, their presence does not mean the presence and availability of M1 timeframe data in the same volume in the HC format.

To save resources, timeframe data is loaded and stored in RAM only when necessary: if there are no data accesses for a long time, they are unloaded from RAM (but they remain in the file). This may lead to an increase in the execution time of the next timeseries request if it has not been used for a long time. All popular timeseries, in particular, those for which charts are open, are available almost instantly if the computer has enough resources.

Receiving new data from the server causes automatic updating of the used price data in the HC format for all timeframes and recalculation of all dependent [indicators](/en/book/applications/indicators_make).

When an MQL program accesses data for a specific symbol and timeframe, there is a possibility that the required timeseries has not yet been generated or synchronized with the trade server (for example, updated prices have appeared on it). In this case, you should implement the waiting for data readiness in one form or another.

For scripts, the only solution is to use loops, since they have no other option due to the lack of event handling. For indicators, such algorithms, like any other waiting cycles, are categorically not recommended, as they lead to a halt in the calculation of all indicators and other processing of price data for a given symbol.

For Expert Advisors and indicators, it is better to use the event processing model. If, when processing an event [OnTick](/en/book/automation/experts/experts_ontick) or [OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate) you failed to get all the necessary data of the required timeseries, then you should exit the event handler and wait for them to appear during the next calls of the handler.

Maximum number of bars  

   

It should be noted that the maximum number of bars that will be calculated for each requested symbol/timeframe pair does not exceed the value of the parameter Max. bars in chart in the Options dialog of the terminal. Thus, this parameter imposes restrictions not only on charts of any timeframes but also on all MQL programs.  

   

This limitation is primarily intended to save resources. When setting large values of this parameter, it should be remembered that if there is a sufficiently deep history of price data for lower timeframes, the memory consumption for storing timeseries and indicator buffers can amount to hundreds of megabytes and take up all the RAM.  

   

Changing the bar limit takes effect only after restarting the client terminal. It affects the amount of data requested from the server to build the required number of bars of working timeframes.  

   

The limit set by the parameter is not hard and can be exceeded in certain cases. For example, if at the beginning of the session, the history of quotes for a specific timeframe is sufficient to select the entire limit, then as new bars form, their number may become greater than the current value of the parameter. The actual number of available bars is returned by the [Bars/iBars](/en/book/applications/timeseries/timeseries_bars) functions.
