# Search bar index by time (iBarShift)

The iBarShift function provides the bar number for the specified time. In this case, the numbering of bars is always meant as in timeseries, that is, index 0 corresponds to the rightmost, freshest bar, and the values increase as you move from right to left (into the past).

int iBarShift(const string symbol, ENUM_TIMEFRAMES timeframe, datetime time, bool exact = false)

The function returns the index of the bar in the timeseries for the specified pair of symbol/timeframe parameters, into which the value of the time parameter falls. Each bar is characterized by an opening time and a duration common to all bars in the series, that is, by a period. For example, on an hourly timeframe, a bar marked with an opening time of 13:00 lasts from 13:00:00 to 13:59:59 (including the entire last minute and second).

If there is no bar for the specified time (for example, the time falls on non-trading hours or days), then the function behaves differently depending on the exact parameter: if precise = true, the function will return -1; if exact=false, it will return the index of the nearest bar whose opening time is less than the specified one. In the case when there is no such bar, that is, there is no history before the specified time, the function will return -1. But there is a nuance here.

Attention! If the iBarShift function returns a specific bar number, that is, a value other than -1, this does not mean that the following attempt to access timeseries by this index will be able to get prices or other characteristics of this bar. In particular, this can happen if the index of the requested bar exceeds the bar limit in the terminal window (TerminalInfoInteger(TERMINAL_MAXBARS)). This can happen as new bars are formed: then older bars may move beyond the limit to the left beyond and be outside the visibility window, although nominally they may remain in memory for some time. The developer should always check such situations.

Let's check the performance of the Bars/iBars and (see the [previous section](/en/book/applications/timeseries/timeseries_bars)) iBarShift functions using the script SeriesBars.mq5.

```
void OnStart()
{
   const datetime target = PRTF(ChartTimeOnDropped());
   PRTF(iBarShift(NULL, 0, target));
   PRTF(iBarShift(NULL, 0, target, true));
   PRTF(iBarShift(NULL, 0, TimeCurrent()));
   PRTF(Bars(NULL, 0, target, TimeCurrent()));
   PRTF(Bars(NULL, 0, TimeCurrent(), target));
   PRTF(iBars(NULL, 0));
   PRTF(Bars(NULL, 0));
   PRTF(Bars(NULL, 0, 0, TimeCurrent()));
   PRTF(Bars(NULL, 0, TimeCurrent(), TimeCurrent()));
}

```

Here we meet another unfamiliar function [ChartTimeOnDropped](/en/book/applications/charts/charts_on_drop) (we will describe it later): it returns the time of a specific bar (in the active chart) to which the script from Navigator was dragged and dropped with the mouse. First, let's drag the script to the area of the chart where there are quotes.

The following entries will be created in the log (the numbers will be different, in accordance with your settings, actions, and the current time):

```
ChartTimeOnDropped()=2021.10.01 09:00:00 / ok
iBarShift(NULL,0,target)=125 / ok
iBarShift(NULL,0,target,true)=125 / ok
iBarShift(NULL,0,TimeCurrent())=0 / ok
Bars(NULL,0,target,TimeCurrent())=126 / ok
Bars(NULL,0,TimeCurrent(),target)=126 / ok
iBars(NULL,0)=10004 / ok
Bars(NULL,0)=10004 / ok
Bars(NULL,0,0,TimeCurrent())=10004 / ok
Bars(NULL,0,TimeCurrent(),TimeCurrent())=0 / ok

```

In this case, the script was dragged to a bar with the time 2021.10.01 09:00 (an hourly timeframe was used). According to iBarShift, this time corresponded to bar number 125.

The number of bars from the bar under the mouse to the last (current time) was 126. This is combined with the bar number 125 since the numbering starts from 0.

The total number of bars on the chart, obtained in different ways (iBars, Bars without date range, and Bars with a full range from 0 to the current moment [TimeCurrent](/en/book/common/timing/timing_local_server)), is equal to 10004. The terminal settings had a limit of 10000 but additional 4 hourly bars were formed during the session.

The number of the bar where the current time falls iBarShift(..., TimeCurrent()) is always 0 for an existing symbol and timeframe, provided exact = false. If exact = true, then we can sometimes get -1 since the server time increases when ticks of all market instruments arrive, and the current symbol may not be traded temporarily. Then the server time may go ahead by more than one bar, and for TimeCurrent there is no new bar to hit it exactly.

If we drag and drop the script in the empty area to the right of the current, last bar (that is, into the future), we get something like this:

```
ChartTimeOnDropped()=2021.10.09 02:30:00 / ok
iBarShift(NULL,0,target)=0 / ok
iBarShift(NULL,0,target,true)=-1 / ok
Bars(NULL,0,target,TimeCurrent())=0 / ok
Bars(NULL,0,TimeCurrent(),target)=0 / ok
iBars(NULL,0)=10004 / ok
Bars(NULL,0)=10004 / ok
Bars(NULL,0,0,TimeCurrent())=10004 / ok
Bars(NULL,0,TimeCurrent(),TimeCurrent())=0 / ok

```

The iBarShift function in the search mode for any previous bar (exact = false) returns 0 because the current bar is closest to the future. However, an exact search (exact = true) gives the result -1. Also, the Bars functions that count bars in the range from the current time to the "target" future return 0 now (there are no bars there yet).

The iBarShift function is especially useful for writing multicurrency MQL programs. Quite often, trading schedules for different financial instruments do not coincide, so for a specific time, a bar may exist on one symbol but not exist on another. Using the iBarShift function in the nearest (previous) bar search mode, you can always get bar indexes with prices that were relevant for different symbols at the same moment. As a rule, even for Forex symbols, the indexes of historical bars for the same time may differ.

For example, the following instructions will log different numbers of bars and their numbers on the same date range for three symbols: EURUSD, XAUUSD, USDRUB on the one-hour timeframe (MQ Demo server):

```
PRTF(Bars("EURUSD", PERIOD_H1, D'2021.05.01', D'2021.09.01')); // 2087
PRTF(Bars("XAUUSD", PERIOD_H1, D'2021.05.01', D'2021.09.01')); // 1991
PRTF(Bars("USDRUB", PERIOD_H1, D'2021.05.01', D'2021.09.01')); // 694
PRTF(iBarShift("EURUSD", PERIOD_H1, D'2021.09.01')); // 671
PRTF(iBarShift("XAUUSD", PERIOD_H1, D'2021.09.01')); // 638
PRTF(iBarShift("USDRUB", PERIOD_H1, D'2021.09.01')); // 224

```
