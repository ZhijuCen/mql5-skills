<!-- source: https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/ | fetched 2026-09-23 | why: request.security + lookahead_off = HTF wash mapping (0001) -->

User ManualConcepts# Other timeframes and data
## Introduction
Pine Script ® allows users to request data from sources and contexts
other than those their charts use. The functions we present on this page
can fetch data from a variety of alternative sources:

- request.security() retrieves data from another symbol, timeframe, or other
context.
- request.security_lower_tf() retrieves intrabar data, i.e., data from a timeframe
lower than the chart timeframe.
- request.currency_rate() requests a daily rate to convert a value expressed in
one currency to another.
- request.dividends(), request.splits(), and request.earnings() respectively retrieve information about an issuing
company’s dividends, splits, and earnings.
- request.financial() retrieves financial data from FactSet .
- request.economic() retrieves economic and industry data.
- request.footprint() retrieves volume footprint data.
- request.seed() retrieves data from a user-maintained GitHub
repository.
Note Throughout this page, and in other parts of our documentation that discuss request.*() functions, we often use the term “context” to describe the symbol, timeframe, and any modifications – such as price adjustments, session settings, and non-standard chart types – that apply to a chart or the data retrieved by a script.

These are the signatures of the functions in the request.* namespace:

```
request.security(symbol, timeframe, expression, gaps, lookahead, ignore_invalid_symbol, currency, calc_bars_count) → series <type>
request.security_lower_tf(symbol, timeframe, expression, ignore_invalid_symbol, currency, ignore_invalid_timeframe, calc_bars_count) → array<type>
request.currency_rate(from, to, ignore_invalid_currency) → series float
request.dividends(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
request.splits(ticker, field, gaps, lookahead, ignore_invalid_symbol) → series float
request.earnings(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
request.financial(symbol, financial_id, period, gaps, ignore_invalid_symbol, currency) → series float
request.economic(country_code, field, gaps, ignore_invalid_symbol) → series float
request.footprint(ticks_per_row, va_percent, imbalance_percent) → series footprint
request.seed(source, symbol, expression, ignore_invalid_symbol, calc_bars_count) → series <type>
```
The request.*() family of functions has numerous potential applications. Throughout this page, we discuss in detail these functions and some of their typical use cases.

Tip Programmers can also enable compatible scripts to perform calculations on data from another timeframe, without requiring request.*() calls, by supplying an argument to the timeframe parameter of the indicator() declaration statement.

## Common characteristics
Many functions in the request.*() namespace share some common properties and parameters. Before we explore each function in depth, let’s familiarize ourselves with these characteristics.

### Behavior
All request.*() functions have similar internal behavior, even though they do not all share the same required parameters. Every unique request.*() call in a script requests a dataset from a defined context (i.e., ticker ID and timeframe) and evaluates an expression across the retrieved data.

The request.security() and request.security_lower_tf() functions allow programmers to specify the context of a request and the expression directly via the symbol , timeframe , and expression parameters, making them suitable for a wide range of data requests.

For example, the request.security() call in this simple script requests daily “AMEX:SPY” data, and it calculates the slope of a 20-bar linear regression line using the retrieved hl2 prices. The first two arguments specify the context of the request, and the third specifies the expression to evaluate across the requested data:

Other functions within the request.*() namespace do not allow programmers to directly define the full context of a request or the evaluated expression. Instead, these functions determine some of the necessary information internally because they perform only specific types of requests.

For instance, request.financial() exclusively retrieves periodic financial data. Its required parameters ( symbol , financial_id , and period ) all define parts of a specific financial ticker ID . The function does not allow specification of the timeframe or expression, as it determines these details internally. The script below demonstrates a simple call to this function that retrieves the annual cost of goods data for the chart symbol’s issuing company:

Scripts can perform up to 40 unique requests using any combination of request.*() function calls, or up to 64 if the user has the Ultimate plan . Unique request.*() calls count toward this limit because they are the only calls that fetch new data . By contrast, redundant calls to the same request.*() function with identical arguments do not typically perform new requests. Instead, they reuse the data from the first executed call. See the request.*() calls section of the Limitations page for more information.

### ​ gaps ​
When using a request.*() function to retrieve data from another context, the data might not come in on each new bar as it would with the current chart. The gaps parameter of a request.*() function controls how the function responds to nonexistent values in the requested series.

Note The timeframe_gaps parameter of the indicator() declaration statement is similar to the gaps parameter for request.*() functions. When the declaration statement includes a timeframe argument, causing the script to evaluate its code using data from a specific timeframe, the timeframe_gaps parameter specifies how the script handles nonexistent values on each chart bar.

Suppose we have a script that requests hourly data for the chart’s symbol using request.security() executing on a 1-minute chart. The function call returns new values only on the 1-minute bars that cover the opening or closing times of the symbol’s hourly bars. On other chart bars, we can decide whether the function returns na values or the last available values via the gaps parameter.

If the gaps parameter uses barmerge.gaps_on , the function returns na results on all chart bars where new data is not yet confirmed from the requested context. Otherwise, if the parameter uses barmerge.gaps_off , the function fills the gaps in the requested data with the last confirmed values on historical bars and the most recent developing values on realtime bars.

The script below demonstrates the difference in behavior by plotting the results from two request.security() calls that fetch the close price of the current symbol from the hourly timeframe on a 1-minute chart. The first call uses gaps = barmerge.gaps_off and the second uses gaps = barmerge.gaps_on :

Note that:

- barmerge.gaps_off is the default value for the gaps parameter in all applicable request.*() functions.
- The script plots the requested series as lines with breaks ( plot.style_linebr ), which do not bridge over na values as the default style ( plot.style_line ) does.
- When using barmerge.gaps_off , the request.security() function returns the last confirmed close from the hourly timeframe on all historical bars. When running on realtime bars (the bars with the color.aqua background in this example), it returns the symbol’s current close value, regardless of confirmation. For more information, see the Historical and realtime behavior section of this page.
### ​ ignore_invalid_symbol ​
The ignore_invalid_symbol parameter of request.*() functions determines how a function handles invalid data requests, e.g.:

- Using a request.*() function with a nonexistent ticker ID as the symbol/ticker parameter.
- Using request.financial() to retrieve information that does not exist for the specified symbol or period .
- Using request.economic() to request a field that does not exist for a country_code .
A request.*() function call produces a runtime error and halts the execution of the script when making an erroneous request if its ignore_invalid_symbol parameter is false . When this parameter’s value is true , the function returns na values in such a case instead of raising an error.

This example uses request.*() calls within a user-defined function to retrieve data for estimating an instrument’s market capitalization (market cap). The user-defined calcMarketCap() function calls request.financial() to retrieve the total shares outstanding for a symbol and request.security() to retrieve a tuple containing the symbol’s close and syminfo.currency values. We’ve included ignore_invalid_symbol = true in both of these request.*() calls to prevent runtime errors for invalid requests.

The script displays a formatted string representing the symbol’s estimated market cap value and currency in a table on the chart and uses a plot() call to visualize the marketCap history:

Note that:

- The calcMarketCap() function only returns non-na values on valid instruments with total shares outstanding data, such as the one we selected for this example. It returns na on others that do not have financial data, including forex, crypto, and derivatives.
- Not all issuing companies publish quarterly financial reports. If the issuing company of the symbol does not report on a quarterly basis, change the “FQ” value in this script to the company’s minimum reporting period. See the request.financial() section for more information.
- We included format.volume in the indicator() and str.tostring() calls to specify that the y-axis of the chart pane represents volume-formatted values and the “string” representation of the marketCap value shows as volume-formatted text.
- For efficiency, this script creates a table and initializes its cell on the first chart bar, then updates the cell’s text on the last bar. To learn more about working with tables, see the Tables page.
### ​ currency ​
The currency parameter of a request.*() function enables programmers to specify the currency of the requested data. If this parameter’s value differs from the symbol’s syminfo.currency value, the function converts the requested values to express them in the specified currency. The currency parameter accepts a built-in constant from the currency.* namespace, such as currency.JPY , or a string representing a valid currency code (e.g., “JPY”). By default, this parameter accepts a “series” argument that can change across executions. However, if dynamic requests are not enabled, it accepts only a value with the “simple” qualifier or a weaker one.

The conversion rate between the syminfo.currency of the requested data and the specified currency depends on the previous daily value of the corresponding currency pair from the most popular exchange. If no exchange provides the rate directly, the function derives the rate using a spread symbol .

Note Not all request.*() function calls return values expressed as a currency amount. Therefore, currency conversion is not always necessary. For example, some of the series that the request.financial() function can retrieve – such as the “PIOTROSKI_F_SCORE” and “NUMBER_OF_EMPLOYEES” metrics – use units other than currency. It is up to programmers to determine when currency conversion is appropriate for their data requests.

### ​ lookahead ​
The lookahead parameter in request.security() , request.dividends() , request.splits() , and request.earnings() specifies the lookahead behavior of the function call. Its default value is barmerge.lookahead_off .

When requesting data from a higher-timeframe (HTF) context, the lookahead value determines whether the request.*() function can return values from times beyond those of the historical bars it executes on. In other words, the lookahead paremeter determines whether the requested data may contain lookahead bias on historical bars.

When requesting data from a lower-timeframe (LTF) context, the lookahead parameter determines whether the function requests values from the first or last intrabar (LTF bar) of each chart-timeframe bar.

Programmers should exercise extreme caution when using lookahead in their requests, especially when requesting data from higher timeframes. When using barmerge.lookahead_on as the lookahead value, ensure that it does not compromise the integrity of the script’s logic by leaking future data into historical chart bars.

The following scenarios are cases where enabling lookahead is acceptable in a request.*() call:

- The expression argument in a request.security() call includes a historical offset (e.g., close[1] ), which prevents the function from requesting future values that it would not have access to on a realtime basis.
- The timeframe argument of the call represents the same timeframe as that of the chart on which the script executes, i.e., timeframe.period .
- The function call requests data from an intrabar timeframe, i.e., a timeframe smaller than the timeframe.period . See the Lower-timeframes section for more information.
Notice Scripts that use request.security() calls with lookahead to leak future data into the past are extremely misleading . As such, they are not allowed as script publications. Although the results of such a script might look great across history due to its apparent aquisition of prescience, those results are unrealistic because the retrieved data was not knowable at the time of each bar. Furthermore, the same behavior is impossible to reproduce on realtime bars. Therefore, before publishing a script to share it with others, ensure that its requests do not mislead traders by using future data on historical bars.

This example demonstrates how the lookahead parameter affects the behavior of higher-timeframe data requests and why enabling lookahead in request.security() without offsetting the expression is misleading. The script calls request.security() to get the HTF high price for the current chart’s symbol in three different ways and plots the resulting series on the chart for comparison.

The first call uses barmerge.lookahead_off (default), and the others use barmerge.lookahead_on . However, the third request.security() call also offsets its expression using the history-referencing operator [] to avoid leaking future data into the past.

As we see on the chart, the plot of the series requested using barmerge.lookahead_on without an offset ( fuchsia line) shows final HTF high prices before they are actually available on historical bars, whereas the other two calls do not:

Note that:

- The series requested using barmerge.lookahead_off has a new historical value at the end of each HTF period, and both series requested using barmerge.lookahead_on have new historical data at the start of each period.
- On realtime bars, the plot of the series without lookahead ( blue ) and the series with lookahead and no historical offset ( fuchsia ) show the same value (i.e., the HTF period’s unconfirmed high price), as no data exists beyond those points to leak into the past. Both of these plots repaint their results after the user reloads the script, because the elapsed realtime bars from the previous run become historical bars in the new run.
- The series that uses lookahead and a historical offset ( aqua ) does not repaint its results, because it always uses the last confirmed value from the higher timeframe. See the Avoiding repainting section of this page for more information.
Notice In Pine Script versions 1 and 2, the security() function did not include a lookahead parameter. However, the request behaved the same as those with lookahead = barmerge.lookahead_on in later versions of Pine, meaning that it systematically accessed future data from a higher timeframe on historical bars. Therefore, exercise caution with Pine v1 or v2 scripts that use HTF security() calls, unless those calls offset the requested series with the [] operator.

### Dynamic requests
By default, unlike all previous Pine Script versions, request.*() function calls in Pine Script v6 are dynamic .

In contrast to non-dynamic requests, dynamic requests can:

- Access data from different data feeds using a single request.*() instance with “series” arguments .
- Execute within the local scopes of conditional structures , loops , and exported functions .
- Execute nested requests .
Aside from the features listed above, there are insignificant differences in the behavior of dynamic and non-dynamic requests. However, for backward compatibility, programmers can deactivate dynamic requests by specifying dynamic_requests = false in the indicator() , strategy() , or library() declaration statement.

Note In Pine Script v5, it is possible for scripts to call user-defined functions or methods containing request.*() calls inside loops or conditional structures without enabling dynamic requests. However, those wrapped requests are not truly dynamic, and they still require “simple” or weaker qualifiers for all arguments that define the requested context. In Pine Script v6, scripts cannot use wrapped request.*() calls within the local blocks of these structures without enabling dynamic requests.

#### ​“series” arguments
Scripts without dynamic requests enabled cannot use “series” arguments for most request.*() function parameters, which means the argument values cannot change . The only exception is the expression parameter in request.security() , request.security_lower_tf() , and request.seed() , which always allows “series” values.

In contrast, when a script allows dynamic requests, all request.*() function parameters that define parts of the ticker ID or timeframe of a request accept “series” arguments that can change with each script execution. In other words, with dynamic requests, it’s possible for a single request.*() instance to fetch data from different contexts in different executions. Some other optional parameters, such as ignore_invalid_symbol , can also accept “series” arguments, allowing additional flexibility in request.*() call behaviors.

The following script declares a symbolSeries variable that is assigned four different symbol strings in 20-bar cycles, with its value changing after every five bars. The request.security() call uses this variable as the symbol argument. The script plots the requestedClose values, which therefore represent a different symbol’s close prices for each five-bar period.

Note that:

- The script draws a label every time the symbolSeries changes, to signify which symbol’s data the requestedClose currently represents.
- Pine v6 scripts enable dynamic requests by default, allowing this script to use a “series string” symbol argument in its request.security() call without error. If the dynamic behavior is disabled by including dynamic_requests = false in the indicator() declaration, then the “series” argument causes a compilation error.
An important limitation is that when using dynamic request.*() calls with “series” arguments or within local scopes , scripts must request all required datasets while executing on historical bars . All request.*() calls on realtime bars can retrieve data from the datasets that the script previously accessed on historical bars, but they cannot request a new context or evaluate a new expression.

To illustrate this limitation, let’s revisit the above script. Notice that it requests close data for all four symbols on the chart’s timeframe during its historical executions. The external datasets for those four contexts are the only ones that any request.*() call on realtime bars can access.

