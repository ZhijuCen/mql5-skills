<!-- source: https://www.tradingview.com/pine-script-docs/concepts/chart-information/ | fetched 2026-09-23 | why: syminfo/chart.* reads (mintick, mincontract, bg/fg colors) -->

User ManualConcepts# Chart information
## Introduction
Scripts can retrieve multiple types of information about the current chart and its dataset by using a subset of built-in variables . The chart data that scripts can access using these variables includes the following:

- The available prices and volume
- The chart’s timeframe
- The dataset’s session information
- Symbol information
- Time series information
- The chart’s type and color
The following sections on this page list the variables that can access chart information, along with examples demonstrating how to use them. To learn more about all the built-in variables available in Pine Script ® , refer to the Built-ins page in this manual and the “Variables” section of our Reference Manual .

Note Several variables described on this page behave differently in data requests . For most of these variables, if a script uses them in the expression arguments of request.*() calls, or if the script is an indicator that includes a timeframe argument in its declaration statement , they represent information from the requested dataset rather than the current chart. For example, if a request.security() call includes "NASDAQ:AAPL" as its symbol argument, the value of the syminfo.prefix variable is "NASDAQ" inside that request’s context, regardless of the symbol used by the current chart. Likewise, the close value inside the request refers to the share price for NASDAQ:AAPL stock. See the Other timeframes and data page to learn more.

## Prices and volume
Most chart datasets include OHLCV (open, high, low, close, and volume) values for each available bar. The chart displays the final values for each closed bar, and the developing values for an open realtime bar . See the section The basics in the Execution model page to learn more about this behavior.

The variables that store final or developing OHLCV data for the current bar are as follows:

- open : Stores the current bar’s opening price. The value does not fluctuate while the bar is open.
- high : Stores the current bar’s highest price. If the bar is open, the value represents the bar’s highest price as of the current tick.
- low : Stores the current bar’s lowest price. If the bar is open, the value represents the bar’s lowest price as of the current tick.
- close : Stores the current bar’s final closing price, or the latest available price if the current bar is open.
- volume : Stores the trading volume reported for the current bar. If the bar is open, the value represents the total volume accumulated from the bar’s opening tick to the current tick. The unit that the volume value uses varies by instrument. For example, the unit is typically shares for stocks, lots for Forex pairs, the base currency for cryptocurrency pairs, and contracts for futures and other derivatives.
Pine Script also includes multiple variables that store values derived from available OHLC data, including the following:

- hl2 : Stores the average of the bar’s high and low values ( (high + low) / 2 ).
- hlc3 : Stores the average of the bar’s high , low , and close values ( (high + low + close) / 3 ).
- ohlc4 : Stores the average of the bar’s open , high , low , and close values ( (open + high + low + close) / 4 ).
- hlcc4 : Stores a weighted average of the bar’s high , low , and close values ( (high + low + close + close) / 4 ).
Note If a bar contains only a single price rather than complete OHLC prices, each of these price-based variables stores that value. If no volume data is available for a bar, the value of the volume variable is na . Some chart types do not display OHLC prices, but their datasets still contain those prices. For example, a line chart displays only one price per bar. However, the variables that access bar prices still use the available OHLC values from the underlying dataset. On non-standard charts, such as Heikin Ashi or Renko , variables that access price data store the chart’s synthetic prices, not the instrument’s actual prices. Therefore, logic that uses these variables can yield different results on these charts.

On tick charts that use the “1T” timeframe, scripts can also use the bid and ask variables to access the current bid and ask prices. The bid is the highest price that an active buyer is willing to pay for the instrument at its current value, and the ask is the lowest price that an active seller is willing to accept at the current value. On timeframes higher than “1T”, the value of these variables is na .

All of these price and volume variables are of the “series float” qualified type , because they store floating-point values that can vary from bar to bar. Scripts can use the [] history-referencing operator to retrieve the past values of these variables from previous bars. For example, the expression close[1] retrieves the previous bar’s closing price. Multiple built-in functions also access past values internally. For instance, the expression ta.change(ohlc4, 20) is equivalent to ohlc4 - ohlc4[20] ; both expressions calculate the difference between the current ohlc4 value and the value from 20 bars back .

