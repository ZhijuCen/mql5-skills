# Trade Functions

This is the group of functions intended for managing trading activities.

Before you proceed to study the trade functions of the platform, you must have a clear understanding of the basic terms: order, deal and position:

- An order is an instruction given to a broker to buy or sell a financial instrument. There are two main types of orders: Market and Pending. In addition, there are special Take Profit and Stop Loss levels.
- A deal is the commercial exchange (buying or selling) of a financial security. Buying is executed at the demand price (Ask), and Sell is performed at the supply price (Bid). A deal can be opened as a result of market order execution or pending order triggering. Note that in some cases, execution of an order can result in several deals.
- A position is a trade obligation, i.e. the number of bought or sold contracts of a financial instrument. A long position is financial security bought expecting the security price go higher. A short position is an obligation to supply a security expecting the price will fall in future.

General information about trading operations is available in the [client terminal help](https://www.metatrader5.com/en/terminal/help/trading/general_concept).

Trading functions can be used in Expert Advisors and scripts. Trading functions can be called only if in the properties of the Expert Advisor or script the "Allow live trading" checkbox is enabled.

Trading can be allowed or prohibited depending on various factors described in the [Trade Permission](/en/docs/runtime/tradepermission) section.

| Function | Action |
| --- | --- |
| OrderCalcMargin | Calculates the margin required for the specified order type, in the deposit currency |
| OrderCalcProfit | Calculates the profit based on the parameters passed, in the deposit currency |
| OrderCheck | Checks if there are enough funds to execute the required  trade operation . |
| OrderSend | Sends  trade requests  to a server |
| OrderSendAsync | Asynchronously sends  trade requests  without waiting for the trade response of the trade server |
| PositionsTotal | Returns the number of open positions |
| PositionGetSymbol | Returns the symbol corresponding to the open position |
| PositionSelect | Chooses an open position for further working with it |
| PositionSelectByTicket | Selects a position to work with by the ticket number specified in it |
| PositionGetDouble | Returns the requested property of an open position (double) |
| PositionGetInteger | Returns the requested property of an open position (datetime or int) |
| PositionGetString | Returns the requested property of an open position (string) |
| PositionGetTicket | Returns the ticket of the position with the specified index in the list of open positions |
| OrdersTotal | Returns the number of orders |
| OrderGetTicket | Return the ticket of a corresponding order |
| OrderSelect | Selects a order for further working with it |
| OrderGetDouble | Returns the requested property of the order (double) |
| OrderGetInteger | Returns the requested property of the order (datetime or int) |
| OrderGetString | Returns the requested property of the order (string) |
| HistorySelect | Retrieves the history of transactions and orders for the specified period of the server time |
| HistorySelectByPosition | Requests the history of deals with a specified  position identifier . |
| HistoryOrderSelect | Selects an order in the history for further working with it |
| HistoryOrdersTotal | Returns the number of orders in the history |
| HistoryOrderGetTicket | Return order ticket of a corresponding order in the history |
| HistoryOrderGetDouble | Returns the requested property of an order in the history (double) |
| HistoryOrderGetInteger | Returns the requested property of an order in the history (datetime or int) |
| HistoryOrderGetString | Returns the requested property of an order in the history (string) |
| HistoryDealSelect | Selects a deal in the history for further calling it through appropriate functions |
| HistoryDealsTotal | Returns the number of deals in the history |
| HistoryDealGetTicket | Returns a ticket of a corresponding deal in the history |
| HistoryDealGetDouble | Returns the requested property of a deal in the history (double) |
| HistoryDealGetInteger | Returns the requested property of a deal in the history (datetime or int) |
| HistoryDealGetString | Returns the requested property of a deal in the history (string) |