Below, we changed the timeframe argument in the script’s request.security() call to specify that it requests symbolSeries data from the chart’s timeframe on historical bars and the “240” (240 minutes = 4H) timeframe on realtime bars. This version raises a runtime error on the first realtime tick, if it is run on any timeframe other than the 4H timeframe, because it cannot access the 4H data feeds without requesting them on historical bars first:

#### In local scopes
When scripts do not allow dynamic requests, all request.*() calls execute once on every bar or realtime tick, which prevents their use within most local scopes. The only exception is for request.*() calls in the scopes of non-exported functions and methods , because the Pine Script compiler extracts such calls into the global scope during translation.

Scripts that allow dynamic requests do not restrict the execution of request.*() calls to the global scope. They can call request.*() functions directly within the scopes of conditional structures and loops , meaning that each request.*() instance in the code can activate zero, one, or several times on each script execution.

The following example uses a single request.security() instance within a loop to request data from multiple forex data feeds. The script declares an array of symbols on the first chart bar, which it iterates through on all bars using a for…in loop. Each loop iteration calls request.security() to retrieve the volume value for one of the symbols and pushes the result into the requestedData array. After the loop terminates, the script calculates the average, maximum, and minimum values from the requestedData array using built-in methods , then plots the results on the chart:

Notice that the expression argument in the above example ( volume ) is loop-invariant , i.e., it does not change on any loop iteration. When using request.*() calls within a loop, all parameters defining parts of the requested context can accept arguments that depend on variables from the loop’s header or mutable variables that change within the loop’s local scope. However, a request.*() call’s evaluated expression cannot depend on the values of those variables.

Here, we modified the above script to use the second form of the for…in loop statement, which creates a tuple containing the index and value of each element in the symbols array. The request.security() instance in this version uses the index ( i ) in its expression argument, resulting in a compilation error :

#### In libraries
Libraries with dynamic requests enabled can export functions and methods that utilize request.*() calls within their local scopes, provided that the evaluated expressions do not depend on any exported function parameters.

For example, this simple library exports an htfPrices() function that requests a tuple of confirmed open , high , low , and close prices using a specified tickerID and timeframe . If we publish this library, another script can import the function to request higher-timeframe prices without explicitly calling request.security() .

Note that:

- The tuple that the request.security() call includes as the expression argument does not depend on the htfPrices() parameters.
- The htfPrices() function includes a runtime.error() call that raises a custom runtime error when the timeframe argument does not represent a higher timeframe than the chart’s timeframe. See the higher timeframes section for more information.
- The request.security() call uses barmerge.lookahead_on and offsets each item in the tuple by one bar. This is the only recommended method to avoid repainting .
#### Nested requests
Scripts can use dynamic requests to execute nested requests , i.e., request.*() calls that dynamically evaluate other request.*() calls that their expression arguments depend on.

When a request.security() or request.security_lower_tf() call uses an empty string or syminfo.tickerid for its symbol argument, or if it uses an empty string or timeframe.period for the timeframe argument, the requested ticker ID or timeframe depends on the context where the call executes. This context is normally the ticker ID or timeframe of the chart that the script is running on. However, if such a request.security() or request.security_lower_tf() function call is evaluated by another request.*() call, the nested request inherits that request.*() call’s ticker ID or timeframe information.

For example, the script below contains two request.security() calls and uses Pine Logs to display their results. The first call uses empty strings as its symbol and timeframe arguments, meaning that the requested context depends on where the call executes. It evaluates a concatenated string containing the call’s requested ticker ID and timeframe, and the script assigns its result to the info1 variable.

The second call requests data for a specific symbol and timeframe using the info1 variable as its expression argument. Since the info1 variable depends on the first request.security() call, the second call evaluates the first call within its own context. Therefore, the first call adopts the second call’s ticker ID and timeframe while executing within that context, resulting in a different returned value:

This script allows the execution of the first request.security() call within the context of the second call because Pine v6 scripts enable dynamic request.*() calls by default. We can disable this behavior by including dynamic_requests = false in the indicator() declaration statement. Without dynamic requests enabled, the script evaluates each call independently , passing the first call’s calculated value directly into the second call rather than executing the first call within the second context. Consequently, the second call’s returned value is the same as the first call’s value, as we see below:

## Data feeds
TradingView’s data providers supply different data feeds that scripts
can access to retrieve information about an instrument, including:

- Intraday historical data (for timeframes < 1D)
- End-of-day (EOD) historical data (for timeframes >= 1D)
- Realtime data (which may be delayed, depending on your account type
and extra data services)
- Extended hours data
Not all of these data feed types exist for every instrument. For
example, the symbol “BNC:BLX” only has EOD data available.

For some instruments with intraday and EOD historical feeds, volume data
may not be the same since some trades (block trades, OTC trades, etc.)
may only be available at the end of the trading day. Consequently, the
EOD feed will include this volume data, but the intraday feed will not.
Differences between EOD and intraday volume feeds are almost nonexistent
for instruments such as cryptocurrencies, but they are commonplace in
stocks.

Slight price discrepancies may also occur between EOD and intraday
feeds. For example, the high value on one EOD bar may not match any
intraday high values supplied by the data provider for that day.

Another distinction between EOD and intraday data feeds is that EOD
feeds do not contain information from extended hours .

When retrieving information on realtime bars with request.*() functions, it’s important to note that historical and realtime data
reported for an instrument often rely on different data feeds. A
broker/exchange may retroactively modify values reported on realtime
bars, which the data will only reflect after refreshing the chart or
restarting the script.

Another important consideration is that the chart’s data feeds and
feeds requested from providers by the script are managed by independent , concurrent processes. Consequently, in some rare cases,
it’s possible for races to occur where requested results temporarily
fall out of synch with the chart on a realtime bar, which a script
retroactively adjusts after restarting its executions.

These points may account for variations in the values retrieved by request.*() functions when requesting data from other contexts. They
may also result in discrepancies between data received on realtime bars
and historical bars. There are no steadfast rules about the variations
one may encounter in their requested data feeds.

Note As a rule, TradingView does not generate data; it relies on its data providers for the information displayed on charts and accessed by scripts.

When using data feeds requested from other contexts, it’s also crucial
to consider the time axis differences between the chart the script
executes on and the requested feeds since request.*() functions adapt
the returned series to the chart’s time axis. For example, requesting
“BTCUSD” data on the “SPY” chart with request.security() will only show new values when the “SPY” chart has new data as well.
Since “SPY” is not a 24-hour symbol, the “BTCUSD” data returned will
contain gaps that are otherwise not present when viewing its chart
directly.

## ​ request.security() ​
The request.security() function allows scripts to request data from other contexts than the
chart the script executes on, such as:

- Other symbols, including spread
symbols
- Other timeframes (see our User Manual’s page on Timeframes to learn
about timeframe specifications in Pine Script)
- Custom contexts , including alternative sessions, price adjustments,
chart types, etc. using ticker.*() functions
This is the function’s signature:

```
request.security(symbol, timeframe, expression, gaps, lookahead, ignore_invalid_symbol, currency, calc_bars_count) → series <type>
```
The symbol value is the ticker identifier representing the symbol to
fetch data from. This parameter accepts values in any of the following
formats:

- A “string” representing a symbol (e.g., “IBM” or “EURUSD”) or
an “Exchange:Symbol” pair (e.g., “NYSE:IBM” or
“OANDA:EURUSD”). When the value does not contain an exchange
prefix, the function selects the exchange automatically. We
recommend specifying the exchange prefix when possible for
consistent results. Users can also pass an empty string to this
parameter, which prompts the function to use the current chart’s
symbol.
- A “string” representing a spread
symbol (e.g., “AMD/INTC”). Note that “Bar Replay” mode does not work
with these symbols.
- The syminfo.ticker or syminfo.tickerid built-in variables, which return the symbol or the
“Exchange:Symbol” pair that the current chart references. We
recommend using syminfo.tickerid to avoid ambiguity unless the exchange information does not matter
in the data request. For more information on syminfo.* variables,
see this section of our Chart information page.
- A custom ticker identifier created using ticker.*() functions.
Ticker IDs constructed from these functions may contain additional
settings for requesting data using non-standard chart calculations, alternative sessions, and other contexts.
See the Custom contexts section for more information.
The timeframe value specifies the timeframe of the requested data.
This parameter accepts “string” values in our timeframe specification format (e.g., a value of “1D” represents the daily
timeframe). To request data from the same timeframe as the chart the
script executes on, use the timeframe.period variable or an empty string.

The expression parameter of the request.security() function determines the data it retrieves from the specified context.
This versatile parameter accepts “series” values of int , float , bool , color , string ,
and chart.point types. It can also accept tuples , collections , user-defined types , and the outputs of function and method calls. For more
details on the data one can retrieve, see the Requestable data section below.

Notice If a request.*() call uses the value from a source input in its expression argument, and that input accesses a plotted series from another indicator, the request evaluates that series using the data for the chart’s symbol , and not the data for the specified symbol. This behavior occurs because request.*() functions cannot evaluate the scopes required by an external series. Therefore, some request.*() calls that use a symbol argument and request the value of a source input can return unintended results.

### Timeframes
The request.security() function can request data from any available timeframe, regardless of
the chart the script executes on. The timeframe of the data retrieved
depends on the timeframe argument in the function call, which may
represent a higher timeframe (e.g., using “1D” as the timeframe value while running the script on an intraday chart) or the chart’s
timeframe (i.e., using timeframe.period or an empty string as the timeframe argument).

Scripts can also request limited data from lower timeframes with request.security() (e.g., using “1” as the timeframe argument while running the script
on a 60-minute chart). However, we don’t typically recommend using this
function for LTF data requests. The request.security_lower_tf() function is more optimal for such cases.

#### Higher timeframes
Most use cases of request.security() involve requesting data from a timeframe higher than or the same as the
chart timeframe. For example, this script retrieves the hl2 price from a requested higherTimeframe . It plots the resulting series
on the chart alongside the current chart’s hl2 for
comparison:

Note that:

- We’ve included an offset to the expression argument and used barmerge.lookahead_on in request.security() to ensure the series returned behaves the same on historical and
realtime bars. See the Avoiding repainting section for more information.
Notice that in the above example, it is possible to select a higherTimeframe value that actually represents a lower timeframe than the one the chart uses, as the code does not prevent it. When
designing a script to work specifically with higher timeframes, we
recommend including conditions to prevent it from accessing lower
timeframes, especially if you intend to publish it.

Below, we’ve added an if structure to our previous example. If the higherTimeframe value represents a timeframe that is smaller than the chart’s timeframe, the script calls runtime.error() within the structure’s local block to raise a custom runtime error, effectively preventing the script from requesting LTF data:

#### Lower timeframes
Although the request.security() function is intended to operate on timeframes greater than or equal to
the chart timeframe, it can request data from lower timeframes as
well, with limitations. When calling this function to access a lower
timeframe, it will evaluate the expression from the LTF context.
However, it returns the results from only a single intrabar (LTF
bar) on each chart bar.

The intrabar that the function returns data from on each historical
chart bar depends on the lookahead value in the function call. When
using barmerge.lookahead_on ,
it will return the first available intrabar from the chart period.
When using barmerge.lookahead_off ,
it will return the last intrabar from the chart period. On realtime
bars, it returns the last available value of the expression from the
timeframe, regardless of the lookahead value, as the realtime intrabar
information retrieved by the function is not yet sorted.

This script retrieves close data from the valid timeframe closest to a fourth of the size of the
chart timeframe. It makes two calls to request.security() with different lookahead values. The first call uses barmerge.lookahead_on to access the first intrabar value in each chart bar. The second uses
the default lookahead value
( barmerge.lookahead_off ),
which requests the last intrabar value assigned to each chart bar. The
script plots the outputs of
both calls on the chart to compare the difference:

Note that:

- The script determines the value of the lowerTimeframe by
calculating the number of seconds in the chart timeframe with timeframe.in_seconds() ,
then dividing by four and converting the result to a valid timeframe string via timeframe.from_seconds() .
- The plot of the series without lookahead
( purple )
aligns with the close value on the chart timeframe, as this is the last intrabar value
in the chart bar.
- Both request.security() calls return the same value (the current close ) on each realtime bar, as shown on the bars with the orange background.
- Scripts can retrieve up to 200,000 intrabars from a lower-timeframe context. The number of chart bars with available intrabar data varies with the requested lower timeframe, the calc_bars_count value, and the user’s plan. For more information, see this section of the Limitations page.
Tip While scripts can use request.security() to retrieve limited intrabar data, we recommend using request.security_lower_tf() function for such requests in most cases. Instead of retrieving data for only a single LTF bar on each chart bar, it returns an array containing the data for all available LTF bars in the chart bar. See the ​request.security_lower_tf() section below to learn more.

### Requestable data
The request.security() function is quite versatile, as it can retrieve values of any
fundamental type ( int , float , bool , color , or string ). It can also request the IDs of data structures and
built-in or user-defined types that reference fundamental types. The data this function
requests depends on its expression parameter, which accepts any of the
following arguments:

- Built-in variables and function calls
- Variables declared by the script
- Tuples
- Calls to user-defined functions
- Chart points
- Collections
- User-defined types
#### Built-in variables and functions
A frequent use case of request.security() is requesting the output of a built-in variable or
function/ method call from
another symbol or timeframe.

For example, suppose we want to calculate the 20-bar SMA of a symbol’s ohlc4 prices from the daily timeframe while on an intraday chart. We can
accomplish this task with a single line of code:

The above line calculates the value of ta.sma(ohlc4, 20) on the current symbol’s data from the daily timeframe.

It’s important to note that newcomers to Pine might sometimes confuse the above line of code as being equivalent to the following:

However, this line returns an entirely different result. Rather
than requesting a 20-bar SMA from the daily timeframe, it requests the ohlc4 price from the daily timeframe and calclates the ta.sma() of the results over 20 chart bars .

In essence, when the intention is to request the results of an
expression from other contexts, pass the expression directly to the expression parameter in the request.security() call, as demonstrated in the initial example.

Let’s expand on this concept. The script below calculates a multi-timeframe (MTF) ribbon of moving averages, where each moving average in the ribbon calculates over the same number of bars on its respective timeframe. Each request.security() call uses a ta.sma() call as its expression argument to return a length -bar SMA from the specified timeframe:

Note that:

- The script calculates the ribbon’s higher timeframes by
multiplying the chart’s timeframe.in_seconds() value by 2, 3, and 4, then converting each result into a valid timeframe string using timeframe.from_seconds() .
- Instead of calling ta.sma() within each request.security() call, one could use the chartAvg variable as the expression in each call to achieve the same result. See the next section for more information.
- On realtime bars, this script also tracks unconfirmed SMA
values from each higher timeframe. See the Historical and realtime behavior section to learn more.
#### Declared variables
The request.security() function’s expression parameter can accept declared variables that are accessible to the scope from which the function call executes. When using a declared variable as the expression argument, the function call duplicates all preceding code that determines the assigned value or reference. This duplication allows the function to evaluate necessary calculations and logic in the requested context without affecting the original variable.

