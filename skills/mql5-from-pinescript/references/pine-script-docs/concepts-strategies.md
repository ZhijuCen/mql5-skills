<!-- source: https://www.tradingview.com/pine-script-docs/concepts/strategies/ | fetched 2026-09-23 | why: strategy.* properties: fills, pyramiding, commission/slippage (ports 0004-0006) -->

User ManualConcepts# Strategies
## Introduction
Pine Script ® strategies are specialized scripts that simulate trades across historical and realtime bars, allowing users to backtest and forward test their trading systems. Strategy scripts have many of the same capabilities as indicator scripts, and they provide the ability to place, modify, and cancel hypothetical orders and analyze performance results.

When a script uses the strategy() function as its declaration statement , it gains access to the strategy.* namespace, which features numerous functions and variables for simulating orders and retrieving essential strategy information. Additionally, the script generates a detailed strategy report in a dedicated tab below the chart.

## A simple strategy example
The following script is a simple strategy that simulates entering a long or short position when two moving averages (MAs) cross. If the fast MA crosses over the slow MA, the strategy places a market order named “Buy” to enter a long position. If the fast MA crosses under the slow MA, it places a market order named “Sell” to open a short position instead:

Note that:

- The strategy() function call declares that the script is a strategy named “Simple strategy demo” that displays visuals on the main chart pane.
- The strategy.entry() function is the command that the script uses to create entry orders and reverse positions . The “Buy” entry order closes any short position and opens a new long position. The “Sell” entry order closes any long position and opens a new short position.
## Applying a strategy to a chart
To test a strategy, add it to the chart. Select a built-in, published, or personal strategy from the “Indicators, metrics, and strategies” menu, or write a custom strategy in the Pine Editor and select the “Add to chart” button from the editor’s options:

The script plots trade markers on the bars in the main chart pane and displays a detailed strategy report within a separate tab in the chart’s bottom panel:

See the Strategy report section below to learn how to read and interpret the performance data displayed by this tab.

Notice The performance results from a strategy applied to non-standard charts ( Heikin Ashi , Renko , line break , Kagi , point & figure , and range ) do not reflect actual market conditions by default. The strategy simulates trades using the chart’s synthetic prices, which do not represent real-world market prices. Consequently, running a strategy on a non-standard chart typically produces unrealistic results. Therefore, we strongly recommend using standard chart types when testing strategies. Alternatively, on Heikin Ashi charts, users can simulate order fills using actual prices by selecting the “Standard bars” option from the “Heikin Ashi mode” input in the script’s “Settings/Properties” tab. Programmers can specify that a strategy uses this behavior by default by including fill_orders_on_standard_ohlc = true in the strategy() declaration statement.

## Strategy report
The strategy report visualizes the hypothetical trading performance of a simulated strategy. The report automatically appears within a tab in the chart’s bottom pannel if at least one strategy script is active on the chart. The report displays performance results for only one strategy at a time. If two or more strategies are active on the chart, users can specify which strategy to analyze by selecting its name from the context menu opened by the dropdown arrow in the tab’s header:

After the selected script executes across the chart’s data, the strategy report populates two main sub-tabs with relevant data from the strategy simulation:

- The “Metrics” tab provdes a detailed summary of the strategy’s performance. The sections in the tab include a time-series chart for analyzing trade activity and equity growth, multiple graphs for analyzing essential performance data, and several useful metrics for assessing the strategy’s long, short, and overall trading performance.
- The “Trades” tab displays a list of the strategy’s simulated trades in chronological order. The items in the list show essential information about each trade, including the trade’s number and direction, the entry and exit prices, and multiple trade-wise performance metrics.
Users can switch between these sub-tabs by selecting the icons in the top-left corner of the strategy report.

Tip Users can also download all applicable data that populates these sub-tabs by selecting the “Download data as XLSX” option in the context menu.

The additional items next to the “Metrics” and “Trades” icons at the top of the strategy report provide quick options where users can customize the testing period and enable Deep Backtesting mode, set the strategy’s initial capital and account currency , control the level of historical bar detail in the simulation, and adjust the script’s execution settings , respectively:

When a script author publishes a strategy, the publication’s script page includes a compact version of the strategy report that displays hypothetical performance results from running the script with specific properties on the published chart. The publication’s report contains similar information to the report displayed below a user’s chart. It also contains an additional “Properties” tab , which displays the input values and properties that the author used while preparing the publication.

### ​“Metrics” tab
The “Metrics” tab of the strategy report provides a detailed summary of a strategy’s performance over a sequence of simulated trades. It organizes the performance details into five main sections:

- Key stats : Displays key overall performance metrics, as well as a chart that plots the series of cumulative equity changes and other overall performance values.
- Return details : Displays graphs and tables for inspecting the strategy’s overall returns and costs, the strategy’s profitability and potential relative to a buy-and-hold system, and the strategy’s risk-adjusted performance ratios.
- Trades analysis : Displays graphs to represent the distribution of trade outcomes, as well as tables containing key trade-wise performance metrics.
- Equity run-ups and drawdowns : Displays graphs and tables with essential information about the strategy’s positive and negative equity fluctuations.
- Capital efficiency : Displays overall metrics relating to the strategy’s capital and margin at the top, as well as a chart and tables containing details about the strategy’s capital usage, margin usage, overall returns, and margin calls.
Some of the tables in this tab contain “All”, “Long”, and “Short” columns. The “All” column shows the performance metrics for all simulated trades. The “Long” and “Short” columns show relevant metrics separately for long and short trades.

The following sections explain the types of information that each part of the “Metrics” tab contains and how it displays the data.

Tip Most of the tables in the “Metrics” tab reveal a “Show description” icon next to a metric’s name when the user hovers over the metric’s row. Clicking that icon opens a Help Center article containing details about the metric’s calculations and meaning. Refer to the Strategy report metrics page in our Help Center for a list of these metrics and their corresponding articles.

#### Key stats
The “Key stats” section of the strategy report’s “Metrics” tab provides a quick overview of the strategy’s overall performance. The top of the section displays a few essential performance metrics, including the strategy’s total profit or loss, the maximum drawdown , the total number of profitable trades compared to the total number of closed trades, and the strategy’s profit factor .

The “Performance” chart below these metrics optionally displays up to four plots to visualize equity growth and trade volatility:

- The “Cumulative PnL” baseline plot displays the cumulative change in the strategy’s equity across all closed trades, experessed as a currency amount or a percentage of the strategy’s initial capital.
- The “Buy and hold” plot displays the cumulative capital or percentage change in equity for a strategy that opens a single long trade and holds it throughout the entire trading period.
- The “Trades excursions” plot displays green and red columns representing the maximum unrealized profit and loss for each trade, expressed as a currency amount or a percentage of the trade’s size.
- The “Run-ups and drawdowns” plot displays green and red horizontal bars to highlight periods of run-up and drawdown in the strategy’s equity across the trading range.
Users can specify the chart’s scale type, download or share an image of the chart, and expand or collapse the chart view by selecting the icons above the chart’s top-right edge.

Hovering over the points on the “Performance” chart anywhere above the “Run-ups and drawdowns” plot reveals a tooltip containing details for a specific trade, including the trade’s number, direction, and closing time. The tooltip also displays the values from the “Cumulative PnL”, “Buy and hold”, and “Trades excursions” plots, depending on which plots are active. When a user clicks the point highlighted by the tooltip, the main price chart automatically scrolls to the chart bar on which the corresponding trade closed, then displays that bar’s time in a temporary tooltip:

Note that:

- The main price chart automatically scrolls to a trade’s closing bar only if the strategy uses the default testing period. Selecting a different period from the “Testing period” menu at the top of the tab activates Deep Backtesting mode, which does not support scrolling the main chart from the report’s “Performance” chart.
Users can also hover over the horizontal bars in the “Run-ups and drawdowns” plot to view a separate tooltip containing the total run-up or drawdown for each displayed period:

#### Return details
The “Return details” section of the “Metrics” tab analyzes the strategy’s cumulative returns and compares them to a buy-and-hold benchmark. The “Overview” sub-tab in this section displays two graphs:

- The “Profit structure” graph on the left displays bars representing the strategy’s total profit, total loss, total commissions, open profit or loss, and the total net profit or loss.
- The “Benchmarking” graph displays the maximum, minimum, and current total return of the strategy compared to the buy-and-hold return values over the same testing range.
The sub-tab also displays the strategy’s open profit or loss, expected payoff per trade, outperformance, and Sharpe ratio above the graphs for quick reference:

The other sub-tabs within this section display detailed information about the strategy’s overall returns:

- The “Returns” tab displays the strategy’s initial capital, open profit or loss, net profit or loss, gross profit and loss, profit factor, commissions paid, and expected payoff per trade. It displays applicable metrics separately for all trades, all long trades, and all short trades.
- The “Benchmarking” tab displays the overall returns of the buy-and-hold benchmark and the strategy’s outperformance.
- The “Risk-adjusted performance” tab displays the strategy’s Sharpe and Sortino ratios, which gauge a strategy’s risk-adjusted return relative to the risk-free rate specified by the strategy() declaration statement.
#### Trades analysis
The “Trades analysis” section of the “Metrics” tab analyzes the overall performance of the strategy’s individual trades. The “Overview” sub-tab in this section displays two graphs for analyzing the distribution of trade outcomes:

- The “Returns distribution” histogram graph displays the distribution of trade returns. Each column in the histogram shows the number of trades that closed with returns within a specific range. Red columns represent negative returns (losses), and green columns represent positive returns (profits). The graph also displays dashed vertical lines at the overall average profit and loss values.
- The “Trades distribution” donut graph displays the quantity of winning, losing, and break-even trades relative to the strategy’s total number of trades.
The “Overview” sub-tab also displays the strategy’s average profit or loss, the average number of bars per trade, and the larget profit and loss from a single trade above the two graphs:

The “Trades analysis details” sub-tab displays multiple useful statistics for all trades, all long trades, and all short trades. It includes metrics such as the total number of trades, the total winning and losing trades, the percentage of profitable trades, the average return amounts, the maximum profit and loss, and the number of outliers in the returns distribution:

#### Equity run-ups and drawdowns
The “Equity run-ups and drawdowns” section of the “Metrics” tab analyzes the strategy’s periods of equity growth ( run-up ) and decline ( drawdown ). The “Overview” sub-tab in this section includes two graphs to simplify run-up and drawdown inspection:

- The “Alternating growth and decline” graph displays vertical bars for periods of run-up and drawdown in chronological order. Green bars represent run-up periods, and red bars represent drawdown periods.
- The “Comparison of growth and decline periods” graph displays horizontal bars representing the maximum, average, and current run-up and drawdown percentages for a quick visual comparison.
The sub-tab also displays the average run-up and drawdown durations, the maximum drawdown as a percentage of the initial capital, and the ratio of the total profit or loss to the maximum drawdown above the graphs:

The “Run-ups” and “Drawdowns” sub-tabs display tables containing detailed metrics for the strategy’s run-up and drawdown periods, including:

- The average duration of each run-up/drawdown period.
- The average run-up/drawdown amount per period.
- The maximum run-up/drawdown across the testing range on both an intrabar and close-to-close basis.
- The maximum intrabar run-up/drawdown as a percentage of the strategy’s initial capital.
- The ratio of the strategy’s total profit or loss relative to the maximum drawdown.
#### Capital efficiency
The “Capital efficiency” section of the “Metrics” tab evaluates how the strategy uses its simulated funds and available margin . The “Overview” sub-tab contains a “Margin usage” chart that displays the amount of margin used on each trade in order, expressed as a currency amount or a percentage of the strategy’s available funds. The sub-tab also shows the strategy’s compound annual growth rate (CAGR), the minimum account size required to avoid a margin call, the overall return on the initial capital, and the total number of margin call events :

The other sub-tabs in this section contain detailed information about the strategy’s capital and margin usage for all trades, all long trades, and all short trades:

- The “Capital usage” tab displays the strategy’s CAGR, the overall return based on the initial capital, the minimum account size, the overall return based on the minimum account size, and the net profit or loss as a percentage of the largest loss.
- The “Margin usage” tab displays the average margin per trade, the maximum margin used on a trade, the average profit per unit of margin, the total number of margin calls, and the total trade volume liquidated by all margin calls.
### ​“Trades” tab
The “Trades” tab of the strategy report lists the strategy’s simulated trades in ascending or descending order by time. The list includes two columns that are always active by default: “Trade number” and “Type”. The “Trade number” column lists each trade’s number and direction. Users can change the sorting order of the list’s items by clicking on the “Trade number” column heading. The list is sorted in descending order by default. The “Type” column contains fields for each trade’s entry and exit order. If the strategy is not running in Deep Backtesting mode, hovering the mouse over either field in a listed item reveals a “Show on chart” icon, which users can click to scroll the main chart to the trade’s entry or exit bar.

