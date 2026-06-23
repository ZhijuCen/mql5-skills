# OrderCalcProfit

The function calculates the profit for the current account, in the current market conditions, based on the parameters passed. The function is used for pre-evaluation of the result of a trade operation. The value is returned in the account currency.

```
bool  OrderCalcProfit(
   ENUM_ORDER_TYPE       action,           // type of the order (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
   string                symbol,           // symbol name
   double                volume,           // volume
   double                price_open,       // open price
   double                price_close,      // close price
   double&               profit            // variable for obtaining the profit value
   );

```

Parameters

action

[in]  Type of the order, can be one of the two values of the [ENUM_ORDER_TYPE](/en/docs/constants/tradingconstants/orderproperties#enum_order_type) enumeration: ORDER_TYPE_BUY or ORDER_TYPE_SELL.

symbol

[in]  Symbol name.

volume

[in]  Volume of the trade operation.

price_open

[in]  Open price.

price_close

[in]  Close price.

profit

[out]  The variable, to which the calculated value of the profit will be written in case the function is successfully executed. The estimated profit value depends on many factors, and can differ in different market environments.

Return Value

The function returns true in case of success; otherwise it returns false. If an invalid order type is specified, the function will return false. In order to obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes), call [GetLastError()](/en/docs/check/getlasterror).

Example:

```
 
#define   VOLUME     1.0   // order volume
#define   DEVIATION  100   // number of points before the close price
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   string currency_profit=SymbolInfoString(_Symbol,SYMBOL_CURRENCY_PROFIT);   // profit currency
   double close_price=ChartPriceOnDropped(); // the price coordinate, corresponding to the point where the script was dropped using the mouse, serves as the close price
 
//---
   for(int i=0; i<=ORDER_TYPE_SELL; i++)
     {
      ENUM_ORDER_TYPE order_type=(ENUM_ORDER_TYPE)i;                 // order type: 0 - Buy, 1 - Sell
      double open_price=PriceOpenByOrderType(_Symbol, order_type);   // open price: for Buy - Ask, for Sell - Bid
     
      //--- if the open price is not received, continue the loop
      if(open_price==0)
         continue;
      
      //--- if the close price is zero (the script was not launched by dragging onto the chart), calculate the price
      if(close_price==0)
         close_price=(order_type==ORDER_TYPE_BUY ? open_price + DEVIATION * _Point : open_price - DEVIATION * _Point);
      
      //--- calculate the approximate profit size for the current account and market environment based on the passed parameters
      double profit=0;
      ResetLastError();
      if(!OrderCalcProfit(order_type, _Symbol, VOLUME, open_price, close_price, profit))
        {
         Print("OrderCalcProfit() failed. Error ", GetLastError());
         continue;
        }
      
      //--- print the received profit value in the journal
      PrintFormat("Estimated profit for %.2f %s position on %s with opening price of %.*f and closing price of %.*f: %.2f %s",
                  VOLUME, OrderTypeDescription(order_type), _Symbol, _Digits, open_price, _Digits, close_price, profit, currency_profit);
      
     }
   /*
   result:
   Estimated profit for 1.00 Buy position on EURUSD with opening price of 1.10757 and closing price of 1.10881: 124.00 USD
   Estimated profit for 1.00 Sell position on EURUSD with opening price of 1.10753 and closing price of 1.10881: -128.00 USD
   */
  }
//+------------------------------------------------------------------+
//| Return open price by order type                                  |
//+------------------------------------------------------------------+
double PriceOpenByOrderType(const string symbol, const ENUM_ORDER_TYPE order_type)
  {
   MqlTick tick={};
 
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
      default                          :  return("Unknown order type");
     }
  }

```

See also

[OrderSend()](/en/docs/trading/ordersend), [Order Properties](/en/docs/constants/tradingconstants/orderproperties), [Trade Operation Types](/en/docs/constants/tradingconstants/enum_trade_request_actions)