For instance, this line of code declares a priceReturn variable that holds the current bar’s arithmetic price return:

We can evaluate the priceReturn variable’s calculations in another context by using it as the expression in a request.security() call. The call below duplicates the variable’s calculation and evaluates it across the data from another symbol , returning a separate series adapted to the chart’s time axis:

This example script compares the price returns of the current chart’s symbol and a user-specified symbol. It calculates the value of the priceReturn variable, then uses that variable as the expression in a request.security() call to evaluate the calculation on the input symbol’s data. After the request, the script calculates the correlation between the priceReturn and requestedReturn series using ta.correlation() and plots the result on the chart:

Note that:

- The request.security() call executes the same calculation used in the priceReturn declaration, but the request’s calculation operates on the close values from the specified symbol’s data.
- The script uses the color.from_gradient() function to calculate the color for the plot of the correlation series on each bar. See this section of the Colors page to learn more about color gradients.
When using a variable as the expression argument of a request.*() call, it’s important to note that the function only duplicates code that affects the variable before the call. It cannot copy any subsequent code following the call. Consequently, if the script reassigns the variable or modifies its referenced data after calling request.security() , the code evaluated on the requested data does not include those additional operations.

For example, the following script declares a counter variable and calls request.security() to evaluate the variable from the same context as the chart. After the call, the script increments the counter value by one with the addition assignment operator ( += ), then uses plots and Pine Logs to display the counter and requestedCounter values for comparison.

As shown below, the plots and logs of the two variables display different values. The requestedCounter variable has a consistent value of 0 because the request.security() call evaluates only the initial variable declaration. The request cannot evaluate the addition assignment operation because the script includes that code after the function call:

#### Tuples
Tuples in Pine Script are comma-separated lists of expressions enclosed in square brackets. Programmers often use tuples when creating functions , conditional structures , or loops that return multiple values or references from their local scopes.

The request.security() function can accept a tuple as its expression argument, allowing
scripts to request multiple series of different types using a single
function call. The expressions within requested tuples can be of any
type outlined throughout the Requestable data section of this page, excluding other tuples.

Note The combined size of all tuples returned by request.*() calls in a script cannot exceed 127 elements. See the Tuple element limit section of the Limitations page for more information.

Tuples are particularly helpful when a script needs to retrieve more than one value from a specific context.

For example, the following script calculates the percent rank of the close series over length bars and assigns the result to the rank variable. It then calls request.security() to request a tuple containing the values of rank , ta.crossover(rank, 50) , and ta.crossunder(rank, 50) from a specified timeframe. The script plots the requestedRank series in a separate pane, then uses the result of a ternary expression based on the crossOver and crossUnder values within a bgcolor() call to conditionally highlight the pane’s background:

Note that:

- We’ve offset the rank variable’s expression by one bar using
the history-referencing operator [] and included barmerge.lookahead_on in the request.security() call to ensure the values on realtime bars do not repaint after
becoming historical bars. See the Avoiding repainting section for more information.
- The request.security() call returns a tuple, so we use a tuple declaration to declare
the requestedRank , crossOver , and crossUnder variables. To
learn more about using tuples, see this section of our User Manual’s Type system page.
#### User-defined functions
User-defined functions and methods are custom functions written by users. They allow users to define
sequences of operations associated with an identifier that scripts can
conveniently call throughout their executions (e.g., myUDF() ).

The request.security() function can request the results of user-defined functions and methods whose scopes consist of any types outlined throughout this page’s Requestable data section.

For example, this script contains a user-defined weightedBB() function
that calculates Bollinger Bands with the basis average weighted by a
specified weight series. The function returns a tuple of custom
band values. The script calls the weightedBB() as the expression argument in request.security() to retrieve a tuple of band values calculated on the specified timeframe and plots the results on the
chart:

Note that:

- We offset the source and weight arguments in the weightedBB() call used as the expression in request.security() and used barmerge.lookahead_on to ensure the requested results reflect the last confirmed
values from the timeframe on realtime bars. See this section to learn more.
#### Chart points
Chart points are objects that represent coordinates on the chart. Lines , boxes , polylines ,
and labels use these objects to set their display locations.

The request.security() function can use the ID of a chart.point instance in its expression argument, allowing scripts to retrieve
chart coordinates from other contexts.

The example below requests a tuple of historical chart points from a higher timeframe and uses them to draw boxes on the
chart. The script declares the topLeft and bottomRight variables
that reference chart.point IDs from the last confirmed bar. It then uses request.security() to request a tuple containing the IDs of chart points representing the topLeft and bottomRight from a higherTimeframe .

When a new bar starts on the higherTimeframe , the script draws a new box using the time and price coordinates from the requestedTopLeft and requestedBottomRight chart points:

Note that:

- Because we designed this example to request data from higher timeframes , we’ve included a runtime.error() call that the script executes if the higherTimeframe value represents a lower timeframe than timeframe.period .
#### Collections
Pine Script collections ( arrays , matrices ,
and maps ) are data structures
that contain an arbitrary number of elements with specified types. The request.security() function can retrieve the IDs of collections whose elements consist of:

- Fundamental types
- Chart points
- User-defined types that satisfy the criteria listed in the section below
This example below calculates the ratio of a confirmed bar’s high-low range to the range between the highest and lowest prices over 10 bars from a from a specified symbol and timeframe . It uses maps to hold the values used in the calculations.

The script uses a data map with “string” keys and “float” values to store the current bar’s high , low , ta.highest() , and ta.lowest() results. It passes the map as the expression argument in a request.security() call on each bar to retrieve another map containing the values calculated from the specified context, then assigns that map’s reference to the otherData variable. The script uses the “float” values associated with the “High”, “Low”, “Highest”, and “Lowest” keys of the otherData map to calculate the ratio series that it plots in the chart pane:

Note that:

- The request.security() call in this script can return na if no data is available from the specified context. Since one
cannot call methods on a map variable when its value is na ,
we’ve added an if structure to only calculate a new ratio value when otherData references a valid map instance.
#### User-defined types
User-defined types (UDTs) are composite types containing an arbitrary number of fields , which can be of any available type, including other user-defined types .

The request.security() function can retrieve the IDs of objects produced by UDTs from other contexts if their fields consist of:

- Fundamental types
- Chart points
- Collections that satisfy the criteria listed in the section above
- Other UDTs whose fields consist of any of these types
The following example requests an object ID using a
specified symbol and displays its field values on a chart pane.

The script contains a TickerInfo UDT with “string” fields for syminfo.* values, an array field to store recent “float” price data, and an “int” field to hold
the requested ticker’s bar_index value. It assigns a new TickerInfo ID to an info variable on every
bar and uses the variable as the expression in request.security() to retrieve the ID of an object representing the calculated info from the specified symbol .

The script displays the requestedInfo object’s description , tickerType , currency , and barIndex values in a label and uses plotcandle() to display the values from its prices array:

Note that:

- The syminfo.* variables used in this script all return
“simple string” qualified types. However, objects in Pine
are always qualified as “series”. Consequently, all values
assigned to the info object’s fields automatically adopt the
“series” qualifier .
- It is possible for the request.security() call to return na due to differences between the data requested from the symbol and the main chart. This script assigns a new TickerInfo object to the requestedInfo in that case to prevent runtime
errors.
## ​ request.security_lower_tf() ​
The request.security_lower_tf() function is an alternative to request.security() designed for reliably requesting information from lower-timeframe (LTF)
contexts.

While request.security() can retrieve data from a single intrabar (LTF bar) in each chart bar, request.security_lower_tf() retrieves data from all available intrabars in each chart bar, which
the script can access and use in additional calculations. Each request.security_lower_tf() call can retrieve up to 200,000 intrabars from a lower timeframe, depending on the user’s plan . See this section of our Limitations page for more information.

Tip Working with the request.security_lower_tf() function involves frequent usage of arrays , because the function always returns array results. Therefore, we recommend reading the Arrays page to make the most of this function and understand how to use its returned data.

Below is the function’s signature, which is similar to the signature of request.security() :

```
request.security_lower_tf(symbol, timeframe, expression, ignore_invalid_symbol, currency, ignore_invalid_timeframe, calc_bars_count) → array<type>
```
This function requests data only from timeframes that are lower than or equal to the chart’s timeframe ( timeframe.period ). If the timeframe argument of the request.security_lower_tf() call represents a higher timeframe, the function raises a runtime error or returns na results, depending on the ignore_invalid_timeframe parameter. The parameter’s default value is false , meaning the function raises an error and halts the script’s executions if the timeframe argument is invalid.

### Requesting intrabar data
Intrabar data can provide a script with additional information that may
not be obvious or accessible from solely analyzing data sampled on the
chart’s timerframe. The request.security_lower_tf() function can retrieve many data types from an intrabar context.

Before you venture further in this section, we recommend exploring the Requestable data portion of the request.security() section above, which provides foundational information about
the types of data one can request. The expression parameter in request.security_lower_tf() accepts most of the same arguments discussed in that section, excluding
direct references to collections and mutable variables.
Although it accepts many of the same types of arguments, this function
returns array results, which comes with some differences in interpretation and
handling, as explained below.

### Intrabar data arrays
Lower timeframes contain more data points than higher timeframes, as new
values come in at a higher frequency . For example, when comparing a
1-minute chart to an hourly chart, the 1-minute chart will have up to 60
times the number of bars per hour, depending on the available data.

To address the fact that multiple intrabars exist within a chart bar, request.security_lower_tf() always creates arrays to store the requested data. The elements in the arrays represent the expression values retrieved from the lower timeframe sorted in
ascending order based on each intrabar’s timestamp.

The type identifier of the constructed arrays corresponds to the
data types passed in the request.security_lower_tf() call. For example, using an “int” as the expression will produce an array<int> instance, a “bool” as the expression will produce an array<bool> instance, etc.

The following script uses intrabar information to decompose the chart’s close-to-close price changes into positive and negative parts. It calls request.security_lower_tf() to fetch a “float” array containing ta.change(close) values from a specified lower timeframe on each chart bar, then accesses all the array’s elements using a for…in loop to accumulate positiveChange and negativeChange sums. The script adds the accumulated values to calculate the netChange value, then plots the results on the chart alongside the priceChange value for comparison:

Note that:

- The plots based on
intrabar data may not appear on all available chart bars, as request.security_lower_tf() can only access up to the most recent 200,000 intrabars
available from the requested context. When executing this
function on a chart bar that doesn’t have accessible intrabar
data, it will return an empty array .
- The number of intrabars per chart bar may vary depending on the
data available from the context and the chart the script
executes on. For example, a provider’s 1-minute data feed may
not include data for every minute within the 60-minute timeframe
due to a lack of trading activity over some 1-minute intervals.
To check the number of intrabars retrieved for a chart bar, one
can use array.size() on the resulting array .
- If the lowerTimeframe value is greater than the chart’s
timeframe, the script will raise a runtime error , as we have
not supplied an ignore_invalid_timeframe argument in the request.security_lower_tf() call.
### Tuples of intrabar data
When passing a tuple or a function call that returns a tuple as the expression argument in request.security_lower_tf() ,
the result is a tuple of arrays with type templates corresponding to the types within the argument. For example,
using a [float, string, color] tuple as the expression will result
in [array<float>, array<string>, array<color>] data returned by the
function. Using a tuple expression allows a script to fetch the IDs of several arrays containing intrabar data
with a single request.security_lower_tf() function call.

Note The combined size of all tuples returned by request.*() calls in a script cannot exceed 127 elements. See the Tuple element limit section of the Limitations page for more information.

The following example requests OHLC data from a lower timeframe and
visualizes the current bar’s intrabars on the chart using lines and boxes . The
script calls request.security_lower_tf() with the [open, high, low, close] tuple as its expression to
retrieve a tuple of arrays representing OHLC information from a calculated lowerTimeframe . It
then uses a for loop
to set line coordinates with the retrieved data and current bar indices
to display the results next to the current chart bar, providing a
“magnified view” of the price movement within the latest candle. It
also draws a box around the lines to indicate the chart region occupied by intrabar drawings:

Note that:

- The script draws each candle using two lines :
one to represent wicks and the other to represent the body.
Since the script can display up to 500 lines on the chart,
we’ve limited the maxIntrabars input to 250.
- The lowerTimeframe value is the result of calculating the math.ceil() of the timeframe.in_seconds() divided by the maxIntrabars and converting to a valid timeframe string with timeframe.from_seconds() .
- The script sets the top of the box drawing using the array.max() of the requested hData array, and it sets the box’s bottom
using the array.min() of the requested lData array. As we see on the chart, these
values correspond to the high and low of the chart bar.
### Requesting collections
In some cases, a script might need to request collections from an intrabar context. However, in contrast to request.security() ,
scripts cannot use collection references or calls to functions that return them as the expression argument in a request.security_lower_tf() call, because arrays cannot
directly store references to other collections .

Despite these limitations, it is possible to request collections from lower timeframes, if needed, with the help of wrapper types.

Notice The technique described below is advanced and not recommended for beginners, because it requires an understanding of how user-defined types with collection fields work. When possible, use simpler methods to manage LTF requests. Use the following technique only if others do not suffice.

To make collections requestable with request.security_lower_tf() ,
we must create a UDT with a field to reference a collection ID. This step is necessary since arrays cannot reference
other collections directly but can reference UDTs with collection fields:

With our Wrapper UDT defined, we can now pass the IDs of objects of the UDT to the expression parameter in request.security_lower_tf() .

A straightforward approach is to use a call to the type’s built-in *.new() function as
the expression argument. For example, this line of code uses a call to Wrapper.new() with array.from(close) as the collection argument directly within the request.security_lower_tf() call:

Alternatively, we can create a user-defined function or method that returns a reference to an object of
the UDT and call that function within request.security_lower_tf() .
For instance, this code calls a custom newWrapper() function that
returns a Wrapper ID as the expression argument:

The result with either of the above is an array containing Wrapper IDs from all available intrabars in the chart bar,
which the script can use to reference Wrapper instances from specific
intrabars and use their collection fields in additional operations.

The script below utilizes this approach to collect the IDs of arrays containing intrabar data
from a lowerTimeframe , then uses those arrays to display data from a specific
lower-timeframe bar. Its custom Prices type contains a single data field to
reference array<float> instances that hold price data, and the
user-defined newPrices() function returns the ID of a Prices object.

The script calls request.security_lower_tf() with a newPrices() call as its expression argument to retrieve the ID of an array containing Prices IDs from each intrabar in the chart bar, then uses array.get() to get the ID from a specified available intrabar, if it exists. Lastly,
it uses array.get() on the data array referenced by that instance and calls plotcandle() to display its values on the chart:

Note that:

- The intrabarPrices variable references a Prices object only if the size of the requestedPrices array is greater than the intrabarIndex , because attempting to use array.get() to retrieve an element that doesn’t exist causes an out of bounds error .
- The intrabarData variable references an array from the intrabarPrices.data field only if the intrabarPrices variable references a Prices object. If intrabarPrices holds na because intrabar data is not available for a bar, the intrabarData variable references an array of na values.
- The process used in this example is not necessary to achieve the intended result. Instead of using UDTs , we can use the tuple [open, high, low, close] as the expression argument in the request to retrieve a tuple of arrays for further operations. See the Tuples of intrabar data section above for more information.
## Custom contexts
Pine Script includes multiple ticker.*() functions that allow scripts
to construct custom ticker IDs that specify additional settings for
data requests when used as a symbol argument in request.security() and request.security_lower_tf() :

- ticker.new() constructs a custom ticker ID from a specified prefix and ticker with additional session and adjustment settings.
- ticker.modify() constructs a modified form of a specified tickerid with additional session and adjustment settings.
- ticker.heikinashi() , ticker.renko() , ticker.pointfigure() , ticker.kagi() ,
and ticker.linebreak() construct a modified form a symbol with non-standard chart settings.
- ticker.inherit() constructs a new ticker ID for a symbol with additional parameters
inherited from the from_tickerid specified in the function call,
allowing scripts to request the symbol data with the same
modifiers as the from_tickerid , including session, dividend
adjustment, currency conversion, non-standard chart type,
back-adjustment, settlement-as-close, etc.
- ticker.standard() constructs a standard ticker ID representing the symbol without additional modifiers.
Let’s explore some practical examples of applying ticker.*() functions to request data from custom contexts.

Suppose we want to include dividend adjustment in a stock symbol’s
prices without enabling the “Adjust data for dividends” option in the
“Symbol” section of the chart’s settings. We can achieve this in a
script by constructing a custom ticker ID for the instrument using ticker.new() or ticker.modify() with an adjustment value of adjustment.dividends .

This script creates an adjustedTickerID using ticker.modify() ,
uses that ticker ID as the symbol in request.security() to retrieve a tuple of adjusted price values, then uses plotcandle() to plot the result as candles on the chart. It also highlights the background of bars where the requested prices differ from the prices without dividend adjustment.

As we see on the “NYSE:XOM” chart below, enabling dividend adjustment
results in different historical values before the date of the latest
dividend:

Note that:

- If a modifier included in a constructed ticker ID does not apply
to the symbol, the script will ignore that modifier when
requesting data. For instance, this script will display the same
values as the main chart on forex symbols such as “EURUSD”.
While the example above demonstrates a simple way to modify the chart’s
symbol, a more frequent use case for ticker.*() functions is applying
custom modifiers to another symbol while requesting data. If a ticker ID
referenced in a script already has the modifiers one would like to apply
(e.g., adjustment settings, session type, etc.), they can use ticker.inherit() to quickly and efficiently add those modifiers to another symbol.

In the example below, we’ve edited the previous script to request data
for a symbolInput using modifiers inherited from the adjustedTickerID . This script calls ticker.inherit() to construct an inheritedTickerID and uses that ticker ID in a request.security() call. It also requests data for the symbolInput without additional
modifiers and plots candles for both ticker IDs in a separate chart pane to compare the difference.

As shown on the chart, the data requested using the inheritedTickerID includes dividend adjustment, whereas the data requested using the symbolInput directly does not:

Note that:

- Since the adjustedTickerID represents a modified form of the syminfo.tickerid ,
if we modify the chart’s context in other ways, such as
changing the chart type or enabling extended trading hours in
the chart’s settings, those modifiers will also apply to the adjustedTickerID and inheritedTickerID . However, they will not apply to the symbolInput since it represents a standard ticker ID.
Another frequent use case for requesting custom contexts is retrieving
data that uses non-standard chart calculations. For example, suppose we want to use Renko price values to calculate trade signals in a strategy() script. If we simply change the chart type to “Renko” to get the
prices, the strategy will also simulate its trades based on those synthetic prices, producing misleading
results :

To ensure our strategy shows results based on actual prices, we can
create a Renko ticker ID using ticker.renko() while keeping the chart on a standard type , allowing the script to
request and use Renko prices to calculate its signals without calculating the strategy results
on them:

## Historical and realtime behavior
Functions in the request.*() namespace can behave differently on
historical and realtime bars. This behavior is closely related to
Pine’s Execution model .

Consider how a script behaves within the main context. Throughout the
chart’s history, the script calculates its required values once and commits them to that bar so their states are accessible on subsequent executions.
On an unconfirmed bar, however, the script recalculates its
values on each update to the bar’s data to align with realtime
changes. Before recalculating the values on that bar, it reverts
calculated values to their last committed states, otherwise known as rollback , and it only commits values to that bar once the bar closes.

Now consider the behavior of data requests from other contexts with request.security() .
As when evaluating historical bars in the main context, request.security() only returns new historical values when it confirms a bar in its
specified context. When executing on realtime bars, it returns
recalculated values on each chart bar, similar to how a script
recalculates values in the main context on the open chart bar.

However, the function only confirms the requested values when a bar
from its context closes. When the script restarts, what
were previously realtime bars become historical bars.
Therefore, request.security() only returns the values it confirmed on those bars. In essence, this
behavior means that requested data may repaint when its values
fluctuate on realtime bars without confirmation from the context.

Tip It is often helpful to distinguish historical bars from realtime bars when working with request.*() functions. Scripts can determine whether bars have historical or realtime states by using the barstate.ishistory and barstate.isrealtime variables.

In most circumstances where a script requests data from a broader
context, one will typically require confirmed, stable values that do
not fluctuate on realtime bars. The section below explains how to achieve such a result and avoid repainting
data requests.

### Avoiding repainting
#### Higher-timeframe data
When requesting values from a higher timeframe, they are subject to
repainting since realtime bars can contain unconfirmed information
from developing HTF bars, and the script may adjust the times that new
values come in on historical bars. To avoid repainting HTF data, one
must ensure that the function only returns confirmed values with
consistent timing on all bars, regardless of bar state.

The most reliable approach to achieve non-repainting results is to use
an expression argument that only references past bars (e.g., close[1] ) while using barmerge.lookahead_on as the lookahead value.

Using barmerge.lookahead_on with non-offset HTF data requests is discouraged since it prompts request.security() to “look ahead” to the final values of an HTF bar, retrieving
confirmed values before they’re actually available in the script’s
history. However, if the values used in the expression are offset by
at least one bar, the “future” data the function retrieves is no
longer from the future. Instead, the data represents confirmed values
from established, available HTF bars. In other words, applying an
offset to the expression effectively prevents the requested data from
repainting when the script restarts its executions and eliminates
lookahead bias in the historical series.

The following example demonstrates a repainting HTF data request. The
script uses request.security() without offset modifications or additional arguments to retrieve the
results of a ta.wma() call from a higher timeframe. It also highlights the background to
indicate which bars were in a realtime state during its calculations.

As shown on the chart below, the plot of the requested WMA only changes on historical bars when HTF bars
close, whereas it fluctuates on all realtime bars since the data
includes unconfirmed values from the higher timeframe:

To avoid repainting in this script, we can add lookahead = barmerge.lookahead_on to the request.security() call and offset the call history of ta.wma() by one bar with the history-referencing operator [] ,
ensuring the request always retrieves the last confirmed HTF bar’s WMA
at the start of each new timeframe . Unlike the previous script, this
version has consistent behavior on historical and realtime bar states,
as we see below:

#### Lower-timeframe data
The request.security() and request.security_lower_tf() functions can retrieve data from lower-timeframe contexts. The request.security() function can only retrieve data from a single intrabar in each chart
bar, and request.security_lower_tf() retrieves data from all available intrabars.

When using these functions to retrieve intrabar data, it’s important to
note that such requests are not immune to repainting behavior.
Historical and realtime series often rely on separate data feeds. Data
providers may retroactively modify realtime data, and it’s possible for
races to occur in realtime data feeds, as explained in the Data feeds section of this page. Either case may result in intrabar
data retrieved on realtime bars repainting after the script restarts its
executions.

Additionally, a particular case that will cause repainting LTF
requests is using request.security() with barmerge.lookahead_on to retrieve data from the first intrabar in each chart bar. While it
will generally work as expected on historical bars, it will track only
the most recent intrabar on realtime bars, as request.security() does not retain all intrabar information, and the intrabars the function retrieves on realtime bars are unsorted until restarting the
script:

One can mitigate this behavior and track the values from the first
intrabar, or any available intrabar in the chart bar, by using request.security_lower_tf() since it maintains an array of intrabar values ordered by the times they come in. Here, we call array.first() on a requested array of intrabar data to retrieve the close price from the first available intrabar in each chart bar:

Note that:

- While request.security_lower_tf() is more optimized for handling historical and realtime
intrabars, it’s still possible in some cases for minor
repainting to occur due to data differences from the provider,
as outlined above.
- This code may not show intrabar data on all available chart
bars, depending on how many intrabars each chart bar contains,
as request.*() functions can retrieve up to 200,000 intrabars
from an LTF context. The maximum number of requestable intrabars depends on the user’s plan . See this section of the Limitations page for more information.
## ​ request.currency_rate() ​
When a script needs to convert values expressed in one currency to
another, one can use request.currency_rate() .
This function requests a daily rate for currency conversion
calculations based on currency pair or spread data from the most popular exchanges, providing a simpler alternative
to fetching specific pairs or spreads with request.security() .

While one can use request.security() to retrieve daily currency rates, its use case is more involved than request.currency_rate() ,
as one needs to supply a valid ticker ID for a currency pair or spread
to request the rate. Additionally, a historical offset and barmerge.lookahead_on are necessary to prevent the results from repainting, as explained in this section .

The request.currency_rate() function, on the other hand, only requires currency codes . No ticker
ID is needed when requesting rates with this function, and it ensures
non-repainting results without requiring additional specification.

The function’s signature is as follows:

```
request.currency_rate(from, to, ignore_invalid_currency) → series float
```
The from parameter specifies the currency to convert, and the to parameter specifies the target currency. Both parameters accept
“string” values representing valid currency codes (e.g.,
“USD”) or any built-in currency.* variable (e.g., currency.USD ).

When the function cannot calculate a valid conversion rate between the specified from and to currencies, programmers can decide whether
it raises a runtime error or returns na via
the ignore_invalid_currency parameter. The default value is false ,
meaning the function raises a runtime error and halts the script’s
executions.

The following example demonstrates a simple use case for request.currency_rate() .
Suppose we want to convert values expressed in Turkish lira
( currency.TRY )
to South Korean won
( currency.KRW )
using a daily conversion rate. If we use request.security() to retrieve the rate, we must supply a valid ticker ID and request the
last confirmed close from the previous day.

In this case, no valid symbol exists that would allow us to
retrieve a conversion rate directly with request.security() .
Therefore, we first need a ticker ID for a spread that converts TRY to an intermediate currency, such as USD, then
converts the intermediate currency to KRW. We can then use that ticker
ID within request.security() with close[1] as the expression and barmerge.lookahead_on as the lookahead value to request a non-repainting daily rate.

Alternatively, we can achieve the same result more simply by calling request.currency_rate() .
This function does all the heavy lifting for us, only requiring from and to currency arguments to perform its calculation.

As we see below, both approaches return the same daily rate:

## ​ request.dividends() ​, ​ request.splits() ​, and ​ request.earnings() ​
Analyzing a stock’s earnings data and corporate actions provides
helpful insights into its underlying financial strength. Pine Script
provides the ability to retrieve essential information about applicable
stocks via request.dividends() , request.splits() ,
and request.earnings() .

These are the functions’ signatures:

```
request.dividends(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
request.splits(ticker, field, gaps, lookahead, ignore_invalid_symbol) → series float
request.earnings(ticker, field, gaps, lookahead, ignore_invalid_symbol, currency) → series float
```
Each function has the same parameters in its signature, with the
exception of request.splits() ,
which doesn’t have a currency parameter.

Note that unlike the symbol parameter in other request.*() functions, the ticker parameter in these functions only accepts an “Exchange:Symbol” pair , such as “NASDAQ:AAPL”. The built-in syminfo.ticker variable does not work with these functions since it does not contain
exchange information. Instead, one must use syminfo.tickerid for such cases.

The field parameter determines the data the function will retrieve.
Each of these functions accepts different built-in variables as the field argument since each requests different information about a
stock:

- The request.dividends() function retrieves current dividend information for a stock, i.e.,
the amount per share the issuing company paid out to investors who
purchased shares before the ex-dividend date. Passing the built-in dividends.gross or dividends.net variables to the field parameter specifies whether the returned
value represents dividends before or after factoring in expenses the
company deducts from its payouts.
- The request.splits() function retrieves current split and reverse split information for a
stock. A split occurs when a company increases its outstanding
shares to promote liquidity. A reverse split occurs when a company
consolidates its shares and offers them at a higher price to attract
specific investors or maintain their listing on a market that has a
minimum per-share price. Companies express their split information
as ratios . For example, a 5:1 split means the company issued
additional shares to its shareholders so that they have five times
the number of shares they had before the split, and the raw price of
each share becomes one-fifth of the previous price. Passing splits.numerator or splits.denominator to the field parameter of request.splits() determines whether it returns the numerator or denominator of the
split ratio.
- The request.earnings() function retrieves the earnings per share (EPS) information for a
stock ticker ’s issuing company. The EPS value is the ratio of a
company’s net income to the number of outstanding stock shares,
which investors consider an indicator of the company’s
profitability. Passing earnings.actual , earnings.estimate ,
or earnings.standardized as the field argument in request.earnings() respectively determines whether the function requests the actual,
estimated, or standardized EPS value.
For a detailed explanation of the gaps , lookahead , and ignore_invalid_symbol parameters of these functions, see the Common characteristics section at the top of this page.

It’s important to note that the values returned by these functions
reflect the data available as it comes in. This behavior differs from
financial data originating from a request.financial() call in that the underlying data from such calls becomes available
according to a company’s fiscal reporting period.

Tip Scripts can also retrieve information about upcoming earnings and dividends for an instrument via the earnings.future_* and dividends.future_* built-in variables.

Here, we’ve included an example that displays a handy table containing the most recent dividend, split, and EPS data. The script
calls the request.*() functions discussed in this section to retrieve
the data, then converts the values to “strings” with str.*() functions and displays the results in the infoTable with table.cell() :

Note that:

- We’ve included barmerge.gaps_on in the request.*() calls, so they only return values when new
data is available. Otherwise, they return na .
- The script assigns a table ID to the infoTable variable on the first chart bar. On
subsequent bars, it updates necessary cells with new information
whenever data is available.
- If no information is available from any of the request.*() calls throughout the chart’s history (e.g., if the ticker has
no dividend information), the script does not initialize the
corresponding cells since it’s unnecessary.
## ​ request.financial() ​
Financial metrics provide investors with insights about a company’s
economic and financial health that are not tangible from solely
analyzing its stock prices. TradingView offers a wide variety of
financial metrics from FactSet that traders
can access via the “Financials” tab in the “Indicators” menu of the
chart. Scripts can access available metrics for an instrument directly
via the request.financial() function.

This is the function’s signature:

```
request.financial(symbol, financial_id, period, gaps, ignore_invalid_symbol, currency) → series float
```
As with the first parameter in request.dividends() , request.splits() ,
and request.earnings() ,
the symbol parameter in request.financial() requires an “Exchange:Symbol” pair . To request financial information
for the chart’s ticker ID, use syminfo.tickerid ,
as syminfo.ticker will not work.

The financial_id parameter accepts a “string” value representing
the ID of the requested financial metric. TradingView has numerous
financial metrics to choose from. See the Financial IDs section below for an overview of all accessible metrics and
their “string” identifiers.

The period parameter specifies the fiscal period for which new
requested data comes in. It accepts one of the following “string” arguments: “FQ” (quarterly), “FH” (semiannual), “FY” (annual), or “TTM”
(trailing twelve months) . Not all fiscal periods are available for all
metrics or instruments. To confirm which periods are available for
specific metrics, see the second column of the tables in the Financial IDs section.

See this page’s Common characteristics section for a detailed explanation of this function’s gaps , ignore_invalid_symbol , and currency parameters.

It’s important to note that the data retrieved from this function comes
in at a fixed frequency , independent of the precise date on which the
data is made available within a fiscal period. For a company’s
dividends, splits, and earnings per share (EPS) information, one can
request data reported on exact dates via request.dividends() , request.splits() ,
and request.earnings() .

This script uses request.financial() to retrieve information about the income and expenses of a stock’s
issuing company and visualize the profitability of its typical business
operations. It requests the “OPER_INCOME”, “TOTAL_REVENUE”, and
“TOTAL_OPER_EXPENSE” financial IDs for the syminfo.tickerid over the latest fiscalPeriod , then plots the results on the
chart:

Note that:

- Not all fiscalPeriod options are available for every ticker
ID. For example, companies in the US typically publish quarterly reports, whereas many European companies publish semiannual reports. See this
page in our Help Center for more information.
### Calculating financial metrics
The request.financial() function can provide scripts with numerous useful financial metrics that
don’t require additional calculations. However, some commonly used
financial estimates require combining an instrument’s current market
price with requested financial data. Such is the case for:

- Market Capitalization (market price * total shares outstanding)
- Earnings Yield (12-month EPS / market price)
- Price-to-Book Ratio (market price / BVPS)
- Price-to-Earnings Ratio (market price / EPS)
- Price-to-Sales Ratio (market cap / 12-month total revenue)
The following script contains user-defined functions that calculate the above financial metrics for the syminfo.tickerid .
We’ve created these functions so users can easily copy them into their
scripts. This example uses them within a str.format() call to construct a tooltipText , which it displays in tooltips on the
chart using labels . Hovering over any bar’s label will expose the tooltip containing the metrics calculated on that bar:

Note that:

- Since not all companies publish quarterly financial reports, one
may need to change the “FQ” in these functions to match the
minimum reporting period for a specific company, as the request.financial() calls will return na when “FQ” data isn’t available.
### Financial IDs
Below is an overview of all financial metrics one can request via request.financial() ,
along with the periods in which reports may be available. We’ve divided
this information into four tables corresponding to the categories
displayed in the “Financials” section of the “Indicators” menu:

- Income statements
- Balance sheet
- Cash flow
- Statistics
Each table has the following three columns:

- The first column contains descriptions of each metric with links to
Help Center pages for additional information.
- The second column lists the possible period arguments allowed for
the metric. Note that all available values may not be compatible
with specific ticker IDs, e.g., while “FQ” may be a possible
argument, it will not work if the issuing company does not publish
quarterly data.
- The third column lists the “string” IDs for the financial_id argument in request.financial() .
Tip The tables in these sections are quite lengthy, because there are many financial_id arguments available. Use the “Click to show/hide” option above each table to toggle its visibility.

#### Income statements
This table lists the available metrics that provide information about a
company’s income, costs, profits and losses.

Click to show/hide| Financial | period | financial_id |
| After tax other income/expense | FQ, FH, FY, TTM | AFTER_TAX_OTHER_INCOME |
| Average basic shares outstanding | FQ, FH, FY | BASIC_SHARES_OUTSTANDING |
| Basic earnings per share (Basic EPS) | FQ, FH, FY, TTM | EARNINGS_PER_SHARE_BASIC |
| Cost of goods sold | FQ, FH, FY, TTM | COST_OF_GOODS |
| Deprecation and amortization | FQ, FH, FY, TTM | DEP_AMORT_EXP_INCOME_S |
| Diluted earnings per share (Diluted EPS) | FQ, FH, FY, TTM | EARNINGS_PER_SHARE_DILUTED |
| Diluted net income available to common stockholders | FQ, FH, FY, TTM | DILUTED_NET_INCOME |
| Diluted shares outstanding | FQ, FH, FY | DILUTED_SHARES_OUTSTANDING |
| Dilution adjustment | FQ, FH, FY, TTM | DILUTION_ADJUSTMENT |
| Discontinued operations | FQ, FH, FY, TTM | DISCONTINUED_OPERATIONS |
| EBIT | FQ, FH, FY, TTM | EBIT |
| EBITDA | FQ, FH, FY, TTM | EBITDA |
| Equity in earnings | FQ, FH, FY, TTM | EQUITY_IN_EARNINGS |
| Gross profit | FQ, FH, FY, TTM | GROSS_PROFIT |
| Interest capitalized | FQ, FH, FY, TTM | INTEREST_CAPITALIZED |
| Interest expense on debt | FQ, FH, FY, TTM | INTEREST_EXPENSE_ON_DEBT |
| Interest expense, net of interest capitalized | FQ, FH, FY, TTM | NON_OPER_INTEREST_EXP |
| Miscellaneous non-operating expense | FQ, FH, FY, TTM | OTHER_INCOME |
| Net income | FQ, FH, FY, TTM | NET_INCOME |
| Net income before discontinued operations | FQ, FH, FY, TTM | NET_INCOME_BEF_DISC_OPER |
| Non-controlling/minority interest | FQ, FH, FY, TTM | MINORITY_INTEREST_EXP |
| Non-operating income, excl. interest expenses | FQ, FH, FY, TTM | NON_OPER_INCOME |
| Non-operating income, total | FQ, FH, FY, TTM | TOTAL_NON_OPER_INCOME |
| Non-operating interest income | FQ, FH, FY, TTM | NON_OPER_INTEREST_INCOME |
| Operating expenses (excl. COGS) | FQ, FH, FY, TTM | OPERATING_EXPENSES |
| Operating income | FQ, FH, FY, TTM | OPER_INCOME |
| Other cost of goods sold | FQ, FH, FY, TTM | COST_OF_GOODS_EXCL_DEP_AMORT |
| Other operating expenses, total | FQ, FH, FY, TTM | OTHER_OPER_EXPENSE_TOTAL |
| Preferred dividends | FQ, FH, FY, TTM | PREFERRED_DIVIDENDS |
| Pretax equity in earnings | FQ, FH, FY, TTM | PRETAX_EQUITY_IN_EARNINGS |
| Pretax income | FQ, FH, FY, TTM | PRETAX_INCOME |
| Research & development | FQ, FH, FY, TTM | RESEARCH_AND_DEV |
| Selling/general/admin expenses, other | FQ, FH, FY, TTM | SELL_GEN_ADMIN_EXP_OTHER |
| Selling/general/admin expenses, total | FQ, FH, FY, TTM | SELL_GEN_ADMIN_EXP_TOTAL |
| Taxes | FQ, FH, FY, TTM | INCOME_TAX |
| Total operating expenses | FQ, FH, FY, TTM | TOTAL_OPER_EXPENSE |
| Total revenue | FQ, FH, FY, TTM | TOTAL_REVENUE |
| Unusual income/expense | FQ, FH, FY, TTM | UNUSUAL_EXPENSE_INC |
#### Balance sheet
This table lists the metrics that provide information about a company’s
capital structure.

Click to show/hide| Financial | period | financial_id |
| Accounts payable | FQ, FH, FY | ACCOUNTS_PAYABLE |
| Accounts receivable - trade, net | FQ, FH, FY | ACCOUNTS_RECEIVABLES_NET |
| Accrued payroll | FQ, FH, FY | ACCRUED_PAYROLL |
| Accumulated depreciation, total | FQ, FH, FY | ACCUM_DEPREC_TOTAL |
| Additional paid-in capital/Capital surplus | FQ, FH, FY | ADDITIONAL_PAID_IN_CAPITAL |
| Book value per share | FQ, FH, FY | BOOK_VALUE_PER_SHARE |
| Capital and operating lease obligations | FQ, FH, FY | CAPITAL_OPERATING_LEASE_OBLIGATIONS |
| Capitalized lease obligations | FQ, FH, FY | CAPITAL_LEASE_OBLIGATIONS |
| Cash & equivalents | FQ, FH, FY | CASH_N_EQUIVALENTS |
| Cash and short term investments | FQ, FH, FY | CASH_N_SHORT_TERM_INVEST |
| Common equity, total | FQ, FH, FY | COMMON_EQUITY_TOTAL |
| Common stock par/Carrying value | FQ, FH, FY | COMMON_STOCK_PAR |
| Current portion of LT debt and capital leases | FQ, FH, FY | CURRENT_PORT_DEBT_CAPITAL_LEASES |
| Deferred income, current | FQ, FH, FY | DEFERRED_INCOME_CURRENT |
| Deferred income, non-current | FQ, FH, FY | DEFERRED_INCOME_NON_CURRENT |
| Deferred tax assets | FQ, FH, FY | DEFERRED_TAX_ASSESTS |
| Deferred tax liabilities | FQ, FH, FY | DEFERRED_TAX_LIABILITIES |
| Dividends payable | FY | DIVIDENDS_PAYABLE |
| Goodwill, net | FQ, FH, FY | GOODWILL |
| Gross property/plant/equipment | FQ, FH, FY | PPE_TOTAL_GROSS |
| Income tax payable | FQ, FH, FY | INCOME_TAX_PAYABLE |
| Inventories - finished goods | FQ, FH, FY | INVENTORY_FINISHED_GOODS |
| Inventories - progress payments & other | FQ, FH, FY | INVENTORY_PROGRESS_PAYMENTS |
| Inventories - raw materials | FQ, FH, FY | INVENTORY_RAW_MATERIALS |
| Inventories - work in progress | FQ, FH, FY | INVENTORY_WORK_IN_PROGRESS |
| Investments in unconsolidated subsidiaries | FQ, FH, FY | INVESTMENTS_IN_UNCONCSOLIDATE |
| Long term debt | FQ, FH, FY | LONG_TERM_DEBT |
| Long term debt excl. lease liabilities | FQ, FH, FY | LONG_TERM_DEBT_EXCL_CAPITAL_LEASE |
| Long term investments | FQ, FH, FY | LONG_TERM_INVESTMENTS |
| Minority interest | FQ, FH, FY | MINORITY_INTEREST |
| Net debt | FQ, FH, FY | NET_DEBT |
| Net intangible assets | FQ, FH, FY | INTANGIBLES_NET |
| Net property/plant/equipment | FQ, FH, FY | PPE_TOTAL_NET |
| Note receivable - long term | FQ, FH, FY | LONG_TERM_NOTE_RECEIVABLE |
| Notes payable | FY | NOTES_PAYABLE_SHORT_TERM_DEBT |
| Operating lease liabilities | FQ, FH, FY | OPERATING_LEASE_LIABILITIES |
| Other common equity | FQ, FH, FY | OTHER_COMMON_EQUITY |
| Other current assets, total | FQ, FH, FY | OTHER_CURRENT_ASSETS_TOTAL |
| Other current liabilities | FQ, FH, FY | OTHER_CURRENT_LIABILITIES |
| Other intangibles, net | FQ, FH, FY | OTHER_INTANGIBLES_NET |
| Other investments | FQ, FH, FY | OTHER_INVESTMENTS |
| Other long term assets, total | FQ, FH, FY | LONG_TERM_OTHER_ASSETS_TOTAL |
| Other non-current liabilities, total | FQ, FH, FY | OTHER_LIABILITIES_TOTAL |
| Other receivables | FQ, FH, FY | OTHER_RECEIVABLES |
| Other short term debt | FY | OTHER_SHORT_TERM_DEBT |
| Paid in capital | FQ, FH, FY | PAID_IN_CAPITAL |
| Preferred stock, carrying value | FQ, FH, FY | PREFERRED_STOCK_CARRYING_VALUE |
| Prepaid expenses | FQ, FH, FY | PREPAID_EXPENSES |
| Provision for risks & charge | FQ, FH, FY | PROVISION_F_RISKS |
| Retained earnings | FQ, FH, FY | RETAINED_EARNINGS |
| Shareholders’ equity | FQ, FH, FY | SHRHLDRS_EQUITY |
| Short term debt | FQ, FH, FY | SHORT_TERM_DEBT |
| Short term debt excl. current portion of LT debt | FQ, FH, FY | SHORT_TERM_DEBT_EXCL_CURRENT_PORT |
| Short term investments | FQ, FH, FY | SHORT_TERM_INVEST |
| Tangible book value per share | FQ, FH, FY | BOOK_TANGIBLE_PER_SHARE |
| Total assets | FQ, FH, FY | TOTAL_ASSETS |
| Total current assets | FQ, FH, FY | TOTAL_CURRENT_ASSETS |
| Total current liabilities | FQ, FH, FY | TOTAL_CURRENT_LIABILITIES |
| Total debt | FQ, FH, FY | TOTAL_DEBT |
| Total equity | FQ, FH, FY | TOTAL_EQUITY |
| Total inventory | FQ, FH, FY | TOTAL_INVENTORY |
| Total liabilities | FQ, FH, FY | TOTAL_LIABILITIES |
| Total liabilities & shareholders’ equities | FQ, FH, FY | TOTAL_LIABILITIES_SHRHLDRS_EQUITY |
| Total non-current assets | FQ, FH, FY | TOTAL_NON_CURRENT_ASSETS |
| Total non-current liabilities | FQ, FH, FY | TOTAL_NON_CURRENT_LIABILITIES |
| Total receivables, net | FQ, FH, FY | TOTAL_RECEIVABLES_NET |
| Treasury stock - common | FQ, FH, FY | TREASURY_STOCK_COMMON |
#### Cash flow
This table lists the available metrics that provide information about
how cash flows through a company.

