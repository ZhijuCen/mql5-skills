# OrderCalcMargin

The function calculates the margin required for the specified order type, on the current account, in the current market environment not taking into account current pending orders and open positions. It allows the evaluation of margin for the trade operation planned. The value is returned in the account currency.

```
bool  OrderCalcMargin(
   ENUM_ORDER_TYPE       action,           // type of order
   string                symbol,           // symbol name
   double                volume,           // volume
   double                price,            // open price
   double&               margin            // variable for obtaining the margin value
   );

```

Parameters

action

[in]  The order type, can be one of the values of the [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration.

symbol

[in]  Symbol name.

volume

[in]  Volume of the trade operation.

price

[in]  Open price.

margin

[out]  The variable, to which the value of the required margin will be written in case the function is successfully executed. The calculation is performed as if there were no pending orders and open positions on the current account. The margin value depends on many factors, and can differ in different market environments.

Return Value

The function returns true in case of success; otherwise it returns false. In order to obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
#define   VOLUME     1.0   // order volume
#define   DEVIATION  100   // distance for setting a pending order
#define   STOP_LIMIT 50    // order StopLimit distance
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string currency=AccountInfoString(ACCOUNT_CURRENCY);
   int array_types[8]={ORDER_TYPE_BUY,
                       ORDER_TYPE_SELL,
                       ORDER_TYPE_BUY_LIMIT,
                       ORDER_TYPE_SELL_LIMIT,
                       ORDER_TYPE_BUY_STOP,
                       ORDER_TYPE_SELL_STOP,
                       ORDER_TYPE_BUY_STOP_LIMIT,
                       ORDER_TYPE_SELL_STOP_LIMIT };
                       
//--- in a loop by the order type array
   for(int i=0; i<(int)array_types.Size(); i++)
     {
      //--- depending on the order type, get ORDER_TYPE_BUY or ORDER_TYPE_SELL type
      ENUM_ORDER_TYPE type=MarketOrderByOrderType((ENUM_ORDER_TYPE)array_types[i]);
      
      //--- depending on the order type, get the price
      double price=PriceByOrderType(_Symbol, type);
      
      //--- get the amount of margin required for the order type specified in 'action' 
      double margin=EMPTY_VALUE;
      ResetLastError();
      if(!OrderCalcMargin(type, _Symbol, VOLUME, price, margin))
        {
         Print("OrderCalcMargin() failed. Error ",GetLastError());
         continue;
        }
      //--- print the result in the journal
      PrintFormat("Margin required for %.2f %s order at price %.*f on %s symbol: %.2f %s", VOLUME, OrderTypeDescription((ENUM_ORDER_TYPE)i), _Digits, price, _Symbol, margin, currency);
     }
   /*
   result:
   Margin required for 1.00 Buy order at price 1.31668 on GBPUSD symbol: 1316.68 USD
   Margin required for 1.00 Sell order at price 1.31661 on GBPUSD symbol: 1316.61 USD
   Margin required for 1.00 Buy Limit order at price 1.31568 on GBPUSD symbol: 1315.68 USD
   Margin required for 1.00 Sell Limit order at price 1.31761 on GBPUSD symbol: 1317.61 USD
   Margin required for 1.00 Buy Stop order at price 1.31768 on GBPUSD symbol: 1317.68 USD
   Margin required for 1.00 Sell Stop order at price 1.31561 on GBPUSD symbol: 1315.61 USD
   Margin required for 1.00 Buy Stop Limit order at price 1.31718 on GBPUSD symbol: 1317.18 USD
   Margin required for 1.00 Sell Stop Limit order at price 1.31611 on GBPUSD symbol: 1316.11 USD
   */
  }