The following example uses the prices and volume of current and previous bars on the chart to calculate a condition for a dynamic background color. The script colors the chart’s background green only if the current values of the volume and close variables are greater than the previous values, and the current close value is greater than its 10-bar moving average. The script also plots the moving average for visual reference:

## Chart timeframe
Scripts can retrieve the timeframe of the current chart by using the timeframe.period or timeframe.main_period variable. Both variables hold a “simple string” value representing the analyzed timeframe:

- The value of the timeframe.period variable represents the timeframe of a specific context. If used outside the expression argument of a request.*() call, the value represents the chart’s timeframe , or the script’s main timeframe if the script is an indicator whose declaration statement includes a timeframe argument. When used in the expression argument of a request.*() call, the value represents the timeframe of the requested dataset .
- The value of the timeframe.main_period variable always represents the chart’s timeframe or the script’s main timeframe, even if the script uses it inside a request.*() call. This behavior is often useful for nested requests that require information from the chart’s timeframe in their logic.
The timeframe strings stored by these variables contain a number representing a quantity (multiplier) followed by a single letter representing the time unit . For all intraday timeframes that Pine expresses in minutes , the timeframe string contains a multiplier without a unit postfix. For example, "1D" represents the one-day timeframe, "5" represents the five-minute timeframe, "60" represents the one-hour (60-minute) timeframe, and "3M" represents the three-month timeframe. See the Timeframe string specifications section of the Timeframes page to learn more.

Multiple built-in functions feature a timeframe parameter that accepts a valid timeframe string. Scripts can pass the timeframe.period or timeframe.main_period variable to this parameter to use the chart’s timeframe in the calculations.

For example, the following script uses the timeframe.period variable in calls to the time() and time_close() functions to retrieve the UNIX timestamps of the current bar’s opening time and the previous bar’s closing time, then measures the difference between the two timestamps to identify time gaps in the chart’s bars. It also uses the variable in a call to timeframe.in_seconds() to retrieve the typical number of seconds represented by the timeframe, then uses the result to express the time difference as an approximate number of bars. Each time that the script detects a gap, it displays formatted text containing the gap’s size in minutes and bars, the timeframe.period value, and the number of bars elapsed since the previous gap in a label at the current bar’s high:

Note that:

- Programmers can also use an empty string ( "" ) as a timeframe argument to specify the same timeframe as timeframe.period . For instance, our example script yields the same results if we use "" instead of the variable in the time() , time_close() , and timeframe.in_seconds() calls.
Scripts can use the timeframe.multiplier variable to retrieve a “simple int” value representing the multiplier of the timeframe referenced by timeframe.period . For example, if the timeframe is “2D”, the timeframe.multiplier value is 2 . If the timeframe is “30S”, the variable’s value is 30 .

The following timeframe.* variables store “simple bool” values to indicate the unit of the timeframe referenced by timeframe.period :

- timeframe.isticks : Stores true if the current timeframe is a tick-based timeframe (e.g., "10T" ), and false otherwise.
- timeframe.isseconds : Stores true if the current timeframe is a second-based timeframe (e.g., "30S" ), and false otherwise.
- timeframe.isminutes : Stores true if the current timeframe is an intraday timeframe in minutes ( "1" to "1440" ), and false otherwise.
- timeframe.isintraday : Stores true if the current timeframe is any intraday timeframe (minutes, seconds, or ticks), and false otherwise.
- timeframe.isdaily : Stores true if the current timeframe is day-based ( "1D" to "365D" ), and false otherwise.
- timeframe.isweekly : Stores true if the current timeframe is week-based ( "1W" to "52W" ), and false otherwise.
- timeframe.ismonthly : Stores true if the current timeframe is month-based ( "1M" to "12M" ), and false otherwise.
- timeframe.isdwm : Stores true if the current timeframe is expressed in days, weeks, or months, and false otherwise.
The example below uses these variables to construct a custom representation of the chart’s timeframe. On the first bar, the script uses multiple timeframe.is* variables in a switch statement to retrieve a string representing the chart timeframe’s unit, then creates a formatted string using the result and the value of timeframe.multiplier . It displays the final text in a single-cell table in the chart’s top-right corner:

Refer to the Timeframes page to learn more about the timeframe.* built-ins and how to use them.

## Session information
Pine Script includes multiple built-in variables that can retrieve information about an intraday dataset’s session , which refers to the days and the times of day in which trading data is available. These variables represent session information for the current chart’s dataset, or for a requested dataset if the script uses them in the expression argument of a request.*() function call.

Scripts can access the named session for the current chart’s dataset by using the syminfo.session variable. The variable holds a “simple string” value representing the session’s name. In most cases, the string matches the value of either of the following session.* constants by default:

- session.regular : Stores the string for the instrument’s default trading session ( "regular" ). The default session varies with the instrument. For instance, on the charts for US equities, the string typically corresponds to regular trading hours (RTH). By contrast, on the charts for several futures contracts, it corresponds to electronic trading hours (ETH), because ETH is enabled by default. On timeframes higher than or equal to 1D, the values of syminfo.session and session.regular are always equal.
- session.extended : Stores the string for the instrument’s extended session ( "extended" ), which includes data from pre- and post-market hours. Outside data requests, the syminfo.session variable holds this string only if the chart includes the option for extended sessions and the user selects that option in the chart’s “Session” settings.
The syminfo.session variable can also hold other unique strings for specific subsessions defined by the exchange or data provider. For instance, the value is "us_regular" on a CME futures chart that uses the RTH session, and "24h" on an equities chart that includes overnight (24-hour) sessions. Refer to the Retrieving named sessions section of the Sessions page to learn more about named session strings.

Programmers can use the string from this variable to create session-specific logic in their scripts, or pass the string to the session parameter of the ticker.new() or ticker.modify() functions to create ticker identifiers for requesting data using the same session as the chart. See the Custom contexts section of the Other timeframes and data page for more information about these ticker.*() functions.

Additional variables in the session namespace hold “series bool” values that indicate the current market state or track the first and last bars in named sessions:

- session.ismarket : Stores true if the current bar belongs to the regular (default) session, and false otherwise. The value is typically always true on timeframes higher than or equal to 1D.
- session.ispremarket : Stores true if the current bar is a pre-market bar, and false otherwise. The value is always false on timeframes higher than or equal to 1D.
- session.ispostmarket : Stores true if the current bar is a post-market bar, and false otherwise. The value is always false on timeframes higher than or equal to 1D.
- session.isfirstbar : Stores true if the current bar is the first bar of the daily session, and false otherwise. If the dataset uses only the regular session, the value is true on the first bar in that session. If the dataset uses extended sessions, the value is true on the first pre-market bar. If the dataset uses 24-hour sessions, the value is true on the first overnight bar.
- session.isfirstbar_regular : Stores true if the current bar is the first bar of the instrument’s regular session, and false otherwise, regardless of the dataset’s session settings.
- session.islastbar : Stores true if the current bar is the last bar of the daily session, and false otherwise. If the dataset uses only regular trading hours, the value is true on the last bar in that session. If the dataset uses extended or overnight sessions, the value is true on the last post-market bar.
- session.islastbar_regular : Stores true if the current bar is the last bar in the instrument’s regular session, and false otherwise, regardless of the dataset’s session settings.
The following example demonstrates the behavior of these variables. The script below calculates and plots the total volume for each subsession on an intraday chart that includes extended or overnight sessions. The script declares four persistent variables to store the total volume for regular, pre-market, post-market, and overnight hours. Then, inside the if structure, it uses session.ismarket , session.ispremarket , and session.ispostmarket as conditions for resetting or incrementing the value of each variable based on the current session state. The script also uses one of the session.isfirstbar* or session.islastbar* variables, depending on the selected inputs, as a condition to color the background of specific session bars. Additionally, the script checks the value of the syminfo.session variable to confirm that these calculations are compatible with the chart. It raises a custom runtime error if the value is not "extended" or "24h" , indicating that the chart is day-based or does not use the “Extended” or “24 hour” session setting:

