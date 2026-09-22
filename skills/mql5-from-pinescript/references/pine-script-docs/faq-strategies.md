<!-- source: https://www.tradingview.com/pine-script-docs/faq/strategies/ | fetched 2026-09-23 | why: broker-emulator & next-bar-open fill Q&A behind our execution model -->

User ManualFAQ# Strategies
Using Pine Script ® strategy scripts, users can test simulated trades on historical and realtime data, to backtest and forward test trading systems. Strategies are similar to indicators, but with added capabilities such as placing, modifying, and canceling simulated orders and analyzing their results. Scripts that use the strategy() function as their declaration statement gain access to the strategy.* namespace, which contains functions and variables for simulating orders and retrieving strategy information.

When a user applies a strategy that uses order placement commands to the chart, the strategy uses the broker emulator to calculate simulated trades, and displays hypothetical performance results in a strategy report in the chart’s bottom panel.

Strategies support various types of orders including market, limit, stop, and stop-limit orders, allowing programmers to simulate different trading scenarios. Strategy order commands can send alerts when order fill events occur. An order fill event is triggered by the broker emulator when it executes a simulated order in realtime.

For a thorough exploration of strategy features, capabilities, and usage, refer to the Strategies section in the User Manual.

## Strategy basics
### How can I turn my indicator into a strategy?
To convert an indicator to a strategy, begin by replacing the indicator() declaration with the strategy() declaration. This designates the script as a strategy.

Add order placement commands for simulating orders. Use logical conditions from the initial indicator to trigger the commands in the converted strategy.

The following example includes two scripts: an initial indicator script and a strategy script converted from the indicator. We use a simple RSI oscillator as a momentum indicator to gauge the direction of a market’s momentum, with values above 50 indicating an upward (bullish) trend and values below 50 signaling a downward (bearish) trend:

The initial indicator colors the plot line and the bars on the chart in a lime color when the RSI is greater than 50 and fuchsia when less than 50. We use plotshape() to plot triangles at the top and bottom of the oscillator on bars where the RSI crosses over or under the 50 level.

In the converted strategy version, we maintain the same RSI crossover and crossunder conditions used in the indicator script. These conditions, which previously only drew the plotshape() triangles, now also trigger entry orders for long and short positions using the strategy.entry() function. A long entry is called when the RSI crosses over 50, and a short entry is initiated when it crosses under 50. A long entry cancels a short trade, and vice-versa.

### How do I set a basic stop-loss order?
Stop losses are a risk management method that traders use to limit potential losses. The strategy.exit() function sets an order to exit a trade once it hits a specified price, thus preventing the loss from exceeding a predetermined amount.

To implement a basic stop loss in Pine Script, use the strategy.exit() function with either the stop or the loss parameter. The stop parameter specifies the price for the stop loss order, while the loss parameter sets the stop loss a certain number of ticks away from the entry order’s price. Similarly, to set a take-profit level, use either the limit parameter, specifying the exact price for taking profit, or the profit parameter, defining the profit
size in ticks from the entry price.

If a strategy.exit() call includes both the stop and loss parameters, or both the limit and profit parameters, the function uses the price level that is expected to trigger an exit first.

The following example script uses the tick-based loss parameter for long positions and the price-based stop parameter for short positions, and plots these stop levels on the chart.
The script enters positions on the crossover or crossunder of two simple moving averages.

Note that:

- In this example, we include from_entry arguments in the strategy.exit() calls so that each exit order closes only open trades with the corresponding entry ID. Without this argument, the exit intended for long positions would apply to both long and short positions, and the exit intended for short positions would likewise attempt to close any open position.
For more information, see the entry in the User Manual on strategy.exit() .

### How do I set an advanced stop-loss order?
Scripts can use different types of exits that are more advanced than simply closing the position at a predetermined level.

Bracket orders

A bracket order is a pair of orders that close the position if price moves far enough in either direction. Scripts can combine a stop-loss and take-profit order within a single strategy.exit() function call. See the FAQ entry about bracket orders for more details.

Trailing stop losses

A trailing stop loss is a stop loss that moves with price, but in the profitable direction only. To create a trailing stop, either adjust the stop price with each new bar, or use the built-in trailing stop parameters in the strategy.exit() function. Refer to the FAQ on implementing a trailing stop loss for information and examples.

Scaled exits

Scaled exits use multiple exit orders at varied price levels. When using tiered exit strategies, which progressively scale out of a position, ensure that the total quantity of all exit orders does not surpass the size of the initial entry position. Consult the FAQ on multiple exits for more information.

Moving a stop loss to breakeven

Adjusting a stop loss to the breakeven point once a specific condition is met can help in risk management. Details can be found in the FAQ on moving stop losses to breakeven .

Adjusting position size based on stop loss

