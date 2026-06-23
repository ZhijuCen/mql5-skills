# Handles and counters of indicator owners

Programmatic work with indicators requires operating with handles. A parallel can be drawn here with file descriptors (see the section [Opening and closing files](/en/book/common/files/files_open_close)): there we used the File Open function to inform the system about the file name and opening modes, after which the descriptor served as a "pass" to all other file functions.

The indicator descriptor system serves several purposes.

It allows to tell the terminal in advance which indicator to launch and which timeseries to calculate. Since some time is required to download initial historical data and to calculate the indicator (at least during the initial request), along with the allocation of resources (memory, graphics), the points when the indicator is created and when it is ready are different. The descriptor is a link between them. This is a kind of link to the internal terminal object storing the set of properties that we set when creating the indicator and its current state.

Of course, in order to work with descriptors, the terminal needs to maintain a certain table of all the requested indicators and their properties. However, the terminal does not provide information on the real number in the general table: instead, each program forms its own private list of indicators requested from it. The entries in this list refer to the elements of the general table, and the descriptor is just a number in the list.

Therefore, there can be completely different indicators behind the same descriptors in different programs. So, it makes no sense to transfer the values of descriptors between programs.

Descriptors are part of the terminal resource management system as they exclude duplication of indicator instances with the same characteristics, when possible. In other words, all built-in and custom indicators created programmatically, manually, or from tpl templates are cached.

Before creating a new indicator instance, the terminal checks if there is an identical indicator among those in the cache. The following criteria apply when checking for a copy:

- Matching character and period
- Matching parameters

For custom indicators, the following must additionally match:

- The path on disk (as a string, without normalization to absolute form)
- The chart on which the indicator is running (when creating an indicator from an MQL program, the indicator being created inherits the chart from the program that creates it)

Built-in indicators are cached per symbol and therefore their instances can be allocated for separate use on different charts (with the same symbol/timeframe).

Note that you cannot create two identical indicators on the same chart manually. Different program instances can request the same indicator, in which case only one copy of it will be created and provided to both programs.

For each unique combination of conditions, the terminal keeps a counter: after the first request to create a specific indicator, its counter is equal to 1, and on subsequent ones, it increases by 1 (a copy of the indicator is not created). When an indicator is released, its counter is decreased by 1. The indicator is unloaded only when the counter is reset, i.e., when all its owners explicitly refuse to use it.

It should be noted that multiple calls to the indicator builder function with the same parameters (including symbol/timeframe) within the same MQL program do not lead to multiple increases in the reference counter — the counter will be increased only once. As a consequence, for each value of the handle, one call of the release function is enough ([IndicatorRelease](/en/book/applications/indicators_use/indicators_indicatorrelease)). All further calls are superfluous and return an error because they have nothing to free.

In addition to creating indicators using [iCustom](/en/book/applications/indicators_use/indicators_icustom) and [IndicatorCreate](/en/book/applications/indicators_use/indicators_indicatorcreate) in MQL5, it is possible to get a handle of a third-party (already existing) indicator. This can be done by using the ChartIndicatorGet function which we will study in the chapter on [charts](/en/book/applications/charts). It's important to note here that acquiring a handle in this way will also increase its reference count and prevent unloading unless the handle is then released.

If the program created subordinate indicators, their handles will be automatically released (the counter decreases by 1) when this program is unloaded, even if the IndicatorRelease function is not called.
