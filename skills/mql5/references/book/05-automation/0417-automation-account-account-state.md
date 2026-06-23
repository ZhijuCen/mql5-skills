# Current financial performance of the account

The MQL5 API allows control over several account properties via its main financial indicators. They are all included in the ENUM_ACCOUNT_INFO_DOUBLE enumeration.

| Identifier | Description |
| --- | --- |
| ACCOUNT_BALANCE | Account balance in the deposit currency |
| ACCOUNT_PROFIT | The amount of current profit on the account in the deposit currency |
| ACCOUNT_EQUITY | Account equity in the deposit currency |
| ACCOUNT_CREDIT | The amount of the credit provided by the broker in the deposit currency |
| ACCOUNT_ASSETS | Current amount of assets on the account |
| ACCOUNT_LIABILITIES | Current amount of liabilities on the account |
| ACCOUNT_COMMISSION_BLOCKED | The current amount of blocked commissions on the account |

In the previous sections, we saw examples of the values of these properties when running the AccountInfo.mq5 script under different conditions. Try to compare these properties for your different accounts.

In the trading process, we will be primarily interested in the first three properties: balance, profit (or loss if the value is negative), and equity, which together cover the account balance, credit, profit, and overhead costs (swap and commission).

Commissions can be considered in different ways, depending on the broker's settings. If commissions are immediately deducted from the account balance at the time of [trades](/en/book/automation/experts/experts_deal_properties) and are reflected in the deal properties, the account property ACCOUNT_COMMISSION_BLOCKED will be equal to 0. However, if the commission calculation is postponed until the end of the period (for example, a day or a month), the amount blocked for the commission will appear in this property. Then, when the final commission amount is determined and deducted from the balance at the end of the period, the property will be reset.

The properties ACCOUNT_ASSETS and ACCOUNT_LIABILITIES are filled, as a rule, only for exchange trading. They reflect the current value of long and short positions in securities.