Click to show/hide| Financial | period | financial_id |
| Amortization | FQ, FH, FY, TTM | AMORTIZATION |
| Capital expenditures | FQ, FH, FY, TTM | CAPITAL_EXPENDITURES |
| Capital expenditures - fixed assets | FQ, FH, FY, TTM | CAPITAL_EXPENDITURES_FIXED_ASSETS |
| Capital expenditures - other assets | FQ, FH, FY, TTM | CAPITAL_EXPENDITURES_OTHER_ASSETS |
| Cash from financing activities | FQ, FH, FY, TTM | CASH_F_FINANCING_ACTIVITIES |
| Cash from investing activities | FQ, FH, FY, TTM | CASH_F_INVESTING_ACTIVITIES |
| Cash from operating activities | FQ, FH, FY, TTM | CASH_F_OPERATING_ACTIVITIES |
| Change in accounts payable | FQ, FH, FY, TTM | CHANGE_IN_ACCOUNTS_PAYABLE |
| Change in accounts receivable | FQ, FH, FY, TTM | CHANGE_IN_ACCOUNTS_RECEIVABLE |
| Change in accrued expenses | FQ, FH, FY, TTM | CHANGE_IN_ACCRUED_EXPENSES |
| Change in inventories | FQ, FH, FY, TTM | CHANGE_IN_INVENTORIES |
| Change in other assets/liabilities | FQ, FH, FY, TTM | CHANGE_IN_OTHER_ASSETS |
| Change in taxes payable | FQ, FH, FY, TTM | CHANGE_IN_TAXES_PAYABLE |
| Changes in working capital | FQ, FH, FY, TTM | CHANGES_IN_WORKING_CAPITAL |
| Common dividends paid | FQ, FH, FY, TTM | COMMON_DIVIDENDS_CASH_FLOW |
| Deferred taxes (cash flow) | FQ, FH, FY, TTM | CASH_FLOW_DEFERRED_TAXES |
| Depreciation & amortization (cash flow) | FQ, FH, FY, TTM | CASH_FLOW_DEPRECATION_N_AMORTIZATION |
| Depreciation/depletion | FQ, FH, FY, TTM | DEPRECIATION_DEPLETION |
| Financing activities - other sources | FQ, FH, FY, TTM | OTHER_FINANCING_CASH_FLOW_SOURCES |
| Financing activities - other uses | FQ, FH, FY, TTM | OTHER_FINANCING_CASH_FLOW_USES |
| Free cash flow | FQ, FH, FY, TTM | FREE_CASH_FLOW |
| Funds from operations | FQ, FH, FY, TTM | FUNDS_F_OPERATIONS |
| Investing activities - other sources | FQ, FH, FY, TTM | OTHER_INVESTING_CASH_FLOW_SOURCES |
| Investing activities - other uses | FQ, FH, FY | OTHER_INVESTING_CASH_FLOW_USES |
| Issuance of long term debt | FQ, FH, FY, TTM | SUPPLYING_OF_LONG_TERM_DEBT |
| Issuance/retirement of debt, net | FQ, FH, FY, TTM | ISSUANCE_OF_DEBT_NET |
| Issuance/retirement of long term debt | FQ, FH, FY, TTM | ISSUANCE_OF_LONG_TERM_DEBT |
| Issuance/retirement of other debt | FQ, FH, FY, TTM | ISSUANCE_OF_OTHER_DEBT |
| Issuance/retirement of short term debt | FQ, FH, FY, TTM | ISSUANCE_OF_SHORT_TERM_DEBT |
| Issuance/retirement of stock, net | FQ, FH, FY, TTM | ISSUANCE_OF_STOCK_NET |
| Net income (cash flow) | FQ, FH, FY, TTM | NET_INCOME_STARTING_LINE |
| Non-cash items | FQ, FH, FY, TTM | NON_CASH_ITEMS |
| Other financing cash flow items, total | FQ, FH, FY, TTM | OTHER_FINANCING_CASH_FLOW_ITEMS_TOTAL |
| Other investing cash flow items, total | FQ, FH, FY | OTHER_INVESTING_CASH_FLOW_ITEMS_TOTAL |
| Preferred dividends paid | FQ, FH, FY | PREFERRED_DIVIDENDS_CASH_FLOW |
| Purchase of investments | FQ, FH, FY, TTM | PURCHASE_OF_INVESTMENTS |
| Purchase/acquisition of business | FQ, FH, FY, TTM | PURCHASE_OF_BUSINESS |
| Purchase/sale of business, net | FQ, FH, FY | PURCHASE_SALE_BUSINESS |
| Purchase/sale of investments, net | FQ, FH, FY, TTM | PURCHASE_SALE_INVESTMENTS |
| Reduction of long term debt | FQ, FH, FY, TTM | REDUCTION_OF_LONG_TERM_DEBT |
| Repurchase of common & preferred stock | FQ, FH, FY, TTM | PURCHASE_OF_STOCK |
| Sale of common & preferred stock | FQ, FH, FY, TTM | SALE_OF_STOCK |
| Sale of fixed assets & businesses | FQ, FH, FY, TTM | SALES_OF_BUSINESS |
| Sale/maturity of investments | FQ, FH, FY | SALES_OF_INVESTMENTS |
| Total cash dividends paid | FQ, FH, FY, TTM | TOTAL_CASH_DIVIDENDS_PAID |
#### Statistics
This table contains a variety of statistical metrics, including commonly
used financial ratios.

Click to show/hide| Financial | period | financial_id |
| Accruals | FQ, FH, FY | ACCRUALS_RATIO |
| Altman Z-score | FQ, FH, FY | ALTMAN_Z_SCORE |
| Asset turnover | FQ, FH, FY | ASSET_TURNOVER |
| Beneish M-score | FQ, FH, FY | BENEISH_M_SCORE |
| Buyback yield % | FQ, FH, FY | BUYBACK_YIELD |
| COGS to revenue ratio | FQ, FH, FY | COGS_TO_REVENUE |
| Cash conversion cycle | FQ, FY | CASH_CONVERSION_CYCLE |
| Cash to debt ratio | FQ, FH, FY | CASH_TO_DEBT |
| Current ratio | FQ, FH, FY | CURRENT_RATIO |
| Days inventory | FQ, FY | DAYS_INVENT |
| Days payable | FQ, FY | DAYS_PAY |
| Days sales outstanding | FQ, FY | DAY_SALES_OUT |
| Debt to EBITDA ratio | FQ, FH, FY | DEBT_TO_EBITDA |
| Debt to assets ratio | FQ, FH, FY | DEBT_TO_ASSET |
| Debt to equity ratio | FQ, FH, FY | DEBT_TO_EQUITY |
| Debt to revenue ratio | FQ, FH, FY | DEBT_TO_REVENUE |
| Dividend payout ratio % | FQ, FH, FY, TTM | DIVIDEND_PAYOUT_RATIO |
| Dividend yield % | FQ, FH, FY | DIVIDENDS_YIELD |
| Dividends per share - common stock primary issue | FQ, FH, FY, TTM | DPS_COMMON_STOCK_PRIM_ISSUE |
| EBITDA margin % | FQ, FH, FY, TTM | EBITDA_MARGIN |
| EPS basic one year growth | FQ, FH, FY, TTM | EARNINGS_PER_SHARE_BASIC_ONE_YEAR_GROWTH |
| EPS diluted one year growth | FQ, FH, FY | EARNINGS_PER_SHARE_DILUTED_ONE_YEAR_GROWTH |
| EPS estimates | FQ, FH, FY | EARNINGS_ESTIMATE |
| Effective interest rate on debt % | FQ, FH, FY | EFFECTIVE_INTEREST_RATE_ON_DEBT |
| Enterprise value | FQ, FH, FY | ENTERPRISE_VALUE |
| Enterprise value to EBIT ratio | FQ, FH, FY | EV_EBIT |
| Enterprise value to EBITDA ratio | FQ, FH, FY | ENTERPRISE_VALUE_EBITDA |
| Enterprise value to revenue ratio | FQ, FH, FY | EV_REVENUE |
| Equity to assets ratio | FQ, FH, FY | EQUITY_TO_ASSET |
| Float shares outstanding | FY | FLOAT_SHARES_OUTSTANDING |
| Free cash flow margin % | FQ, FH, FY | FREE_CASH_FLOW_MARGIN |
| Fulmer H factor | FQ, FY | FULMER_H_FACTOR |
| Goodwill to assets ratio | FQ, FH, FY | GOODWILL_TO_ASSET |
| Graham’s number | FQ, FY | GRAHAM_NUMBERS |
| Gross margin % | FQ, FH, FY, TTM | GROSS_MARGIN |
| Gross profit to assets ratio | FQ, FY | GROSS_PROFIT_TO_ASSET |
| Interest coverage | FQ, FH, FY | INTERST_COVER |
| Inventory to revenue ratio | FQ, FH, FY | INVENT_TO_REVENUE |
| Inventory turnover | FQ, FH, FY | INVENT_TURNOVER |
| KZ index | FY | KZ_INDEX |
| Long term debt to total assets ratio | FQ, FH, FY | LONG_TERM_DEBT_TO_ASSETS |
| Net current asset value per share | FQ, FY | NCAVPS_RATIO |
| Net income per employee | FY | NET_INCOME_PER_EMPLOYEE |
| Net margin % | FQ, FH, FY, TTM | NET_MARGIN |
| Number of employees | FY | NUMBER_OF_EMPLOYEES |
| Operating earnings yield % | FQ, FH, FY | OPERATING_EARNINGS_YIELD |
| Operating margin % | FQ, FH, FY | OPERATING_MARGIN |
| PEG ratio | FQ, FY | PEG_RATIO |
| Piotroski F-score | FQ, FH, FY | PIOTROSKI_F_SCORE |
| Price earnings ratio forward | FQ, FY | PRICE_EARNINGS_FORWARD |
| Price sales ratio forward | FQ, FY | PRICE_SALES_FORWARD |
| Quality ratio | FQ, FH, FY | QUALITY_RATIO |
| Quick ratio | FQ, FH, FY | QUICK_RATIO |
| Research & development to revenue ratio | FQ, FH, FY | RESEARCH_AND_DEVELOP_TO_REVENUE |
| Return on assets % | FQ, FH, FY | RETURN_ON_ASSETS |
| Return on common equity % | FQ, FH, FY | RETURN_ON_COMMON_EQUITY |
| Return on equity % | FQ, FH, FY | RETURN_ON_EQUITY |
| Return on equity adjusted to book value % | FQ, FH, FY | RETURN_ON_EQUITY_ADJUST_TO_BOOK |
| Return on invested capital % | FQ, FH, FY | RETURN_ON_INVESTED_CAPITAL |
| Return on tangible assets % | FQ, FH, FY | RETURN_ON_TANG_ASSETS |
| Return on tangible equity % | FQ, FH, FY | RETURN_ON_TANG_EQUITY |
| Revenue estimates | FQ, FH, FY | SALES_ESTIMATES |
| Revenue one year growth | FQ, FH, FY, TTM | REVENUE_ONE_YEAR_GROWTH |
| Revenue per employee | FY | REVENUE_PER_EMPLOYEE |
| Shares buyback ratio % | FQ, FH, FY | SHARE_BUYBACK_RATIO |
| Sloan ratio % | FQ, FH, FY | SLOAN_RATIO |
| Springate score | FQ, FY | SPRINGATE_SCORE |
| Sustainable growth rate | FQ, FY | SUSTAINABLE_GROWTH_RATE |
| Tangible common equity ratio | FQ, FH, FY | TANGIBLE_COMMON_EQUITY_RATIO |
| Tobin’s Q (approximate) | FQ, FH, FY | TOBIN_Q_RATIO |
| Total common shares outstanding | FQ, FH, FY | TOTAL_SHARES_OUTSTANDING |
| Zmijewski score | FQ, FY | ZMIJEWSKI_SCORE |
## ​ request.economic() ​
The request.economic() function provides scripts with the ability to retrieve economic data for
a specified country or region, including information about the state of
the economy (GDP, inflation rate, etc.) or of a particular industry
(steel production, ICU beds, etc.).

Below is the signature for this function:

```
request.economic(country_code, field, gaps, ignore_invalid_symbol) → series float
```
The country_code parameter accepts a “string” value representing
the identifier of the country or region to request economic data for
(e.g., “US”, “EU”, etc.). See the Country/region codes section for a complete list of codes this function supports.
Note that the economic metrics available depend on the country or region
specified in the function call.

The field parameter accepts a “string” specifying the metric that the function requests.
The Field codes section covers all accessible metrics and the
countries/regions they’re available for.

For a detailed explanation on the last two parameters of this function,
see the Common characteristics section at the top of this page.

This simple example requests the growth rate of the Gross Domestic
Product (“GDPQQ”) for the United States (“US”) using request.economic() ,
then plots its value on the
chart with a gradient color :

Note that:

- This example does not include a gaps argument in the request.economic() call, so the function uses the default barmerge.gaps_off .
In other words, it returns the last retrieved value when new
data isn’t yet available.
Tip The tables in the sections below are rather large, because there are numerous country_code and field arguments available. Use the “Click to show/hide” option above each table to toggle its visibility.

### Country/region codes
The table in this section lists all country/region codes available for
use with request.economic() .
The first column of the table contains the “string” values that
represent the country or region code, and the second column contains the
corresponding country/region names.

It’s important to note that the value used as the country_code argument determines which field codes are accessible to the function.

