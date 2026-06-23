# Pending order expiration rules

When working with pending orders (including Stop Loss and Take Profit levels), an MQL program should check a couple of properties that define the rules for their expiration. Both properties are available as members of the ENUM_SYMBOL_INFO_INTEGER enumeration for the call of the [SymbolInfoInteger](/en/book/automation/symbols/symbols_info) function.

| Identifier | Description |
| --- | --- |
| SYMBOL_EXPIRATION_MODE | Flags of allowed order expiration modes (bit mask) |
| SYMBOL_ORDER_GTC_MODE | The validity period is defined by one of the elements of the ENUM_SYMBOL_ORDER_GTC_MODE enumeration |

The SYMBOL_ORDER_GTC_MODE property is taken into account only if SYMBOL_EXPIRATION_MODE contains SYMBOL_EXPIRATION_GTC (see further). GTC is an acronym for Good Till Canceled.

For each financial instrument, the SYMBOL_EXPIRATION_MODE property can specify several modes of validity (expiration) of pending orders. Each mode has a flag (bit) associated with it.

| Identifier (Value) | Description |
| --- | --- |
| SYMBOL_EXPIRATION_GTC (1) | Order is valid according to the ENUM_SYMBOL_ORDER_GTC_MODE property |
| SYMBOL_EXPIRATION_DAY (2) | Order is valid until the end of the current day |
| SYMBOL_EXPIRATION_SPECIFIED (4) | The expiration date and time are specified in the order |
| SYMBOL_EXPIRATION_SPECIFIED_DAY (8) | The expiration date is specified in the order |

The flags can be combined with a logical OR ('|') operation, for example, SYMBOL_EXPIRATION_GTC | SYMBOL_EXPIRATION_SPECIFIED, equivalent to 1 | 4, which is the number 5. To check whether a particular mode is enabled for a tool, perform a logical AND ('&') operation on the function result and the desired mode bit: a non-zero value means the mode is available.

In the case of SYMBOL_EXPIRATION_SPECIFIED_DAY, the order is valid until 23:59:59 of the specified day. If this time does not fall on the trading session, the expiration will occur at the nearest next trading time.

The ENUM_SYMBOL_ORDER_GTC_MODE enumeration contains the following members.

| Identifier | Description |
| --- | --- |
| SYMBOL_ORDERS_GTC | Pending orders and Stop Loss/Take Profit levels are valid indefinitely until explicitly canceled |
| SYMBOL_ORDERS_DAILY | Orders are valid only within one trading day: upon its completion, all pending orders are deleted, as well as Stop Loss and Take Profit levels |
| SYMBOL_ORDERS_DAILY_EXCLUDING_STOPS | When changing the trading day, only pending orders are deleted, but Stop Loss and Take Profit levels are saved |

Depending on the set bits in the SYMBOL_EXPIRATION_MODE property, when preparing an order for sending, an MQL program can select one of the modes corresponding to these bits. Technically, this is done by filling in the type_time field in a special structure [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) before calling the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function. The field value must be an element of the ENUM_ORDER_TYPE_TIME enumeration (see [Pending order expiration dates](/en/book/automation/experts/experts_pending_expiration)): as we will see later, it has something in common with the above set of flags, that is, each flag sets the corresponding mode in the order: ORDER_TIME_GTC, ORDER_TIME_DAY, ORDER_TIME_SPECIFIED, ORDER_TIME_SPECIFIED_DAY. The expiration time or day itself must be specified in another field of the same structure.

The script SymbolFilterExpiration.mq5 allows you to find out the statistics of the use of each of the flags in the available symbols (in the market overview or in general, depending on the input parameter UseMarketWatch). The second parameter in ShowPerSymbolDetails, being set to true, will cause all flags for each character to be logged, so be careful: if at the same time, the mode UseMarketWatch equals false, a very large number of log entries will be generated.

```
#property script_show_inputs
   
#include <MQL5Book/SymbolFilter.mqh>
   
input bool UseMarketWatch = false;
input bool ShowPerSymbolDetails = false;

```

In the OnStart function, in addition to the filter object and receiving arrays for symbol names and property values, we describe MapArray to calculate statistics separately for each of the SYMBOL_EXPIRATION_MODE and SYMBOL_ORDER_GTC_MODE properties.

```
void OnStart()
{
   SymbolFilter f;                // filter object
   string symbols[];              // receiving array for symbol names
   long flags[][2];               // receiving array for property values
   
   MapArray<SYMBOL_EXPIRATION,int> stats;        // mode counters
   MapArray<ENUM_SYMBOL_ORDER_GTC_MODE,int> gtc; // GTC counters
   
   ENUM_SYMBOL_INFO_INTEGER ints[] =
   {
      SYMBOL_EXPIRATION_MODE,
      SYMBOL_ORDER_GTC_MODE
   };
   ...

```

