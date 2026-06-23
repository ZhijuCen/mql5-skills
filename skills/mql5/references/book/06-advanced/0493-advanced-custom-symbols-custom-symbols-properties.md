# Custom symbol properties

Custom symbols have the same properties as broker-provided symbols. The properties are read by the standard functions discussed in the chapter on [financial instruments](/en/book/automation/symbols).

The properties of custom symbols can be set by a special group of CustomSymbolSet functions, one function for each fundamental type (integer, real, string).

bool CustomSymbolSetInteger(const string name, ENUM_SYMBOL_INFO_INTEGER property, long value)

bool CustomSymbolSetDouble(const string name, ENUM_SYMBOL_INFO_DOUBLE property, double value)

bool CustomSymbolSetString(const string name, ENUM_SYMBOL_INFO_STRING property, string value)

The functions set for a custom symbol named name a value of property to value. All existing properties are grouped into enumerations ENUM_SYMBOL_INFO_INTEGER, ENUM_SYMBOL_INFO_DOUBLE, ENUM_SYMBOL_INFO_STRING, which were considered element by element in the sections of the aforementioned chapter.

The functions return an indication of success (true) or error (false). One possible problem for errors is that not all properties are allowed to change. When trying to set a read-only property, we get the error CUSTOM_SYMBOL_PROPERTY_WRONG (5307). If you try to write an invalid value to the property, you will get a CUSTOM_SYMBOL_PARAMETER_ERROR (5308) error.

Please note that the minute and tick history of a custom symbol is completely deleted if any of the following properties are changed in the symbol specification:

- SYMBOL_CHART_MODE — price type used to build bars (Bid or Last)
- SYMBOL_DIGITS — number of decimal places in price values
- SYMBOL_POINT — value of one point
- SYMBOL_TRADE_TICK_SIZE — the value of one tick, the minimum allowable price change
- SYMBOL_TRADE_TICK_VALUE — price change cost per tick (see also SYMBOL_TRADE_TICK_VALUE_PROFIT, SYMBOL_TRADE_TICK_VALUE_LOSS)
- SYMBOL_FORMULA — formula for price calculation

If a custom symbol is calculated by a formula, then after deleting its history, the terminal will automatically try to create a new history using the updated properties. However, for programmatically generated symbols, the MQL program itself must take care of the recalculation.

Editing individual properties is most in demand for modifying custom symbols created earlier (after specifying the third parameter origin in the [CustomSymbolCreate](/en/book/advanced/custom_symbols/custom_symbols_create_delete) function).

In other cases, changing properties in bulk can cause subtle effects. The point is that properties are internally linked and changing one of them may require a certain state of other properties in order for the operation to complete successfully. Moreover, setting some properties leads to automatic changes in others.

In the simplest example, after setting the SYMBOL_DIGITS property, you will find that the SYMBOL_POINT property has changed as well. Here is the less obvious case: assigning SYMBOL_CURRENCY_MARGIN or SYMBOL_CURRENCY_PROFIT has no effect on Forex symbols, since the system assumes currency names to occupy the first 3 and next 3 letters of the name ("XXXYYY[suffix]"), respectively. Please note that immediately after the creation of an "empty" symbol, it is by default considered a Forex symbol, and therefore these properties cannot be set for it without first changing the market.

When copying or setting symbol properties, be aware that the platform implies some specifics. In particular, the property [SYMBOL_TRADE_CALC_MODE](/en/book/automation/symbols/symbols_margin) has a default value of 0 (immediately after the symbol is created, but before any property is set), while 0 in the ENUM_SYMBOL_CALC_MODE enumeration corresponds to the SYMBOL_CALC_MODE_FOREX member. At the same time, special naming rules are implied for Forex symbols in the form XXXYYY (where XXX and YYY are currency codes) plus an optional suffix. Therefore, if you do not change SYMBOL_TRADE_CALC_MODE to another required mode in advance, substrings of the specified symbol name (the first and second triple of symbols) will automatically fall into the properties of the base currency (SYMBOL_CURRENCY_BASE) and profit currency (SYMBOL_CURRENCY_PROFIT). For example, if you specify the name "Dummy", it will be split into 2 pseudo-currencies "Dum" and "my".

Another nuance is that before setting the value of SYMBOL_POINT with an accuracy of N decimal places, you need to ensure that SYMBOL_DIGITS is at least N.

The book comes with the script CustomSymbolProperties.mq5, which allows you to experiment with creating copies of the symbol of the current chart and study the resulting effects in practice. In particular, you can choose the name of the symbol, its path, and the direction of bypassing (setting) all supported properties, direct or reverse in terms of property numbering in the language. The script uses a special class CustomSymbolMonitor, which is a wrapper for the above built-in functions: we will describe it [later](/en/book/advanced/custom_symbols/custom_symbols_ticks).
