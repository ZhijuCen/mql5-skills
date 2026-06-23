# Overview of functions of the MetaTrader5 package for Python

The API functions available in Python can be conditionally divided into 2 groups: functions that have full analogs in the MQL5 API and functions available only in Python. The presence of the second group is partly due to the fact that the connection between Python and MetaTrader 5 must be technically organized before application functions can be used. This explains the presence and purpose of a pair of functions [initialize](/en/book/advanced/python/python_init) and [shutdown](/en/book/advanced/python/python_init): the first establishes a connection to the terminal, and the second one terminates it.

It is important that during the initialization process, the required copy of the terminal can be launched (if it has not been executed yet) and a specific trading account can be selected. In addition, it is possible to change the trading account in the context of an already opened connection to the terminal: this is done by the [login](/en/book/advanced/python/python_init) function.

After connecting to the terminal, a Python script can get a summary of the terminal version using the [version](/en/book/advanced/python/python_init) function. Full information about the terminal is available through [terminal_info](/en/book/advanced/python/python_terminal_info) which is a complete analog of three TerminalInfo functions, as if they were united in one call.

The following table lists the Python application functions and their counterparts in the MQL5 API.

| Python | MQL5 |
| --- | --- |
| last_error | GetLastError  (Attention! Python has its native error codes) |
| account_info | AccountInfoInteger ,  AccountInfoDouble ,  AccountInfoString |
| terminal_info | TerminalInfoInteger ,  TerminalInfoDouble ,  TerminalInfoDouble |
| symbols_total | SymbolsTotal  (all symbols, including custom and disabled) |
| symbols_get | SymbolsTotal  +  SymbolInfo  functions |
| symbol_info | SymbolInfoInteger ,  SymbolInfoDouble ,  SymbolInfoString |
| symbol_info_tick | SymbolInfoTick |
| symbol_select | SymbolSelect |
| market_book_add | MarketBookAdd |
| market_book_get | MarketBookGet |
| market_book_release | MarketBookRelease |
| copy_rates_from | CopyRates  (by the number of bars, starting from date/time) |
| copy_rates_from_pos | CopyRates  (by the number of bars, starting from the bar number) |
| copy_rates_range | CopyRates  (in the date/time range) |
| copy_ticks_from | CopyTicks  (by the number of ticks, starting from the specified time) |
| copy_ticks_range | CopyTicksRange  (in the specified time range) |
| orders_total | OrdersTotal |
| orders_get | OrdersTotal  +  OrderGet  functions |
| order_calc_margin | OrderCalcMargin |
| order_calc_profit | OrderCalcProfit |
| order_check | OrderCheck |
| order_send | OrderSend |
| positions_total | PositionsTotal |
| positions_get | PositionsTotal  +  PositionGet  functions |
| history_orders_total | HistoryOrdersTotal |
| history_orders_get | HistoryOrdersTotal  +  HistoryOrderGet  functions |
| history_deals_total | HistoryDealsTotal |
| history_deals_get | HistoryDealsTotal  +  HistoryDealGet  functions |

Functions from the Python API have several features.

As already noted, functions can have named parameters: when a function is called, such parameters are specified together with a name and value, in each pair of name and value they are combined with the equal sign '='. The order of specifying named parameters is not important (unlike positional parameters, which are used in MQL5 and must follow the strict order specified by the function prototype).

Python functions operate on data types native to Python. This includes not only the usual numbers and strings but also several composite types, somewhat similar to MQL5 arrays and structures.

For example, many functions return special Python data structures: tuple and namedtuple.

A tuple is a sequence of elements of an arbitrary type. It can be thought of as an array, but unlike an array, the elements of a tuple can be of different types. You can also think of a tuple as a set of structure fields.

An even closer resemblance to structure can be found with named tuples, where each element is given an ID. Only an index can be used to access an element in a common tuple (in square brackets, as in MQL5, that is, [i]). However, we can apply the dereference operator (dot '.') to a named tuple to get its "property " just like in the MQL5 structure (tuple.field).

Also, tuples and named tuples cannot be edited in code (that is, they are constants).

Another popular type is a dictionary: an associative array that stores key and value pairs, and the types of both can vary. The dictionary value is accessed using the operator [], and the key (whatever type it is, for example, a string) is indicated between the square brackets, which makes dictionaries similar to arrays. A dictionary cannot have two pairs with the same key, that is, the keys are always unique. In particular, a named tuple can easily be turned into a dictionary using the method namedtuple._asdict().
