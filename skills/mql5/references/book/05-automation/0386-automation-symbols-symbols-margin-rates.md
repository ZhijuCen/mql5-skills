# Symbol margin rates

Among the characteristics of the symbol specification available in the MQL5 API, which we will discuss in detail in further sections, there are several characteristics related to margin requirements, which apply when opening and maintaining trading positions. Due to the fact that the terminal provides trading on different markets and different types of instruments, these requirements may vary significantly. In a generalized form, this is expressed in the application of margin correction rates that are set individually for symbols and different types of trading operations. For the user, the rates are displayed in the terminal in the Specifications window.

As we will see below, the multiplier (if applied) is multiplied by the margin value from the symbol properties. The margin ratio can be obtained programmatically using the SymbolInfoMarginRate function.

bool SymbolInfoMarginRate(const string symbol, ENUM_ORDER_TYPE orderType, double &initial, double &maintenance)

For the specified symbol and order type ([ENUM_ORDER_TYPE](/en/book/automation/experts/experts_order_type)), the function fills in passed by reference initial and maintenance parameters with initial and maintaining margin ratios, respectively. The resulting rates should be multiplied by the margin value of the corresponding type (how to request it is described in the section on [margin requirements](/en/book/automation/symbols/symbols_margin)) to get the amount that will be reserved in the account when placing an order such as orderType.

The function returns true in case of successful execution.

Let's use as an example a simple script SymbolMarginRate.mq5, which outputs margin ratios for Market Watch or all available symbols, depending on the MarketWatchOnly parameter. The operation type can be specified in the OrderType parameter.

```
#include <MQL5Book/MqlError.mqh>
   
input bool MarketWatchOnly = true;
input ENUM_ORDER_TYPE OrderType = ORDER_TYPE_BUY;
   
void OnStart()
{
   const int n = SymbolsTotal(MarketWatchOnly);
   PrintFormat("Margin rates per symbol for %s:", EnumToString(OrderType));
   for(int i = 0; i < n; ++i)
   {
      const string s = SymbolName(i, MarketWatchOnly);
      double initial = 1.0, maintenance = 1.0;
      if(!SymbolInfoMarginRate(s, OrderType, initial, maintenance))
      {
         PrintFormat("Error: %s(%d)", E2S(_LastError), _LastError);
      }
      PrintFormat("%4d %s = %f %f", i, s, initial, maintenance);
   }
}

```

Below is the log.

```
Margin rates per symbol for ORDER_TYPE_BUY:
   0 EURUSD = 1.000000 0.000000
   1 XAUUSD = 1.000000 0.000000
   2 BTCUSD = 0.330000 0.330000
   3 USDCHF = 1.000000 0.000000
   4 USDJPY = 1.000000 0.000000
   5 AUDUSD = 1.000000 0.000000
   6 USDRUB = 1.000000 1.000000

```

You can compare the received values with the symbol specifications in the terminal.
