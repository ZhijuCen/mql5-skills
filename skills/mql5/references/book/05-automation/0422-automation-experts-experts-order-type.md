# Order types

As you know, MetaTrader 5 supports several [order types](https://www.metatrader5.com/en/terminal/help/trading/general_concept#order_type): two market orders for buying and selling at the current price, and six pending ones with predefined activation levels above and below the market. All these types are available in the MQL5 API and are described by the elements of the ENUM_ORDER_TYPE enumeration. Later we will consider how to create an order of a particular type in a program. For now, let's get acquainted with the enumeration.

| Identifier | Description |
| --- | --- |
| ORDER_TYPE_BUY | Market buy order |
| ORDER_TYPE_SELL | Market sell order |
| ORDER_TYPE_BUY_LIMIT | Buy Limit  pending order |
| ORDER_TYPE_SELL_LIMIT | Sell Limit  pending order |
| ORDER_TYPE_BUY_STOP | Buy Stop  pending order |
| ORDER_TYPE_SELL_STOP | Sell Stop  pending order |
| ORDER_TYPE_BUY_STOP_LIMIT | Buy Limit   pending order to be placed when the price reaches the specified upper level |
| ORDER_TYPE_SELL_STOP_LIMIT | Sell Limit   pending order to be placed when the price reaches the specified lower level |
| ORDER_TYPE_CLOSE_BY | Order to close one position with an oppositely directed position |

The last element corresponds to the action to close opposite positions: this possibility exists only on [hedging](/en/book/automation/account/account_netting_hedge) accounts and for the financial instruments having properties that allow such operations ([SYMBOL_ORDER_CLOSEBY](/en/book/automation/symbols/symbols_trade_mode)).

The following picture may remind you of the general pending order activation principles. It shows the expected future price movements in gray. But at the current time, it is not known which forecast will turn out to be correct.

![Buy Stop  and  Sell Stop  pending orders follow the level breakdown principle: for  Buy Stop , this level should be located above the current price, and it should be below the current price for  Sell Stop . In other words, at a given level, we want a buy or sell operation to be executed expecting further trading in the trend direction.](pics/order_types.png)

Buy Stop and Sell Stop pending orders follow the level breakdown principle: for Buy Stop, this level should be located above the current price, and it should be below the current price for Sell Stop. In other words, at a given level, we want a buy or sell operation to be executed expecting further trading in the trend direction.

Buy Limit and Sell Limit implement the strategy of rebounding from the level, and in this case, the buy activation price is below the current price, and the sell price is higher. This implies a change in trend or fluctuation in the corridor. In the diagram above, the same upper (Higher Price) and lower (Lower Price) activation levels of pending orders are used to illustrate both a breakout and a rebound.

Pending orders can be placed at the current price, and they will most likely be executed immediately. In addition, this technique applied to limit orders guarantees a trade price that is no worse than the requested one, unlike a market order.

Order of Buy Stop Limit and Sell Stop Limit types are not sent to the market as a result of their activation, but they place set pending orders, Buy Limit or Sell Limit, at some additional levels specified in the original order.

For exchange instruments, limit orders (Buy Limit, Sell Limit) are usually directly displayed in the order book and are visible to other market participants.

In contrast, Stop and Stop Limit orders (Buy Stop, Sell Stop, Buy Stop Limit, and Sell Stop Limit) are not output directly to the external trading system. Until the stop price is reached, these types of orders are processed within the MetaTrader 5 platform. When the stop price specified in the Buy Stop or Sell Stop order is reached, the corresponding market operation is executed. Upon reaching the stop price specified in the Buy Stop Limit or Sell Stop Limit order, a corresponding limit order is placed.

In exchange execution mode, the price specified when placing limit orders is not checked. It can be specified above the current Ask price (for buy orders) and below the Bid price (for sell orders). When placing an order with such a price, it almost immediately gets triggered and turns into a market one.

Please note that not all types of orders may be allowed for a specific financial instrument: the [SYMBOL_ORDER_MODE](/en/book/automation/symbols/symbols_trade_mode) property describes flags of allowed order types.
