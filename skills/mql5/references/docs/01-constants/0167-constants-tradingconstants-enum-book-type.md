# Trade Orders in Depth Of Market

For equity securities, the Depth of Market window is available, where you can see the current Buy and Sell orders. Desired direction of a trade operation, required amount and requested price are specified for each order.

To obtain information about the current state of the DOM by MQL5 means, the [MarketBookGet()](/en/docs/marketinformation/marketbookget) function is used, which places the DOM "screen shot" into the [MqlBookInfo](/en/docs/constants/structures/mqlbookinfo) array of structures. Each element of the array in the type field contains information about the direction of the order - the value of the ENUM_BOOK_TYPE enumeration.

ENUM_BOOK_TYPE

| Identifier | Description |
| --- | --- |
| BOOK_TYPE_SELL | Sell order (Offer) |
| BOOK_TYPE_BUY | Buy order (Bid) |
| BOOK_TYPE_SELL_MARKET | Sell order by Market |
| BOOK_TYPE_BUY_MARKET | Buy order by Market |

See also

[Structures and classes](/en/docs/basis/types/classes), [Structure of the DOM](/en/docs/constants/structures/mqlbookinfo), [Trade operation types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Market Info](/en/docs/marketinformation)