Modify the position size relative to the stop loss to maintain a constant risk percentage of total equity. For more insights, see the FAQ on position sizing .

### How can I save the entry price in a strategy?
Scripts can access the entry price for a specific trade , or the average entry price for a position .

Average entry price

The strategy.position_avg_price variable automatically updates to the average entry price of the current position. If the position consist of only one trade, the average price of the position is equal to the entry price of that single trade.
If a strategy closes a market position that consists of multiple trades, trades are closed in the order they were opened, by default. Since the average price of the open position changes according to which positions are still open, be aware of the order in which trades are closed, and if necessary, configure it using the close_entries_rule parameter of the strategy() declaration function.

Specific entry price

The strategy.opentrades.entry_price() function returns the entry price for a given trade ID. To find the entry price for the most recent open trade, and remembering that the trade indexes start at zero, use float entryPrice = strategy.opentrades.entry_price(strategy.opentrades - 1) .

### How do I filter trades by a date or time range?
Using a date and time range filter in a strategy allows trades to be simulated only during a certain time period. Such filters can be useful to backtest specific historical periods, or to focus on particular times of the trading day.

Additionally, if the strategy sends signals for live trading, consider excluding all trades earlier than the trading start date and time, to ensure that the broker emulator starts in a neutral state.

The following example script restricts trading if a bar falls within a defined startTime and endTime , or outside of an optional intraday session window. The script colors the background red for bars that fall outside the time windows. On the screenshot, we’ve limited the trading range from June 1st 2024 to June 10th 2024, and additionally forbidden trading from 0000-0300 UTC:

Note that:

- We use the time() function to calculate whether bars are outside the user-defined session times. For additional details on integrating session data in Pine Script, refer to the Sessions section in the User Manual.
- We set the confirm argument to true for the inputs that define the time range. When the script is first added to the chart, it prompts the user to confirm the values by clicking on the chart.
- We use a constant string TZ in our script to represent the time zone (set to "GMT+0" by default). Adjust this string to the local time zone or the exchange’s time zone. We use a constant rather than an input so that we can include the time zone in input titles.
## Order execution and management
### Why are my orders executed on the bar following my triggers?
Each historical bar in a chart is composed of a single set of open , high , low and close (OHLC) data. Pine scripts execute on this data once per historical bar, at the close of the bar.

So that results are consistent between historical and realtime bars, strategies also execute at the close of realtime bars. The next possible moment for an order to be filled is the beginning of the next bar.

Users can alter a strategy’s calculation behavior by configuring strategies to process orders at the close of the signal bar instead, by selecting the “Fill orders/On bar close” setting in the “Settings/Properties” tab. Programmers can do the same by setting the process_orders_on_close parameter to true in the strategy() declaration statement:

An alternative method is to specify the immediately parameter as true in a strategy.close() or strategy.close_all() function call. This setting causes the broker emulator to close a position on the same tick that the strategy creates the close order – meaning, when bar closes instead of the beginning of the next one. The process_orders_on_close parameter affects all closing orders in the strategy, whereas the immediately parameter affects only the close order in which it is used.

However, processing orders on close might not give accurate results. For instance, if an alert occurs at the close of the session’s last bar, the actual order can be executed only on the next trading day, since the bar is already closed. In contrast, the emulator would simulate the order being filled at the previous day’s close. This discrepancy can lead to repainting, where the behavior of the strategy’s simulation on historical bars differs from that seen in live trading.

### How can I use multiple take-profit levels to close a position?
Setting up a strategy with multiple take profit levels enables traders to scale out of trades in segments to secure profits incrementally.

There are two main methods for scaling out at varying levels:

- Multiple strategy.exit() calls. This method is most suitable when each take-profit level has a corresponding stop loss.
- An OCA reduce group . This method is ideal for a different number of take-profit levels and stop losses.
#### Multiple ​ strategy.exit() ​ functions
Each strategy.exit() call can set a bracket order for a specific take-profit and stop-loss level.
However, if a strategy uses multiple strategy.exit() functions with the same stop level, each function call triggers a separate order (and therefore multiple order alerts). If order alerts are configured to trigger real trades, ensure that the trade system handles multiple alerts at the same stop level appropriately.

The following example script uses two separate strategy.exit() functions, each with its own stop-loss and take-profit levels. The quantity for the first bracket order is set to 50% of the total position size. This combination of orders creates a scaled exit with distinct stop levels.

Note that:

- We use persistent global variables for the take-profit and stop-loss levels so that we can plot them. Otherwise, declaring the variables in the first if block would be simpler.
#### Using ​ strategy.oca.reduce ​
Creating exit orders as a group, using the strategy.oca.reduce type, ensures that when one exit order from the group is filled, the quantity of the remaining orders is reduced accordingly. This method is ideal in scripts that have an unequal number of take-profit levels to stops.