The list optionally includes any of the following additional columns, depending on the user’s selections:

- “Date and time”: Shows the entry and exit date and time for each trade.
- “Signal”: Shows the name or comment assigned to each trade’s entry and exit orders.
- “Price”: Shows each trade’s entry and exit price in the instrument’s quoted currency.
- “Size”: Shows each trade’s size, expressed as a number of contracts/lots/shares/units and a quantity of the strategy’s account currency.
- “Return”: Shows each trade’s net return as a percentage of the trade’s size.
- “Favorable excursion”: Shows each trade’s maximum unrealized profit as a currency amount and a percentage of the trade’s size.
- “Adverse excursion”: Shows each trade’s maximum unrealized loss as a currency amount and a percentage of the trade’s size.
- “Cumulative PnL”: Shows the strategy’s total profit or loss at the time of each trade, expressed as a currency amount and a percentage of the strategy’s initial capital.
- “Duration (bars)”: Shows the number of bars for which each trade remained open.
Users can specify which columns to display by selecting the “Column setup” icon above the list’s top-right edge. The adjacent “Download” icon enables users to download all available data for the list as a CSV file.

Note that:

- The downloaded CSV file for the list of trades contains data for all available columns, regardless of the display columns selected in the “Column setup” menu.
- If a strategy uses the default testing range, it preserves individual data for up to the latest 9000 trades . If the strategy uses a different testing range, enabling Deep Backtesting mode, it maintains individual trade data for all trades. This behavior affects the results available from the list of trades, any downloaded CSV files, and the built-in strategy.*() functions that retrieve individual trade information . However, it does not affect the data displayed in the “Metrics” tab or accessed by other strategy.* built-ins. See the trade limit section to learn more.
### ​“Properties” tab
When a script author publishes a strategy, the publication’s script page displays a compact version of the strategy report to demonstrate the script’s performance results for a specific dataset. The published report also includes an extra “Properties” tab, which displays details about the dataset, script inputs, and strategy properties that the author used while preparing the publication. The tab organizes this information into four collapsible sections:

- The “Date range” section shows the selected testing range and the overall available backtesting range.
- The “Symbol info” section displays the chart’s symbol, timeframe, type, point value, currency, and tick size. It also includes the chart’s specified precision setting.
- The “Strategy inputs” section lists the names and values of all the inputs available in the strategy’s “Settings/Inputs” tab. This section appears in the tab only if the script includes input*() calls or specifies a nonzero calc_bars_count argument in the strategy() declaration statement.
- The “Strategy properties” section provides an overview of the properties that the author specified in the script’s “Settings/Properties” tab, including the strategy’s initial capital, account currency, order size, leverage, pyramiding, commission, slippage, and other settings.
Note that:

- If users download performance data as an XLSX file from the strategy report below their charts, the exported data from that report also includes “Properties” tab data for reference.
## Broker emulator
TradingView uses a broker emulator to simulate trades while running a strategy script. Unlike brokers in real-world trading, the broker emulator fills a strategy’s orders using only the available chart data by default. Consequently, it executes orders on historical bars after a bar closes . Similarly, depending on the selected calculation behavior , the earliest point at which it can fill orders on realtime bars is after a new tick . For detailed information about this behavior, refer to the Execution model page.

Because the broker emulator uses only price data from the chart by default, it makes default assumptions about intrabar price movement when filling orders on historical bars. The emulator analyzes the opening, high, low, and closing prices of chart bars to infer historical intrabar activity using the following logic:

- If the opening price of a bar is closer to the high than it is to the low, the emulator assumes that the market price moved in this order: open → high → low → close .
- If the opening price of a bar is closer to the low than it is to the high, the emulator assumes that the market price moved in this order: open → low → high → close .
- When filling price-based orders (all orders except market orders ), the emulator assumes that no gaps exist inside each chart bar; it considers any price within the bar’s range as a valid level for filling pending orders.
- If the market price crosses a price-based order’s level during the gap between one bar’s closing time and the next bar’s opening time, the emulator assumes that intrabar data does not exist within the gap. Rather than filling the order at the specified price in that case, the emulator fills the order at the opening price of the bar following the gap.
The following image labels the OHLC values of a few historical bars using numbers 1-4 to demonstrate the broker emulator’s default assumptions about intrabar price movement. The “1” label represents the bar’s first tick, and the “4” label represents the last tick:

### Adjusting historical bar detail
Users with Premium and Ultimate plans can override the broker emulator’s chart-based assumptions and increase the level of intrabar detail on historical bars, allowing for more precise order fills in the strategy’s backtest. To enable high historical bar detail, select the “High” option from the strategy’s Bar detalization settings, which are available in the “Settings/Properties” tab and at the top of the strategy report below the chart. Programmers can also configure a strategy to use high historical detail by default by including use_bar_magnifier = true in the strategy() declaration statement.

If a strategy enables high historical detail, the broker emulator retrieves open, high, low, and close prices from the bars on a suitable lower timeframe , when possible, to increase the number of ticks available for estimating price action and filling orders on historical bars. This setting also allows the script to perform multiple additional executions on each historical bar, depending on the selected Script execution settings. See the Altering calculation behavior section below to learn more.

The following example illustrates how changing the level of historical bar detail can enhance the behavior of limit orders . The script below creates entry and exit limit orders, named “Buy” and “Exit”, on the first bar whose opening time equals or exceeds an input timestamp. For visual reference, the script highlights the chart’s background in orange when it places the orders, and it draws two horizontal lines at the order prices. The strategy() statement does not include use_bar_magnifier = true . Therefore, the broker emulator uses only chart data to determine when it can fill both orders by default:

If we apply this script to a weekly “NASDAQ:MSFT” chart, the broker emulator fills the “Buy” order one bar after the script creates the orders, then fills the “Exit” order several bars later. On the bar where the “Buy” order fills, the open is closer to the high than it is to the low, so the emulator assumes that the price moved from open to high, high to low, then low to close. Consequently, the emulator infers that after the market price crossed below the blue line, triggering the “Buy” order, it did not move back up and touch the fuchsia line to trigger the “Exit” order on the same bar. In other words, the strategy could not enter and exit the position in the same week, according to the broker emulator’s assumptions:

If we include use_bar_magnifier = true in the strategy() statement, the strategy enables high historical detail by default. When this setting is active on a weekly chart, the broker emulator retrieves open, high, low, and close prices from the daily timeframe . The bars on the daily timeframe show that, contrary to the broker emulator’s default assumption, the market price did move to the “Exit” order’s price after triggering the “Entry” order in the same week. Therefore, the emulator can fill both orders on the same weekly bar in this case. Below, we show the strategy’s result on the weekly chart after enabling high historical detail, alongside the bars on the daily chart with the entry and exit points annotated:

Note that:

- We used the Horizontal line , Vertical line , and Callout drawing tools to annotate the daily chart on the right.
Note A strategy’s “Bar detalization” setting does not affect the level of bar detail on the “1S” or “1T” timeframes. The broker emulator always analyzes one tick per bar on a “1T” chart, and four ticks per bar on a “1S” chart. Scripts can request a maximum of 200,000 bars from any lower timeframe. Due to this limitation, the requested datasets for some symbols and timeframes might not include intrabar coverage for early bars on the chart. The broker emulator uses its default assumptions when filling orders on bars that do not have intrabar data on the requested timeframe.

## Orders and trades
Pine Script strategies use orders to initiate trades and manage positions, similar to real-world trading. In this context, an order is an instruction that a strategy sends to the broker emulator to perform a market action, and a trade is the resulting transaction that opens after the emulator fills an entry order. A market position is total of all open trades.

Let’s take a closer look at how strategy orders work and how they become trades. Every 20 bars, the following script creates a long market order with strategy.entry() and draws a label . It calls strategy.close_all() on each bar from the global scope to generate a market order to close any open position:

Note that:

- Although the script calls strategy.close_all() on every bar, the function creates a new exit order only if the strategy has an open position . If there is no open position, the function call has no effect.
The blue arrows on the above chart show where the strategy entered a long position, and the purple arrows mark the bars where the strategy closed the position. Notice that the label drawings appear one bar before the entry markers, and the entry markers appear one bar before the closing markers. This sequence illustrates order creation and execution in action.

By default, the earliest point at which the broker emulator fills an order is on the next available tick, because creating and filling an order on the same tick is unrealistic . If a strategy uses the default calculation behavior , it updates its calculations only after a bar closes, meaning the next tick on which an order can fill is at the open of the following bar . For example, when the above script’s longCondition value is true on bar 20, the script places an entry order that fills on the next available tick, which is at the open of bar 21. When the script updates its calculations at the close of bar 21, it then places an exit order to close the current position on the following tick, at the open of bar 22.

## Order types
Pine Script strategies can simulate different order types to suit specific trading system needs. The main order types include market , limit , stop , and stop-limit .

### Market orders
A market order is the simplest type of order. A market order is an instruction to buy or sell an instrument as soon as possible, irrespective of the price. Therefore, the broker emulator always executes it on the next available tick. Most order placement commands generate market orders by default, but also include parameters for creating other types of orders.

The example script below alternates between placing long and short market orders in cycles of a specified length. When the bar_index value is divisible by twice the input length, the script generates a long market order. If the bar_index value is divisible by the input length but not by twice the length, the script places a short market order instead. The script also draws labels to indicate bars on which it creates the orders:

Note that:

- This script uses the default calculation behavior : it executes once on each bar’s closing tick. Therefore, as indicated by the labels and trade markers, the broker emulator fills each new order at the open of the following bar.
- The strategy.entry() command can automatically reverse an open position in the opposite direction. See the Reversing positions section below for more information.
### Limit orders
A limit order is an instruction to buy or sell an instrument at a specific price or better (lower than specified for long orders, and higher than specified for short orders), irrespective of the time. To simulate a limit order in a strategy script, pass a price value to the limit parameter of an applicable order placement command .

When the market price reaches a limit order’s value, or crosses it in the favorable direction, the broker emulator fills the order at that value or a better price. When a strategy generates a limit order at a worse value than the current market price (higher for long orders and lower for short orders), the emulator fills the order on the next available tick rather than waiting for the market price to reach that value.

For example, when the following script executes on the bar that is 100 bars before the latest bar, it calls the strategy.entry() command with a limit argument to generate a long limit order 800 ticks above the bar’s close value. The script also draws a label on the bar where it creates the order, and it draws a horizontal line to visualize the order’s price:

Notice that the label and the start of the line in the chart above occur several bars before the “Long” entry marker. The broker emulator cannot fill the limit order while the market price remains above the limitPrice value, because that value is a worse price for the long trade. After the price subsequently drops and reaches the order’s price, the emulator fills the order mid-bar at that price.

If we change the previous example to place a long limit order above the bar’s close value rather than below , the broker emulator fills the order on the next available tick – similar to a market order – because the closing price is already a more favorable value for the long trade. In the script version below, we set the limit order’s price to 800 ticks above the bar’s close to demonstrate this effect:

### Stop and stop-limit orders
A stop order is an instruction to activate a new market or limit order when the market price reaches a specific price or a worse value (higher than specified for long orders and lower than specified for short orders). To simulate a stop order, pass a price value to the stop parameter of an applicable order placement command .

If a strategy generates a stop order at a better value than the current market price, it activates the subsequent order without waiting for the market price to reach that value.

The following example script calls the strategy.entry() with a stop argument to place a stop order 800 ticks above the current close value while executing on the bar that is 100 bars before the last bar. It also draws a label to indicate the bar on which it created the order, and it draws a horizontal line at the stop price.

The following example calls strategy.entry() to place a stop order 800 ticks above the close 100 bars before the last historical chart bar. It also draws a label on the bar where it creates the order and a line to display the stop price. As we see in the chart below, the strategy enters a long position immediately after the price crosses the stop level:

Note that:

- A basic stop order is essentially the opposite of a limit order in terms of its execution based on the market price. If we use a limit order instead of a stop order in this scenario, the order executes immediately on the next bar. See the Limit orders section above for an example.
If a strategy.entry() or strategy.order() call includes a stop and limit argument, it creates a stop-limit order . Unlike a basic stop order, which triggers a market order when the current price is at the stop level or a worse value, a stop-limit order creates a subsequent limit order to fill at the specified limit price.

Below, we modified the previous script to simulate and visualize a stop-limit order. This script version includes the bar’s low as the limit price in the strategy.entry() command. It also creates additional drawings to show where the strategy activates the subsequent limit order and to visualize the limit price.

