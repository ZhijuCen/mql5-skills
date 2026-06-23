# Account margin settings

For trading robots, it is important to control the amount of margin blocked and the amount available to secure new trades. In particular, if there are not enough free funds, the program will not be able to execute a trade. When maintaining open unprofitable positions, first a Margin Call is received, and if it is not fulfilled, the positions are forcedly closed by the broker (Stop Out). All associated account properties are included in the ENUM_ACCOUNT_INFO_DOUBLE enumeration.

| Identifier | Description |
| --- | --- |
| ACCOUNT_MARGIN | Current reserved margin on the account in the deposit currency |
| ACCOUNT_MARGIN_FREE | Current free margin on the account in the deposit currency, available for opening a position |
| ACCOUNT_MARGIN_LEVEL | Margin level on the account in percent (equity/margin*100) |
| ACCOUNT_MARGIN_SO_CALL | The minimum margin level at which account replenishment will be required (Margin Call) |
| ACCOUNT_MARGIN_SO_SO | The minimum margin level at which the most unprofitable position will be forced to close (Stop Out) |
| ACCOUNT_MARGIN_INITIAL | Funds reserved on the account to provide margin for all pending orders |
| ACCOUNT_MARGIN_MAINTENANCE | Funds reserved on the account to provide the minimum required margin for all open positions |

ACCOUNT_MARGIN_SO_CALL and ACCOUNT_MARGIN_SO_SO are expressed as a percentage or deposit currency depending on the set ACCOUNT_MARGIN_SO_MODE (see further). This property, with the possibility to measure margin thresholds for the Margin Call or Stop Out, is included in the ENUM_ACCOUNT_INFO_INTEGER enumeration. In addition, the total leverage (used to calculate the margin for certain types of instruments) is also indicated there.

| Identifier | Description |
| --- | --- |
| ACCOUNT_LEVERAGE | The leverage amount |
| ACCOUNT_MARGIN_SO_MODE | The mode for setting the minimum allowable margin level from the ENUM_ACCOUNT_STOPOUT_MODE enumeration |

And here are the elements of the ENUM_ACCOUNT_STOPOUT_MODE enumeration.

| Identifier | Description |
| --- | --- |
| ACCOUNT_STOPOUT_MODE_PERCENT | The level is set as a percentage |
| ACCOUNT_STOPOUT_MODE_MONEY | The level is set in the account currency |

For example, for the ACCOUNT_STOPOUT_MODE_PERCENT option, the specified percentage (Margin Call or Stop Out) should be checked against the ratio of equity to the value of the ACCOUNT_MARGIN property:

```
AccountInfoDouble(ACCOUNT_EQUITY) / AccountInfoDouble(ACCOUNT_MARGIN) * 100
   > AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)

```

In the next section, you will find more details about the ACCOUNT_EQUITY property and other financial indicators of the account.

However, the current margin level in percent is already provided in the ACCOUNT_MARGIN_LEVEL property. This is easy to check using the AccountInfo.mq5 script which logs all account properties, including those listed above.

We have already run this script in the section [Account identification](/en/book/automation/account/account_number_identity). At that moment, one position was opened (1 lot USDRUB, equal to 100,000 USD), and the financials were as follows:

```
  0 ACCOUNT_BALANCE=10000.00
  1 ACCOUNT_CREDIT=0.00
  2 ACCOUNT_PROFIT=-78.76
  3 ACCOUNT_EQUITY=9921.24
  4 ACCOUNT_MARGIN=1000.00
  5 ACCOUNT_MARGIN_FREE=8921.24
  6 ACCOUNT_MARGIN_LEVEL=992.12
  7 ACCOUNT_MARGIN_SO_CALL=50.00
  8 ACCOUNT_MARGIN_SO_SO=30.00

```

With a margin of 1000.00 USD, it is easy to check that the leverage of the account, ACCOUNT_LEVERAGE, is indeed 100 (according to the formula for calculating [margin for Forex](/en/book/automation/symbols/symbols_margin) and [margin ratio](/en/book/automation/symbols/symbols_margin_rates) which is equal to 1.0). The margin amount does not need to be converted at the current rate into the account currency, since it is the same as the base currency of the instrument.

To get 992.12 in ACCOUNT_MARGIN_LEVEL, just divide 9921.24 by 1000.00 and multiply by 100%.

Then another 1 lot position was opened, and the quotes went in an unfavorable direction, as a result of which the situation changed:

```
  0 ACCOUNT_BALANCE=10000.00
  1 ACCOUNT_CREDIT=0.00
  2 ACCOUNT_PROFIT=-1486.07
  3 ACCOUNT_EQUITY=8513.93
  4 ACCOUNT_MARGIN=2000.00
  5 ACCOUNT_MARGIN_FREE=6513.93
  6 ACCOUNT_MARGIN_LEVEL=425.70

```

We can see a loss in the ACCOUNT_PROFIT column and a corresponding decrease in equity ACCOUNT_EQUITY. The margin ACCOUNT_MARGIN increased proportionally from 1000 to 2000, free margin and margin level decreased (but still far from the 50% and 30% limits). Again, the level 425.70 is obtained as the result of calculating the expression 8513.93 / 2000.00 * 100.

It is more practical to use this formula to calculate the future margin level before opening a new position. In this case, it is necessary to increase the amount of the existing margin by the additional margin of X. In addition, if a market entry deal involves an instant commission deduction C, then, strictly speaking, it should also be taken into account (although usually it has a size significantly less than the margin and it can be neglected, plus the API does not provide a way to find out the commission in advance, before performing a trade: it can only be estimated by the commissions of already completed trades in trading history).

```
(AccountInfoDouble(ACCOUNT_EQUITY) - C) / (AccountInfoDouble(ACCOUNT_MARGIN) + X) * 100
   > AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)

```

Later we will learn how to obtain the X value using the [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin) function, but in addition to it, adjustments may be required according to the rules announced in the [Margin Requirements](/en/book/automation/symbols/symbols_margin) section, in particular, taking into account the possible [position hedging](https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex#hedging), discounts, and [margin adjustments](https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_exchange).

For the option of setting the margin limit in money (ACCOUNT_STOPOUT_MODE_MONEY), the check for sufficient funds must be different.

```
AccountInfoDouble(ACCOUNT_EQUITY) > AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)

```

Here the commission is omitted. Please note that the margin X for a new position being prepared for opening 'now' does not affect the assessment of the 'future' margin in any way.

However, in any case, it is desirable not to load the deposit so much that the inequalities are barely fulfilled. The values of ACCOUNT_MARGIN_SO_CALL and ACCOUNT_MARGIN_SO_SO are quite close, and although the margin at the ACCOUNT_MARGIN_SO_CALL level is just a warning to the trader, it is easy to get a forced closing. That is why the formulas use the ACCOUNT_MARGIN_SO_CALL property.
