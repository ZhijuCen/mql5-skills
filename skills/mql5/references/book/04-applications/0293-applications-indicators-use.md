# Using ready-made indicators from MQL programs

In the previous chapter, we learned how to develop custom indicators. Users can place them on charts and perform manual technical analysis with them. But this is not the only way to use indicators. MQL5 allows you to create instances of indicators and request their calculated data programmatically. This can be done both from other indicators, combining several simple ones into more complex ones, and from Expert Advisors that implement automatic or semi-automatic trading on indicator signals.

It is enough to know the indicator parameters, as well as the location and meaning of the calculated data in its public buffers, in order to organize the construction of these newly applied timeseries and gain access to them.

In this chapter, we will study the functions for creating and deleting indicators, as well as reading their buffers. This applies not only to custom indicators written in MQL5 but also to a large set of built-in indicators.

The general principles of programmatic interaction with indicators include several steps:

- Creating the indicator descriptor which is a unique identification number issued by the system in response to a certain function call ([iCustom](/en/book/applications/indicators_use/indicators_icustom) or [IndicatorCreate](/en/book/applications/indicators_use/indicators_indicatorcreate)) and through which the MQL code reports the name and parameters of the required indicator
- Reading data from the indicator buffers specified by the descriptor using the [CopyBuffer](/en/book/applications/indicators_use/indicators_copybuffer) function
- Freeing the handle ([IndicatorRelease](/en/book/applications/indicators_use/indicators_indicatorrelease)) if the indicator is no longer needed

Creating and freeing the descriptor are usually performed during program initialization and deinitialization, respectively, and buffers are read and analyzed repeatedly, as needed, for example, when ticks arrive.

In all cases, except for exotic ones, when it is required to dynamically change indicator settings during program execution, it is recommended to obtain indicator descriptors once in OnInit or in the constructor of the global object class.

All indicator creation functions have at least 2 parameters: symbol and timeframe. Instead of a symbol, you can pass NULL, which means the current instrument. Also, the value 0 corresponds to the current timeframe. Optionally, you can use built-in variables _Symbol and _Period. If necessary, you can set an arbitrary symbol and timeframe that are not related to the chart. Thus, in particular, it is possible to implement multi-asset and multi-timeframe indicators.

You can't access the indicator data immediately after creating its instance because the calculation of buffers takes some time. Before reading the data, you should check their readiness using the [BarsCalculated](/en/book/applications/indicators_use/indicators_barscalculated) function (it also takes a descriptor argument and returns the number of calculated bars). Otherwise, an error will be received instead of data. Although it is not critical as it does not cause the program to stop and unload, the absence of data will make the program useless.

Further in this chapter, for brevity, we will refer to the creation of instances of indicators and obtaining their descriptors simply as "creating indicators". It should be distinguished from the similar term "creating custom indicators", by which we meant writing the source code of indicators in the previous chapter.