When using a group of orders whose OCA type is strategy.oca.reduce , we recommend ensuring that the total size of all exit orders, after any reductions, matches the size of the initial entry orders. Matching the sizes guarantees that the strategy closes the position entirely without leaving any part open or inadvertently opening a new position in the opposite direction.

The following example script uses two take-profit levels but only one stop level. All three sell orders have the same oca_name , which means they form a group. They have oca_type = strategy.oca.reduce set, so that filling one of the limit orders reduces the quantity of the remaining orders. The total quantity of the exit orders matches the entry order quantity, preventing the strategy from trading an excessive number of units and causing a reversal.

### How can I execute a trade partway through a bar?
On historical bars , Pine scripts can access only a single set of open , high , low and close (OHLC) data per bar.
Consequently, strategies are calculated once, at the close of each bar. This limitation means it’s not possible to evaluate logical conditions that occur mid-bar, such as a price cross, on historical data.

#### Using ​ calc_on_every_tick ​
Strategies running on realtime bars can simulate orders partway through a bar by enabling the calc_on_every_tick parameter. This setting allows the strategy to process each tick (incoming price update) and execute trades on the tick after a logical condition occurs.

Notice In contrast to realtime bars, historical bars do not contain data for each incoming tick. Those bars contain only confirmed price data. Consequently, a strategy that enables calculation on every tick might repaint on elapsed realtime bars after reloading, because those bars become historical and no longer contain data for each tick before their close. Therefore, we recommend setting calc_on_every_tick to false while backtesting.

#### Using predefined prices
Stop or limit orders at predefined prices can execute orders partway through a bar, even when the strategy does not enable the calc_on_every_tick parameter. This method is effective on both realtime and historical data. Even though orders are processed on the close of historical bars, the broker emulator simulates an order fill at the predefined price level, if the broker determines that price has hit that level during the bar.
For information about the assumptions that the broker emulator makes about price movements, see the Broker emulator section of the User Manual.

The following example script uses stop and limit orders to exit a trade partway through a bar. The script calls the strategy.exit() function with the stop and limit parameters, determining the specific price levels at which the trade will exit.

### How can I exit a trade in the same bar as it opens?
Sometimes, traders want to enter and exit trades on the same bar. By default, if an exit condition occurs during the same bar that a trade is opened, the broker emulator closes the trade at the open of the next bar. To learn why this happens, refer to this FAQ entry .

To override this default behavior, either specify exit prices, or exit with a market order at the bar close.

#### Specifying exit prices
If the entry command also sets stop-loss or take-profit orders to trigger an exit when certain price levels are reached, then the trade can exit during the same bar that it opens.

In the following example script, the trade exits within the same bar if the price hits either of the defined profit or loss levels. Setting small profit and loss values increases the likelihood of triggering an exit within the entry bar, although the trade could hit those levels for the first time in a subsequent bar instead.

#### Using a market order at bar close
Another method to exit a trade in the same bar that it opens is to use a market order at the bar’s close, by setting the immediately argument to true in the strategy.close() function.

In the following example script, if the buy order is opened, the strategy closes the position at the end of the entry bar. Scripts can call the strategy.close() function conditionally within a local block if necessary. For simplicity, in this example we apply the command to every entry.

Notice The immediately parameter operates in a similar way to process_orders_on_close , but it is specific to the strategy.close() and strategy.close_all() functions. The emulator calculates the close order using bar closing prices, but the same prices might not always be attainable in realtime trading. Additionally, this behavior can cause repainting .

## Advanced order types and conditions
### How can I set stop-loss and take-profit levels as a percentage from my entry point?
To set exit orders as a percentage from the entry price, the script needs the average entry price calculated by the broker emulator (which is affected by conditions including multiple entries and slippage). However, the built-in variable strategy.position_avg_price returns na until the close of the entry bar. This means that take-profit and stop-loss orders based on the entry price can only be placed during the next bar.

If programmers want strategies to be able to close trades on the same bar that they are opened, there are two workarounds, each of which have their own benefits and limitations: altering the emulator behavior and using a different, fixed value.

#### Using ​ calc_on_order_fills ​
Setting the calc_on_order_fills argument of the strategy() declaration function to true recalculates the strategy immediately after simulating an order fill. This setting provides access to data such as the current average price of a position on an unconfirmed bar.

Notice Enabling calc_on_order_fills for some strategies might lead to unrealistic results on historical bars. During the extra script execution after an order fills, the script has access to the confirmed OHLC values for the historical bar, but those values would not be available in the real world until the bar’s closing time. For an explanation of this form of lookahead bias , see this Help Center article .

The following example script sets take-profit and stop-loss orders during the entry bar, based on the entry price strategy.position_avg_price . The script uses the calc_on_order_fills setting to enable this behavior.

Note that:

- If we change calc_on_order_fills to false in this script, the exit orders are placed on the bar after the entry bar, and can fill at very different levels depending on the movement of price.
#### Using predefined prices
The following example script calculates the stop and limit orders based on the closing price of the signal bar. The disadvantage of this approach is that the close price might not match the average opening price exactly. The advantage is that this method doesn’t introduce potential lookahead bias like using calc_on_order_fills .

### How do I move my stop-loss order to breakeven?
Moving a stop-loss order to breakeven can be a useful technique to manage risk.

The following example script sets a persistent stopLoss variable when the strategy enters a position. The script then updates the stop price to the entry price when the market price gets halfway to the take-profit level. The script calls the strategy.exit() function on every bar to ensure that the broker emulator receives any updates made to the stopLoss value. Lastly, it plots the average price according to the strategy.position_avg_price variable for reference.

Note that:

- This strategy uses strategy.position_avg_price as the breakeven level. However, the real breakeven price of a trade is affected by slippage and commission.
### How do I place a trailing stop loss?
A trailing stop loss limits a trader’s losses while allowing a position to remain open as long as the price moves favorably.

Strategies can create trailing stops either by using the built-in functionality of the strategy.exit() function or by creating custom trailing stop-loss logic.

Trailing stops set in the strategy.exit() use live price updates in realtime but assumed price movements for historical bars. These assumptions can cause repainting . This type of trailing stop is therefore potentially more responsive but less accurate.

Custom trailing stop values are typically updated at the close of each bar, and so do not capture realtime intrabar price movements with the same responsiveness. This delay helps to avoid repainting strategy results.

#### Using built-in trailing stop functionality
To set a trailing stop in the strategy.exit() function, specify both when the trail should activate and how far behind price it should trail.

Activation level

When price crosses this level, the trailing stop activates. The activation level can be set as a number of ticks past the entry price via the trail_points parameter, or as a price value via the trail_price parameter.

Trail offset

After it activates, the stop loss trails behind the bar’s high or low price by this distance, defined in ticks using the trail_offset parameter.

In the following long-only example script, the strategy.exit() function uses the trail_points and trail_offset parameters to set a trailing stop. The
stop-loss trails the high , minus the offset points, after it activates. The script creates and plots a separate trailingStop variable to visualize the trailing stop price that the function calculates internally, although this is not necessary for the trailing stop to function. We also set a separate stop-loss order to close trades that go too low before they trigger the trailing stop.

#### Coding a custom trailing stop
A custom trailing stop can use different activation conditions, and can trail in a different way, to the trailing stop built into the strategy.exit() function. To work correctly, a custom trailing stop must calculate the stop price on each bar that the stop is active, and call the strategy.exit() function on each bar to set the stop price.

The following example script triggers long and short trades based on crosses of two moving averages. A custom function calculates the trailing stop using the highest or lowest price from the last five bars, adjusted by an Average True Range (ATR) buffer. This method of distancing the stop by a measure of average price movement attempts to reduce premature stop triggers in volatile conditions.

Note that:

- Because strategies run once per bar, the trailing stop price in this example script updates at the close of each bar. During realtime bars the previous bar’s stop value is used. This approach, while slightly delayed compared to using the built-in trailing stop described in the FAQ entry about how to place a trailing stop loss using built-in trailing stop functionality , ensures that the
trailing stop price is not subject to assumptions about intrabar price movements, and thus avoids repainting.
### How can I set a time-based condition to close out a position?
To close positions after a certain amount of time has passed, track the entry time for each trade and close the position using strategy.close() after the timeout.

Because strategies calculate at the close of each bar on historical data, time-based conditions can only be evaluated at the close, so trade times are assessed in multiples of the chart bar’s duration . Further, if the timeout value is not divisible by the duration of a chart bar, each trade will last at least one additional chart bar. For instance, setting a timeout of 100 seconds on a 1-minute chart effectively means a minimum of two bars before a position can be closed.

In realtime, the same logic applies unless the strategy uses the calc_on_every_tick parameter, in which case the trade closes as soon as the first tick exceeds the timeout value. Remember that altering emulator behavior typically introduces repainting .

The following example script calculates the duration of each open trade by comparing the current time against the trade entry time. If a trade’s duration exceeds the specified timeout, the script closes the trade and marks the event with a comment on the chart including the trade’s duration in seconds.

Note that:

