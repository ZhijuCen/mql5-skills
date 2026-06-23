# Setting margin rates

Previously, we studied the [SymbolInfoMarginRate](/en/book/automation/symbols/symbols_margin_rates) function, which returns the margin rates per symbol set by the broker. For a custom symbol, we are free to set these rates using the function CustomSymbolSetMarginRate.

bool CustomSymbolSetMarginRate(const string name, ENUM_ORDER_TYPE orderType, double initial, double maintenance)

The function sets margin rates depending on the type and direction of the order (according to the orderType value from the [ENUM_ORDER_TYPE](/en/book/automation/experts/experts_order_type) enumeration). The rates for calculating the initial and maintenance margin (collateral for each lot of an opened or existing position) are transmitted, respectively, in the initial and maintenance parameters.

The final margin amounts are determined based on several symbol properties (SYMBOL_TRADE_CALC_MODE, SYMBOL_MARGIN_INITIAL, SYMBOL_MARGIN_MAINTENANCE, and others) described in the section [Margin requirements](/en/book/automation/symbols/symbols_margin), so they should also be set on the custom symbol if needed.

The function will return an indicator of success (true) or error (false).

With the help of this function and the properties related to margin calculation, you can emulate trading conditions of servers that are unavailable for one reason or another, and debug your MQL programs in the tester.
