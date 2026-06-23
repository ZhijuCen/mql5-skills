# Economic calendar

When developing trading strategies, it is desirable to take into account the fundamental factors that affect the market. MetaTrader 5 has a built-in economic calendar, which is available in the program interface as a separate tab in the toolbar, as well as labels, optionally displayed directly on the chart. The calendar can be enabled by a separate flag on the Community tab in the terminal settings dialog (login to the community is not necessary).

Since MetaTrader 5 supports algorithmic trading, economic calendar events can also be accessed programmatically from the MQL5 API. In this chapter, we will introduce the functions and data structures that enable reading, filtering, and monitoring changes in economic events.

The economic calendar contains a description, release schedule, and historical values of macroeconomic indicators for many countries. For each event, the exact time of the planned release, the degree of importance, the impact on specific currencies, forecast values, and other attributes are known. Actual values of macroeconomic indicators arrive at MetaTrader 5 immediately at the time of publication.

The availability of the calendar allows you to automatically analyze incoming events and react to them in Expert Advisors in a variety of ways, for example, trading as part of a breakout strategy or volatility fluctuations within the corridor. On the other hand, knowing the upcoming fluctuations in the market allows you to find quiet hours in the schedule and temporarily turn off those robots for which strong price movements are dangerous due to possible losses.

Values of datetime type used by all functions and structures that work with the economic calendar are equal to the trade server time ([TimeTradeServer](/en/book/common/timing/timing_local_server)) including its time zone and DST (Daylight Saving Time) settings. In other words, for correct testing of news-trading Expert Advisors, their developer must independently change the times of historical news in those periods (about half a year within each year) when the DST mode differs from the current one.

Calendar functions cannot be used in the [tester](/en/book/automation/tester): when trying to call any of them, we get the FUNCTION_NOT_ALLOWED (4014) error. In this regard, testing calendar-based strategies involves first saving calendar entries in external storages (for example, in files) when running the MQL program on the online chart, and then loading and reading them from the MQL program running in the tester.
