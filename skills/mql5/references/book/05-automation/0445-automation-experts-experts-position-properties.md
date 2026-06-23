# Position properties

All position properties are divided into three groups according to the type of values: integer and compatible with them, real numbers, and strings. They are used to read PositionGet functions similar to [OrderGet](/en/book/automation/experts/experts_orderget_funcs)[ functions](/en/book/automation/experts/experts_orderget_funcs). We will describe the functions themselves in the next section, and here we will give the identifiers of all properties that are available for specifying in the first parameter of these functions.

Integer properties are provided in the ENUM_POSITION_PROPERTY_INTEGER enumeration.

| Identifier | Description | Type |
| --- | --- | --- |
| POSITION_TICKET | Position ticket | ulong |
| POSITION_TIME | Position opening time | datetime |
| POSITION_TIME_MSC | Position opening time in milliseconds | ulong |
| POSITION_TIME_UPDATE | Position change (volume) time | datetime |
| POSITION_TIME_UPDATE_MSC | Position change (volume) time in milliseconds | ulong |
| POSITION_TYPE | Position type | ENUM_POSITION_TYPE |
| POSITION_MAGIC | Position Magic number (based on  ORDER_MAGIC ) | ulong |
| POSITION_IDENTIFIER | Position identifier; a unique number that is assigned to each newly opened position and does not change during its entire life. | ulong |
| POSITION_REASON | Reason for opening a position | ENUM_POSITION_REASON |

As a rule, POSITION_IDENTIFIER corresponds to the ticket of the order that opened the position. The position identifier is indicated in each order (ORDER_POSITION_ID) and deal (DEAL_POSITION_ID) that opened, changed, or closed it. Therefore, it is convenient to use it to search for orders and deals related to a position.

If the order is filled partially, then both the position and the active pending order for the remaining volume with matching tickets can exist simultaneously. Moreover, such a position can be closed in time, and at the next filling of the rest of the pending order, a position with the same ticket will appear again.

In netting mode, reversing a position with one trade is considered a position change, not a new one, so the POSITION_IDENTIFIER is preserved. A new position on a symbol is possible only after closing the previous one in zero volume.

The POSITION_TIME_UPDATE property only responds to volume changes (for example, as a result of partial closing or position increase), but not other parameters like Stop Loss/Take Profit levels or swap charges.

There are only two types of positions (ENUM_POSITION_TYPE).

| Identifier | Description |
| --- | --- |
| POSITION_TYPE_BUY | Buy |
| POSITION_TYPE_SELL | Sell |

Options for the origin of a position, that is, how the position was opened, are provided in the ENUM_POSITION_REASON enumeration.

| Identifier | Description |
| --- | --- |
| POSITION_REASON_CLIENT | Triggering of an order placed from the desktop terminal |
| POSITION_REASON_MOBILE | Triggering of an order placed from a mobile application |
| POSITION_REASON_WEB | Triggering of an order placed from the web platform (browser) |
| POSITION_REASON_EXPERT | Triggering of an order placed by an Expert Advisor or a script |

Real properties are collected in ENUM_POSITION_PROPERTY_DOUBLE.

| Identifier | Description |
| --- | --- |
| POSITION_VOLUME | Position volume |
| POSITION_PRICE_OPEN | Position price |
| POSITION_SL | Stop Loss Price |
| POSITION_TP | Take profit price |
| POSITION_PRICE_CURRENT | Current symbol price |
| POSITION_SWAP | Accumulated swap |
| POSITION_PROFIT | Current profit |

The current price type corresponds to the position closing operation. For example, a long position must be closed by selling, and therefore the Bid price for it is tracked in POSITION_PRICE_CURRENT.

Finally, the following string properties (ENUM_POSITION_PROPERTY_STRING) are supported for positions.

| Identifier | Description |
| --- | --- |
| POSITION_SYMBOL | The symbol on which the position is opened |
| POSITION_COMMENT | Position comment |
| POSITION_EXTERNAL_ID | Position ID in the external system (on the exchange) |

After reviewing the list of position properties, we are ready to look at the functions for reading these properties.