Refer to the Sessions page to learn more about market sessions and the session-related built-ins.

## Symbol information
The built-in variables in the syminfo namespace hold essential information about the chart’s symbol and the underlying instrument. Most of these variables, excluding syminfo.main_tickerid , can also represent information relating to a requested dataset if a script uses them as the expression argument in a request.*() function call. Most syminfo.* variables have the “simple” type qualifier , because their values do not change after the first bar. However, the variables relating to analyst recommendations and targets have the “series” qualifier, because they store dynamic data that can change over time.

The available syminfo.* variables include the following:

- syminfo.ticker : Stores a string representing the dataset’s symbol without the exchange prefix. For example, the value is "AAPL" for a NASDAQ:AAPL chart, "BTCUSD" for a BITSTAMP:BTCUSD chart, and "ES1!" for a CME_MINI_DL:ES1! chart.
- syminfo.prefix : Stores a string representing the symbol’s broker/exchange identifier. For example, the value is "NASDAQ" for a NASDAQ:AAPL chart, "BITSTAMP" for a BITSTAMP:BTCUSD chart, and "CME_MINI_DL" for a CME_MINI_DL:ES1! chart.
- syminfo.root : Stores a string representing the instrument’s root code if the symbol refers to a futures contract or another applicable derivative. Otherwise, it stores the same value as syminfo.ticker . For example, the value is "ZW" for wheat futures symbols such as ZW1! and ZWU2026.
- syminfo.tickerid : Stores a string representing the ticker identifier (ticker ID) of the chart’s dataset, or of a requested dataset if the script uses it in the expression argument of a request.*() call. The ticker ID contains the dataset’s symbol with the exchange prefix (e.g., "NASDAQ:AAPL" ). The string can also contain information about dataset modifiers , such as extended hours, dividend adjustments, and currency conversion. Programmers can retrieve the dataset’s ticker ID without modifiers by passing this variable to the ticker.standard() function.
- syminfo.main_tickerid : Stores a string representing the ticker ID of the main dataset on which the script runs. Unlike syminfo.tickerid , this variable does not store a different value when used in a request.*() call’s expression argument. Therefore, scripts can use this variable to retrieve the current chart’s ticker ID while executing data requests.
- syminfo.basecurrency : Stores a string representing the instrument’s base currency if the current symbol refers to a Forex pair, a cryptocurrency pair, or a derivative instrument based on a currency pair. Otherwise, it stores an empty string. For example, the variable’s value is "EUR" for any EURJPY pair, "BTC" for any BTCUSDT pair, "CAD" for CME:6C1! futures, and "" for NASDAQ:AAPL stock.
- syminfo.currency : Stores a string representing the currency of the instrument’s quoted prices, or "NONE" if the dataset’s values do not represent currency amounts. For example, the value is "JPY" for a EURJPY pair, "USD" for NASDAQ:AAPL stock, and "NONE" for the TVC:US10Y bond yield dataset.
- syminfo.country : Stores a string representing the two-letter country code of the instrument’s exchange or data provider, or an empty string if the exchange is not linked to a specific country. For example, the value is "US" for NASDAQ:AAPL, "GB" for LSE:AAPL, and "" for BITSTAMP:BTCUSD.
- syminfo.timezone : Stores a string representing the dataset’s exchange time zone in the IANA time zone database format. For example, the value is "America/New_York" for stocks traded on the NASDAQ exchange. See the Time zone strings section of the Time page to learn more about IANA identifiers.
- syminfo.session : Stores a string representing the dataset’s session setting. See the Session information section above for more information.
- syminfo.current_contract : Stores the “string” ticker identifier of the underlying contract if the current symbol refers to a continuous futures dataset, and an empty string otherwise.
- syminfo.description : Stores a string containing the description or extended name of the current instrument or dataset.
- syminfo.employees : Stores the issuing company’s reported number of employees if the current symbol refers to a stock, and na otherwise.
- syminfo.shareholders : Stores an “int” value representing the total number of reported shareholders if the current instrument is a stock, and na otherwise.
- syminfo.shares_outstanding_float : Stores the total reported number of outstanding shares, excluding any restricted shares, if the symbol refers to a stock. For other symbols, the value is na .
- syminfo.shares_outstanding_total : Stores the total reported number of outstanding shares, including restricted shares held by insiders, major shareholders, and employees, if the symbol refers to a stock. For other symbols, the value is na .
- syminfo.expiration_date : Stores an “int” UNIX timestamp representing the start of the last day of the current contract if the symbol refers to a non-continuous futures dataset. On other datasets, the value is na .
- syminfo.isin : Holds a string representing the International Securities Identification Number (ISIN) for the underlying instrument, or an empty string if no ISIN information is available for the instrument.
- syminfo.mincontract : Stores a “float” value representing the minimum number of contracts/lots/shares/units required for a trade, as set by the exchange. For many instruments, the value is 1. Additionally, note that the value is 1 if the symbol does not refer to a tradable instrument.
- syminfo.minmove : Stores a whole number for calculating the smallest increment by which the instrument’s prices change. It is the numerator of the syminfo.mintick formula: syminfo.mintick = syminfo.minmove / syminfo.pricescale .
- syminfo.pricescale : Stores a whole number for calculating the smallest increment by which the instrument’s prices change. It is the denominator of the syminfo.mintick formula: syminfo.mintick = syminfo.minmove / syminfo.pricescale .
- syminfo.mintick : Stores the dataset’s minimum tick size, i.e., the smallest increment by which the instrument’s recorded prices change. For example, the value is 0.00001 for the OANDA:EURUSD pair, 0.01 for NASDAQ:AAPL stock, and 0.25 for CME_MINI_DL:ES1! futures.
- syminfo.pointvalue : Stores the instrument’s point value, which represents a multiplier of the instrument’s price for determining the value of a single contract. For most instruments, the variable’s value is typically 1, which means the instrument’s price directly represents the value of a contract, share, etc. However, for some futures instruments, the price on the chart represents the value per index point or unit of the underlying commodity . For example, the point value for COMEX:GC1! futures is 100, because the standard size of a single contract is 100 troy ounces of gold. Therefore, the cost of purchasing one contract is 100 times the price on the chart.
- syminfo.type : Stores a string representing the instrument’s type. Possible values include "stock" , "futures" , "index" , "forex" , "crypto" , "fund" , "dr" , "cfd" , "bond" , "warrant" , "structured" , and "right" .
- syminfo.volumetype : Stores a string indicating the type of volume reported for the instrument. Possible values include "base" , "quote" , "tick" , and "n/a" .
- syminfo.sector : Stores a string representing the sector associated with the underlying instrument, or an empty string if there is no associated sector. The sector refers to a broad classification of the associated economy. For example, the value is "Electronic Technology" for NASDAQ:AAPL, "Technology Services" for NYSE:IBM, and "Miscellaneous" for AMEX:SPY.
- syminfo.industry : Stores a string representing the industry associated with the underlying instrument, or an empty string if there is no associated industry. The industry associated with an instrument refers to a subset of the corresponding sector. For example, the value is "Telecommunications Equipment" for NASDAQ:AAPL, "Information Technology Services" for NYSE:IBM, "Investment Trusts/Mutual Funds" for AMEX:SPY, and "" for SP:SPX.
- syminfo.recommendations_buy : Stores the total number of analysts who gave the current instrument a “Buy” rating.
- syminfo.recommendations_buy_strong : Stores the total number of analysts who gave the current instrument a “Strong Buy” rating.
- syminfo.recommendations_sell : Stores the total number of analysts who gave the current instrument a “Sell” rating.
- syminfo.recommendations_sell_strong : Stores the total number of analysts who gave the current instrument a “Strong Sell” rating.
- syminfo.recommendations_hold : Stores the total number of analysts who gave the current instrument a “Hold” rating.
- syminfo.recommendations_total : Stores the total number of recommendations for the current instrument.
- syminfo.recommendations_date : Stores an “int” UNIX timestamp representing the starting date of the latest set of recommendations for the current instrument.
- syminfo.target_price_average : Stores the average of the last yearly analyst price targets for the instrument.
- syminfo.target_price_high : Stores the last highest yearly analyst price target for the instrument.
- syminfo.target_price_low : Stores the last lowest yearly analyst price target for the instrument.
- syminfo.target_price_median : Stores the median of the last yearly analyst price targets for the instrument.
- syminfo.target_price_date : Stores an “int” UNIX timestamp representing the starting date of the last analyst price target prediction for the current instrument.
- syminfo.target_price_estimates : Stores the latest total number of analyst price target predictions for the current instrument.
The example script below displays a table containing a simple summary of symbol and instrument information from the chart. On the first bar, the script creates two “string” arrays using the array.from function. The first array contains titles for the table’s first column. The second array contains corresponding strings from multiple syminfo.* variables for the second column. The script iterates through the arrays and populates the cells on each table row within a for loop:

