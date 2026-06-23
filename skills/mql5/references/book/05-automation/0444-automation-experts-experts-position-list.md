# Getting the list of positions

In many examples of Expert Advisors, we have already used the MQL5 API functions designed to analyze open trading positions. This section presents their formal description.

It is important to note that the functions of this group are not able to create, modify, or delete positions. As we saw earlier, all such actions are performed indirectly through the sending of orders. If they are successfully executed, transactions are made, as a result of which positions are formed.

Another feature is that the functions are only applicable to online positions. To restore the history of positions, it is necessary to analyze the history of trades.

The PositionsTotal function allows you to find out the total number of open positions on the account (for all financial instruments).

int PositionsTotal()

With netting accounting of positions (ACCOUNT_MARGIN_MODE_RETAIL_NETTING and ACCOUNT_MARGIN_MODE_EXCHANGE), there can be only one position for each symbol at any time. This position can result from one or more deals.

With the independent representation of positions (ACCOUNT_MARGIN_MODE_RETAIL_HEDGING), several positions can be opened simultaneously for each symbol, including multidirectional ones. Each market entry trade creates a separate position, so a partial step-by-step execution of one order can generate several positions.

The PositionGetSymbol function returns the symbol of a position by its number.

string PositionGetSymbol(int index)

The index must be between 0 and N-1, where N is the value received by the pre-call of PositionsTotal. The order of positions is not regulated.

If the position is not found, then an empty string will be returned, and the error code will be available in _LastError.

Examples of using these two functions were provided in several test Experts Advisors ([TrailingStop.mq5](/en/book/automation/experts/experts_trailing_stop), [TradeCloseBy.mq5](/en/book/automation/experts/experts_closeby), and others) in functions with names GetMyPosition/GetMyPositions.

An open position is characterized by a unique ticket which is the number that distinguishes it from other positions, but may change during its life in some cases, such as a position reversal in netting mode by one trade, or as a result of service operations on the server (reopening for swap accrual, clearing).

To get a position ticket by its number, we use the PositionGetTicket function.

ulong PositionGetTicket(int index)

Additionally, the function highlights a position in the trading environment of the terminal, which then allows you to read its properties using a group of special [PositionGet](/en/book/automation/experts/experts_positionget_funcs)[ functions](/en/book/automation/experts/experts_positionget_funcs). In other words, by analogy with orders, the terminal maintains an internal cache for each MQL program to store the properties of one position. To highlight a position, in addition to PositionGetTicket, there are two functions: PositionSelect and PositionSelectByTicket which we will discuss below.

In case of an error, the PositionGetTicket function will return 0.

The ticket should not be confused with the identifier that is assigned to each position and never changes. It is the identifiers that are used to link positions with orders and deals. We will talk about this a little later.   

   

Tickets are needed to fulfill requests involving positions: the tickets are specified in the position and position_by fields of the MqlTradeRequest structure. Besides, by saving the ticket in a variable, the program can subsequently select a specific position using the PositionSelectByTicket function (see below) and work with it without resorting to repeated enumeration of positions in the loop.

When a position is reversed on a netting account, POSITION_TICKET is changed to the ticket of the order that initiated this operation. However, such a position can still be tracked using an ID. Position reversal is not supported in hedging mode.

bool PositionSelect(const string symbol)

The function selects an open position by the name of the financial instrument.

With the independent representation of positions (ACCOUNT_MARGIN_MODE_RETAIL_HEDGING), there can be several open positions for each symbol at the same time. In this case, PositionSelect will select the position with the smallest ticket.

The returned result signals a successful (true) or unsuccessful (false) function execution.

The fact that the properties of the selected position are cached means that the position itself may no longer exist, or it may be changed if the program reads its properties after some time. It is recommended to call the PositionSelect function just before accessing the data.

bool PositionSelectByTicket(ulong ticket)

The function selects an open position for further work on the specified ticket.

We will look at examples of using functions later when studying [properties](/en/book/automation/experts/experts_position_properties) and related [PositionGet](/en/book/automation/experts/experts_positionget_funcs)[ functions](/en/book/automation/experts/experts_positionget_funcs).

When constructing algorithms using the PositionsTotal, OrdersTotal, and similar functions, the asynchronous principles of the terminal operation should be taken into account. We have already touched on this topic when writing the MqlTradeSync.mqh classes and implementing waiting for the execution results from trade requests. However, this wait is not always possible on the client side. In particular, if we place a pending order, then its transformation into a market order and subsequent execution will take place on the server. At this moment, the order may cease to be listed among the active ones (OrdersTotal will return 0), but the position is not displayed yet (PositionsTotal also equals 0). Therefore, an MQL program that has a condition for placing an order in the absence of a position may erroneously initiate a new order, as a result of which the position will eventually double.

To solve this problem, an MQL program must analyze the trading environment more deeply than just checking the number of orders and positions at once. For example, you can keep a snapshot of the last correct state of the trading environment and not allow any entities to disappear without some kind of confirmation. Only then can a new cast be formed. Thus, an order can be deleted only together with a position change (creation, closing) or moved to history with a cancel status. One of the possible solutions is proposed in the form of the TradeGuard class in the TradeGuard.mqh file. The book also includes the demo script TradeGuardExample.mq5 which you can study additionally.