- The script uses either the time of the bar’s close using the time_close variable, or the current time from the timenow variable (if the strategy uses the calc_on_every_tick parameter).
- The script uses the built-in functions strategy.opentrades.entry_time() and strategy.opentrades.entry_id() to measure trade duration and identify individual trades.
- The strategy.close() function uses the immediately argument to simulate trades at the end of the bar that exceeds the timer, rather than waiting for the opening of the next bar. Consequently, when a 120-second timeout is applied and the script runs on a 1-minute chart, it gives the appearance that trades last exactly two bars.
### How can I configure a bracket order with a specific risk-to-reward (R:R) ratio?
To create a bracket order, define a stop-loss and a take-profit order using a single strategy.exit() call.
To apply a specific risk-to-reward ratio, calculate the distance between the entry point and the stop-loss level. This stop distance represents the “risk”. Then place the take-profit order a certain multiple of the stop distance away. The distance to the take-profit order represents the “reward”, and the ratio between them is the risk:reward (R:R) ratio.

The following example script simulates long and short trades using inputs to define the stop distance in ticks and the R:R ratio. The loss parameter of the strategy.exit() function is simply the stop distance. The profit parameter is the stop distance multiplied by the R:R ratio. The script fills the areas between the entry and stop-loss points, and between the entry and take-profit points, to illustrate the risk and reward.

### How can I risk a fixed percentage of my equity per trade?
Adjusting the position size to risk a fixed percentage of equity normalizes risk exposure, regardless of equity fluctuations, and helps avoid disproportionate risks across a strategy’s trading history.

Calculate the position size so that as the stop distance increases, the position size decreases, and vice-versa, to maintain a constant risk percentage:

- Calculate monetary risk per contract by multiplying the stop distance in ticks by the monetary value of each tick ( syminfo.mintick ) and by the number of units each contract represents ( syminfo.pointvalue ).
- Determine risk amount by multiplying the current equity ( strategy.equity ) by the percentage of equity that you want to risk.
- Calculate position size by dividing the risk amount by the risk per contract .
Tip Smaller stop distances require larger position sizes to achieve a specific fixed risk. In some cases, the strategy might require increased leverage to achieve the required sizes. To prevent the strategy from entering trades with increased leverage, set the strategy’s margin requirements to 100% by passing a value of 100 (default) to the margin_long and margin_short parameters of the strategy() declaration statement. Alternatively, set the “Margin for long/short positions” inputs to 100 in the script’s “Settings/Properties” tab. To learn more about leverage and margin in strategies, see this Help Center article .

The following example script uses moving average crosses to generate long and short orders. The stop distance, risk:reward ratio, and percentage of equity to risk are all configurable via inputs.
The script plots the current equity, the current value of a new position, and the percentage change in equity to the Data Window. Note that the actual exposure level can be less than intended if the available capital does not divide neatly by the unit value, particularly with small equity amounts, high unit prices, or assets such as stocks where trading partial shares is not possible.

Additionally, we display lines on the chart for the current total equity (in green) and the value of a position needed for the specified risk exposure at the current price (in blue). If the position value exceeds the total equity, the strategy requires leverage to achieve the required exposure, and the script colors the background red and displays the minimum leverage ratio needed in the data window.

Note that:

- The stop distance in our example script is set to a constant value for demonstration purposes. In practice, the stop distance normally varies for each trade.
## Strategy optimization and testing
### Why did my trade results change dramatically overnight?
Strategy results can vary over time depending on where the historical data starts. The starting point of the data set aligns with the start of the nearest day, week, month or year, depending on the chart timeframe. Additionally, different TradingView plans provide access to varying amounts of historical bars. Refer to the User Manual entry on starting points for a discussion of these factors.

For strategies, this means the historical results seen today might change as the dataset’s starting point moves. This can lead to a natural repainting of strategy results over time. To reduce the effect of these changes on backtesting, follow these tips:

Export strategy results

Regularly exporting strategy results to a file maintains a record of performance over time despite changes in historical data. Use the “Download data as XLSX” option from the context menu in the strategy report to export all the available report data. Alternatively, use the “Download” button in the upper-right corner of the panel’s “Trades” tab to export only the list of trades data as a comma-separated values (CSV) file.

Use Deep Backtesting

Users with Premium and higher plans have access to the Deep Backtesting feature, which provides results from the entire available dataset of a symbol. Deep Backtesting results are displayed in the strategy report but are not visible on the chart.

Use Bar Replay

Use the Bar Replay feature on the first chart bar to extend the dataset backward, allowing a strategy to run on an additional full dataset prior to the current range. This process can be repeated a few times to analyze multiple datasets.

### Why is backtesting on Heikin Ashi and other non-standard charts not recommended?
Non-standard charts like Heikin Ashi , Renko , Line Break , Kagi , Point & Figure , and Range Charts offer unique perspectives on price action. However, these chart types are not suited for strategy backtesting or automated trading systems execution, because the prices and time intervals do not match market prices and times.

Renko , Line Break , Kagi , Point & Figure , and Range Charts simplify price action, losing some price detail. Heikin Ashi charts calculate synthetic prices for each bar’s open , high , low ,
and close (OHLC) values based on averages.

Further, all non-standard chart types with the exception of Heikin Ashi charts form new price units based on price movement only and omit the element of time.

