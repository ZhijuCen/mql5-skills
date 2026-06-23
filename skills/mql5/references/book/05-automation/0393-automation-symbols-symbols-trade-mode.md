# Trading permission

As a continuation of the subject related to the correct preparation of trading orders which we started in the [previous section](/en/book/automation/symbols/symbols_volume), let's turn to the following pair of properties that play a very important role in the development of [Expert Advisors](/en/book/automation/experts).

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_MODE | Permissions for different trading modes for the symbol (see ENUM_SYMBOL_TRADE_MODE) |
| SYMBOL_ORDER_MODE | Flags of allowed order types, bit mask (see further) |

Both properties are of integer type and are available through the SymbolInfoInteger function.

We have already used the SYMBOL_TRADE_MODE property in the script [SymbolPermissions.mq5](/en/book/automation/symbols/symbols_sessions). Its value is one of the elements of the ENUM_SYMBOL_TRADE_MODE enumeration.

| Identifier | Value | Description |
| --- | --- | --- |
| SYMBOL_TRADE_MODE_DISABLED | 0 | Trading is disabled for the symbol |
| SYMBOL_TRADE_MODE_LONGONLY | 1 | Only buy trades are allowed |
| SYMBOL_TRADE_MODE_SHORTONLY | 2 | Only sell trades are allowed |
| SYMBOL_TRADE_MODE_CLOSEONLY | 3 | Only closing operations are allowed |
| SYMBOL_TRADE_MODE_FULL | 4 | No restrictions on trading operations |

Recall the Permissions class contains the isTradeOnSymbolEnabled method which checks several aspects that affect the availability of symbol trading, and one of them is the SYMBOL_TRADE_MODE property. By default, we consider that we are interested in full access to trading, that is, selling and buying: SYMBOL_TRADE_MODE_FULL. Depending on the trading strategy, the MQL program may consider sufficient, for example, permissions only to buy, only to sell, or only to close operations.

```
   static bool isTradeOnSymbolEnabled(string symbol, const datetime now = 0,
      const ENUM_SYMBOL_TRADE_MODE mode = SYMBOL_TRADE_MODE_FULL)
   {
      // checking sessions
      bool found = now == 0;
      ...
      // checking the trading mode for the symbol
      return found && (SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) == mode);
   }

```

In addition to the trading mode, we will need to analyze the permissions for orders of different types in the future: they are indicated by separate bits in the SYMBOL_ORDER_MODE property and can be arbitrarily combined with a logical OR ('|'). For example, the value 127 (0x7F) corresponds to all bits set, that is, the availability of all types of orders.

| Identifier | Value | Description |
| --- | --- | --- |
| SYMBOL_ORDER_MARKET | 1 | Market orders are allowed (Buy and Sell) |
| SYMBOL_ORDER_LIMIT | 2 | Limit orders are allowed (Buy Limit and Sell Limit) |
| SYMBOL_ORDER_STOP | 4 | Stop orders are allowed (Buy Stop and Sell Stop) |
| SYMBOL_ORDER_STOP_LIMIT | 8 | Stop limit orders are allowed (Buy Stop Limit and Sell Stop Limit) |
| SYMBOL_ORDER_SL | 16 | Setting Stop Loss levels is allowed |
| SYMBOL_ORDER_TP | 32 | Setting Take Profit levels is allowed |
| SYMBOL_ORDER_CLOSEBY | 64 | Permission to close a position by an opposite one for the same symbol, Close By operation |

The SYMBOL_ORDER_CLOSEBY property is only set for accounts with hedging accounting (ACCOUNT_MARGIN_MODE_RETAIL_HEDGING, see [Account type](/en/book/automation/account/account_netting_hedge)).

In the test script SymbolFilterTradeMode.mq5, we will request a couple of described properties for symbols visible in Market Watch. The output of bits and their combinations as numbers is not very informative, so we will utilize the fact that in the SymbolMonitor class, we have a convenient method stringify to print enumeration members and bit masks of all properties.

```
void OnStart()
{
   SymbolFilter f;                      // filter object
   string symbols[];                    // array for names 
   long permissions[][2];               // array for data (property values)
   
   // list of requested symbol properties
   ENUM_SYMBOL_INFO_INTEGER modes[] =
   {
      SYMBOL_TRADE_MODE,
      SYMBOL_ORDER_MODE
   };
   
   // apply the filter, get arrays with results
   f.let(SYMBOL_VISIBLE, true).select(true, modes, symbols, permissions);
   
   const int n = ArraySize(symbols);
   PrintFormat("===== Trade permissions for the symbols (%d) =====", n);
   for(int i = 0; i < n; ++i)
   {
      Print(symbols[i] + ":");
      for(int j = 0; j < ArraySize(modes); ++j)
      {
         // display bit and number descriptions "as is"
         PrintFormat("  %s (%d)",
            SymbolMonitor::stringify(permissions[i][j], modes[j]),
            permissions[i][j]);
      }
   }
}

```

Below is part of the log resulting from running the script.

```
===== Trade permissions for the symbols (13) =====
EURUSD:
  SYMBOL_TRADE_MODE_FULL (4)
  [ _SYMBOL_ORDER_MARKET _SYMBOL_ORDER_LIMIT _SYMBOL_ORDER_STOP
  _SYMBOL_ORDER_STOP_LIMIT _SYMBOL_ORDER_SL _SYMBOL_ORDER_TP
  _SYMBOL_ORDER_CLOSEBY ] (127)
GBPUSD:
  SYMBOL_TRADE_MODE_FULL (4)
  [ _SYMBOL_ORDER_MARKET _SYMBOL_ORDER_LIMIT _SYMBOL_ORDER_STOP
  _SYMBOL_ORDER_STOP_LIMIT _SYMBOL_ORDER_SL _SYMBOL_ORDER_TP
  _SYMBOL_ORDER_CLOSEBY ] (127)
... 
SP500m:
  SYMBOL_TRADE_MODE_DISABLED (0)
  [ _SYMBOL_ORDER_MARKET _SYMBOL_ORDER_LIMIT _SYMBOL_ORDER_STOP
  _SYMBOL_ORDER_STOP_LIMIT _SYMBOL_ORDER_SL _SYMBOL_ORDER_TP ] (63)

```

Please note that trading for the last symbol SP500m is completely disabled (its quotes are provided only as "indicative"). At the same time, its set of flags by order types is not 0 but does not make any difference.

Depending on the events in the market, the broker can change the properties of the symbol at their own discretion, for example, leaving only the opportunity to close positions for some time, so a correct trading robot must control these properties before each operation.
