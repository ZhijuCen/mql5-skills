# Account type: real, demo or contest

MetaTrader 5 supports several types of accounts that can be opened for a client. The ACCOUNT_TRADE_MODE property, which is part of ENUM_ACCOUNT_INFO_INTEGER, allows you to find out the current account type. Possible values for this property are described in the ENUM_ACCOUNT_TRADE_MODE enumeration.

| Identifier | Description |
| --- | --- |
| ACCOUNT_TRADE_MODE_DEMO | Demo trading account |
| ACCOUNT_TRADE_MODE_CONTEST | Contest trading account |
| ACCOUNT_TRADE_MODE_REAL | Real trading account |

This property is convenient for building demo (free) versions of MQL programs. A full-featured, paid version may require linking to an account number, and the account must be real.

As we saw in the example of running the script AccountInfo.mq5 in the previous section, the account on the "MetaQuotes-Demo" server is of the ACCOUNT_TRADE_MODE_DEMO type.
