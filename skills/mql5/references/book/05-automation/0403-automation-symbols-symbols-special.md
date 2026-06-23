# Specific properties (stock exchange, derivatives, bonds)

In this final section of the chapter, we will briefly review other symbol properties that are outside the scope of the book but may be useful for implementing advanced trading strategies. Detailed information about these properties can be found in the [MQL5 documentation](https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants).

As you know, MetaTrader 5 allows you to trade derivatives market instruments, including options, futures, and bonds. This is reflected in the software interface as well. The MQL5 API provides a lot of specific symbol properties related to the mentioned instrument categories.

In particular, for options, this is the circulation period (the start date SYMBOL_START_TIME and the end date SYMBOL_EXPIRATION_TIME of trading), the strike price (SYMBOL_OPTION_STRIKE), the right to buy or sell (SYMBOL_OPTION_RIGHT, Call/Put), European or American type (SYMBOL_OPTION_MODE) depending on the possibility of early exercising, day-to-day change in closing prices (SYMBOL_PRICE_CHANGE) and volatility (SYMBOL_PRICE_VOLATILITY), as well as estimated coefficients (the Greeks) characterizing the dynamics of price behavior.

For bonds, the accumulated coupon income (SYMBOL_TRADE_ACCRUED_INTEREST), face value (SYMBOL_TRADE_FACE_VALUE), liquidity ratio (SYMBOL_TRADE_LIQUIDITY_RATE) are of particular interest.

For futures — open interest (SYMBOL_SESSION_INTEREST) and total order volumes by buy (SYMBOL_SESSION_BUY_ORDERS_VOLUME) and sell (SYMBOL_SESSION_SELL_ORDERS_VOLUME), clearing price at the close of the trading session (SYMBOL_SESSION_PRICE_SETTLEMENT).

Apart from the [current market data](/en/book/automation/symbols/symbols_tick_parts) that make up a tick, MQL5 allows you to know their daily range: the maximum and minimum values for each of the tick fields. For example, SYMBOL_BIDHIGH is the maximum Bid per day, and SYMBOL_BIDLOW is the minimum. Note that the properties SYMBOL_VOLUMEHIGH, SYMBOL_VOLUMELOW (of type long) actually duplicate, but only with less precision, the volumes in SYMBOL_VOLUMEHIGH_REAL and SYMBOL_VOLUMELOW_REAL (double).

Information about the Last prices and volumes is available, as a rule, only for exchange symbols.

Bear in mind that filling in the properties depends on the settings of the server implemented by the broker.
