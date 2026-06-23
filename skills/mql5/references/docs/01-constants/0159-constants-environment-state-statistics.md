# Testing Statistics

After the testing is over, different parameters of the trading results statistics are calculated. The values of the parameters can be obtained using the [TesterStatistics()](/en/docs/common/testerstatistics) function, by specifying the parameter ID from the ENUM_STATISTICS enumeration.

Although two types of parameters (int and double) are used for calculating statistics, the function returns all values in the double form. All the statistic values of the double type are expressed in the deposit currency by default, unless otherwise specified.

ENUM_STATISTICS

| ID | Description of a statistic parameter | Type |
| --- | --- | --- |
| STAT_INITIAL_DEPOSIT | The value of the initial deposit | double |
| STAT_WITHDRAWAL | Money withdrawn from an account | double |
| STAT_PROFIT | Net profit after testing, the sum of  STAT_GROSS_PROFIT and STAT_GROSS_LOSS (STAT_GROSS_LOSS is always less than or equal to zero) | double |
| STAT_GROSS_PROFIT | Total profit, the sum of all profitable (positive) trades. The value is greater than or equal to zero | double |
| STAT_GROSS_LOSS | Total loss, the sum of all negative trades. The value is less than or equal to zero | double |
| STAT_MAX_PROFITTRADE | Maximum profit – the largest value of all profitable trades. The value is greater than or equal to zero | double |
| STAT_MAX_LOSSTRADE | Maximum loss – the lowest value of all losing trades. The value is less than or equal to zero | double |
| STAT_CONPROFITMAX | Maximum profit in a series of profitable trades. The value is greater than or equal to zero | double |
| STAT_CONPROFITMAX_TRADES | The number of trades that have formed  STAT_CONPROFITMAX  (maximum profit in a series of profitable trades) | int |
| STAT_MAX_CONWINS | The total profit of the longest series of profitable trades | double |
| STAT_MAX_CONPROFIT_TRADES | The number of trades in the longest series of profitable trades  STAT_MAX_CONWINS | int |
| STAT_CONLOSSMAX | Maximum loss in a series of losing trades. The value is less than or equal to zero | double |
| STAT_CONLOSSMAX_TRADES | The number of trades that have formed  STAT_CONLOSSMAX  (maximum loss in a series of losing trades) | int |
| STAT_MAX_CONLOSSES | The total loss of the longest series of losing trades | double |
| STAT_MAX_CONLOSS_TRADES | The number of trades in the longest series of losing trades  STAT_MAX_CONLOSSES | int |
| STAT_BALANCEMIN | Minimum balance value | double |
| STAT_BALANCE_DD | Maximum balance drawdown in monetary terms. In the process of trading, a balance may have numerous drawdowns; here the largest value is taken | double |
| STAT_BALANCEDD_PERCENT | Balance drawdown as a percentage that was recorded at the moment of the maximum balance drawdown in monetary terms ( STAT_BALANCE_DD ). | double |
| STAT_BALANCE_DDREL_PERCENT | Maximum balance drawdown as a percentage. In the process of trading, a balance may have numerous drawdowns, for each of which the relative drawdown value in percents is calculated. The greatest value is returned | double |
| STAT_BALANCE_DD_RELATIVE | Balance drawdown in monetary terms that was recorded at the moment of the maximum balance drawdown as a percentage ( STAT_BALANCE_DDREL_PERCENT ). | double |
| STAT_EQUITYMIN | Minimum equity value | double |
| STAT_EQUITY_DD | Maximum equity drawdown in monetary terms. In the process of trading, numerous drawdowns may appear on the equity; here the largest value is taken | double |
| STAT_EQUITYDD_PERCENT | Drawdown in percent that was recorded at the moment of the maximum equity drawdown in monetary terms ( STAT_EQUITY_DD ). | double |
| STAT_EQUITY_DDREL_PERCENT | Maximum equity drawdown as a percentage. In the process of trading, an equity may have numerous drawdowns, for each of which the relative drawdown value in percents is calculated. The greatest value is returned | double |
| STAT_EQUITY_DD_RELATIVE | Equity drawdown in monetary terms that was recorded at the moment of the maximum equity drawdown in percent ( STAT_EQUITY_DDREL_PERCENT ). | double |
| STAT_EXPECTED_PAYOFF | Expected payoff | double |
| STAT_PROFIT_FACTOR | Profit factor, equal to  the ratio of  STAT_GROSS_PROFIT/STAT_GROSS_LOSS. If STAT_GROSS_LOSS=0, the profit factor is equal to  DBL_MAX | double |
| STAT_RECOVERY_FACTOR | Recovery factor, equal to the ratio of  STAT_PROFIT/STAT_BALANCE_DD | double |
| STAT_SHARPE_RATIO | Sharpe ratio | double |
| STAT_MIN_MARGINLEVEL | Minimum value of the margin level | double |
| STAT_CUSTOM_ONTESTER | The value of the calculated custom optimization criterion returned by the  OnTester()  function | double |
| STAT_DEALS | The number of deals | int |
| STAT_TRADES | The number of trades | int |
| STAT_PROFIT_TRADES | Profitable trades | int |
| STAT_LOSS_TRADES | Losing trades | int |
| STAT_SHORT_TRADES | Short trades | int |
| STAT_LONG_TRADES | Long trades | int |
| STAT_PROFIT_SHORTTRADES | Profitable short trades | int |
| STAT_PROFIT_LONGTRADES | Profitable long trades | int |
| STAT_PROFITTRADES_AVGCON | Average length of a profitable series of trades | int |
| STAT_LOSSTRADES_AVGCON | Average length of a losing series of trades | int |
| STAT_COMPLEX_CRITERION | Complex  optimization criterion |  |
