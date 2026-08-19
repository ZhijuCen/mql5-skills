# market_book_release

Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol.

```
market_book_release(
   symbol      // financial instrument name
)

```

symbol

[in]  Financial instrument name. Required unnamed parameter.

Return Value

True if successful, otherwise – False.

Note

The function is similar to [MarketBookRelease](/en/docs/marketinformation/marketbookrelease).

See also

[market_book_add](/en/docs/python_metatrader5/mt5marketbookadd_py), [market_book_get](/en/docs/python_metatrader5/mt5marketbookget_py), [Market Depth structure](/en/docs/constants/structures/mqlbookinfo)