Note that:

- The script initializes and populates the table only on the first bar because the values of the syminfo.* variables used in the code do not change from bar to bar. After the script creates the table and sets its cells on the first bar, the table’s output persists on the right side of the chart.
- The script uses the chart.fg_color variable to set the color of the table’s borders and text. The variable’s value changes based on the color of the chart’s background . See the Chart type and color section below for more information.
## Time series information
Two built-in variables store information about the bar indices in the time series for the current chart, or for a requested dataset if used in the expression argument of a request.*() function call:

- bar_index : Stores a “series int” value representing the time series index for the current bar. The value is 0 on the first available bar, 1 on the second bar, and so on. The value on the last available bar is one less than the total number of bars.
- last_bar_index : Stores a “series int” value representing the time series index of the last available bar. The value is consistently one less than the total number of available bars, even while the script executes on the first bar.
Several variables in the barstate namespace hold “series bool” values to indicate the states of each bar in the chart’s dataset or a requested dataset. These variables include the following:

- barstate.isfirst : Stores true if the current bar is the first available bar, and false otherwise. The value is equivalent to the result of bar_index == 0 .
- barstate.islast : Stores true if the current bar is the last available bar, and false otherwise. The value is equivalent to the result of bar_index == last_bar_index .
- barstate.isnew : Stores true on all historical bars and on the first tick of an open realtime bar. On subsequent ticks within an open bar, the value is false .
- barstate.isconfirmed : Stores true if the current bar is closed (confirmed), and false if the bar is open . The runtime system commits (saves) a script’s calculated data to the time series when the value is true .
- barstate.ishistory : Stores true if the current bar is historical, meaning that it closed before the script loaded on the dataset, and false otherwise.
- barstate.isrealtime : The opposite of barstate.ishistory . Stores true if the current bar is a realtime bar, which closes after the script loads, and false otherwise.
- barstate.islastconfirmedhistory : Stores true on the last available historical bar, and false otherwise.
Refer to the Bar states page to learn more about these variables and how they work. For detailed information about how scripts execute across historical and realtime bars, and how they manage data in the time series based on bar states, refer to the Execution model page.

