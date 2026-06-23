# Symbol trading conditions and order execution modes

In this section, we will dive deeper into aspects of trading automation that depend on the settings of financial instruments. For now, we will study only the properties, while their practical application will be presented in later chapters. It is assumed that the reader is already familiar with the basic terminology such as market and pending order, trade, and position.

When sending a trade request for execution, it should be taken into account that in the financial markets there is no guarantee that at a particular moment, the entire requested volume is available for this financial instrument at the desired price. Therefore, real-time trading is regulated by price and volume execution modes. Modes, or in other words, execution policies, define the rules for cases when the price has changed or the requested volume cannot be fully executed at the current moment.

In the MQL5 API, these modes are available for each symbol as the following properties which can be obtained through the function SymbolInfoInteger.

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_EXEMODE | Trade execution modes related to the price |
| SYMBOL_FILLING_MODE | Flags of allowed order filling modes related to the volume (bitmask, see further) |

The value of the SYMBOL_TRADE_EXEMODE property is a member of the ENUM_SYMBOL_TRADE_EXECUTION enumeration.

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_EXECUTION_REQUEST | Trade at the requested price |
| SYMBOL_TRADE_EXECUTION_INSTANT | Instant execution (trading at streamed prices) |
| SYMBOL_TRADE_EXECUTION_MARKET | Market execution |
| SYMBOL_TRADE_EXECUTION_EXCHANGE | Exchange execution |

All or most of these modes should be known to terminal users from the drop-down list Type in the New order dialogue (F9). Let's briefly recall what they mean. For further details, please refer to the terminal documentation.

- Execution on request (SYMBOL_TRADE_EXECUTION_REQUEST) — execution of a market order at a price previously received from the broker. Before sending a market order, the trader requests the current price from the broker. Further execution of the order at this price can either be confirmed or rejected.
- Instant execution (SYMBOL_TRADE_EXECUTION_INSTANT) — execution of a market order at the current price. When sending a trade request for execution, the terminal automatically inserts the current prices into the order. If the broker accepts the price, the order is executed. If the broker does not accept the requested price, the broker returns the prices at which this order can be executed, which is called a requote.
- Market execution (SYMBOL_TRADE_EXECUTION_MARKET) — the broker inserts the execution price into the order without additional confirmation from the trader. Sending a market order in this mode implies an early agreement with the price at which it will be executed.
- Exchange execution (SYMBOL_TRADE_EXECUTION_EXCHANGE) — trading operations are performed at the prices of current market offers.

As for the bits in SYMBOL_FILLING_MODE that can be combined with the logical operator OR ('|'), their presence or absence indicates the following actions.

| Identifier | Value | Fill policy |
| --- | --- | --- |
| SYMBOL_FILLING_FOK | 1 | Fill Or Kill (FOK); the order must be executed exclusively in the specified volume or canceled |
| SYMBOL_FILLING_IOC | 2 | Immediate or Cancel (IOC); trade the maximum volume available on the market within the limits specified in the order or cancel |
| (Identifier missing) | (any, including 0) | Return; in case of partial execution, the market or limit order with the remaining volume is not canceled but stays valid |

The possibility of using FOK and IOC modes is determined by the trade server.

If the SYMBOL_FILLING_FOK mode is enabled, then, while sending an order with the [OrderSend](/en/book/automation/experts/experts_ordersend_ordersendasync) function, the MQL program will be able to use the relevant order fill type in the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure: ORDER_FILLING_FOK. If at the same time, there is not enough volume of the financial instrument on the market, the order will not be executed. It should be taken into account that the required volume can be made up of several offers currently available on the market, resulting in several transactions.

If the SYMBOL_FILLING_IOC mode is enabled, the MQL program will have access to the ORDER_FILLING_IOC order filling method of the same name (it is also specified in the special "filling" field (type_filling) in the MqlTradeRequest structure before sending the order to the OrderSend function). When using this mode, in case of impossibility of full execution, the order will be executed on the available volume, and the remaining volume of the order will be canceled.

The last policy without an identifier is the default mode and is available regardless of other modes (which is why it matches zero or any other value). In other words, even if we get the value 1 (SYMBOL_FILLING_FOK), 2 (SYMBOL_FILLING_IOC), or 3 (SYMBOL_FILLING_FOK | SYMBOL_FILLING_IOC) for the SYMBOL_FILLING_MODE property, the return mode will be implied. To use this policy, when forming an order (filling in the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure) we should specify the fill type ORDER_FILLING_RETURN.

Among all SYMBOL_TRADE_EXEMODE modes, there is one specificity regarding market execution (SYMBOL_TRADE_EXECUTION_MARKET): Return orders are always prohibited in market execution mode.

Since ORDER_FILLING_FOK corresponds to the constant 0, the absence of an explicit indication of the filling type in a trade request will imply this particular mode.

We will consider all these nuances in practice when developing Expert Advisors but for now, let's check the reading of properties in a simple script SymbolFilterExecMode.mq5.

```
#include <MQL5Book/SymbolFilter.mqh>
   
void OnStart()
{
   SymbolFilter f;                      // filter object
   string symbols[];                    // array of symbol names
   long permissions[][2];               // array with property value vectors
   
   // properties to read
   ENUM_SYMBOL_INFO_INTEGER modes[] =
   {
      SYMBOL_TRADE_EXEMODE,
      SYMBOL_FILLING_MODE
   };
   // apply filter - fill arrays
   f.select(true, modes, symbols, permissions);
   
   const int n = ArraySize(symbols);
   PrintFormat("===== Trade execution and filling modes for the symbols (%d) =====", n);
   for(int i = 0; i < n; ++i)
   {
      Print(symbols[i] + ":");
      for(int j = 0; j < ArraySize(modes); ++j)
      {
         // output properties as descriptions and numbers
         PrintFormat("  %s (%d)",
            SymbolMonitor::stringify(permissions[i][j], modes[j]),
            permissions[i][j]);
      }
   }
}

```

Below is a fragment of the log with the results of the script. Almost all symbols here have an immediate execution mode at prices (SYMBOL_TRADE_EXECUTION_INSTANT) except for the last SP500m (SYMBOL_TRADE_EXECUTION_MARKET). Here we can find various volume filling modes, both separate SYMBOL_FILLING_FOK, SYMBOL_FILLING_IOC, and their combination. Only BTCUSD has SYMBOL_FILLING_RETURN specified, i.e. a value of 0 was received (no FOK and IOC bits).

```
===== Trade execution and filling modes for the symbols (13) =====
EURUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK ] (1)
GBPUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK ] (1)
...
USDCNH:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK _SYMBOL_FILLING_IOC ] (3)
USDRUB:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_IOC ] (2)
AUDUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK ] (1)
NZDUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK _SYMBOL_FILLING_IOC ] (3)
...
XAUUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [ _SYMBOL_FILLING_FOK _SYMBOL_FILLING_IOC ] (3)
BTCUSD:
  SYMBOL_TRADE_EXECUTION_INSTANT (1)
  [(_SYMBOL_FILLING_RETURN)] (0)
SP500m:
  SYMBOL_TRADE_EXECUTION_MARKET (2)
  [ _SYMBOL_FILLING_FOK ] (1)

```

Recall that the underscores in the fill mode identifiers appear due to the fact that we had to define our own enumeration SYMBOL_FILLING (SymbolMonitor.mqh) with elements with constant values. This was done because MQL5 does not have such a built-in enumeration, but at the same time, we cannot name the elements of our enumeration exactly as built-in constants as this would cause a name conflict.
