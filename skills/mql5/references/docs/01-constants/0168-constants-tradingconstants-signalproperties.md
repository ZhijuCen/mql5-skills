# Signal Properties

The following enumerations are used when working with trading signals and signal copy settings.

Enumeration of [double](/en/docs/basis/types/double) type properties of the trading signal:

ENUM_SIGNAL_BASE_DOUBLE

| ID | Description |
| --- | --- |
| SIGNAL_BASE_BALANCE | Account balance |
| SIGNAL_BASE_EQUITY | Account equity |
| SIGNAL_BASE_GAIN | Account gain |
| SIGNAL_BASE_MAX_DRAWDOWN | Account maximum drawdown |
| SIGNAL_BASE_PRICE | Signal subscription price |
| SIGNAL_BASE_ROI | Return on Investment (%) |

Enumeration of [integer](/en/docs/basis/types/integer) type properties of the trading signal:

ENUM_SIGNAL_BASE_INTEGER

| ID | Description |
| --- | --- |
| SIGNAL_BASE_DATE_PUBLISHED | Publication date (date when it become available for subscription) |
| SIGNAL_BASE_DATE_STARTED | Monitoring starting date |
| SIGNAL_BASE_DATE_UPDATED | The date of the last update of the signal's trading statistics |
| SIGNAL_BASE_ID | Signal ID |
| SIGNAL_BASE_LEVERAGE | Account leverage |
| SIGNAL_BASE_PIPS | Profit in pips |
| SIGNAL_BASE_RATING | Position in rating |
| SIGNAL_BASE_SUBSCRIBERS | Number of subscribers |
| SIGNAL_BASE_TRADES | Number of trades |
| SIGNAL_BASE_TRADE_MODE | Account type (0-real, 1-demo, 2-contest) |

Enumeration of [string](/en/docs/basis/types/stringconst) type properties of the trading signal:

ENUM_SIGNAL_BASE_STRING

| ID | Description |
| --- | --- |
| SIGNAL_BASE_AUTHOR_LOGIN | Author login |
| SIGNAL_BASE_BROKER | Broker name (company) |
| SIGNAL_BASE_BROKER_SERVER | Broker server |
| SIGNAL_BASE_NAME | Signal name |
| SIGNAL_BASE_CURRENCY | Signal base currency |

Enumeration of [double](/en/docs/basis/types/double) type properties of the signal copy settings:

ENUM_SIGNAL_INFO_DOUBLE

| ID | Description |
| --- | --- |
| SIGNAL_INFO_EQUITY_LIMIT | Equity limit |
| SIGNAL_INFO_SLIPPAGE | Slippage (used when placing market orders in synchronization of positions and copying of trades) |
| SIGNAL_INFO_VOLUME_PERCENT | Maximum percent of deposit used (%), r/o |

Enumeration of [integer](/en/docs/basis/types/integer) type properties of the signal copy settings:

ENUM_SIGNAL_INFO_INTEGER

| ID | Description |
| --- | --- |
| SIGNAL_INFO_CONFIRMATIONS_DISABLED | The flag enables synchronization without confirmation dialog |
| SIGNAL_INFO_COPY_SLTP | Copy Stop Loss and Take Profit flag |
| SIGNAL_INFO_DEPOSIT_PERCENT | Deposit percent (%) |
| SIGNAL_INFO_ID | Signal id, r/o |
| SIGNAL_INFO_SUBSCRIPTION_ENABLED | "Copy trades by subscription" permission flag |
| SIGNAL_INFO_TERMS_AGREE | "Agree to terms of use of Signals service" flag, r/o |

Enumeration of [string](/en/docs/basis/types/stringconst) type properties of the signal copy settings:

ENUM_SIGNAL_INFO_STRING

| ID | Description |
| --- | --- |
| SIGNAL_INFO_NAME | Signal name, r/o |

See also

[Trade signals](/en/docs/signals)
