# Order execution modes by price and volume

When sending trade requests, we will need to specify the buying/selling price and volume in the algorithm in a special way. At the same time, it should be taken into account that in the financial markets there is no guarantee that at the moment the entire requested volume is available for the financial instrument at the desired price. Therefore, trading operations are regulated by price and volume execution modes (or policies). They define the rules for cases when the price has changed during the process of sending the request, or it cannot be fully satisfied.

In the chapter on symbols, in the section [Trading conditions and order execution modes](/en/book/automation/symbols/symbols_execution_filling), we have already discussed the settings for order execution by price (SYMBOL_TRADE_EXEMODE) and order filling by volume (SYMBOL_FILLING_MODE), which are set by the broker. In accordance with the available SYMBOL_FILLING_MODE modes, the MQL program must select the fill mode for the newly formed order in a special structure [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) (soon we will see this in practice).

Versions are provided in the ENUM_ORDER_TYPE_FILLING enumeration: their identifiers echo those of SYMBOL_FILLING_MODE.

| Execution policy (Values) | Description |
| --- | --- |
| ORDER_FILLING_FOK (0) | Fill or Kill |
| ORDER_FILLING_IOC (1) | Immediate or Cancel |
| ORDER_FILLING_RETURN (2) | Return |

With the ORDER_FILLING_FOK policy, an order can only be filled in the specified volume. If there is not enough volume of the financial instrument on the market at the moment, the order will not be executed. The required volume can be made up of several offers currently available on the market. The ability to use FOK orders is determined by the presence of the SYMBOL_FILLING_FOK permission.

With the ORDER_FILLING_IOC policy, the trader agrees to make a deal on the maximum volume available on the market within the limits specified in the order. If full coverage is not possible, the order will be executed on the available volume, and the missing volume will be canceled. The ability to use IOC orders is determined by the presence of the SYMBOL_FILLING_IOC permission.

With the ORDER_FILLING_RETURN policy, in case of partial execution, the order with the remaining volume is not canceled but continues to operate. This is the default mode and is always available. However, there is one exception: Return orders are not allowed in market execution mode (SYMBOL_TRADE_EXECUTION_MARKET in the SYMBOL_TRADE_EXEMODE symbol property).

Thus, before sending a market (not pending) order, the MQL program should correctly set one of the ORDER_TYPE_FILLING policies based on the SYMBOL_FILLING_MODE property of the corresponding financial instrument: this property contains a combination of bit flags of allowed modes.

For pending orders, regardless of the SYMBOL_TRADE_EXEMODE execution mode, you must use the ORDER_FILLING_RETURN policy, since such orders will be filled with volume later and according to the rules that the broker sets at that time.

Unlike the volume fill policy, the order execution mode at a price cannot be selected as it is predetermined by the broker for each symbol. This affects which fields of the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure should be filled in before submitting a trade request.

The application of fill policies depending on the execution modes can be represented as a table ('+' — allowed, '-' — disabled, '±' — depends on the symbol settings):

| Fill policy 
 Execution mode | ORDER_FILLING 
 _FOK | ORDER_FILLING 
 _IOC | ORDER_FILLING 
 _RETURN |
| --- | --- | --- | --- |
| SYMBOL_TRADE_EXECUTION_INSTANT | + | + | + |
| SYMBOL_TRADE_EXECUTION_REQUEST | + | + | + |
| SYMBOL_TRADE_EXECUTION_MARKET | ± | ± | - |
| SYMBOL_TRADE_EXECUTION_EXCHANGE | ± | ± | + |
| Pending | - | - | + |

In the SYMBOL_TRADE_EXECUTION_INSTANT and SYMBOL_TRADE_EXECUTION_REQUEST execution modes, all volume filling policies are allowed.