The following example calculates a volume-weighted average price (VWAP) over periods spanning a specified number of bars. The script resets the VWAP calculation on each bar whose bar_index value is divisible by the specified period. For instance, with the default input value of 100, the calculation resets on bar 0, 100, 200, and so on. The script plots the VWAP series and highlights the background of each bar on which the reset occurs. Additionally, the script uses the bar_index , last_bar_index , and barstate.ishistory variables to calculate the total number of historical bars, realtime bars, and completed periods, then displays the results in a single-cell table on the last bar:

Note that:

- On the first bar where the bar_index and last_bar_index values are equal, the script checks the value of the barstate.ishistory variable to determine whether that bar is historical. If the value is true , the total number of historical bars is one greater than the bar index on that bar. Otherwise, the number of historical bars equals the bar index. As new bars become available, the script counts the number of realtime bars by subtracting the historical total from the value of bar_index + 1 .
- The script counts the total number of completed VWAP periods by dividing the latest bar_index value by the input period, then rounding the result down to the nearest integer.
Pine Script also features several built-in variables that access time information for the bars on the chart or a requested dataset:

- The time and time_close variables hold UNIX timestamps representing the current bar’s opening and closing times, respectively.
- The last_bar_time variable stores a UNIX timestamp representing the opening time of the last available bar.
- The time_tradingday variable holds a UNIX timestamp representing the starting time of the trading day to which the current bar belongs.
- The timenow variable stores the UNIX timestamp of the script’s latest execution.
- The year , month , weekofyear , dayofmonth , dayofweek , hour , minute , and second variables store calendar-based values derived from the current bar’s opening time. The values are expressed in the exchange time zone .
- The chart.left_visible_bar_time and chart.right_visible_bar_time variables store UNIX timestamps representing the opening times of the leftmost and rightmost visible chart bars.
Refer to the Time page for detailed information about these variables and examples of how they work.