Click to show/hide| country_code | Country/region name |
| AF | Afghanistan |
| AL | Albania |
| DZ | Algeria |
| AD | Andorra |
| AO | Angola |
| AG | Antigua and Barbuda |
| AR | Argentina |
| AM | Armenia |
| AW | Aruba |
| AU | Australia |
| AT | Austria |
| AZ | Azerbaijan |
| BS | Bahamas |
| BH | Bahrain |
| BD | Bangladesh |
| BB | Barbados |
| BY | Belarus |
| BE | Belgium |
| BZ | Belize |
| BJ | Benin |
| BM | Bermuda |
| BT | Bhutan |
| BO | Bolivia |
| BA | Bosnia and Herzegovina |
| BW | Botswana |
| BR | Brazil |
| BN | Brunei |
| BG | Bulgaria |
| BF | Burkina Faso |
| BI | Burundi |
| KH | Cambodia |
| CM | Cameroon |
| CA | Canada |
| CV | Cape Verde |
| KY | Cayman Islands |
| CF | Central African Republic |
| TD | Chad |
| CL | Chile |
| CN | China |
| CO | Colombia |
| KM | Comoros |
| CG | Congo |
| CR | Costa Rica |
| HR | Croatia |
| CU | Cuba |
| CY | Cyprus |
| CZ | Czech Republic |
| DK | Denmark |
| DJ | Djibouti |
| DM | Dominica |
| DO | Dominican Republic |
| TL | East Timor |
| EC | Ecuador |
| EG | Egypt |
| SV | El Salvador |
| GQ | Equatorial Guinea |
| ER | Eritrea |
| EE | Estonia |
| ET | Ethiopia |
| EU | Euro area |
| FO | Faroe Islands |
| FJ | Fiji |
| FI | Finland |
| FR | France |
| GA | Gabon |
| GM | Gambia |
| GE | Georgia |
| DE | Germany |
| GH | Ghana |
| GR | Greece |
| GL | Greenland |
| GD | Grenada |
| GT | Guatemala |
| GN | Guinea |
| GW | Guinea Bissau |
| GY | Guyana |
| HT | Haiti |
| HN | Honduras |
| HK | Hong Kong |
| HU | Hungary |
| IS | Iceland |
| IN | India |
| ID | Indonesia |
| IR | Iran |
| IQ | Iraq |
| IE | Ireland |
| IM | Isle of Man |
| IL | Israel |
| IT | Italy |
| CI | Ivory Coast |
| JM | Jamaica |
| JP | Japan |
| JO | Jordan |
| KZ | Kazakhstan |
| KE | Kenya |
| KI | Kiribati |
| XK | Kosovo |
| KW | Kuwait |
| KG | Kyrgyzstan |
| LA | Laos |
| LV | Latvia |
| LB | Lebanon |
| LS | Lesotho |
| LR | Liberia |
| LY | Libya |
| LI | Liechtenstein |
| LT | Lithuania |
| LU | Luxembourg |
| MO | Macau |
| MK | Macedonia |
| MG | Madagascar |
| MW | Malawi |
| MY | Malaysia |
| MV | Maldives |
| ML | Mali |
| MT | Malta |
| MR | Mauritania |
| MU | Mauritius |
| MX | Mexico |
| MD | Moldova |
| MC | Monaco |
| MN | Mongolia |
| ME | Montenegro |
| MA | Morocco |
| MZ | Mozambique |
| MM | Myanmar |
| NA | Namibia |
| NP | Nepal |
| NL | Netherlands |
| NC | New Caledonia |
| NZ | New Zealand |
| NI | Nicaragua |
| NE | Niger |
| NG | Nigeria |
| KP | North Korea |
| NO | Norway |
| OM | Oman |
| PK | Pakistan |
| PS | Palestine |
| PA | Panama |
| PG | Papua New Guinea |
| PY | Paraguay |
| PE | Peru |
| PH | Philippines |
| PL | Poland |
| PT | Portugal |
| PR | Puerto Rico |
| QA | Qatar |
| CD | Republic of the Congo |
| RO | Romania |
| RU | Russia |
| RW | Rwanda |
| WS | Samoa |
| SM | San Marino |
| ST | Sao Tome and Principe |
| SA | Saudi Arabia |
| SN | Senegal |
| RS | Serbia |
| SC | Seychelles |
| SL | Sierra Leone |
| SG | Singapore |
| SK | Slovakia |
| SI | Slovenia |
| SB | Solomon Islands |
| SO | Somalia |
| ZA | South Africa |
| KR | South Korea |
| SS | South Sudan |
| ES | Spain |
| LK | Sri Lanka |
| LC | St Lucia |
| VC | St Vincent and the Grenadines |
| SD | Sudan |
| SR | Suriname |
| SZ | Swaziland |
| SE | Sweden |
| CH | Switzerland |
| SY | Syria |
| TW | Taiwan |
| TJ | Tajikistan |
| TZ | Tanzania |
| TH | Thailand |
| TG | Togo |
| TO | Tonga |
| TT | Trinidad and Tobago |
| TN | Tunisia |
| TR | Turkey |
| TM | Turkmenistan |
| UG | Uganda |
| UA | Ukraine |
| AE | United Arab Emirates |
| GB | United Kingdom |
| US | United States |
| UY | Uruguay |
| UZ | Uzbekistan |
| VU | Vanuatu |
| VE | Venezuela |
| VN | Vietnam |
| YE | Yemen |
| ZM | Zambia |
| ZW | Zimbabwe |
### Field codes
The table in this section lists the field codes available for use with request.economic() .
The first column contains the “string” values used as the field argument, and the second column contains names of each metric and links
to our Help Center with additional information, including the
countries/regions they’re available for.

Click to show/hide| field | Metric |
| AA | Asylum Applications |
| ACR | API Crude Runs |
| AE | Auto Exports |
| AHE | Average Hourly Earnings |
| AHO | API Heating Oil |
| AWH | Average Weekly Hours |
| BBS | Banks Balance Sheet |
| BCLI | Business Climate Indicator |
| BCOI | Business Confidence Index |
| BI | Business Inventories |
| BLR | Bank Lending Rate |
| BOI | NFIB Business Optimism Index |
| BOT | Balance Of Trade |
| BP | Building Permits |
| BR | Bankruptcies |
| CA | Current Account |
| CAG | Current Account To GDP |
| CAP | Car Production |
| CAR | Car Registrations |
| CBBS | Central Bank Balance Sheet |
| CCC | Claimant Count Change |
| CCI | Consumer Confidence Index |
| CCOS | Cushing Crude Oil Stocks |
| CCP | Core Consumer Prices |
| CCPI | Core CPI |
| CCPT | Consumer Confidence Price Trends |
| CCR | Consumer Credit |
| CCS | Credit Card Spending |
| CEP | Cement Production |
| CF | Capital Flows |
| CFNAI | Chicago Fed National Activity Index |
| CI | API Crude Imports |
| CIND | Coincident Index |
| CIR | Core Inflation Rate, YoY |
| CJC | Continuing Jobless Claims |
| CN | API Cushing Number |
| COI | Crude Oil Imports |
| COIR | Crude Oil Imports from Russia |
| CONSTS | Construction Spending |
| COP | Crude Oil Production |
| COR | Crude Oil Rigs |
| CORD | Construction Orders, YoY |
| CORPI | Corruption Index |
| CORR | Corruption Rank |
| COSC | Crude Oil Stocks Change |
| COUT | Construction Output, YoY |
| CP | Copper Production |
| CPCEPI | Core PCE Price Index |
| CPI | Consumer Price Index |
| CPIHU | CPI Housing Utilities |
| CPIM | CPI Median |
| CPIT | CPI Transportation |
| CPITM | CPI Trimmed Mean |
| CPMI | Chicago PMI |
| CPPI | Core Producer Price Index |
| CPR | Corporate Profits |
| CRLPI | Cereals Price Index |
| CRR | Cash Reserve Ratio |
| CS | Consumer Spending |
| CSC | API Crude Oil Stock Change |
| CSHPI | Case Shiller Home Price Index |
| CSHPIMM | Case Shiller Home Price Index, MoM |
| CSHPIYY | Case Shiller Home Price Index, YoY |
| CSS | Chain Store Sales |
| CTR | Corporate Tax Rate |
| CU | Capacity Utilization |
| DFMI | Dallas Fed Manufacturing Index |
| DFP | Distillate Fuel Production |
| DFS | Distillate Stocks |
| DFSI | Dallas Fed Services Index |
| DFSRI | Dallas Fed Services Revenues Index |
| DG | Deposit Growth |
| DGO | Durable Goods Orders |
| DGOED | Durable Goods Orders Excluding Defense |
| DGOET | Durable Goods Orders Excluding Transportation |
| DIR | Deposit Interest Rate |
| DPI | Disposable Personal Income |
| DRPI | Dairy Price Index |
| DS | API Distillate Stocks |
| DT | CBI Distributive Trades |
| EC | ADP Employment Change |
| ED | External Debt |
| EDBR | Ease Of Doing Business Ranking |
| EHS | Existing Home Sales |
| ELP | Electricity Production |
| EMC | Employment Change |
| EMCI | Employment Cost Index |
| EMP | Employed Persons |
| EMR | Employment Rate |
| EOI | Economic Optimism Index |
| EP | Export Prices |
| ESI | ZEW Economic Sentiment Index |
| EWS | Economy Watchers Survey |
| EXP | Exports |
| EXPYY | Exports, YoY |
| FAI | Fixed Asset Investment |
| FBI | Foreign Bond Investment |
| FDI | Foreign Direct Investment |
| FE | Fiscal Expenditure |
| FER | Foreign Exchange Reserves |
| FI | Food Inflation, YoY |
| FO | Factory Orders |
| FOET | Factory Orders Excluding Transportation |
| FPI | Food Price Index |
| FSI | Foreign Stock Investment |
| FTE | Full Time Employment |
| FYGDPG | Full Year GDP Growth |
| GASP | Gasoline Prices |
| GBP | Government Budget |
| GBV | Government Budget Value |
| GCI | Competitiveness Index |
| GCR | Competitiveness Rank |
| GD | Government Debt |
| GDG | Government Debt To GDP |
| GDP | Gross Domestic Product |
| GDPA | GDP From Agriculture |
| GDPC | GDP From Construction |
| GDPCP | GDP Constant Prices |
| GDPD | GDP Deflator |
| GDPGA | GDP Growth Annualized |
| GDPMAN | GDP From Manufacturing |
| GDPMIN | GDP From Mining |
| GDPPA | GDP From Public Administration |
| GDPPC | GDP Per Capita |
| GDPPCP | GDP Per Capita, PPP |
| GDPQQ | GDP Growth Rate |
| GDPS | GDP From Services |
| GDPSA | GDP Sales |
| GDPT | GDP From Transport |
| GDPU | GDP From Utilities |
| GDPYY | GDP, YoY |
| GDTPI | Global Dairy Trade Price Index |
| GFCF | Gross Fixed Capital Formation |
| GNP | Gross National Product |
| GP | Gold Production |
| GPA | Government Payrolls |
| GPRO | Gasoline Production |
| GR | Government Revenues |
| GRES | Gold Reserves |
| GS | API Gasoline Stocks |
| GSC | Grain Stocks Corn |
| GSCH | Gasoline Stocks Change |
| GSG | Government Spending To GDP |
| GSP | Government Spending |
| GSS | Grain Stocks Soy |
| GSW | Grain Stocks Wheat |
| GTB | Goods Trade Balance |
| HB | Hospital Beds |
| HDG | Households Debt To GDP |
| HDI | Households Debt To Income |
| HICP | Harmonised Index of Consumer Prices |
| HIRMM | Harmonised Inflation Rate, MoM |
| HIRYY | Harmonised Inflation Rate, YoY |
| HMI | NAHB Housing Market Index |
| HOR | Home Ownership Rate |
| HOS | Heating Oil Stocks |
| HOSP | Hospitals |
| HPI | House Price Index |
| HPIMM | House Price Index, MoM |
| HPIYY | House Price Index, YoY |
| HS | Home Loans |
| HSP | Household Spending |
| HST | Housing Starts |
| IC | Changes In Inventories |
| ICUB | ICU Beds |
| IE | Inflation Expectations |
| IFOCC | IFO Assessment Of The Business Situation |
| IFOE | IFO Business Developments Expectations |
| IJC | Initial Jobless Claims |
| IMP | Imports |
| IMPYY | Imports, YoY |
| INBR | Interbank Rate |
| INTR | Interest Rate |
| IPA | IP Addresses |
| IPMM | Industrial Production, MoM |
| IPRI | Import Prices |
| IPYY | Industrial Production, YoY |
| IRMM | Inflation Rate, MoM |
| IRYY | Inflation Rate, YoY |
| IS | Industrial Sentiment |
| ISP | Internet Speed |
| JA | Job Advertisements |
| JAR | Jobs To Applications Ratio |
| JC | Challenger Job Cuts |
| JC4W | Jobless Claims, 4-Week Average |
| JO | Job Offers |
| JV | Job Vacancies |
| KFMI | Kansas Fed Manufacturing Index |
| LB | Loans To Banks |
| LC | Labor Costs |
| LEI | Leading Economic Index |
| LFPR | Labor Force Participation Rate |
| LG | Loan Growth, YoY |
| LIVRR | Liquidity Injections Via Reverse Repo |
| LMIC | LMI Logistics Managers Index Current |
| LMICI | LMI Inventory Costs |
| LMIF | LMI Logistics Managers Index Future |
| LMITP | LMI Transportation Prices |
| LMIWP | LMI Warehouse Prices |
| LPS | Loans To Private Sector |
| LR | Central Bank Lending Rate |
| LTUR | Long Term Unemployment Rate |
| LWF | Living Wage Family |
| LWI | Living Wage Individual |
| M0 | Money Supply M0 |
| M1 | Money Supply M1 |
| M2 | Money Supply M2 |
| M3 | Money Supply M3 |
| MA | Mortgage Approvals |
| MAPL | Mortgage Applications |
| MCE | Michigan Consumer Expectations |
| MCEC | Michigan Current Economic Conditions |
| MD | Medical Doctors |
| ME | Military Expenditure |
| MGDPYY | Monthly GDP, YoY |
| MIE1Y | Michigan Inflation Expectations |
| MIE5Y | Michigan 5 Year Inflation Expectations |
| MIP | Mining Production, YoY |
| MMI | MBA Mortgage Market Index |
| MO | Machinery Orders |
| MP | Manufacturing Payrolls |
| MPI | Meat Price Index |
| MPRMM | Manufacturing Production, MoM |
| MPRYY | Manufacturing Production, YoY |
| MR | Mortgage Rate |
| MRI | MBA Mortgage Refinance Index |
| MS | Manufacturing Sales |
| MTO | Machine Tool Orders |
| MW | Minimum Wages |
| NDCGOEA | Orders For Non-defense Capital Goods Excluding Aircraft |
| NEGTB | Goods Trade Deficit With Non-EU Countries |
| NFP | Nonfarm Payrolls |
| NGI | Natural Gas Imports |
| NGIR | Natural Gas Imports from Russia |
| NGSC | Natural Gas Stocks Change |
| NHPI | Nationwide House Price Index |
| NHS | New Home Sales |
| NHSMM | New Home Sales, MoM |
| NMPMI | Non-Manufacturing PMI |
| NO | New Orders |
| NODXMM | Non-Oil Domestic Exports, MoM |
| NODXYY | Non-Oil Domestic Exports, YoY |
| NOE | Non-Oil Exports |
| NPP | Nonfarm Payrolls Private |
| NURS | Nurses |
| NYESMI | NY Empire State Manufacturing Index |
| OE | Oil Exports |
| OPI | Oils Price Index |
| PCEPI | PCE Price Index |
| PDG | Private Debt To GDP |
| PFMI | Philadelphia Fed Manufacturing Index |
| PHSIMM | Pending Home Sales Index, MoM |
| PHSIYY | Pending Home Sales Index, YoY |
| PI | Personal Income |
| PIN | Private Investment |
| PIND | MBA Purchase Index |
| PITR | Personal Income Tax Rate |
| POP | Population |
| PPI | Producer Price Index |
| PPII | Producer Price Index Input |
| PPIMM | Producer Price Inflation, MoM |
| PPIYY | Producer Prices Index, YoY |
| PRI | API Product Imports |
| PROD | Productivity |
| PS | Personal Savings |
| PSC | Private Sector Credit |
| PSP | Personal Spending |
| PTE | Part Time Employment |
| PUAC | Pandemic Unemployment Assistance Claims |
| RAM | Retirement Age Men |
| RAW | Retirement Age Women |
| RCR | Refinery Crude Runs |
| REM | Remittances |
| RFMI | Richmond Fed Manufacturing Index |
| RFMSI | Richmond Fed Manufacturing Shipments Index |
| RFSI | Richmond Fed Services Index |
| RI | Redbook Index |
| RIEA | Retail Inventories Excluding Autos |
| RPI | Retail Price Index |
| RR | Repo Rate |
| RRR | Reverse Repo Rate |
| RSEA | Retail Sales Excluding Autos |
| RSEF | Retail Sales Excluding Fuel |
| RSMM | Retail Sales, MoM |
| RSYY | Retail Sales, YoY |
| RTI | Reuters Tankan Index |
| SBSI | Small Business Sentiment Index |
| SFHP | Single Family Home Prices |
| SP | Steel Production |
| SPI | Sugar Price Index |
| SS | Services Sentiment |
| SSR | Social Security Rate |
| SSRC | Social Security Rate For Companies |
| SSRE | Social Security Rate For Employees |
| STR | Sales Tax Rate |
| TA | Tourist Arrivals |
| TAXR | Tax Revenue |
| TCB | Treasury Cash Balance |
| TCPI | Tokyo CPI |
| TI | Terrorism Index |
| TII | Tertiary Industry Index |
| TOT | Terms Of Trade |
| TR | Tourism Revenues |
| TVS | Total Vehicle Sales |
| UC | Unemployment Change |
| UP | Unemployed Persons |
| UR | Unemployment Rate |
| WAG | Wages |
| WES | Weapons Sales |
| WG | Wage Growth, YoY |
| WHS | Wages High Skilled |
| WI | Wholesale Inventories |
| WLS | Wages Low Skilled |
| WM | Wages In Manufacturing |
| WPI | Wholesale Price Index |
| WS | Wholesale Sales |
| YUR | Youth Unemployment Rate |
| ZCC | ZEW Current Conditions |
## ​ request.footprint() ​
The request.footprint() function enables scripts to retrieve volume footprint data for the bars in the datasets on which they run. For a given bar, a volume footprint categorizes volume values from lower timeframes as “buy” (upward) or “sell” (downward) based on intrabar price action, then collects the categorized volume data into equally sized rows that cover the bar’s price range. Programmers can use retrieved footprint data to inspect the distribution of “buy”, “sell”, and total volume across the rows for a bar’s range, identify a bar’s Point of Control (POC) and other significant price levels, calculate volume delta information, detect volume imbalances, and more.