In example chart below, notice how the market price reaches the limit level on the next bar after the script creates the stop-limit order, but the strategy does not enter a position because the limit order is not yet active. After the market price reaches the stop level, the strategy places the subsequent limit order, and then the broker emulator fills that order after the market price reverses to the limit level:

## Order placement and cancellation
The strategy.* namespace features the following five functions that simulate the placement of orders, known as order placement commands : strategy.entry() , strategy.order() , strategy.exit() , strategy.close() , and strategy.close_all() .

Additionally, the namespace includes the following two functions that cancel pending orders, known as order cancellation commands : strategy.cancel() and strategy.cancel_all() .

The sections below explain these commands, their unique characteristics, and how to use them.

### ​ strategy.entry() ​
The strategy.entry() command generates entry orders . Its unique features help simplify opening and managing positions. This order placement command generates market orders by default. It can also create limit , stop , and stop-limit orders by using the limit and stop parameters, as explained in the Order types section above.

#### Reversing positions
One of the strategy.entry() command’s unique features is its ability to reverse an open position automatically. By default, when an order from a strategy.entry() call executes while a position is open in the opposite direction, the command automatically adds the position’s size to the new order’s size. The added quantity allows the order to close the current position and open a new position for the specified number of contracts/lots/shares/units in the new direction.

For instance, if a strategy has an open position of 15 shares in the strategy.long direction, then calls strategy.entry() to place a new market order in the strategy.short direction, the size of the resulting transaction is the specified entry size plus 15 shares.

The example below demonstrates this behavior in action. On each 100th bar, the script calls strategy.entry() with the argument qty = 15 to enter a long position of 15 shares. Then, 50 bars later, it executes another call with a qty argument of 5, to enter a short position of five shares. The script also highlights the chart’s background in blue when the long condition occurs, and in red when the short condition occurs, to indicate the bars where it places each order:

Although the long and short orders open trades with different sizes, each trade marker on the chart above shows 20 shares as the traded quantity. These markers display the total size of each transaction , not the size of each resulting position . Each execution of one of the strategy.entry() calls automatically reverses the current position by adding the position’s size (e.g., 15 for a long trade) to the new entry size (e.g., 5 for a short entry), resulting in a total transaction size of 20 shares. However, the resulting positions are 15 shares for long entries and 5 shares for short entries.

Note The strategy.risk.allow_entry_in() function overrides the allowed direction for the strategy.entry() command. If a script specifies a trade direction with this risk management command, orders from strategy.entry() calls in the opposite direction close an open position without reversing it.

#### Pyramiding
Another unique characteristic of the strategy.entry() command is its connection to a strategy’s pyramiding property. Pyramiding specifies the maximum number of open trades, from the orders created by strategy.entry() calls, that a strategy allows for a single position. After the number of open trades from strategy.entry() calls reaches the pyramiding limit, the strategy does not execute new orders from subsequent calls to the command until at least one of those trades closes.

Programmers can specify the default pyramiding limit for a strategy by including a pyramiding argument in the strategy() declaration statement. The default argument is 1, meaning the strategy can open new positions but cannot add to them using orders from strategy.entry() calls. Script users can adjust a strategy’s pyramiding limit via the “Pyramiding” input in the “Settings/Properties” tab.

The following example calls the strategy.entry() function to place a market order once on every 25th bar. The order direction changes once every 100 bars. Therefore, each 100-bar cycle executes the command using the same direction four times. The script highlights the chart’s background for each bar on which the entry condition occurs.

As shown below, although the script calls the strategy.entry() command using the same direction argument four times per 100-bar cycle, only the first call in each cycle results in a new trade if we run the script with the default settings. The others do not contribute to the open position because the script’s default pyramiding value is 1:

If we include pyramiding = 4 in the script’s strategy() declaration statement, the script can use strategy.entry() calls to open up to four trades in the same direction by default. After applying this change to our example script, all the script’s entry orders now result in new trades:

Notice In some cases, price-based orders from the strategy.entry() command can cause a strategy’s entry count for a position to exceed the specified pyramiding limit. If multiple calls to this command generate limit , stop , or stop-limit orders on the same tick , the broker emulator fills each one that the price action triggers, regardless of the specified limit.

### ​ strategy.order() ​
The strategy.order() command generates a basic order . Unlike other order placement commands, which can behave differently based on a strategy’s properties and open trades, this command ignores most properties, such as pyramiding , and simply creates orders with the specified parameters. This command generates market orders by default. It can also create limit , stop , and stop-limit orders by using the limit and stop parameters. Orders from strategy.order() calls can open new positions and modify or close existing ones. When a strategy executes an order from this command, the resulting market position is the net sum of the open position size and the filled order quantity.

The following script uses strategy.order() calls to enter and exit positions. The strategy places a long market order for 15 units once every 100 bars. On every 25th bar that is not a multiple of 100, it places a short market order for five units. The script also highlights the background to signify where the strategy places each “buy” and “sell” order:

The strategy above never opens a short position . Unlike the strategy.entry() command, the strategy.order() command does not automatically reverse open positions. After filling a “buy” order, the strategy has an open long position of 15 units. The three subsequent “sell” orders reduce the position by five units each, and 15 - 5 * 3 = 0. In other words, the strategy opens a long position on every 100th bar and gradually reduces the size to 0 using three successive short orders. If we used the strategy.entry() command instead of strategy.order() in this example, the strategy would alternate between entering long and short trades of 15 and five units, respectively.

### ​ strategy.exit() ​
The strategy.exit() command generates exit orders . It features several unique behaviors that link to open trades, helping to simplify closing market positions and creating multi-level exits with take-profit , stop-loss , and trailing stop orders.

Unlike other order placement commands, which can generate a single order per call, each call to strategy.exit() can produce more than one type of exit order, depending on its arguments. Additionally, a single call to this command can generate exit orders for multiple entries , depending on the specified from_entry argument and the strategy’s open trades.

#### Take-profit and stop-loss
The most basic use of the strategy.exit() command is the placement of limit orders to trigger exits after earning enough money (take-profit), stop orders to trigger exits after losing too much money (stop-loss), or both (bracket).

Four parameters determine the prices of the command’s take-profit and stop-loss orders:

- The profit and loss parameters accept relative values representing the number of ticks by which the market price must move away from the entry price to trigger an exit.
- The limit and stop parameters accept absolute values representing the specific prices that trigger an exit when the market price reaches them.
When a strategy.exit() call includes arguments for the relative and absolute parameters defining take-profit or stop-loss levels ( profit and limit or loss and stop ), it creates orders only at the levels expected to trigger exits first .

For instance, if the profit distance is 19 ticks and the limit level is 20 ticks past the entry price in the favorable direction, the strategy.exit() command places a take-profit order based on the profit argument, because the market price will move 19 ticks past the entry price before it reaches the limit value. In contrast, if the profit distance is 20 ticks and the limit level is 19 ticks past the entry price in the favorable direction, the command places a take-profit order at the limit value because the price will reach that value first.

Notice The strategy.exit() command’s limit and stop parameters do not behave the same as the limit and stop parameters of the strategy.entry() and strategy.order() commands. Calling strategy.entry() or strategy.order() with limit and stop arguments creates a single stop-limit order . In contrast, calling strategy.exit() with both arguments creates two exit orders : a take-profit order at the limit price and a stop-loss order at the stop price.

The following example creates exit bracket (take-profit and stop-loss) orders with the strategy.exit() command. When the buyCondition value is true , the script calls the strategy.entry() command to place a “buy” market order . Then, it calls the strategy.exit() command with limit and stop arguments to create a take-profit order at the limitPrice value and a stop-loss order at the stopPrice value. The script plots the limitPrice and stopPrice values on the chart to visualize the exit order prices:

Note that:

- We did not specify a qty or qty_percent argument in the strategy.exit() call, meaning it creates orders to exit 100% of the “buy” order’s size.
- The strategy.exit() command’s exit orders do not necessarily execute at the specified prices. Strategies can fill limit orders at better prices and stop orders at worse prices, depending on the range of values available to the broker emulator .
If a strategy.exit() call includes a from_entry argument, the resulting exit orders apply to only the existing entry orders that have a matching ID. If the specified from_entry value does not match the entry ID of any trade in the current position, the command does not create any exit orders.

Below, we changed the from_entry argument of the strategy.exit() call in our previous script to "buy2" , instructing the command to create exit orders only for open trades that have the “buy2” entry ID. This version does not place any exit orders, because the strategy does not create any entry order with the “buy2” ID:

Note that:

- If a strategy.exit() call does not include a from_entry argument, it creates exit orders for all open trades in the current position, regardless of their entry IDs. See the Exits for multiple entries section below to learn more.
#### Partial and multi-level exits
Strategies can use more than one call to the strategy.exit() command to create successive partial exit orders for the same entry ID. This behavior helps simplify the formation of multi-level exit strategies. To exit from a position using multiple strategy.exit() calls, include a qty or qty_percent argument in each call to specify the portion of the traded quantity to close. If the sum of the exit order sizes exceeds the open position, the strategy automatically reduces their sizes to match the total size of the position.

Note If a strategy.exit() call includes both qty and qty_percent arguments, the command uses the qty value to size the order and ignores the qty_percent value.

The following example demonstrates a simple strategy that creates two partial exit order brackets for an entry ID. When the buyCondition value is true , the script places a “buy” market order for two shares with a strategy.entry() call, and it creates “exit1” and “exit2” bracket orders using two calls to strategy.exit() . The first call uses a qty value of 1, and the second uses a qty value of 3:

As we can see from the trade markers on the chart above, the strategy first executes the “exit1” take-profit or stop-loss order to reduce the open position by one share, leaving only one remaining share in the position. However, the “exit2” order bracket has a specified size of three shares , which exceeds the remaining position. Rather than using this specified quantity, the strategy automatically reduces the “exit2” orders to one share, allowing it to close the position successfully.

Note that:

- The broker emulator fills only one exit order from the “exit1” bracket, not both . If a strategy.exit() call generates more than one exit order type for an entry ID, the strategy fills the only the first triggered one and automatically cancels the others.
- The strategy reduces the “exit2” orders because all orders from the strategy.exit() calls automatically belong to the same strategy.oca.reduce OCA group by default. See the OCA groups section below to learn more.
When creating multiple exit orders with different strategy.exit() calls, it’s crucial to note that the orders from each call automatically reserve a portion of the open position. The orders from one strategy.exit() call cannot exit the portion of a position that a previous call already reserved.

For example, the script below generates a “buy” entry order for 20 shares with a strategy.entry() call, then creates “limit” and “stop” exit orders with two separate calls to strategy.exit() , while executing on the bar that is 100 bars before the last bar. The exit commands specify a quantity of 19 shares for the “limit” order and 20 for the “stop” order:

Users who are unfamiliar with the strategy.exit() command’s unique behaviors might expect the above strategy to close the entire market position if it fills the “stop” order before the “limit” order. However, the trade markers on the chart below show that the “stop” order reduces the position by only one share . The strategy.exit() call for the “limit” order executes first in the code. Consequently, the “limit” exit order reserves 19 shares of the open position. This reservation leaves only one share available for the “stop” order to close, regardless of when the strategy fills it:

#### Trailing stops
One of the strategy.exit() command’s key features is its ability to create trailing stops , i.e., stop-loss orders that trail behind the market price by a specified amount whenever it moves to a more favorable value (higher for long positions and lower for short positions).

This type of exit order has two components: an activation level and a trail offset . The activation level is the value that the market price must cross to activate the trailing stop calculation. The trail offset is the distance by which the activated stop follows behind the market price as it reaches successively better values.

Three strategy.exit() parameters determine the activation level and the trail offset of a trailing stop order:

- The trail_price parameter accepts an absolute price value for the trailing stop’s activation level.
- The trail_points parameter is an alternative way to specify the activation level. Its value represents the tick distance from the entry price required to activate the trailing stop.
- The trail_offset parameter accepts a value representing the order’s trail offset as a specified number of ticks.
To create and activate a trailing stop order, a strategy.exit() call must specify a trail_offset argument and either a trail_price or trail_points argument. If the call contains both trail_price and trail_points arguments, the command uses the level expected to activate the stop first . For instance, if the trail_points distance is 50 ticks and the trail_price value is 51 ticks past the entry price in the favorable direction, the strategy.exit() command uses the trail_points value to set the activation level because the market price will move that distance before reaching the trail_price level.

The example below demonstrates how a trailing stop order works in detail. The strategy places a “Long” market order with the strategy.entry() command 100 bars before the last chart bar. Then, it calls the strategy.exit() command with trail_price and trail_offset arguments on the following bar to create a trailing stop. The script uses lines , labels , and a plot to visualize the trailing stop’s behavior.