## Chart type and color
Multiple built-in variables in the chart namespace hold “simple bool” values to indicate the type of chart on which the script runs. These variables can also indicate a requested chart dataset’s type when used in the expression argument of a request.*() function call:

- chart.is_standard : Stores true if the chart is any of the standard types, including line charts , bar charts , candlestick charts , and other chart types that use the instrument’s actual OHLC prices, as opposed to calculated prices. Otherwise, the value is false .
- chart.is_heikinashi : Stores true if the chart type is Heikin Ashi , and false otherwise.
- chart.is_linebreak : Stores true if the chart type is line break , and false otherwise.
- chart.is_pnf : Stores true if the chart type is point & figure , and false otherwise.
- chart.is_kagi : Stores true if the chart type is Kagi , and false otherwise.
- chart.is_range : Stores true if the chart type is range , and false otherwise.
- chart.is_renko : Stores true if the chart type is Renko , and false otherwise.
These chart.is_* variables are typically useful when a script’s logic must respond differently on non-standard charts. For example, the following script demonstrates a simple strategy that places market orders to enter trades based on the crossing of two moving averages. On a non-standard chart, these orders can generate misleading results, because Pine’s broker emulator fills them at the chart’s calculated prices rather than using the instrument’s actual prices. To prevent such results, the script allows orders only on standard chart types by using chart.is_standard in the conditions that control the strategy.entry() commands. As shown below, if the script runs on a non-standard chart, it does not generate any orders or display performance data in the strategy report :

Note that:

- An alternative way to avoid misleading trade prices on Heikin Ashi charts is to include fill_orders_on_standard_ohlc = true in the strategy() declaration statement. This argument configures the broker emulator to fill orders using standard chart prices by default. See the Strategies page to learn more about strategy scripts.
The chart namespace also features the following variables that store “input color” values based on the background color defined in the chart’s settings:

- chart.bg_color : Stores the value of the chart’s background color, as defined by the “Background” inputs in the “Canvas” tab of the chart’s settings.
- chart.fg_color : Stores a grayscale color that provides high contrast with most chart background colors. For dark backgrounds, the color is #dbdbdb . For light backgrounds, the color is #0f0f0f .
The following script creates a single-cell table to indicate whether the chart’s background is light or dark, based on the value of chart.fg_color . If the value is #0f0f0f , the table’s text states that the background is considered light. Otherwise, it states that the background is considered dark. The script colors the table’s background using the foreground color, and it sets the text color using the value of chart.bg_color . The script also sets the table’s frame color using the middle value of a gradient from the background color to the foreground color:

PreviousBar statesNextInputs## On this page
IntroductionPrices and volumeChart timeframeSession informationSymbol informationTime series informationChart type and color