Both the distortion of price data and the omission of time in non-standard charts lead to unrealistic and potentially misleading backtesting results.

Programmers can specify the fill_orders_on_standard_ohlc parameter of the strategy() declaration, which causes the strategy to calculate on standard chart data even if the current view is of Heikin Ashi candles. The user can do the same thing by by enabling the “Fill orders on standard OHLC” option in the strategy’s properties . This option has no effect on other non-standard chart types, because they use non-standard time as well as price.

For a more detailed analysis of how non-standard chart types affect strategy results, refer to this script from the PineCoders account.

### How can I backtest deeper into history?
Different TradingView plans give access to different amounts of historical information. To conduct more comprehensive backtesting in Pine Script, exploring further into an asset’s historical data, use Bar Replay or Deep Backtesting.

Bar Replay

Starting the Bar Replay from the first chart bar in history effectively rolls back the dataset to an earlier point in time. Each iteration of the bar replay extends the dataset further back, offering analysis of multiple historical datasets. However, there is a limit to the number of times this process can be repeated. This method has the added benefit of visualizing the strategy’s performance directly on the chart, which can be insightful for understanding trade entries, exits, and behavior during specific historical market conditions.

Deep Backtesting

For TradingView users with Premium and higher plans , the Deep Backtesting mode can execute the strategy across all historical data available for the selected symbol. The results from Deep Backtesting mode are displayed only in the strategy report , and the trade markers from using this mode are not visible on the chart; the trades shown on the chart are always calculated without Deep Backtesting. The strategy report results from Deep Backtesting mode might be different from the results in regular mode for the same chart and strategy, as explained in this Help Center article .

### How can I backtest multiple symbols?
Each Pine Script strategy runs on one dataset at a time. To evaluate a strategy across various markets or instruments:

- Apply the strategy to the chart and then switch the chart to the desired symbol.
- Use TradingView’s watchlist feature to organize and quickly access different symbols.
- Export the results from the strategy report and use external tools such as spreadsheet software to compare the performance of a strategy on different symbols.
## Advanced features and integration
### Can my strategy script place orders with TradingView brokers?
Pine Script strategies and indicators cannot directly place orders on exchanges.
Traders can use external tools or platforms that can interpret alert signals from Pine scripts using webhooks and execute trades accordingly.

### How can I add a time delay between orders?
Adding a time delay between orders can help to prevent too many trades in a short time. Strategies can also prevent trading for a time after a series of losses. Here’s how to set up a time delay between orders:

- Define the delay duration, whether in time units (minutes, hours, days) or a number of bars. For time-based delays, convert the chosen time unit into milliseconds, because Pine time variables use milliseconds.
- Check the time or bar_index of the last trade using strategy.closedtrades.exit_time() or strategy.closedtrades.exit_bar_index() .
- If the difference between the current bar time or bar_index and that of the last trade’s exit exceeds the delay duration, set a boolean flag to allow new orders. Make sure to include the flag in the strategy entry conditions.
The following example script provides two methods for delaying orders: a time-based delay or a specified number of bars. The strategy creates a long entry order when either the time of a bar or its bar_index exceeds the set delay from the last active trade bar. No other conditions are used for entry in this demonstration, but users can add their own logic to these conditions.

To keep the chart clean, the script calls the strategy.close() function to close active trades after they have been open for 10 bars. The script uses background shading, labels and arrows to illustrate the trade entries and exits.

Consider the following limitations when adding time-based delays.

Historical bars

Strategies calculate at the close of each bar, so they can only evaluate time-based conditions at that moment. This constraint entails that on historical bars, delay times are assessed in increments equal to the chart bar’s duration .

Session times

Strategies cannot evaluate delays when the market is closed, because there are no price updates to trigger script execution. This means that if a delay extends beyond the end of a trading session, the delay condition cannot be identified until the script runs again on the next session, resulting in a longer-than-anticipated time between orders.

Delay duration on different timeframes

If the delay value is not divisible by the duration of a chart bar, each delay lasts at least one additional chart bar. For instance, setting a delay of 100 seconds on a 1-minute chart effectively means a minimum of two bars before the delay is exceeded.

### How can I calculate custom statistics in a strategy?
To track metrics other than the default metrics that the strategy report tracks, strategies can calculate custom statistics. These calculations might need to detect order executions, track closed trades, monitor entries into trades, and assess whether a trade is active. Changes in built-in variables such as strategy.opentrades and strategy.closedtrades can track the execution of orders.

The following example script uses a moving average crossover strategy to generate orders. It calculates custom metrics, including the price risk at entry, average position size, and the average percentage of bars involved in trades across the dataset, and plots the custom metrics and some built-in variables to the Data Window. Users can view the history of values plotted in the Data Window by moving the cursor over any bar. In contrast, the strategy report summarizes data over the entire testing period.