Next, apply the filter and calculate the statistics.

```
   f.select(UseMarketWatch, ints, symbols, flags);
   const int n = ArraySize(symbols);
   
   for(int i = 0; i < n; ++i)
   {
      if(ShowPerSymbolDetails)
      {
         Print(symbols[i] + ":");
         for(int j = 0; j < ArraySize(ints); ++j)
         {
            // properties in the form of descriptions and numbers
            PrintFormat("  %s (%d)",
               SymbolMonitor::stringify(flags[i][j], ints[j]),
               flags[i][j]);
         }
      }
      
      const SYMBOL_EXPIRATION mode = (SYMBOL_EXPIRATION)flags[i][0];
      for(int j = 0; j < 4; ++j)
      {
         const SYMBOL_EXPIRATION bit = (SYMBOL_EXPIRATION)(1 << j);
         if((mode & bit) != 0)
         {
            stats.inc(bit);
         }
         
         if(bit == SYMBOL_EXPIRATION_GTC)
         {
            gtc.inc((ENUM_SYMBOL_ORDER_GTC_MODE)flags[i][1]);
         }
      }
   }
   ...

```

Finally, we output the received numbers to the log.

```
   PrintFormat("===== Expiration modes for %s symbols =====",
      (UseMarketWatch ? "Market Watch" : "all available"));
   PrintFormat("Total symbols: %d", n);
   
   Print("Stats per expiration mode:");
   stats.print();
   Print("Legend: key=expiration mode, value=count");
   for(int i = 0; i < stats.getSize(); ++i)
   {
      PrintFormat("%d -> %s", stats.getKey(i), EnumToString(stats.getKey(i)));
   }
   Print("Stats per GTC mode:");
   gtc.print();
   Print("Legend: key=GTC mode, value=count");
   for(int i = 0; i < gtc.getSize(); ++i)
   {
      PrintFormat("%d -> %s", gtc.getKey(i), EnumToString(gtc.getKey(i)));
   }
}

```

Let's run the script two times. The first time, with the default settings, we can get something like the following picture.

```
===== Expiration modes for all available symbols =====
Total symbols: 52357
Stats per expiration mode:
    [key] [value]
[0]     1   52357
[1]     2   52357
[2]     4   52357
[3]     8   52303
Legend: key=expiration mode, value=count
1 -> _SYMBOL_EXPIRATION_GTC
2 -> _SYMBOL_EXPIRATION_DAY
4 -> _SYMBOL_EXPIRATION_SPECIFIED
8 -> _SYMBOL_EXPIRATION_SPECIFIED_DAY
Stats per GTC mode:
    [key] [value]
[0]     0   52357
Legend: key=GTC mode, value=count
0 -> SYMBOL_ORDERS_GTC

```

Here you can see that almost all flags are allowed for most symbols, and for the SYMBOL_EXPIRATION_GTC mode, the only variant SYMBOL_ORDERS_GTC is used.

Run the script a second time by setting UseMarketWatch and ShowPerSymbolDetails to true (it is assumed that a limited number of symbols is selected in Market Watch).

```
GBPUSD:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED ] (7)
  SYMBOL_ORDERS_GTC (0)
USDCHF:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED ] (7)
  SYMBOL_ORDERS_GTC (0)
USDJPY:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED ] (7)
  SYMBOL_ORDERS_GTC (0)
...
XAUUSD:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED
  _SYMBOL_EXPIRATION_SPECIFIED_DAY ] (15)
  SYMBOL_ORDERS_GTC (0)
SP500m:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED
  _SYMBOL_EXPIRATION_SPECIFIED_DAY ] (15)
  SYMBOL_ORDERS_GTC (0)
UK100:
  [ _SYMBOL_EXPIRATION_GTC _SYMBOL_EXPIRATION_DAY _SYMBOL_EXPIRATION_SPECIFIED
  _SYMBOL_EXPIRATION_SPECIFIED_DAY ] (15)
  SYMBOL_ORDERS_GTC (0)
===== Expiration modes for Market Watch symbols =====
Total symbols: 15
Stats per expiration mode:
    [key] [value]
[0]     1      15
[1]     2      15
[2]     4      15
[3]     8       6
Legend: key=expiration mode, value=count
1 -> _SYMBOL_EXPIRATION_GTC
2 -> _SYMBOL_EXPIRATION_DAY
4 -> _SYMBOL_EXPIRATION_SPECIFIED
8 -> _SYMBOL_EXPIRATION_SPECIFIED_DAY
Stats per GTC mode:
    [key] [value]
[0]     0      15
Legend: key=GTC mode, value=count
0 -> SYMBOL_ORDERS_GTC

```

Of the 15 selected symbols, only 6 have the SYMBOL_EXPIRATION_SPECIFIED_DAY flag set. Details about the flags for each symbol can be found above.
