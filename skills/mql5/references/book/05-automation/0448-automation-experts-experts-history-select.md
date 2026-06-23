# Selecting orders and deals from history

MetaTrader 5 allows you to create a snapshot of history for a specific time period for an Expert Advisor or a script. The snapshot is a list of orders and deals which can be further accessed through the appropriate functions. In addition, history can be requested in relation to specific orders, deals or positions.

Selecting the required period explicitly (by dates) is performed by the HistorySelect function. After that, the size of the list of deals and the list of orders can be found using the HistoryDealsTotal and HistoryOrdersTotal functions, respectively. The elements of the orders list can be checked using the HistoryOrderGetTicket function; for elements of the deals list use HistoryDealGetTicket.

It is necessary to distinguish between active (working) orders and orders in history, i.e., those executed, canceled or rejected. To analyze active orders, use the functions discussed in the sections related to [getting a list of active orders](/en/book/automation/experts/experts_order_list) and [reading their properties](/en/book/automation/experts/experts_orderget_funcs).

bool HistorySelect(datetime from, datetime to)

The function requests the history of deals and orders for the specified period of server time (from and to inclusive, to >= from) and returns true in case of success.

Even if there are no orders and transactions in the requested period, the function will return true in the absence of errors. An error can be, for example, a lack of memory for building a list of orders or deals.

Please note that orders have two times: set (ORDER_TIME_SETUP) and execution (ORDER_TIME_DONE). The function HistorySelect selects orders by execution time.

To extract the entire account history, you can use the syntax HistorySelect(0, LONG_MAX).

Another way to access a part of the history is by position ID.

bool HistorySelectByPosition(ulong positionID)

The function requests the history of deals and orders with the specified position ID in the ORDER_POSITION_ID, DEAL_POSITION_ID properties.

Attention! The function does not select orders by the ID of the opposite position for Close By operations. In other words, the ORDER_POSITION_BY_ID property is ignored, despite the fact that the order data was involved in the formation of the position.   

   

For example, an Expert Advisor could complete a buy (order #1) and sell (order #2) on a hedging-enabled account. This will then lead to the formation of positions #1 and #2. Opposite closing of positions requires the ORDER_TYPE_CLOSE_BY (#3) order. As a result, the HistorySelectByPosition(#1) call will select orders #1 and #3, which is expected. However, the call of HistorySelectByPosition(#2) will select only order #2 (despite the fact that order #3 has #2 in the ORDER_POSITION_BY_ID property, and strictly speaking, order #3 participated in closing position #2).

Upon successful execution of either of the two functions, HistorySelect or HistorySelectByPosition, the terminal generates an internal list of orders and deals for the MQL program. You can also change the historical context with the functions HistoryOrderSelect and HistoryDealSelect, for which you need to know the ticket of the corresponding object in advance (for example, save it from the request result).

It is important to note that HistoryOrderSelect affects only the list of orders, and HistoryDealSelect is only used for the list of deals.

All context selection functions return a bool value for success (true) or error (false). The error code can be read in the built-in _LastError variable.

bool HistoryOrderSelect(ulong ticket)

The HistoryOrderSelect function selects an order in the history by its ticket. The order is then used for further operations with the deal (reading properties).

During the application of the HistoryOrderSelect function, if the search for an order by ticket was successful, the new list of orders selected in the history will consist of the only order just found. In other words, the previous list of selected orders (if any) is reset. However, the function does not reset the previously selected transaction history, i.e., it does not select the transaction(s) associated with the order.

bool HistoryDealSelect(ulong ticket)

The function HistoryDealSelect selects a deal in the history for further access to it through the appropriate functions. The function does not reset the order history, i.e., it does not select the order associated with the selected deal.

After a certain context is selected in the history by calling one of the above functions, the MQL program can call the functions to iterate over the orders and deals that fall into this context and read their properties.

int HistoryOrdersTotal()

The HistoryOrdersTotal function returns the number of orders in history (in the selection).

ulong HistoryOrderGetTicket(int index)

The HistoryOrderGetTicket function allows you to get an order ticket by its serial number in the selected history context. The index must be between 0 and N-1, where N is obtained from the HistoryOrdersTotal function.

Knowing the order ticket, it is easy to get all the necessary properties of it using [HistoryOrderGet](/en/book/automation/experts/experts_historyorderget_funcs)[ functions](/en/book/automation/experts/experts_historyorderget_funcs). The properties of historical orders are exactly the same as those of [existing](/en/book/automation/experts/experts_order_properties) orders.

There is a similar pair of functions for working with deals.

int HistoryDealsTotal()

The HistoryDealsTotal function returns the number of deals in history (in the selection).

ulong HistoryDealGetTicket(int index)

The HistoryDealGetTicket function allows you to get a deal ticket by its serial number in the selected history context. This is necessary for further processing of the deal using [HistoryDealGet](/en/book/automation/experts/experts_historydealget_funcs)[ functions](/en/book/automation/experts/experts_historydealget_funcs). The list of [deal properties](/en/book/automation/experts/experts_deal_properties) accessible through these functions was described in the previous section.

We will consider an example of using functions after studying HistoryOrderGet and HistoryDealGet functions.