The green line on the chart shows the level that the market price must reach to activate the trailing stop order. After the price reaches that level from below, the script uses a blue plot to display the trailing stop’s price. Each time the market price reaches a new high after activating the trailing stop, the stop’s price increases to maintain a maximum distance of trailOffsetInput ticks from the best value. The exit order does not change its price level when the price decreases or does not reach a new high. Eventually, the market price crosses below the trailing stop, triggering an exit:

#### Exits for multiple entries
A single call to the strategy.exit() command can generate exit orders for more than one entry in an open position, depending on the call’s from_entry value.

If an open position consists of two or more entries with the same ID, a single strategy.exit() call that uses the ID as the from_entry argument places exit orders for every corresponding entry created before or on the bar where the call occurs.

For example, the following script periodically calls the strategy.entry() command on two consecutive bars to enter and add to a long position. Both calls use "buy" as the id argument. After creating the second entry order, the script calls the strategy.exit() command once with "buy" as its from_entry argument to generate separate exit orders for each trade with that entry ID. When the market price reaches the takeProfit or stopLoss value, the broker emulator fills two exit orders and closes the position:

A single strategy.exit() call can also generate exit orders for all entries in an open position, irrespective of entry ID, if it does not include a from_entry argument.

Below, we changed the strategy.entry() instance in the above script to create an entry order with a distinct ID on each call, and we removed the from_entry argument from the strategy.exit() call. Because this script version does not specify the entries to which the exit orders apply, the strategy.exit() call creates orders for every trade in the position:

It’s crucial to note that a call to strategy.exit() without a from_entry argument persists and creates exit orders for all open trades in a position, regardless of when the entries occur. This behavior can affect strategies that manage positions with multiple entries or exits. If a strategy has an open position and calls strategy.exit() on any bar without specifying a from_entry ID, it generates exit orders for each entry created before or on that bar, and it continues to generate exit orders for subsequent entries after that bar until the position closes.

Let’s explore this behavior and how it works. The script below calls the strategy.entry() command to create a long entry order on each bar within a user-specified time range. It also calls the strategy.exit() command without a from_entry argument on only one bar within that range to generate exit orders for every entry in the open position. The exit command uses a loss value of 0, which means that an exit order fills each time the market price is not above one of the entry prices.

The script prompts the user to select three points before it starts its calculations. The first point specifies when order creation begins, the second determines when the single strategy.exit() call occurs, and the third specifies when order creation stops:

Note that:

- We included pyramiding = 100 in the strategy() declaration statement, allowing the position to include up to 100 open trades from strategy.entry() orders.
- The script uses labels and a bgcolor() call to signify when order placement starts and stops and when the strategy.exit() call occurs.
- The script draws a line and a label at the lowest entry price to show the value the market price must reach to close the entire position.
We can observe the unique exit behavior of the strategy.exit() command in this example by comparing the code itself with the script’s visuals. The script calls the strategy.exit() command one time , only on the bar with the blue label. However, that single call places exit orders for every entry that occurs before or on that bar, then continues placing exit orders for each new entry after that bar. This behavior occurs because the strategy.exit() function cannot determine when to stop placing orders if it does not link to entries with a specific ID. In this case, the command only ceases to create new exit orders only after the position fully closes .

The above script exhibits different behaviors if we include a from_entry argument in the strategy.exit() call. If a call to this command specifies a from_entry ID, the exit orders apply to entries that the strategy created before or on the bar of the call using that ID. The command does not place exit orders for subsequent entries created after the bar in that case, even if those entries have the same ID.

In the script version below, we added from_entry = "Entry" to our script’s strategy.exit() call to specify that it produces exit orders only for entries that have the “Entry” ID. Only 17 exits occur across the same range this time, each corresponding to an entry order created before or on the bar with the blue label. The call does not generate new orders for any trade that the strategy opens after that bar, regardless of their entry ID:

### ​ strategy.close() ​ and ​ strategy.close_all() ​
The strategy.close() and strategy.close_all() commands generate orders to exit from an open position. Unlike strategy.exit() , which creates price-based exit orders (e.g., stop-loss ), these commands generate market orders that the broker emulator fills on the next available tick, irrespective of the price.

The example script below demonstrates a simple strategy that enters and exits a position using only market orders . The script executes a strategy.entry() call to place a “buy” market order once every 50 bars, then calls the strategy.close() command to close any open “buy” trade 25 bars later:

Notice that the strategy.close() call in this script uses “buy” as its required id argument. Unlike strategy.exit() , this command’s id parameter specifies the entry ID of an open trade. It does not represent the ID of the resulting exit order. If a market position consists of multiple open trades with the same entry ID, a single strategy.close() call with that ID as its id argument generates a single market order to close all of those trades in one transaction.

The following script creates a “buy” order using a strategy.entry() call once every 25 bars, and it calls the strategy.close() command with "buy" as its id argument to close all open trades with that entry ID once every 100 bars. The market order from the strategy.close() call closes the entire position in this case because every open trade in the position has the same “buy” entry ID:

Note that:

- We included pyramiding = 3 in the strategy() declaration statement, allowing the script to generate up to three entries per position using strategy.entry() calls.
The strategy.close_all() command generates a market order to close any open position. Unlike strategy.close() , this command does not link to any specific entry ID. Using the strategy.close_all() command is helpful when a strategy must exit as soon as possible from a position consisting of multiple open trades with different entry IDs.

The script below places “A”, “B”, and “C” entry orders sequentially based on the number of open trades as tracked by the strategy.opentrades variable. Then, it calls the strategy.close_all() command to create a single order that closes the entire position on the following bar:

### ​ strategy.cancel() ​ and ​ strategy.cancel_all() ​
The strategy.cancel() and strategy.cancel_all() commands allow strategies to cancel unfilled orders before the broker emulator processes them. These order cancellation commands are most helpful when working with price-based orders , including all orders from strategy.exit() calls and the orders from strategy.entry() or strategy.order() calls that include limit or stop arguments.

The strategy.cancel() command has a required id parameter, which specifies the ID of the entry or exit orders to cancel. The strategy.cancel_all() command does not have such a parameter because it cancels all unfilled orders, regardless of ID.

The following strategy calls the strategy.entry() command to place a “buy” limit order 500 ticks below the closing price while executing on the bar that is 100 bars before the latest bar. Then, on the next bar, it calls the strategy.cancel() command to cancel the order before the broker emulator executes it.

The following strategy places a “buy” limit order 500 ticks below the closing price 100 bars before the last chart bar with strategy.entry() , and it cancels the order on the next bar with strategy.cancel() . The script highlights the chart’s background to signify when it places and cancels the “buy” order, and it draws a horizontal line at the order’s price. As shown below, our example chart shows no entry marker when the market price crosses the horizontal line, because the strategy already cancels the order (when the chart’s background is orange) before the price reaches that level:

The strategy.cancel() command cancels all unfilled orders that have the specified entry ID. It does nothing if the specified id represents the ID of an order that does not exist. If the strategy has more than one unfilled order with the same entry ID, the command cancels all of them at once.

Below, we modified the previous script to place a “buy” limit order on three consecutive bars, starting 100 bars before the last chart bar. After placing all three orders, the strategy cancels them using a single strategy.cancel() call with “buy” as the id argument, resulting in no new trades when the market price reaches any of the order prices indicated by the horizontal lines:

Note that:

- We included pyramiding = 3 in the strategy() declaration statement, allowing three successive entries from strategy.entry() calls per position. The script would also achieve the same result without this setting if it called the strategy.order() command instead, because a strategy’s pyramiding setting does not affect orders from that command.
The strategy.cancel() and strategy.cancel_all() commands can cancel orders of any type, including market orders . However, it is important to note that either command can cancel a market order only if its call occurs on the same script execution as the order placement command. The cancellation command has no effect if the call happens after that point, because the broker emulator always fills market orders by the next available tick .

The example below places a “buy” market order with a strategy.entry() call 100 bars before the latest bar. Then, it attempts to cancel that order with a strategy.cancel_all() call on the next bar. The cancellation command does not affect the “buy” order in this case. The broker emulator fills the market order on the next bar’s opening tick, before the script executes the strategy.cancel_all() call:

## Position sizing
Pine Script strategies feature two ways to control the sizes of the orders that open and modify positions:

- Set a default fixed quantity type and value for the orders. Programmers can specify defaults for these properties by including default_qty_type and default_qty_value arguments in the strategy() declaration statement. Script users can adjust these defaults via the “Default order size” inputs in the “Settings/Properties” tab.
- Include a non-na qty argument in the strategy.entry() or strategy.order() call. If a call to either of these commands specifies a non-na qty value, that call ignores the strategy’s default quantity type and value and places an order for qty contracts/shares/lots/units instead.
The following example uses strategy.entry() calls with different qty arguments for long and short trades. When the current bar’s low equals the lowest value, the script places a “Buy” order to enter a long position of longAmount units. Otherwise, when the high equals the highest value, it places a “Sell” order to enter a short position of shortAmount units:

Notice that although we’ve included default_qty_type and default_qty_value arguments in the strategy() declaration statement, the strategy does not use this default setting to size its orders. Instead, the specified qty value in the entry commands takes precedence. To use the strategy’s default order size, we must remove the qty arguments from the strategy.entry() calls or set their values to na .

Below, we edited the previous script by including ternary expressions for the qty arguments in both strategy.entry() calls. These expressions replace input values of 0 with na . Now, if the specified longAmount or shortAmount value is 0, the corresponding entry orders use the strategy’s default order size instead, as we see below:

## Closing a market position
By default, strategies close a market position using the First In, First Out (FIFO) method. If a strategy uses this behavior, any exit order closes or reduces the position starting with the first open trade, even if the exit command specifies the entry ID of a different open trade. To override this default behavior, include close_entries_rule = "ANY" in the strategy() declaration statement.

The following example script places “Buy1” and “Buy2” entry orders sequentially, starting 100 bars before the latest chart bar. When the position size is 0, it calls the strategy.entry() command to place the “Buy1” order for five units. After the strategy’s position size matches the size of that order, the second strategy.entry() call places the “Buy2” order for ten units. The strategy then creates “bracket” exit orders for both entries using a single strategy.exit() call without a from_entry argument. For visual reference, the script also plots the strategy.position_size value in a separate pane:

Note that:

- We included pyramiding = 2 in the strategy() declaration statement, allowing two successive entries from strategy.entry() calls per position.
Each time the market price triggers an exit order, the above script exits from the open position, starting with the oldest open trade. This FIFO behavior applies even if we explicitly specify an exit from “Buy2” before “Buy1” in the code.

The script version below calls the strategy.close() command with “Buy2” as the id argument, and it includes “Buy1” as the from_entry argument in the strategy.exit() call. The market order from the strategy.close() call executes on the next available tick. Therefore, the broker emulator fills it before the take-profit and stop-loss orders from the strategy.exit() call:

The market order from the script’s strategy.close() call is for 10 units because it links to the open trade with the “Buy2” entry ID. A user might expect this strategy to close that trade completely when the order executes. However, the “Trades” tab in the strategy report shows that five units of the order close the “Buy1” trade first because it is the oldest, and the remaining five units close half of the “Buy2” trade. Then, the “bracket” orders from the strategy.exit() call close the rest of the position later:

Note that:

- If we included close_entries_rule = "ANY" in the strategy() declaration statement, the market order from the strategy.close() call would close the open trade with the “Buy2” entry ID first , and then the “bracket” orders from the strategy.exit() call would close the trade with the “Buy1” entry ID.
## OCA groups
One-Cancels-All (OCA) groups allow a strategy to fully or partially cancel specific orders when the broker emulator executes another order from the same group. To assign an order to an OCA group, include an oca_name argument in the call to the order placement command . The strategy.entry() and strategy.order() commands also allow programmers to specify an OCA type , which defines whether a strategy cancels , reduces , or does not modify the order after executing other orders.

Note All order placement commands that issue orders for the same OCA group must specify the same group name and OCA type. If two commands have the same oca_name value but different oca_type values, the strategy considers them to be from two distinct groups . In other words, an OCA group cannot mix the strategy.oca.cancel , strategy.oca.reduce , and strategy.oca.none OCA types.

### ​ strategy.oca.cancel ​
If an order placement command uses strategy.oca.cancel as its oca_type argument, the strategy completely cancels the resulting order if another order from the same OCA group executes first.

