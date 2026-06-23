# Deal properties

A deal is a reflection of the fact that a trading operation was performed on the basis of an order. One order can generate several deals due to the execution in parts or the opposite closing of positions.

Deals are characterized by properties of three basic types: integer (and compatible with them), real, and string. Each property is described by its own constant in one of the enumerations: ENUM_DEAL_PROPERTY_INTEGER, ENUM_DEAL_PROPERTY_DOUBLE, ENUM_DEAL_PROPERTY_STRING.

To read deal properties, use the [HistoryDealGet](/en/book/automation/experts/experts_historydealget_funcs)[ functions](/en/book/automation/experts/experts_historydealget_funcs). All of them assume that the necessary section of history was previously requested using special functions for the [selection of orders and deals from history](/en/book/automation/experts/experts_history_select).

Integer properties are described in the ENUM_DEAL_PROPERTY_INTEGER enumeration.

| Identifier | Description | Type |
| --- | --- | --- |
| DEAL_TICKET | Deal ticket; a unique number that is assigned to each transaction | ulong |
| DEAL_ORDER | The ticket of the order on the basis of which the deal was executed | ulong |
| DEAL_TIME | Deal time | datetime |
| DEAL_TIME_MSC | Deal time in milliseconds | ulong |
| DEAL_TYPE | Deal type | ENUM_DEAL_TYPE (see below) |
| DEAL_ENTRY | Deal direction; market entry, market exit, or reversal | ENUM_DEAL_ENTRY (see below) |
| DEAL_MAGIC | Magic number for the deal (based on ORDER_MAGIC) | ulong |
| DEAL_REASON | Deal reason or source | ENUM_DEAL_REASON (see below) |
| DEAL_POSITION_ID | Identifier of the position that was opened, modified or closed by the deal | ulong |

Possible deal types are represented by the ENUM_DEAL_TYPE enumeration.

| Identifier | Description |
| --- | --- |
| DEAL_TYPE_BUY | Buy |
| DEAL_TYPE_SELL | Sell |
| DEAL_TYPE_BALANCE | Balance accrued |
| DEAL_TYPE_CREDIT | Credit accrual |
| DEAL_TYPE_CHARGE | Additional charges |
| DEAL_TYPE_CORRECTION | Correction |
| DEAL_TYPE_BONUS | Bonuses |
| DEAL_TYPE_COMMISSION | Additional commission |
| DEAL_TYPE_COMMISSION_DAILY | Commission charged at the end of the trading day |
| DEAL_TYPE_COMMISSION_MONTHLY | Commission charged at the end of the month |
| DEAL_TYPE_COMMISSION_AGENT_DAILY | Agent commission charged at the end of the trading day |
| DEAL_TYPE_COMMISSION_AGENT_MONTHLY | Agent commission charged at the end of the month |
| DEAL_TYPE_INTEREST | Interest accrual on free funds |
| DEAL_TYPE_BUY_CANCELED | Canceled buy deal |
| DEAL_TYPE_SELL_CANCELED | Canceled sell deal |
| DEAL_DIVIDEND | Dividend accrual |
| DEAL_DIVIDEND_FRANKED | Accrual of a franked dividend (tax exempt) |
| DEAL_TAX | Tax accrual |

The DEAL_TYPE_BUY_CANCELED and DEAL_TYPE_SELL_CANCELED options reflect the situation when an earlier deal is canceled. In this case, the type of the previously executed deal (DEAL_TYPE_BUY or DEAL_TYPE_SELL) is changed to DEAL_TYPE_BUY_CANCELED or DEAL_TYPE_SELL_CANCELED, and its profit/loss is reset to zero. Previously received profit/loss is credited/debited from the account as a separate balance operation.

Deals differ in the way the position is changed. This can be a simple opening of a position (entry to the market), increasing the volume of a previously opened position, closing a position with a deal in the opposite direction or position reversal when the opposite deal covers the volume of a previously opened position. The latter operation is only supported on netting accounts.

All these situations are described by the elements of the ENUM_DEAL_ENTRY enumeration.

| Identifier | Description |
| --- | --- |
| DEAL_ENTRY_IN | Market entry |
| DEAL_ENTRY_OUT | Market exit |
| DEAL_ENTRY_INOUT | Reversal |
| DEAL_ENTRY_OUT_BY | Closing by an opposite position |

The reasons for the deal are summarized in the ENUM_DEAL_REASON enumeration.

| Identifier | Description |
| --- | --- |
| DEAL_REASON_CLIENT | Triggering of an order placed from the desktop terminal |
| DEAL_REASON_MOBILE | Triggering of an order placed from a mobile application |
| DEAL_REASON_WEB | Triggering of an order placed from the web platform |
| DEAL_REASON_EXPERT | Triggering of an order placed by an Expert Advisor or a script |
| DEAL_REASON_SL | Stop Loss order triggered |
| DEAL_REASON_TP | Take Profit order triggering |
| DEAL_REASON_SO | Stop Out event |
| DEAL_REASON_ROLLOVER | Position transfer to a new day |
| DEAL_REASON_VMARGIN | Add/deduct variation margin |
| DEAL_REASON_SPLIT | Split (lower price) the instrument on which there was a position |

Real type properties are represented by the ENUM_DEAL_PROPERTY_DOUBLE enumeration.

| Identifier | Description |
| --- | --- |
| DEAL_VOLUME | Deal volume |
| DEAL_PRICE | Deal price |
| DEAL_COMMISSION | Deal commission |
| DEAL_SWAP | Accumulated swap at close |
| DEAL_PROFIT | Financial result of the deal |
| DEAL_FEE | Fee for the deal which is charged immediately after the deal |
| DEAL_SL | Stop Loss Level |
| DEAL_TP | Take Profit level |

The two last properties are filled as follows: for an entry or reversal deal, the Stop Loss/Take Profit value is taken from the order by which the position was opened or expanded. For the exit deal, the Stop Loss/Take Profit value is taken from the position at the time of its closing.

String deal properties are available via ENUM_DEAL_PROPERTY_STRING enumeration constants.

| Identifier | Description |
| --- | --- |
| DEAL_SYMBOL | The name of the symbol for which the deal was made |
| DEAL_COMMENT | Deal comment |
| DEAL_EXTERNAL_ID | Deal identifier in the external trading system (on the exchange) |

We will test how to read the properties in the section on [HistoryDealGet](/en/book/automation/experts/experts_historydealget_funcs)[ functions](/en/book/automation/experts/experts_historydealget_funcs) through the DealMonitor and DealFilter classes.
