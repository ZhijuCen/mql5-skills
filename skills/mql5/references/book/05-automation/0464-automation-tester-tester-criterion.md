# Optimization criteria

An optimization criterion is a certain metric that defines the quality of the tested set of input parameters. The greater the value of the optimization criterion, the better the test result with a given set of parameters is estimated. The parameter is selected on the "Settings" tab to the right of the "Optimization" field.

The criterion is important not only for the user to be able to compare the results. Without an optimization criterion, it is impossible to use a genetic algorithm, since on the basis of the criterion it "decides" how to select candidates for new generations. The criterion is not used during full optimization with a complete iteration of all possible variants.

The following built-in optimization criteria are available in the tester:

- Maximum balance
- Maximum profitability
- Maximum expected win (average profit/loss per trade)
- Minimum drawdown as a percentage of equity
- Maximum recovery factor
- Maximum Sharpe ratio
- Custom optimization criterion

When choosing the latter option, the value of the OnTester function implemented in the Expert Advisor will be taken into account as an optimization criterion — we will consider it [later](/en/book/automation/tester/tester_ontester). This parameter allows the programmer to use any custom index for optimization.

A special "complex criterion" is also available in MetaTrader 5. This is an integral metric of the quality of the testing pass, which takes into account several parameters at once:

- Number of deals
- Drawdown
- Recovery factor
- Mathematical expectation of winning
- Sharpe ratio

The formula is not disclosed by the developers, but it is known that possible values range from 0 to 100. It is important that the values of the complex parameter affect the color of the cells of the Result column in the optimization table regardless of the criterion, i.e., highlighting following this scheme works even when another criterion is chosen for display in the Result column. Weak combinations with values below 20 are highlighted in red, strong combinations above 80 are highlighted in dark green.

The search for a universal criterion of the trading system quality factor is an urgent and difficult task for most traders, since the choice of settings based on the maximum value of one criterion (for example, profit) is, as a rule, far from the best option in terms of stable and predictable behavior of the Expert Advisor in the foreseeable future.

The presence of a complex indicator allows you to level the weaknesses of each individual metric (and they are necessarily available and widely known) and provides a guideline when developing your own custom variables for calculation in OnTester. We will deal with this soon.