To understand how this OCA type impacts a strategy’s orders, consider the following script, which places orders when the ma1 value crosses the ma2 value. If the strategy.position_size value is 0 when the cross occurs, the strategy places two stop orders using strategy.order() calls. The first is a long order at the bar’s high, and the second is a short order at the bar’s low. If the strategy already has an open position during the cross, it calls the strategy.close_all() command to close the position with a market order :

Depending on the price action, the strategy might fill both stop orders before creating the closing market order. In that case, the strategy exits the position without executing the strategy.close_all() call because both orders have the same size. We see this behavior in the chart below, where the strategy alternated between filling the “Long” and “Short” orders a few times without executing an order from the strategy.close_all() command:

To eliminate cases in which the strategy fills the “Long” and “Short” orders before evaluating the strategy.close_all() call, we can instruct it to cancel one of the orders after the broker emulator fills the other. Below, we included “Entry” as the oca_name argument and strategy.oca.cancel as the oca_type argument in both strategy.order() calls. Now, after the either the “Long” or “Short” order fills, the strategy cancels the other order and waits for the market order from the strategy.close_all() command to close the position:

### ​ strategy.oca.reduce ​
If an order placement command uses strategy.oca.reduce as its OCA type, the strategy does not cancel the resulting order entirely if another order with the same OCA name executes first. Instead, it reduces the order’s size by the filled number of contracts/shares/lots/units. This behavior is particularly useful for custom exit strategies.

The following example demonstrates a long-only strategy that generates a single stop-loss order and two take-profit orders for each new entry. When a faster moving average crosses over a slower one, the script calls the strategy.entry() command with the argument qty = 6 to create an entry order. Then, it uses three strategy.order() calls to create a stop order at the stop value and two limit orders at the limit1 and limit2 values. The strategy.order() call for the “Stop” order uses the argument qty = 6 , and the two calls for the “Limit 1” and “Limit 2” orders both use qty = 3 :

After adding this strategy to the chart, we see that it does not work as initially intended. The problem with this script is that the orders from the strategy.order() command do not belong to an OCA group by default (unlike strategy.exit() , whose orders automatically belong to a strategy.oca.reduce OCA group). Because the strategy does not assign the strategy.order() calls to any OCA group, it cannot reduce any unfilled stop or limit orders after a pending order executes. Consequently, if the broker emulator fills the stop order and at least one of the limit orders, the traded quantity exceeds the open long position, resulting in an open short position:

For our long-only strategy to work as we intended, we must instruct it to reduce the sizes of the unfilled stop/limit orders after one of them executes to prevent selling a larger quantity than the open long position.

Below, we specified “Bracket” as the oca_name argument and strategy.oca.reduce as the oca_type argument in all the script’s strategy.order() calls. These changes tell the strategy to reduce the sizes of the orders in the “Bracket” group each time the broker emulator fills one of them. This version of the strategy never simulates a short position, because the total size of its filled stop and limit orders never exceeds the long position’s size:

Note that:

- We also changed the qty value of the “Limit 2” order to 6 instead of 3 because the strategy reduces that order’s amount by three units after it executes the “Limit 1” order. Keeping the qty value of 3 would cause the second limit order’s size to decrease to 0 after the strategy fills the first limit order, resulting in no effect on the position.
### ​ strategy.oca.none ​
If an order placement command uses strategy.oca.none as its oca_type value, all orders from that command execute independently of any OCA group. This value is the default oca_type argument for the strategy.order() and strategy.entry() commands.

## Currency
Pine Script strategies can simulate trades using different account currencies in their calculations. To set the default account currency for a strategy, include one of the currency* variables as the currency argument in the strategy() declaration statement. The default argument is currency.NONE , which specifies that the strategy uses the quoted currency on the chart by default (the currency indicated by the syminfo.currency variable). Users can change the strategy’s account currency via the “Initial capital” inputs in the “Settings/Properties” tab and at the top of the strategy report .

If a strategy script uses an account currency that differs from the chart’s currency, it uses the previous daily value of a corresponding currency pair from the most popular exchange to determine the conversion rate for all necessary calculations. If no available exchange provides the conversion rate directly, the strategy uses a spread to calculate the rate. The strategy multiplies all monetary values, such as simulated profits and losses, by the retrieved rate to express them in the account currency. Likewise, it inverts the rate to convert values in the account currency to prices in the quoted currency. To retrieve the rate that the strategy uses for currency conversion, call the request.currency_rate() function with syminfo.currency as the from argument and strategy.account_currency as the to argument.

Tip Programmers can also directly convert values expressed in a strategy’s account currency to the chart’s currency, and vice versa, by using the strategy.convert_to_symbol() and strategy.convert_to_account() functions.

The following example demonstrates how currency conversion affects a strategy’s monetary values, and how conversion rate calculations in a strategy match the calculations used by the request.*() functions.

On each of the latest 500 bars, the strategy below places an entry market order with the strategy.entry() command, then places a take-profit and stop-loss order one tick away from the entry price using the strategy.exit() command. Each entry order uses the size 1.0 / syminfo.mintick . Therefore, the resulting profit or loss from each trade is syminfo.pointvalue units of chart currency per tick. We included currency.EUR as the currency argument in the strategy() declaration statement, causing the strategy to convert necessary values to Euros by default.

The script calculates the absolute one-bar change in the ratio of the strategy’s net profit to the symbol’s point value to derive the value of one unit of the chart’s currency in Euros. It plots the result alongside the value returned by a request.currency_rate() call that uses syminfo.currency and strategy.account_currency as the from and to arguments. As shown on the chart below, both plots show the same values, confirming that the strategy and the data request use the same daily conversion rate in their calculations:

Note that:

- If a strategy executes on a chart with a timeframe higher than “1D”, it uses the data from one day before each historical bar’s closing time in currency conversions. For example, on a weekly chart, the strategy performs currency conversions using the confirmed rate from the previous Thursday’s close. However, it still uses the latest confirmed daily rate on realtime bars.
## Altering calculation behavior
Similar to an indicator, a strategy script executes across all historical chart bars in order, then continues to execute across realtime bars that become available after updates from the data feed. However, while indicators always executes once per bar on historical bars and once per tick on realtime bars, a strategy script can execute differently on historical bars, realtime bars, or both, depending on the selected strategy properties.

Tip Understanding how these settings impact a strategy requires some knowledge of Pine’s Execution model . Therefore, we recommend reviewing the basics of the model before exploring the information below.

Unless otherwise specified, a strategy script executes strictly once per closed bar , regardless of whether a bar is part of the historical dataset or a new bar from the realtime data feed. If the current bar is open, the strategy waits until the bar closes before updating calculations or placing new orders. Additionally, each new order in the strategy’s simulation has a one-tick delay by default. Therefore, when using these default behaviors, a strategy places orders on a bar only when it reaches the bar’s close, and the earliest point at which the broker emulator can fill those orders is at the open of the following bar.

Users can configure a strategy to perform more than one execution per historical or realtime bar, allowing for more granular calculations and order fills, by selecting the checkboxes in the strategy’s Script execution settings. Users can also change the strategy’s order delay on closed bars to zero ticks by selecting the “None” option from the “Order execution delay” input in the “Settings/Properties” tab. Programmers can set the default script execution and order delay behaviors by including arguments for the calc_on_every_tick , calc_on_order_fills , calc_on_every_history_tick , and process_orders_on_close parameters in the strategy() declaration statement.

The sections below explain how each of these parameters affects a strategy’s default calculation behaviors.

Notice Modifying a strategy’s “Script execution” settings can cause repainting in the strategy’s calculations and results, because they define different behaviors for historical and realtime bars, and both types of bars often have different levels of intrabar detail. Such differences can affect the behavior of order placement commands , Pine Logs , alerts , and any variables or fields that use the varip declaration mode . Therefore, when modifying these settings, we recommend inspecting a strategy’s logic carefully to ensure that it behaves as intended.

### ​ calc_on_every_tick ​
The calc_on_every_tick parameter of the strategy() declaration statement specifies the default behavior of the strategy’s executions on realtime bars . If the value is true , the script executes to update its calculations on every new tick in an open realtime bar, similar to an indicator. The default value is false . Script users can override the specified default by selecting the “On realtime bar tick” checkbox from the Script execution settings in the “Settings/Properties” tab and at the top of the strategy report .

Configuring a strategy to execute on each realtime tick is sometimes useful when forward testing or updating visuals on live data, because it allows the strategy to perform more granular calculations using the latest price and volume updates for an open bar. However, depending on the strategy’s logic, using this setting can also cause the strategy to behave differently across historical and realtime bars, leading to repainting in the strategy’s orders and performance results. After a script reloads, all elapsed realtime bars from the previous run become historical bars in the new run, and the new historical bars do not preserve intrabar data from previous realtime ticks. Consequently, if a strategy places orders on the ticks within an open bar, it might not be able to reproduce the same orders after reloading.

The following example demonstrates how executing a strategy’s logic on each new tick can significantly change the behavior of orders on realtime bars. If the current value of the close variable is the highest value in the series over a specified length, the script below calls the strategy.entry() command to place a long entry order. Otherwise, if the close value is the lowest over the same length, the script uses a separate strategy.entry() call to place a short entry order. We included calc_on_every_tick = true in the script’s strategy() declaration statement to allow a new execution on each realtime tick by default:

Note that:

- The script uses a pyramiding value of 20, which allows to 20 entries per position using calls to the strategy.entry() command.
- The script indicates realtime bars by highlighting the chart’s background in orange when the barstate.isrealtime value is true .
Because this strategy allows executions on every realtime tick, it updates its calculations and can place new orders after each new update from the data feed. Below, we applied the script to a chart and let it run on several realtime bars. On the chart’s historical bars, the script places up to one market order per bar, and the broker emulator fills each order at the open of the following bar. By contrast, on realtime bars (the bars with an orange background), the script places multiple orders per bar – one for every tick on which the latest available close value equals the highest or lowest value over the specified length. Additionally, the broker emulator fills most of the orders on each highlighted bar before the next bar opens, because every update to a realtime bar is a valid tick for filling orders:

After we refresh our chart and run the script on the same bars again, the elapsed realtime bars from the previous script run become historical bars in the new run, and the script’s behavior changes on those bars. Rather than placing multiple orders per bar on the former realtime bars, the script places only one order on each closed bar whose final price equals the highest or lowest value, and the broker emulator fills that order at the open of the following bar:

Note that:

- This strategy also behaves differently if we enable executions after each order fill or on each historical tick , because both settings allow additional executions and fill prices for orders on historical bars . See the calc_on_order_fills and calc_on_every_history_tick sections below to learn more.
Tip When using the “On realtime bar tick” setting, users can help align script behaviors on historical and realtime bars by enabling the “On history bar tick” setting. When active, the script executes on each available tick across historical bars to approximate how the strategy would behave when executing on those bars as they formed. Allowing executions on historical ticks does not eliminate repainting. However, it can help reduce significant differences between the script’s behaviors on historical and realtime bars for more realistic results. See the calc_on_every_history_tick section for more information.

### ​ calc_on_order_fills ​
The calc_on_order_fills parameter of the strategy() declaration statement affects the default behavior of the strategy’s executions on both historical bars and realtime bars. If the value is true , the script performs an additional execution on each tick where the broker emulator fills an order. The default value is false . Script users can override the specified default behavior by selecting the “On order fill” checkbox from the Script execution settings in the “Settings/Properties” tab and at the top of the strategy report .

When using this setting, a strategy updates its calculations and can place new orders immediately after an order fills, without waiting for a bar’s closing tick. Those extra calculations update the strategy.* built-ins with more granular information that is otherwise not available until the closing tick, such as the current size or the average price of a new or modified position. This behavior is sometimes useful when backtesting or forward testing strategies that enter and exit trades mid-bar.

The example script below uses the strategy.entry() command to place a “Buy” entry order on any bar where the value of the strategy.position_size variable is 0. It also calls the strategy.exit() command on each bar to place “Exit” bracket orders to close any active “Buy” trade. The script calculates the stop-loss and take-profit prices for the exit orders based on the value of the strategy.position_avg_price variable.

The strategy() declaration statement includes the argument calc_on_order_fills = true . Therefore, in addition to updating calculations on each bar’s close, the strategy performs new calculations on each tick where the broker emulator fills a “Buy” or “Exit” order by default. Each time an “Exit” order fills, the strategy’s position size reverts to 0, triggering a new “Buy” order. The emulator then fills the “Buy” order on the next available tick, and the strategy.position_avg_price value automatically updates on that tick to store the average price of the new position. The strategy then uses the updated price to set the prices of new “Exit” orders. This cycle of intrabar entries and exits repeats across the bars in the dataset:

Note that:

