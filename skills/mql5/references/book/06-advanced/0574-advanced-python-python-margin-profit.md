# Calculating margin requirements and evaluating profits

A Python developer can directly calculate the margin and potential profit or loss of the proposed trading operation in the script using the order_calc_margin and order_calc_profit functions. In the case of successful execution, the result of any function is a real number; otherwise, it's None.

float order_calc_margin(action, symbol, volume, price)

The order_calc_margin function returns the margin amount (in the account currency) required to complete the specified trade operation action which can be one of the two elements of the [ENUM_ORDER_TYPE](/en/book/automation/experts/experts_order_type) enumeration: ORDER_TYPE_BUY or ORDER_TYPE_SELL. The following parameters specify the name of the financial instrument, the volume of the trade operation, and the opening price.

The function is an analog of [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin).

float order_calc_profit(action, symbol, volume, price_open, price_close)

The order_calc_profit function returns the amount of profit or loss (in the account currency) for the specified type of trade, symbol, and volume, as well as the difference between market entry and exit prices.

The function is an analog of [OrderCalcProfit](/en/book/automation/experts/experts_ordercalcprofit).

It is recommended to check the margin and the expected result of the trading operation before [sending an order](/en/book/advanced/python/python_ordercheck_ordersend).