Note that:

- The strategy incorporates trading costs . Failing to account for these costs can lead to an unrealistic perception of strategy performance and diminish the credibility of test results.
- We round the open , high , low and close (OHLC) built-in variables to the symbol’s precision. This rounding ensures that any statistics the script calculates align within the strategy report and with strategy order-related built-in variables.
- The script creates global variables changeInOpenTrades and changeInClosedTrades for the changes in built-in variables for open and closed trades so that it calls the ta.change() function on every bar for consistency. See the Storing and using data from previous bars section of the Execution model page to learn more.
### How do I incorporate leverage into my strategy?
Trading with leverage means borrowing capital from a broker to control larger position sizes than the amount of capital risked. This amplifies both potential profits and losses, making it a powerful but risky tool. The amount of the trader’s capital that they risk is called the margin .

For example, setting a 20% margin ratio means that the trader’s balance funds only 20% of the position’s value, allowing positions up to five times the account balance. A margin ratio of 20% is therefore the same as 5:1 leverage. With an available balance of $10,000 and a 20% margin setting, a strategy can open positions up to $50,000 in value.

Pine Script strategies can simulate trading with leverage by specifying margin requirements for long and short positions. Users can adjust the “Margin for long positions” and Margin for short positions” in the strategy’s “Properties” tab. Programmers can set the default margin in the script using the margin_long and margin_short parameters in the strategy() declaration function.

Notice If a leveraged trade, or even a short trade with 1:1 leverage, incurs significant losses that cause the strategy’s account balance to drop below the required margin, the broker emulator initiates a margin call event by liquidating four times the amount required to cover the loss. This behavior helps prevent constant margin calls on subsequent bars.

For more information on using leverage in strategies, see the Help Center article How do I simulate trading with leverage?

### Can you hedge in a Pine Script strategy?
When traders offset the risk of one position by opening another position at the same time, this is called hedging .

The main ways to hedge an open position are:

- By opening a second position in a related asset that is expected to move in the opposite direction to the first asset.
- By opening a short position to offset a long position or vice-versa.
- By using derivatives such as options.
Strategies cannot use these methods, because Pine strategies can only have positions open in one direction at a time, either long or short. Pine strategies run on only the chart asset and cannot open positions in different assets.

### Can I connect my strategies to my paper trading account?
Pine Script does not support placing orders using the brokers integrated via the Trading Panel, or using TradingView’s built-in paper trading account . The strategy report closely mimics a paper trading account by simulating orders and tracking theoretical positions and capital in a risk-free environment.

Strategies can customize order fill alerts to include detailed results and performance metrics in the alert strings, providing a record of the strategy’s theoretical fills and overall performance in realtime.

Tip When configuring alerts for forward testing, it is often helpful to restrict the strategy’s logic to remove the effects of historical trades by using a date filter set to today’s date.

## Troubleshooting and specific issues
### Why are no trades executed after I add the strategy to the chart?
The strategy report , which displays a strategy’s simulated trading results, becomes available when at least one strategy script is active (loaded and visible) on the chart. If a strategy that is running on the chart does not place any orders, the panel displays a message to inform the user that no trade data is available.

If a valid script that uses the strategy() declaration statement is running but is not placing any orders, consider the following potential problems and their solutions:

Lack of order placement commands

The strategy must use either the strategy.order() or strategy.entry() order placement commands to place orders. Add log.info() messages and review the Pine Logs to check whether the conditions to run those commands are met.

Insufficient capital

Verify that the strategy has enough initial capital to cover the position sizes it attempts to open. Remember, the cost of entering a futures contract position is the chart price multiplied by the syminfo.pointvalue , which can be significantly greater than the chart price. For a quick fix, increase the initial capital to a very high value in the strategy’s “Settings/Properties” tab.

Runtime errors

Check for runtime errors indicated by a red exclamation mark on the chart pane next to the script’s title. Resolve any issues by correcting the script as necessary.

By contrast, if a strategy produces too few trades, or executes over too short a duration, there might not be enough information to populate the full strategy report. In that case, the strategy report panel can generate a portion of its results, but some report sections might display no results for certain metrics or show the message “Not enough data to display” in place of certain visuals. To address this problem, adjust the chosen dataset, testing range, and strategy configuration to ensure that the strategy produces a reasonable number of simulated trades to assess its hypothetical performance (ideally 100 trades or more).

For more detailed guidance on this topic and troubleshooting tips, refer to the Help Center article I’ve successfully added a strategy to my chart, but it doesn’t generate orders .

### Why does my strategy not place any orders on recent bars?
If a strategy places one or more orders early in the testing range but then stops placing orders, check the following issues:

Total account loss

