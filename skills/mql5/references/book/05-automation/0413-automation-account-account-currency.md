# Account currency

Balance, profit, margin, commissions, and other [financial indicators](/en/book/automation/account/account_state) are always converted to the account currency in the end, even if the specifications for some trades require settlement in other currencies, for example, in the margin currency of a Forex pair.

The MQL5 API provides two properties that describe the account currency: its name and the accuracy of the representation, that is, the size of the minimum unit of measurement (such as cents).

| Identifier | Description |
| --- | --- |
| ACCOUNT_CURRENCY | Deposit currency (string) |
| ACCOUNT_CURRENCY_DIGITS | Number of decimal places for account currency required for the accurate display of trading results (integer) |

For example, for the demo account used to test the AccountInfo script in the section on [Account identification](/en/book/automation/account/account_number_identity), the ACCOUNT_CURRENCY property was "USD", and the accuracy of ACCOUNT_CURRENCY_DIGITS was 2 decimal places. We have used the ACCOUNT_CURRENCY_DIGITS property in the AccountMonitor class in the stringify method for values of type double (in the characteristics of the account, they are all associated with money).