- This strategy can repaint after running on realtime bars. As the strategy runs on historical bars, the broker emulator uses the chart’s OHLC prices or the prices from a lower timeframe to determine the ticks available for filling orders, depending on the selected level of historical bar detail . By contrast, each new update to a realtime bar is a valid tick on which an order can fill. Consequently, when elapsed realtime bars become historical bars after the script reloads, the strategy may place or fill orders on those bars at different prices or times.
- If we deactivate executions after order fills, the strategy would not place new orders before a bar closes. Instead, it would wait for a bar’s closing tick before placing any “Buy” order. The broker emulator would then fill the order at the open of the following bar, and the strategy.position_avg_price variable would return a usable value for calculating the “Exit” order prices on that bar.
It’s crucial to note that enabling some strategies to execute after order fills can cause lookahead bias on historical bars. As a strategy executes across a dataset’s history while using this setting, built-in variables that store price and volume data for the current bar – including high , low , close , and volume – consistently hold the bar’s final values . Consequently, if the strategy uses these built-ins to control order logic on the ticks within a historical bar, it may produce misleading backtest results, as the logic relies on data that would not be available in live trading until the market reaches the bar’s closing tick. Furthermore, the strategy’s apparent future awareness on historical bars is impossible to reproduce on realtime bars . The bottom of the strategy report typically displays a warning banner when the “On order fill” execution setting is active to inform users about this behavior.

The following example demonstrates a simple strategy that produces lookahead bias when using the “On order fill” execution setting. The script calls the strategy.entry() command to place a long market order, then calls the strategy.exit() command to place a take-profit order at the current bar’s high value. By default, the script places the entry order at the current bar’s closing tick, and the broker emulator fills that order at the open of the following bar. The order fill on that bar triggers an additional execution, causing the strategy.exit() call to set the exit level to that bar’s high price. As shown below, on most historical bars where the script enters a new long trade, it then exits the trade at the bar’s exact high . This behavior is misleading , because knowing the exact high of a bar on the opening tick – let alone numerous consecutive times – is impossible to achieve in real-world trading:

Note that:

- This script declares the openTime variable using the varip keyword. If a variable declaration uses this keyword, the variable persists across all executions without resetting to a previous state. The script uses this variable in the if structure to limit the placement of new orders to the current bar’s first tick – where the variable’s value does not yet match the current bar’s opening time. To learn more about the behavior of this keyword, refer to the varip section of the Variable declarations page.
- This script behaves very differently on realtime bars . Rather than exiting trades at a bar’s exact high, the strategy exits each trade at the bar’s developing high as of the next tick or the current tick, because the final high price on a realtime bar is unknown until after the bar closes.
Tip To enable script executions on historical intrabar ticks without causing this form of lookahead bias, use the “On history bar tick” execution setting rather than “On order fill”. See the calc_on_every_history_tick section below to learn more.

### ​ calc_on_every_history_tick ​
The calc_on_every_history_tick parameter of the strategy() declaration statement specifies the default behavior of the strategy’s executions on historical bars . This parameter requires a named argument , which includes the parameter’s name and the assigned value (e.g., calc_on_every_history_tick = true ). If the value is true , the script executes to update its calculations on every available tick in each historical bar. The default value is false . Script users can override the specified default by selecting the “On history bar tick” checkbox from the Script execution settings in the “Settings/Properties” tab and at the top of the strategy report .

Note The “On history bar tick” feature is available only to users who have a Premium or Ultimate plan . Additionally, the feature requires a standard chart type. If the setting is enabled by default, the strategy raises a runtime error if it is not compatible with the user’s plan or the current chart.

A strategy that uses the “On history bar tick” setting treats historical bars similarly to realtime bars . As the script executes on the available ticks of each historical bar, multiple built-in variables that hold price and volume data for the bar, including high , low , close , and volume , update on every tick to approximate the progression of values that would have been visible to the strategy when the bar was still open. This behavior helps reduce the risk of lookahead bias while executing on historical ticks, as the strategy cannot access the final price or volume data for a historical bar before reaching the bar’s closing tick.

Note This setting does not affect the behavior of variables that track bar states . For example, the value of the barstate.isconfirmed variable is always true on historical bars. It never changes to false during the executions across a historical bar’s intrabar ticks while the “On history bar tick” setting is active.

The visibility of values within each historical bar depends on the selected level of historical bar detail . If the strategy uses high historical detail, it determines the high, low, close, and volume values available on each tick by requesting data from a lower timeframe . Otherwise, if the strategy uses the default level of detail, the values available on each tick depend on the broker emulator’s assumptions about the price action within the historical bar. The following tables describe the values stored by the high , low , close , and volume variables on each tick in a historical bar when using the default level of detail, based on the assumed order of price action within the bar:

Open → High → Low → Close

| Tick | high | low | close | volume |
| 1 | Open | Open | Open | Total volume * 0.25 |
| 2 | High | Open | High | Total volume * 0.5 |
| 3 | High | Low | Low | Total volume * 0.75 |
| 4 | High | Low | Close | Total volume |
Open → Low → High → Close

| Tick | high | low | close | volume |
| 1 | Open | Open | Open | Total volume * 0.25 |
| 2 | Open | Low | Low | Total volume * 0.5 |
| 3 | High | Low | High | Total volume * 0.75 |
| 4 | High | Low | Close | Total volume |
Note that:

- Variables that store values calculated from the chart’s OHLCV data also update on each tick based on these assumptions. For example, if the second tick of the current historical bar is at the high , the value of the ohlc4 variable equals (open + open + high + high) / 4 . However, the value still equals (open + high + low + close) / 4 on the bar’s final tick.
The following example demonstrates a strategy that enters trades on the ticks within historical bars when using the “On history bar tick” execution setting. The script declares two persistent variables named openTime and firstPrice to track time and price information from the first tick on which it executes in each historical bar. On each tick where the openTime value does not match the bar’s opening time, the script reassigns that variable to store the current timestamp, then reassigns the firstPrice variable to hold the close value (i.e., the current price) for that tick.

The script uses the firstPrice value and the 10-bar highest and lowest prices to control order placement commands. On each tick where the current price is less than the firstPrice value and not equal to the current highest or lowest price, the script calls the strategy.entry command to place a long market order, then calls the strategy.exit() command to place take-profit and stop-loss orders at the highest and lowest values:

Note that:

- This script simulates historical trades only while using the “On history bar tick” setting. Without the setting enabled, the value of the close variable on historical bars always represents the final closing price rather than the intrabar price on each tick. Therefore, when the script reassigns the firstPrice variable on any historical bar, that variable also stores the bar’s final price, and the close < firstPrice condition consistently evaluates to false , resulting in no trades .
- By default, this script does not simulate trades on realtime bars , because it executes only once at each bar’s close on that part of the dataset. To enable trades on realtime bars, select the “On realtime bar tick” checkbox in the “Script execution” settings or add calc_on_every_tick = true to the strategy() declaration statement.
- By default, the broker emulator fills the strategy’s orders based on the chart prices of each historical bar, because the script uses the default level of historical bar detail . Users can simulate the trades using more granular prices by selecting the “High” option in the script’s Bar detalization settings or including use_bar_magnifier = true in the declaration statement.
### ​ process_orders_on_close ​
The process_orders_on_close parameter of the strategy() declaration statement specifies the default behavior of orders created on a bar’s closing tick . If the value is true , the broker emulator can fill orders created on a bar’s close immediately, on the same tick , rather than waiting for the next available tick. If the value is false (the default), the earliest point at which the emulator can fill orders created on a bar’s closing tick is on the next tick, at the open of the following bar. Script users can override the specified default behavior via the “Order execution delay” dropdown menu in the “Settings/Properties” tab.

Strategies apply a one-tick delay to order fills by default because creating and filling an order on the same tick is typically unrealistic in real-world trading. However, simulating order fills at a bar’s close can be useful in some scenarios, such as when backtesting manual strategies in which traders exit a position immediately before the market closes, or when using order fill alerts to potentially trigger real-world orders before the start of the next trading session.

Note Sending alerts to a third-party service for filling orders when using this setting might not work as a trader intends, especially in non-continuous markets, because the alerts still occur after the session closes. Depending on the external service and the type of market, real-world orders based on such alerts might not fill until after the market opens again. This setting does not affect the execution of orders that a strategy places before a bar’s closing tick. If a strategy places orders on the ticks within a bar, the broker emulator fills those orders on the next available tick.

The following example demonstrates how removing the execution delay in orders at a bar’s close changes the timing of trades. The initial script below uses the strategy.entry() command to place alternating long and short market orders across the dataset. The script places an order only at the close of each bar, then highlights the chart’s background in blue or red to indicate the order direction. The strategy() declaration statement does not include a process_orders_on_close argument. Therefore, the broker emulator applies a one-tick delay to all orders placed on a bar’s close by default. As shown by the trade markers on the chart’s bars, after the strategy creates an order, the broker emulator fills the order at the open of the following bar:

If we add process_orders_on_close = true to the strategy() declaration statement, broker emulator fills each market order on the same closing tick where the script creates it by default. After applying this change to the script above, the trade markers on the chart now align with the displayed background colors, indicating that each order fills immediately rather than at the next bar’s opening tick:

Tip The strategy.close() and strategy.close_all() commands feature an immediately parameter, which enables programmers to remove the delay for closing market orders without affecting the behavior of other order placement commands. If the value is true , the broker emulator fills the resulting market order on the same tick where the strategy calls the command. If false (the default), the behavior of the order depends on the strategy’s “Order execution delay” setting.

## Simulating trading costs
Strategy performance reports are more relevant and meaningful when they include potential real-world trading costs. Without modeling the potential costs associated with their trades, traders may overestimate a strategy’s historical profitability, potentially leading to suboptimal decisions in live trading. Pine Script strategies include inputs and parameters for simulating trading costs in performance results.

### Commission
Commission is the fee that a broker/exchange charges when executing orders. The commission can be a flat fee per order, a fee per contract/share/lot/unit, or a percentage of the total transaction value. Programmers can specify the default commission settings for their strategies by including commission_type and commission_value arguments in the strategy() declaration statement. If not specified, the strategy applies no commission to filled orders. Users can override the specified defaults by adjusting the “Commision” inputs in the strategy’s “Settings/Properties” tab.

The following script is a simple strategy that enters a long position using 2% of its available equity when the current close value is the highest value over a user-specified length, and closes the trade when the close value is the lowest across that same number of bars. Because the declaration statement does not specify any commission_* arguments, the strategy simulates transactions without any commission by default:

Note that:

- The default_qty_type and default_qty_value arguments in the strategy() statement set the strategy’s default order type and size. This default order size applies only to orders from strategy.entry() and strategy.order() calls that do not include a qty argument. See the Position sizing section above for more information.
For our daily “NASDAQ:AAPL” chart above, the results in the strategy report show that the strategy had a positive equity growth of 18.67% over the testing range. However, these backtesting results do not account for any fees that the broker/exchange may charge.

Let’s see what happens to these results when we add commission to every trade in the strategy simulation. In the example below, we modified the previous script to include the arguments commission_type = strategy.commission.percent and commission_value = 1 in the strategy() declaration statement. With this change, the broker emulator now applies a commission of 1% of the transaction size to each filled order by default.

As shown below, after applying 1% commission to the strategy’s orders on the same dataset, the strategy report shows a significantly reduced net profit, as well as increased volatility in the strategy’s cumulative returns and an elevated maximum drawdown. These results highlight the impact that commission can have on a strategy’s simulated performance:

### Slippage and unfilled limits
In real-world trading, orders may execute at prices that differ from what the trader intended, due to volatility, liquidity, order size, and other market factors. Such differences can profoundly impact a strategy’s performance. The disparity between the expected fill price of an order and the actual fill price is known as slippage . Slippage is dynamic and unpredictable, making it impossible to simulate precisely. However, applying a small, fixed amount of slippage to every order in a backtest or forward test can help overall performance results align more closely with reality. Programmers can specify a strategy’s default slippage amount, as a fixed number of ticks , by including a slippage argument in the strategy() declaration statement. The default argument is 0. Script users can override the specified default by adjusting the “Slippage” input in the strategy’s “Settings/Properties” tab.

The following example demonstrates how simulating slippage impacts the fill prices of market orders in a strategy test. The script below places a “Buy” market order of 2% equity when the market price is above a rising EMA, then closes the position with another market order when the price dips below the EMA while it’s falling. The strategy() declaration statement includes the argument slippage = 20 . Therefore, by default, each order fills 20 ticks beyond the intended price in the unfavorable direction (higher for long orders, and lower for short orders). The script plots the each order’s expected fill price along with the simulated fill price after slippage to visually compare the difference:

Note that:

- Because the strategy applies constant slippage to all order fills, some orders can fill outside the candle range in the simulation. Therefore, we recommend exercising caution with this setting, as adding excessive simulated slippage can produce unrealistically worse testing results.
Some traders might assume that they can avoid the adverse effects of slippage by using limit orders . While market orders execute as soon as possible, irrespective of the price, limit orders execute at the specified price or a better value. They cannot execute at a worse price. However, in real-world trading, some limit orders might not fill when the market price reaches the specified value, due to insufficient liquidity or price action. Programmers can simulate the possibility of unfilled limit orders in their scripts by using the backtest_fill_limits_assumption parameter in the strategy() declaration statement. The parameter specifies the number of ticks that the price must move beyond each limit order’s level to trigger an order fill at that level. The default argument is 0, meaning that the broker emulator fills any limit order immediately if the price reaches the order’s level.

Note The “Limit order execution” input in a strategy’s “Settings/Properties” tab overrides the default assumption for filling limit orders. This input includes the options to fill each limit order when either the market price reaches the specified level or it moves one tick beyond that level. If the backtest_fill_limits_assumption argument is greater than 1, users can restore the default assumption specified in the declaration statement after using this input by selecting “Reset settings” from the “Defaults” dropdown menu at the bottom of the “Properties” tab.

The following example script places a limit order for 2% of the strategy’s equity at a bar’s hlcc4 price if the current high value is the highest price over a specified number of bars and no pending entry orders are active. The strategy closes the market position and cancels all pending orders if the current low value is the lowest price over the same length. Each time that the strategy triggers an order, it draws a horizontal line at the limitPrice value. It then updates the line on each bar until it closes the position or cancels the order:

By default, the broker emulator assumes that all limit orders are guaranteed to fill when the market price reaches their values. However, that may not be the case in a real-world market. Let’s add price verification to our script’s limit orders to account for potentially unfilled ones. In the example below, we added backtest_fill_limits_assumption = 3 to the strategy() statement. With this change, the broker emulator assumes that there is sufficient liquidity to fill a limit order only if the price moves three ticks beyond the order’s level. As shown below, using this fill assumption prevents the execution of some orders and changes the times of others:

Notice Using a nonzero backtest_fill_limits_assumption argument can affect the times at which limit orders execute, as shown above. However, regardless of the fill time, the broker emulator still executes verified limit orders at their specified prices . This behavior is a necessary compromise to preserve the intended fill prices of limit orders without causing lookahead bias , but it can also cause the orders to execute at times that may not be possible in real-word trading, especially if the argument is a large value. Therefore, we recommend that users exercise caution and understand this price-time limitation when applying price verification to limit orders.

## Risk management
Designing a strategy that performs well, especially across a broad range of markets, is a challenging task. Most strategies are designed for specific market patterns or conditions and can produce uncontrolled losses when applied to other datasets. Therefore, a strategy’s risk management behavior can be critical to its performance. Programmers can specify risk management criteria in their strategy scripts by using the strategy.risk.*() commands.

Strategies can incorporate any number of risk management criteria in any combination. All risk management commands execute on every tick and order execution event , regardless of any changes to the strategy’s calculation behavior . There is no way to deactivate any of these commands on specific script executions. Irrespective of a risk management command’s location, the command always applies to the strategy unless the programmer removes the call from the code. Below, we list the available risk management commands and the behaviors they define:

strategy.risk.allow_entry_in()

This command overrides the market direction allowed for all calls to the strategy.entry() command. If a user specifies the trade direction with the strategy.risk.allow_entry_in() function (e.g., strategy.direction.long ), the strategy enters trades only in that direction. If the script calls an entry command in the opposite direction of an open market position, the strategy generates a market order to close the position without entering a new trade in that direction.

strategy.risk.max_cons_loss_days()

This command cancels all pending orders, closes any open market position, and stops all additional trade actions after the strategy simulates a defined number of trading days with consecutive losses.

strategy.risk.max_drawdown()

This command cancels all pending orders, closes any open market position, and stops all additional trade actions after the strategy’s drawdown reaches the amount specified in the function call.

strategy.risk.max_intraday_filled_orders()

This command specifies the maximum number of filled orders per trading day (or per chart bar if the chart’s timeframe is higher than “1D”). If the strategy fills more orders than the specified limit, the command cancels all pending orders, closes any open market position, and halts trading activity until the end of the current session.

strategy.risk.max_intraday_loss()

This command controls the maximum allowed loss per trading day (or per chart bar if the chart’s timeframe is higher than “1D”). If the strategy’s losses reach the specified threshold, the command cancels all pending orders, closes the open market position, and stops all trading activity until the end of the current session.

strategy.risk.max_position_size()

This command specifies the maximum possible position size when calling the strategy.entry() command. If the size of an entry order results in a market position that exceeds the specified threshold, the strategy reduces the order quantity so that the resulting position does not exceed the limit.

## Margin and leverage
Margin is the minimum percentage of a market position that a trader must hold in their account as collateral to open and maintain that position. With a margin of 100%, the trader must cover the entire position using their account’s available funds. With a margin of 25%, the trader must cover only one-fourth of each position using their account’s funds to maintain a loan for the other three-fourths from the broker. Most brokers define a trader’s margin requirements based on a specified leverage amount, where leverage is the inverse of margin. For example, a leverage ratio of 4:1 is equivalent to 25% margin. A trader can open a position for up to four times their available funds when using this amount of leverage, because they must maintain only a fourth of each position’s size as collateral. In other words, the trader has four times the purchasing power that they would otherwise have when trading using only their account’s funds.

The margin_long and margin_short parameters of the strategy() declaration statement define the default required margin percentages for long and short trades, respectively. The strategy converts the specified percentages to leverage ratios and uses those ratios as the default values for the “Long leverage” and “Short leverage” inputs in the “Settings/Properties” tab. The default argument for both parameters is 100, which is equivalent to a leverage ratio of 1:1.

Notice A margin requirement of less than 0.2% (i.e., leverage greater than 500:1) is typically unrealistic in a real-world market. Using unrealistic levels of margin in a strategy can cause very misleading backtest results. Furthermore, using a margin of 0% is extremely misleading because it is equivalent to infinite leverage, which is impossible to achieve in any live trading environment. Therefore, when setting a strategy’s margin via the margin_* parameters, or adjusting leverage using the “Leverage *” inputs, we recommend specifying realistic values that align with current market conditions.

Trading with less than 100% margin can significantly increase a trader’s potential profits and their potential losses . In real-world trading, if the loss from a position causes the trader’s available margin to fall below the required margin, the broker issues a margin call , which is a demand for the trader to immediately deposit additional funds to cover the loss. If the trader fails to meet the demand, or if the losses reach beyond the broker’s limits, the broker forcibly liquidates all or part of the position to prevent further losses that the trader cannot cover.

To simulate this process in strategies, the broker emulator generates margin call events if a strategy’s available funds fall below the required margin percentage. Each time that a margin call event occurs, the emulator immediately liquidates four times the number of contracts/shares/lots/units required to cover the loss to help prevent continuous margin calls across subsequent bars. The emulator uses the following algorithm to determine the liquidated quantity for each event:

- Calculate the amount of capital spent on the position: Money Spent = Quantity * Entry Price
- Calculate the Market Value of Security (MVS): MVS = Position Size * Current Price
- Calculate the Open Profit as the difference between MVS and Money Spent . If the position is short, multiply this value by -1.
- Calculate the strategy’s equity value: Equity = Initial Capital + Net Profit + Open Profit
- Calculate the margin ratio: Margin Ratio = Margin Percent / 100
- Calculate the margin value, which is the cash required to cover the hypothetical account’s portion of the position: Margin = MVS * Margin Ratio
- Calculate the strategy’s available funds: Available Funds = Equity - Margin
- Calculate the total amount of money lost: Loss = Available Funds / Margin Ratio
- Calculate the number of contracts/shares/lots/units the account must liquidate to cover the loss, truncated to the same decimal precision as the minimum position size for the current instrument: Cover Amount = TRUNCATE(Loss / Current Price).
- Multiply the quantity required to cover the loss by four to determine the margin call size: Margin Call Size = Cover Amount * 4
Note A short trade typically entails borrowing shares from a broker to sell them at the current market price, then buying the shares back at a different price and returning them to the lender. The trade thus produces a profit if the trader purchases the shares at a lower price, or a loss if they purchase the shares at a higher price. Consequently, unlike long trades, short trades carry the risk of uncapped losses , because there is no definite limit on how far an instrument’s price can rise. Therefore, short trades in a strategy that uses any nonzero margin are subject to forced liquidation from margin call events, even if the margin_short argument is 100 or the “Short leverage” input value is 1.

To examine the above calculations in detail, the following example applies the Supertrend Strategy built-in script to a daily “NASDAQ:TSLA” chart. In the strategy’s properties, we set the order size to 300% of equity, and we set the strategy’s long leverage to 4. On the chart below, the strategy opens a long trade, then the broker emulator triggers margin call event a few bars later:

In the above image, the script enters the long position at the bar’s opening price on 16 Sep 2010. The strategy purchases 682,438 shares (Position Size) at 4.43 USD (Entry Price) using 25% margin. Then, on 23 Sep 2010, when the price drops to 3.9 USD (Current Price), the emulator triggers the margin call event and forcibly liquidates 111,052 shares . The calculations below explain how the broker emulator determines the liquidation quantity for this event:

```
Money spent: 682438 * 4.43 = 3023200.34MVS: 682438 * 3.9 = 2661508.2Open Profit: −361692.14Equity: 1000000 + 0 − 361692.14 = 638307.86Margin Ratio: 25 / 100 = 0.25Margin: 2661508.2 * 0.25 = 665377.05Available Funds: 638307.86 - 665377.05 = -27069.19Money Lost: -27069.19 / 0.25 = -108276.76Cover Amount: TRUNCATE(-108276.76 / 3.9) = TRUNCATE(-27763.27) = -27763Margin Call Size: -27763 * 4 = - 111052
```
Tip Programmers can use the strategy.margin_liquidation_price variable to retrieve the current price level at which the broker emulator will trigger a margin call event and forcibly liquidate part or all of an open position if the market price reaches it. For more information about how margin and leverage work in strategies, as well as details on how to calculate the liquidation price, refer to the How to simulate trading with leverage in Pine Script article in our Help Center.

## Using strategy information in scripts
Numerous built-ins within the strategy.* namespace and its sub-namespaces provide convenient solutions for programmers to use a strategy’s trade and performance information, including data shown in the strategy report , directly within their code’s logic and calculations.

Several strategy.* variables store essential information about a strategy, including its starting capital, equity, profits and losses, run-up and drawdown, and open position:

- strategy.account_currency
- strategy.initial_capital
- strategy.equity
- strategy.netprofit and strategy.netprofit_percent
- strategy.grossprofit and strategy.grossprofit_percent
- strategy.grossloss and strategy.grossloss_percent
- strategy.openprofit and strategy.openprofit_percent
- strategy.max_runup and strategy.max_runup_percent
- strategy.max_drawdown and strategy.max_drawdown_percent
- strategy.position_size
- strategy.position_avg_price
- strategy.position_entry_name
Additionally, the namespace features multiple variables that store general trade information, such as the number of open and closed trades, the number of winning and losing trades, average trade profits, and maximum trade sizes:

- strategy.opentrades
- strategy.closedtrades
- strategy.wintrades
- strategy.losstrades
- strategy.eventrades
- strategy.avg_trade and strategy.avg_trade_percent
- strategy.avg_winning_trade and strategy.avg_winning_trade_percent
- strategy.avg_losing_trade and strategy.avg_losing_trade_percent
- strategy.max_contracts_held_all
- strategy.max_contracts_held_long
- strategy.max_contracts_held_short
Programmers can use these variables to display relevant strategy information on their charts, create customized trading logic based on strategy data, calculate custom performance metrics, and more.

The following example demonstrates a few simple use cases for these strategy.* variables. The script uses them in its order placement and display calculations. When the calculated rank value crosses above 10 and the strategy.opentrades value is 0, the script calls the strategy.entry() command to place a “Buy” market order . On the following bar, where that order fills, the script calls strategy.exit() to create a stop-loss order at a user-specified percentage below the strategy.position_avg_price value. If the rank crosses above 80 during the open trade, the script calls strategy.close() to exit the position on the next bar.

The script creates a table to display formatted strings representing information from several of the above strategy.* variables on the main chart pane. The text in the table shows the strategy’s net profit and net profit percentage, the account currency, the number of winning trades and the win percentage, the ratio of the average winning trade to the average losing trade, and the profit factor (the ratio of the gross profit to the gross loss). The script also plots the strategy.equity series in a separate pane and highlights the pane’s background based on the strategy.openprofit value:

Note that:

- This script creates a stop-loss order one bar after the entry order because it uses strategy.position_avg_price to determine the price level. This variable has a non-na value only when the strategy has an open position .
- The script draws the table only on the last historical bar and all realtime bars because the historical states of tables are never visible . See the Reducing drawing updates section of the Profiling and optimization page for more information.
- The table.new() call includes force_overlay = true to display the table on the main chart pane.
### Individual trade information
The strategy.* namespace features two sub-namespaces that provide access to individual trade information: strategy.opentrades.* and strategy.closedtrades.* . The strategy.opentrades.* built-ins return data for incomplete (open) trades, and the strategy.closedtrades.* built-ins return data for completed (closed) trades. With these built-ins, programmers can use granular trade data in their scripts, allowing for more detailed strategy analysis and advanced calculations.

Both sub-namespaces contain several similar functions that return information about a trade’s orders, simulated costs, and profit/loss, including:

- strategy.opentrades.entry_id() / strategy.closedtrades.entry_id()
- strategy.opentrades.entry_price() / strategy.closedtrades.entry_price()
- strategy.opentrades.entry_bar_index() / strategy.closedtrades.entry_bar_index()
- strategy.opentrades.entry_time() / strategy.closedtrades.entry_time()
- strategy.opentrades.entry_comment() / strategy.closedtrades.entry_comment()
- strategy.opentrades.size() / strategy.closedtrades.size()
- strategy.opentrades.profit() / strategy.closedtrades.profit()
- strategy.opentrades.profit_percent() / strategy.closedtrades.profit_percent()
- strategy.opentrades.commission() / strategy.closedtrades.commission()
- strategy.opentrades.max_runup() / strategy.closedtrades.max_runup()
- strategy.opentrades.max_runup_percent() / strategy.closedtrades.max_runup_percent()
- strategy.opentrades.max_drawdown() / strategy.closedtrades.max_drawdown()
- strategy.opentrades.max_drawdown_percent() / strategy.closedtrades.max_drawdown_percent()
- strategy.closedtrades.exit_id()
- strategy.closedtrades.exit_price()
- strategy.closedtrades.exit_time()
- strategy.closedtrades.exit_bar_index()
- strategy.closedtrades.exit_comment()
Note that:

- Most built-ins within these namespaces are functions . However, the strategy.opentrades.* namespace also features a unique variable : strategy.opentrades.capital_held . Its value represents the amount of capital reserved by all open trades.
- Only the strategy.closedtrades.* namespace has .exit_*() functions that return information about exit orders .
All strategy.opentrades.*() and strategy.closedtrades.*() functions have a trade_num parameter, which accepts an “int” value representing the index of the open or closed trade. The index of the first open/closed trade is 0, and the last trade’s index is one less than the value of the strategy.opentrades / strategy.closedtrades variable.

The following example places up to five long entry orders per position, each with a unique ID, and it calculates metrics for specific closed trades.

The strategy places a new entry order when the close crosses above the median value without reaching the highest value, but only if the number of open trades is less than five. It exits each position using stop-loss orders from strategy.exit() or a market order from strategy.close_all() . Each successive entry order’s ID depends on the number of open trades. The first entry ID in each position is "Buy0" , and the last possible entry ID is "Buy4" .

The script calls strategy.closedtrades.*() functions within a for loop to access closed trade entry IDs, profits, entry bar indices, and exit bar indices. It uses this information to calculate the total number of closed trades with the specified entry ID, the number of winning trades, the average number of bars per trade, and the total profit from all the trades. The script then organizes this information in a formatted string and displays the result using a single-cell table :

Note that:

- This strategy can open up to five long trades per position by default because we included pyramiding = 5 in the strategy() declaration statement. See the pyramiding section for more information.
- The strategy.exit() call in this script persists and generates exit orders for every entry in the open position because it does not include a from_entry argument. See the Exits for multiple entries section to learn more about this behavior.
## Strategy alerts
Pine Script indicators (not strategies) have two different mechanisms to set up custom alert conditions: the alertcondition() function, which defines a separate alert trigger per function call, and the alert() function, which defines a single alert trigger based on all calls in the code, but provides greater flexibility in the number of calls, alert messages, etc.

Pine Script strategies cannot create alert triggers using the alertcondition() function, but they can create triggers with the alert() function. Additionally, each order placement command comes with its own built-in alert functionality that does not require any additional code to implement. As such, any strategy that uses an order placement command can issue alerts upon order execution. The precise mechanics of such built-in strategy alerts are described in the Order Fill events section of the Alerts page.

If a strategy uses both the alert() function and functions that create orders in the same script, the “Create Alert” dialog box provides a choice between the conditions to use as a trigger: alert() events, order fill events, or both.

For many trading strategies, the delay between a triggered alert and a live trade can be a critical performance factor. By default, strategy scripts execute alert() function calls only on the close of realtime bars, as if they used the alert.freq_once_per_bar_close frequency, regardless of the freq argument in the call. Users can change the allowed alert frequency by enabling the “On realtime bar tick” or “On order fill” Script execution setting. See the Altering calculation behavior section above to learn more about these settings.

Order fill alert triggers do not suffer the same limitations as the triggers from alert() calls. Alerts from order fill events execute immediately , regardless of the script’s execution settings. Therefore, they are often more suitable for sending alerts to third parties for automation. Users can specify the default message for order fill alerts by using the //@strategy_alert_message compiler annotation. The text included in the annotation populates the “Message” field in the “Create alert” dialog box.

The following script shows a simple example of a default order fill alert message. Above the strategy() declaration statement, the script includes the //@strategy_alert_message annotation with placeholders for the trade action, current position size, ticker name, and fill price values in the message text:

This script populates the “Create alert” dialog box with its default message when the user selects its name from the “Condition” section:

Each time the alert occurs, the strategy replaces the placeholders in the alert message with their corresponding values. For example:

## Notes on testing strategies
Testing and tuning strategies in historical and live market conditions can provide insight into a strategy’s characteristics, potential weaknesses, and possibly its future potential. However, traders should always be cautious of the biases and limitations of simulated strategy results, especially when using the results to support live trading decisions. This section outlines some caveats associated with strategy validation and tuning, and lists possible solutions to mitigate their effects.

Notice Although testing strategies on existing data might provide traders useful information about a strategy’s qualities, it’s crucial to understand that neither the past nor the present guarantees the future . Financial markets can change rapidly and unpredictably, leading to uncontrollable, unforeseen losses. Additionally, simulated results may not fully account multiple real-world factors that can impact trading performance. Therefore, we recommend that traders thoroughly understand the limitations of strategy simulations, and consider them only “parts of the whole” in their validation processes rather than basing decisions solely on the results.

### Backtesting and forward testing
Backtesting is a technique to evaluate the past performance of a trading strategy or model by simulating and analyzing its results on historical market data. This technique assumes that a strategy’s results on past data can provide insight into its strengths and weaknesses. When backtesting, many traders adjust the parameters of a strategy in an attempt to optimize its results. Analysis and optimization of historical results can help traders to gain a deeper understanding of a strategy’s characteristics. However, traders should always understand the risks and limitations when basing their live trading decisions on optimized backtest results.

It is prudent to also use realtime analysis as a tool for evaluating a trading system on a forward-looking basis. Forward testing aims to gauge the performance of a strategy in live market conditions, where factors such as trading costs, slippage, and liquidity can meaningfully affect overall trading performance. While forward testing has the distinct advantage of not being affected by some types of biases (e.g., lookahead bias or “future data leakage”), it does carry the disadvantage of being limited in the quantity of data to test. Therefore, although it can provide helpful insights into a strategy’s performance in current market conditions, forward testing is not typically used on its own.

### Lookahead bias
One typical issue in backtesting strategies that request alternate timeframe data, use repainting variables such as timenow , or alter calculation behavior for intrabar order fills, is the leakage of future data into the past during evaluation. We refer to this behavior as lookahead bias . Not only is lookahead bias a common cause of unrealistic strategy results, because the future is always unknown, but it is also one of the common causes of strategy repainting .

Traders can often confirm whether a strategy has lookahead bias by forward testing it on realtime data, where no known data exists beyond the latest bar. Because there is no future data to leak into the past on realtime bars, the strategy will behave differently on historical and realtime bars if it is affected by lookahead bias.

To eliminate lookahead bias in a strategy:

- Do not use repainting variables that leak future values into the past in the strategy’s order placement or cancellation logic.
- Do not include barmerge.lookahead_on in request.*() calls without offsetting the data series with the history-referencing operator , especially when requesting data from a higher timeframe. See the lookahead section of the Other timeframes and data page for more information.
- When using the “On order fill” Script execution setting, avoid using the current values of built-in variables that hold price or volume data for each bar. During the script’s historical executions, the current value of a variable such as close always refers to the final value as of the bar’s closing tick , even while the script executes on the bar’s first tick. See the calc_on_order_fills section above to learn more about this behavior.
### Selection bias
Selection bias occurs when a trader analyzes performance results for a set of specific instruments, timeframes, or testing ranges while ignoring others. This bias can distort the trader’s perspective of the strategy’s robustness, thus impacting trading decisions and performance optimizations. Traders can reduce the effects of selection bias by evaluating their strategies on multiple, ideally diverse datasets, and avoiding ignoring poor performance results or “cherry-picking” testing ranges.

### Overfitting
A common problem when optimizing a strategy based on backtest results is overfitting (“curve fitting”), which refers to tailoring the strategy for improved performance on specific datasets. A strategy that suffers from overfitting often fails to perform well on new, unseen data. One widely-used approach to help reduce overfitting and promote better generalization is to split an instrument’s data into two or more parts to test the strategy outside the sample used for optimization. This process is often known as “in-sample” (IS) and “out-of-sample” (OOS) backtesting.

When using this approach, traders optimize strategy parameters on the IS data. Then, they test the optimized configuration on the OOS data without additional fine-tuning. Although this technique and other, more robust approaches might provide a glimpse into how a strategy might fare after optimization, traders should still exercise caution. No trading strategy can guarantee future performance, regardless of the data used for optimization and testing, because the future is inherently unknown .

### Trade limit
By default, strategies preserve information for up to the latest 9000 trades . If a strategy simulates more than 9000 trades, it trims the information for the oldest closed trades and maintains data for only the most recent trades. Information for trimmed trades or their orders are not visible in the strategy report interface or any downloaded XLSX or CSV files. Likewise, the strategy.closedtrades.*() functions return na for all trimmed trades. However, if the strategy uses Deep Backtesting mode, it maintains information for every closed trade and does not trim any orders from the report.

Programmers can retrieve the index of the oldest untrimmed trade, which corresponds to the oldest trade listed in the strategy report’s “Trades” tab , by using the strategy.closedtrades.first_index variable. Scripts can use the index in strategy.closedtrades.*() calls to retrieve information for the oldest available closed trade. If the strategy simulates fewer than 9000 trades or runs in Deep Backtesting mode, the variable’s value is 0, representing the actual first trade in the simulation.

Note Deep Backtesting mode only affects the testing range of results displayed in the strategy report . When using this mode, the strategy’s trade markers, plots , alerts , and Pine Logs are calculated using only the available chart data, regardless of the specified testing range.

To learn more about retrieving trade data using the strategy.closedtrades.*() built-ins, refer to the Individual trade information section above.

PreviousSessionsNextStrings## On this page
IntroductionA simple strategy exampleApplying a strategy to a chartStrategy report​“Metrics” tabKey statsReturn detailsTrades analysisEquity run-ups and drawdownsCapital efficiency​“Trades” tab​“Properties” tabBroker emulatorAdjusting historical bar detailOrders and tradesOrder typesMarket ordersLimit ordersStop and stop-limit ordersOrder placement and cancellationstrategy.entry()Reversing positionsPyramidingstrategy.order()strategy.exit()Take-profit and stop-lossPartial and multi-level exitsTrailing stopsExits for multiple entriesstrategy.close() and strategy.close_all()strategy.cancel() and strategy.cancel_all()Position sizingClosing a market positionOCA groupsstrategy.oca.cancelstrategy.oca.reducestrategy.oca.noneCurrencyAltering calculation behaviorcalc_on_every_tickcalc_on_order_fillscalc_on_every_history_tickprocess_orders_on_closeSimulating trading costsCommissionSlippage and unfilled limitsRisk managementMargin and leverageUsing strategy information in scriptsIndividual trade informationStrategy alertsNotes on testing strategiesBacktesting and forward testingLookahead biasSelection biasOverfittingTrade limit