Note Volume footprints are available exclusively to users who have a Premium or Ultimate plan . Accounts with lower-tier plans cannot use scripts that request volume footprint data with the request.footprint() function.

The function’s signature is as follows:

```
request.footprint(ticks_per_row, va_percent, imbalance_percent) → series footprint
```
The ticks_per_row parameter specifies the size of each row in the calculated volume footprint, in ticks. It requires a positive “simple int” value representing a multiplier for the instrument’s minimum tick size. For example, if the argument is 100, the price range of each row equals the value of 100 * syminfo.mintick . The specified row size affects the total number of rows in each bar’s footprint. Increase the value for fewer rows with a larger size, or decrease the value for the opposite.

The va_percent parameter accepts a “simple float” value specifying the percentage of the footprint’s total volume to use for calculating the bar’s Value Area (VA) , where a value of 100 represents 100% of the total volume. Specifying an argument is optional. The default value is 70, meaning that the footprint’s VA includes 70% of the total volume.

The imbalance_percent parameter accepts a “simple float” value specifying the required percentage difference between “buy” and “sell” volume in adjacent footprint rows for detecting volume imbalances :

- The footprint considers a row to have a buy imbalance if the row’s “buy” volume exceeds the “sell” volume of the row below it by the specified percentage.
- The footprint considers a row to have a sell imbalance if the row’s “sell” volume exceeds the “buy” volume of the row above it by the given percentage.
Including an imbalance_percent argument is optional. The default value is 300, meaning that the “buy” or “sell” volume of a footprint row must be three times (300%) larger than the opposing volume of an adjacent row to signify an imbalance.

A call to the request.footprint() function returns either the reference (ID) of a footprint object that contains the volume footprint data for the current bar, or na if no footprint is available for that bar.

Notice Scripts cannot perform more than one footprint request with the request.footprint() function. If a script contains multiple calls to this function, it raises a runtime error .

Scripts can use any returned footprint ID that is not na in calls to the built-in footprint.*() functions to retrieve data from a bar’s volume footprint.

For example, the following script calls request.footprint() on each bar to request the ID of a footprint object that contains the bar’s volume footprint data. If the requested data is available, the script then uses the returned ID in calls to four footprint.*() functions – footprint.total_volume() , footprint.buy_volume() , footprint.sell_volume() , and footprint.delta() – to retrieve the footprint’s total volume, total “buy” and “sell” volume, and overall volume delta.

The script plots the “buy” volume, the negative “sell” volume, and the volume delta as columns for visual comparison. It also displays a color-coded label at each bar’s high price to indicate whether the bar’s “buy” volume exceeds its “sell” volume or vice versa. Hovering over a label reveals a tooltip that shows the corresponding bar’s total volume and volume delta:

Note that:

- The id parameter of each footprint.*() function does not allow na arguments. Therefore, this script uses ternary operations that execute footprint.*() calls only if the retrieved footprint ID is not na . If no data is available, the operations return na directly without executing the calls.
- On timeframes higher than or equal to “1D”, a footprint’s total volume might differ significantly from the value of the volume variable. Such differences occur for some instruments because EOD data feeds can include data from block trades, OTC trades, and other sources, whereas requested intraday data feeds do not. See the Data feeds section to learn more about the types of data feeds and their differences.
While some of the footprint.*() functions retrieve values representing overall metrics for a requested volume footprint, as shown above, others retrieve the IDs of volume_row objects that contain data for individual rows from the footprint for more detailed analysis. For instance, the footprint.poc() function retrieves the ID of the volume_row object that contains data for a footprint’s Point of Control row (i.e., the row with the highest total volume), and the footprint.rows() function constructs an array containing the volume_row IDs for every row within a footprint.

Scripts can use non-na IDs of the volume_row type in calls to the built-in volume_row.*() functions to retrieve data for a specific footprint row, including the row’s price levels, volume sums, volume delta, and buy or sell imbalances.

The advanced example below retrieves and displays detailed volume footprint information for visible chart bars. On each visible bar, the script requests a footprint ID using request.footprint() . If the ID is not na , the script calls footprint.rows() to create an array containing the volume_row IDs for all rows in the footprint, and uses other footprint.*() calls to retrieve the individual IDs for the footprint’s POC and Value Area rows.

Afterward, the script loops through the array using a for...in loop . It calls multiple volume_row.*() functions within the loop to retrieve price levels, categorized volume values, volume delta, and imbalance states for each row. On each iteration, the script formats the retrieved “buy” and “sell” volume, volume delta, and imbalance information for the current row into a string, and then displays the text in a box drawn at the row’s price range in a separate pane. Each box uses a gradient background color based on the row’s volume delta and its total volume relative to the POC row’s total volume. The text color of each box is the chart’s foreground color if the row is the POC, purple if the row is a VA boundary, and gray otherwise.

The script also plots the retrieved POC levels and the VA boundaries as circles on the main chart pane for visual reference:

Note that:

- As with the built-in functions for most other reference types , scripts can call footprint.*() and volume_row.*() built-ins as functions or methods . This script calls the built-ins using method syntax .
- The array created by footprint.rows() sorts its elements in ascending order by price level, where the first element refers to the volume_row object for the row with the lowest prices, and the last refers to the one for the row with the highest prices.
- The results of volume_row.has_buy_imbalance() and volume_row.has_sell_imbalance() calls depend on the imbalance_percent argument of the request.footprint() call that creates the parent footprint object. In this example, the “Imbalance percentage” input controls the argument, and therefore controls the behavior of the script’s volume_row.has_*_imbalance() calls.
To learn more about the footprint and volume_row types, and the available functions in their namespaces, refer to the footprint and volume_row section of the Type system page.

For more information about volume footprints and how they work, refer to the Volume footprint charts article in our Help Center.

### Requesting footprints on other datasets
Scripts can request volume footprint data, or the results of calculations that use footprint data, from other datasets by passing an expression that returns or uses IDs of the footprint or volume_row type as the expression argument in a request.security() or request.security_lower_tf() function call. If a call to either of these functions requests the result of an expression that relies on volume footprint data, it calculates footprints on the specified dataset rather than the script’s main dataset.

For example, the following script requests volume footprint data for the last confirmed period on a specified higher timeframe , then uses the data to display boxes across the current period for footprint rows whose total volume equals or exceeds an input percentage of the Point of Control (POC) row’s total volume.

The script uses a request.security() call with request.footprint(ticksInput)[1] as the expression argument and barmerge.lookahead_on as the lookahead argument to fetch the last confirmed footprint ID for the selected timeframe. If the result is not na at the start of the current HTF period, the script compares each row’s volume to the volume of the POC row in a for…in loop, and draws boxes to project the levels of rows whose volume meets the specified threshold. Each box uses a volume-based gradient color, where blue hues correspond to rows with lower volume, and orange hues correspond to rows with higher volume:

Note that:

- The request.security() call includes barmerge.gaps_on as the gaps argument to return a non-na footprint ID only on the first chart bar of each new HTF period, because the script does not require new footprint data on every bar.
- The script calls the time() and time_close() functions to retrieve the expected opening and closing timestamps for the current HTF period. The box drawings use these timestamps as their left and right coordinates.
Any request.security() or request.security_lower_tf() call whose expression depends on footprint objects counts toward the total number of request.footprint() calls, because such requests copy all code required to calculate the result on the retrieved dataset. A script raises a runtime error if its outputs depend on data from more than one unique request.footprint() call, regardless of whether those requests execute on the script’s main dataset or on the datasets fetched by other request.*() calls.

Consider the following script, which defines a calculation that requests volume footprint data for the current dataset, computes a moving average of the POC row’s median price, then declares a pocMA variable to store the average. The script uses the variable as the expression argument in a request.security() call to calculate the average POC level on the “1D” timeframe, then assigns the result to the requestedMA variable. Lastly, the script attempts to plot both the pocMA and requestedMA series on the chart, but fails and raises a runtime error :

The above script raises an error because its outputs (in this case, its plots ) depend on both the pocMA and requestedMA variables, and the values of those variables depend on two separate footprint requests – one for the script’s main dataset and the other for the dataset retrieved by the request.security() call. Both of these requests count toward the total number of request.footprint() calls, even though one of those calls is not defined explicitly in the code.

A simple way to resolve this error is to remove one of the script’s two plot() calls. As explained in the Compiled tokens section of the Limitations page, the Pine Script compiler automatically discards code that a script’s outputs do not depend on, including request.*() calls. Therefore, if we remove the plot of the pocMA series, for example, the request.footprint() call defined explicitly in the global scope does not execute. Instead, only the request.footprint() call copied into the request.security() call’s context executes, because that is the only one that the script’s outputs now require:

Note that:

- Although the pocMA variable declaration and its dependencies no longer execute directly, the Pine Profiler displays performance details next to that code in the Pine Editor. Those details represent the performance of the copied calculations that execute within the request.security() call’s context in this case, as the profiler cannot display that information elsewhere. See the When requesting other contexts section of the Profiling and optimization page to learn more about this behavior.
## ​ request.seed() ​
TradingView aggregates a vast amount of data from its many providers, including price and volume information on tradable instruments, financials, economic data, and more, which users can retrieve in Pine Script using the functions discussed in the sections above, as well as multiple built-in variables.

To further expand the horizons of possible data one can analyze on TradingView, we have Pine Seeds , which allows users to supply custom user-maintained EOD data feeds via GitHub for use on TradingView charts and within Pine Script code.

Notice The creation of new Pine Seeds repositories is currently unavailable . However, the data feeds from existing repositories are still accessible to charts and scripts. The Pine Seeds documentation on GitHub provides in-depth information about Pine Seeds functionality and instructions for requesting the return of full Pine Seeds support.

To retrieve data from a Pine Seeds data feed within a script, use the request.seed() function. Below is the function’s signature:

```
request.seed(source, symbol, expression, ignore_invalid_symbol, calc_bars_count) → series <type>
```
The source parameter specifies the unique name of the user-maintained GitHub repository that contains the data feed.

The symbol parameter represents the file name from the “data/” directory of the source repository, excluding the “.csv” file extension. See this page for information about the structure of the data stored in repositories.

The expression parameter is the series to evaluate using data extracted from the requested context. It is similar to the equivalent in request.security() and request.security_lower_tf() . Data feeds stored in user-maintained repos contain time , open , high , low , close , and volume information, meaning the expression argument can use the corresponding built-in variables, including variables derived from them (e.g., bar_index , ohlc4 , etc.) to request their values from the context of the custom data.

The script below visualizes sample data from the seed_crypto_santiment demo repository. It uses two calls to request.seed() to retrieve the close values from the repository’s BTC_SENTIMENT_POSITIVE_TOTAL and BTC_SENTIMENT_NEGATIVE_TOTAL data feeds and plots the results on the chart as step lines:

Note that:

- This example requests data from the repository highlighted in the Pine Seeds documentation . It exists solely for example purposes, and its data does not update on a regular basis.
- Unlike most other request.*() functions, request.seed() does not have a gaps parameter. It always returns na values when no new data exists.
- Pine Seeds data is searchable from the chart’s symbol search bar. To load a data feed on the chart, enter the “Repo:File” pair , similar to searching for an “Exchange:Symbol” pair.
PreviousNon-standard charts dataNextRepainting## On this page
IntroductionCommon characteristicsBehaviorgapsignore_invalid_symbolcurrencylookaheadDynamic requests​“series” argumentsIn local scopesIn librariesNested requestsData feedsrequest.security()TimeframesHigher timeframesLower timeframesRequestable dataBuilt-in variables and functionsDeclared variablesTuplesUser-defined functionsChart pointsCollectionsUser-defined typesrequest.security_lower_tf()Requesting intrabar dataIntrabar data arraysTuples of intrabar dataRequesting collectionsCustom contextsHistorical and realtime behaviorAvoiding repaintingHigher-timeframe dataLower-timeframe datarequest.currency_rate()request.dividends(), request.splits(), and request.earnings()request.financial()Calculating financial metricsFinancial IDsIncome statementsBalance sheetCash flowStatisticsrequest.economic()Country/region codesField codesrequest.footprint()Requesting footprints on other datasetsrequest.seed()