//+------------------------------------------------------------------+
//| Return the Buy or Sell order type                                |
//+------------------------------------------------------------------+
ENUM_ORDER_TYPE MarketOrderByOrderType(ENUM_ORDER_TYPE type)
  {
   switch(type)
     {
      case ORDER_TYPE_BUY  : case ORDER_TYPE_BUY_LIMIT  : case ORDER_TYPE_BUY_STOP  : case ORDER_TYPE_BUY_STOP_LIMIT  :
        return(ORDER_TYPE_BUY);
      case ORDER_TYPE_SELL : case ORDER_TYPE_SELL_LIMIT : case ORDER_TYPE_SELL_STOP : case ORDER_TYPE_SELL_STOP_LIMIT :
        return(ORDER_TYPE_SELL);
     }
   return(WRONG_VALUE);
  }
//+------------------------------------------------------------------+
//| Return open price by order type                                  |
//+------------------------------------------------------------------+
double PriceByOrderType(const string symbol, const ENUM_ORDER_TYPE order_type)
  {
   int     digits=0;
   double  point=0;
   MqlTick tick={};
 
//--- get the symbol Point value
   ResetLastError();
   if(!SymbolInfoDouble(symbol, SYMBOL_POINT, point))
     {
      Print("SymbolInfoDouble() failed. Error ", GetLastError());
      return 0;
     }
     
//--- get the symbol Digits value
   long value=0;
   if(!SymbolInfoInteger(symbol, SYMBOL_DIGITS, value))
     {
      Print("SymbolInfoInteger() failed. Error ", GetLastError());
      return 0;
     }
   digits=(int)value;
   
//--- get the last prices by symbol
   if(!SymbolInfoTick(symbol, tick))
     {
      Print("SymbolInfoTick() failed. Error ", GetLastError());
      return 0;
     }
     
//--- return the price depending on the order type
   switch(order_type)
     {
      case ORDER_TYPE_BUY              :  return(tick.ask);
      case ORDER_TYPE_SELL             :  return(tick.bid);
      case ORDER_TYPE_BUY_LIMIT        :  return(NormalizeDouble(tick.ask - DEVIATION * point, digits));
      case ORDER_TYPE_SELL_LIMIT       :  return(NormalizeDouble(tick.bid + DEVIATION * point, digits));
      case ORDER_TYPE_BUY_STOP         :  return(NormalizeDouble(tick.ask + DEVIATION * point, digits));
      case ORDER_TYPE_SELL_STOP        :  return(NormalizeDouble(tick.bid - DEVIATION * point, digits));
      case ORDER_TYPE_BUY_STOP_LIMIT   :  return(NormalizeDouble(tick.ask + DEVIATION * point - STOP_LIMIT * point, digits));
      case ORDER_TYPE_SELL_STOP_LIMIT  :  return(NormalizeDouble(tick.bid - DEVIATION * point + STOP_LIMIT * point, digits));
      default                          :  return(0);
     }
  }
//+------------------------------------------------------------------+
//| Return the order type description                                |
//+------------------------------------------------------------------+
string OrderTypeDescription(const ENUM_ORDER_TYPE order_type)
  {
   switch(order_type)
     {
      case ORDER_TYPE_BUY              :  return("Buy");
      case ORDER_TYPE_SELL             :  return("Sell");
      case ORDER_TYPE_BUY_LIMIT        :  return("Buy Limit");
      case ORDER_TYPE_SELL_LIMIT       :  return("Sell Limit");
      case ORDER_TYPE_BUY_STOP         :  return("Buy Stop");
      case ORDER_TYPE_SELL_STOP        :  return("Sell Stop");
      case ORDER_TYPE_BUY_STOP_LIMIT   :  return("Buy Stop Limit");
      case ORDER_TYPE_SELL_STOP_LIMIT  :  return("Sell Stop Limit");
      case ORDER_TYPE_CLOSE_BY         :  return("Close By");
      default                          :  return("Unknown order type");
     }
  }
//+------------------------------------------------------------------+

```

See also

[OrderSend()](/en/docs/trading/ordersend), [Order Properties](/en/docs/constants/tradingconstants/orderproperties), [Trade Operation Types](/en/docs/constants/tradingconstants/enum_trade_request_actions)
