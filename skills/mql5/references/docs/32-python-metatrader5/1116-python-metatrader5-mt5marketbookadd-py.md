# market_book_add

Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol.

```
market_book_add(
   symbol      // financial instrument name
)

```

symbol

[in]  Financial instrument name. Required unnamed parameter.

Return Value

True if successful, otherwise – False.

Note

The function is similar to [MarketBookAdd](/en/docs/marketinformation/marketbookadd).

See also

[market_book_get](/en/docs/python_metatrader5/mt5marketbookget_py), [market_book_release](/en/docs/python_metatrader5/mt5marketbookrelease_py), [Market Depth structure](/en/docs/constants/structures/mqlbookinfo)