Check whether the simulated account balance experienced a total loss of equity earlier in the available history. As a result, the account might lack sufficient capital to continue trading the symbol and fail to show trades only in the chart’s recent history.

No exit condition

Some programmers define entry conditions that rely on having no positions currently open. Make sure to explicitly close trades by specifying corresponding exit conditions for all trades. Without explicit instructions to close an open position using strategy.close() or strategy.exit() commands, the strategy might display only a single entry order early in the chart’s history and in the strategy report’s “Trades” tab . If trades are not closed, they do not generate results in the report’s “Metrics” tab .

### Why is my strategy repainting?
Pine scripts repaint if they behave differently on historical and realtime bars. If strategies repaint, their backtesting results are not reliable because they do not accurately represent the strategy’s behavior in realtime.

Some strategy properties cause repainting:

- The calc_on_every_tick setting causes a strategy to recalculate with every price update, which may cause orders and alerts to trigger during the formation of a bar in realtime. By contrast, on historical bars, calculations are performed at the close of the bar.
- The calc_on_order_fills setting causes a strategy to recalculate immediately after simulating an order fill. For example, this feature is particularly useful for strategies that rely on entry prices to set exit prices on the entry bar, rather than waiting for the bar to close, such as the first example script in the FAQ entry How can I set stop-loss and take-profit levels as a percentage from my entry point using calc_on_order_fills ? However, using this setting can introduce lookahead bias into the strategy, leading to potentially unrealistic outcomes. For instance, if a strategy’s entry conditions are met within a bar that also triggers an exit, the strategy would execute an entry order within the same bar on the next tick. On historical bars, such entries could occur at any of the bar’s open , high , low , or close (OHLC) prices, resulting in entry prices that are unrealistically favorable.
- Since strategies and their alerts execute at the close of a historical bar, the next possible moment for an entry order to be filled is the beginning of the next bar. However, the process_orders_on_close setting causes the strategy to use the close price of the bar where the condition is met for its order prices instead. See the FAQ entry Why are my orders executed on the bar following my triggers? for more information.
To avoid repainting, set the calc_on_every_tick , calc_on_order_fills , and process_orders_on_close parameters to false in the strategy() declaration statement.

Additionally, using unfixed data from a higher timeframe can cause repainting. If the data from the higher timeframe changes during the higher timeframe bar, this can change the script’s oputput for historical bars.
Ensure that strategies use only fixed values from a higher timeframe, as described in the Avoiding repainting section of the Other timeframes and data page.

Although these are the most common causes of repainting in strategies, they are not the only causes. For additional information, refer to the Repainting page in the User Manual.

### How do I turn off alerts for stop loss and take profit orders?
In automated trading strategies, it is common practice to set stop-loss and take-profit orders at the same time as an entry order, using the alert from the entry order as a trigger. In this case, sending alerts for the stop-loss and take-profit order fills can be unnecessary or even problematic. To disable alerts for a specific order placement command, set the disable_alert parameter to true . The broker emulator still simulates the fills for these orders, but sends no alerts for them.

Here is an example of an order fill command with this parameter set:

PreviousProgrammingNextStrings and formatting## On this page
OverviewStrategy basicsHow can I turn my indicator into a strategy?How do I set a basic stop-loss order?How do I set an advanced stop-loss order?How can I save the entry price in a strategy?How do I filter trades by a date or time range?Order execution and managementWhy are my orders executed on the bar following my triggers?How can I use multiple take-profit levels to close a position?Multiple strategy.exit() functionsUsing strategy.oca.reduceHow can I execute a trade partway through a bar?Using calc_on_every_tickUsing predefined pricesHow can I exit a trade in the same bar as it opens?Specifying exit pricesUsing a market order at bar closeAdvanced order types and conditionsHow can I set stop-loss and take-profit levels as a percentage from my entry point?Using calc_on_order_fillsUsing predefined pricesHow do I move my stop-loss order to breakeven?How do I place a trailing stop loss?Using built-in trailing stop functionalityCoding a custom trailing stopHow can I set a time-based condition to close out a position?How can I configure a bracket order with a specific risk-to-reward (R:R) ratio?How can I risk a fixed percentage of my equity per trade?Strategy optimization and testingWhy did my trade results change dramatically overnight?Why is backtesting on Heikin Ashi and other non-standard charts not recommended?How can I backtest deeper into history?How can I backtest multiple symbols?Advanced features and integrationCan my strategy script place orders with TradingView brokers?How can I add a time delay between orders?How can I calculate custom statistics in a strategy?How do I incorporate leverage into my strategy?Can you hedge in a Pine Script strategy?Can I connect my strategies to my paper trading account?Troubleshooting and specific issuesWhy are no trades executed after I add the strategy to the chart?Why does my strategy not place any orders on recent bars?Why is my strategy repainting?How do I turn off alerts for stop loss and take profit orders?
