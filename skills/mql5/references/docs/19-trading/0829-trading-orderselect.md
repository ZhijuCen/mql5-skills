# OrderSelect

Selects an order to work with. Returns true if the function has been successfully completed. Returns false if the function completion has failed. For more information about an error call [GetLastError()](/en/docs/check/getlasterror).

```
bool  OrderSelect(
   ulong   ticket      // Order ticket 
   );

```

Parameters

ticket

[in]  Order ticket.

Return Value

Value of the bool type.

Note

Do not confuse current [pending orders](/en/docs/constants/tradingconstants/orderproperties) with positions, which are also displayed on the "Trade" tab of the "Toolbox" of the client terminal.

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

Function OrderSelect() copies data about an order into the program environment, and further calls of [OrderGetDouble()](/en/docs/trading/ordergetdouble), [OrderGetInteger()](/en/docs/trading/ordergetinteger), [OrderGetString()](/en/docs/trading/ordergetstring) return the earlier copied data. This means that the order itself may no longer exist (or its open price, Stop Loss/Take Profit levels or expiration has changed), but data of this order still can be obtained. To ensure receipt of fresh data about an order, it is recommended to call OrderSelect() right before referring to them.

Example:

```
#define   EXPERT_MAGIC  123456
#define   OFFSET        50                      // offset from the current price to place the order, in points
#define   DIRECTION     ORDER_TYPE_BUY_LIMIT    // order type
#define   VOLUME        1.0                     // volume
#define   DEVIATION     2                       // allowed deviation from the price
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//-- declare and initialize the trade request, result and variables
   MqlTradeRequest request={};
   MqlTradeResult  result ={};
   double          order_price=0;
   
//--- pending order placing parameters
   request.action    = TRADE_ACTION_PENDING;                               // trading operation type
   request.symbol    = _Symbol;                                            // symbol
   request.volume    = VOLUME;                                             // volume
   request.deviation = DEVIATION;                                          // allowed deviation from the price
   request.magic     = EXPERT_MAGIC;                                       // order MagicNumber
   
//--- check operation type
   switch(DIRECTION)
     {
      case ORDER_TYPE_BUY_LIMIT :
        request.type = ORDER_TYPE_BUY_LIMIT;                               // order type
        order_price  = SymbolInfoDouble(_Symbol, SYMBOL_ASK)-OFFSET*_Point;// open price 
        request.price= NormalizeDouble(order_price, _Digits);              // normalized open price 
        break;
      case ORDER_TYPE_SELL_LIMIT :
        request.type = ORDER_TYPE_SELL_LIMIT;                              // order type
        order_price  = SymbolInfoDouble(_Symbol, SYMBOL_BID)+OFFSET*_Point;// open price 
        request.price= NormalizeDouble(order_price,_Digits);               // normalized open price 
        break;
      case ORDER_TYPE_BUY_STOP :
        request.type = ORDER_TYPE_BUY_STOP;                                // order type
        order_price  = SymbolInfoDouble(_Symbol, SYMBOL_ASK)+OFFSET*_Point;// open price 
        request.price= NormalizeDouble(order_price,_Digits);               // normalized open price 
        break;
      case ORDER_TYPE_SELL_STOP :
        request.type = ORDER_TYPE_SELL_STOP;                               // order type
        order_price  = SymbolInfoDouble(_Symbol, SYMBOL_BID)-OFFSET*_Point;// open price 
        request.price= NormalizeDouble(order_price,_Digits);               // normalized open price 
        break;
      default: // if non-pending or StopLimit order is selected
        Alert("This example is only for placing pending orders BuyLimit, SellLimit, BuyStop and SellStop");
        break;
     }
 
//--- send a request. If failed to send a request, display the error code and complete operation
   if(!OrderSend(request, result))
     {
      Print("OrderSend error ", GetLastError());
      return;
     }
     
//--- display operation data
   PrintFormat("Trade request result: retcode=%u, order=%I64u", result.retcode, result.order);
   
//--- get the order ticket from the trade operation result and select the order by ticket
   ulong ticket=result.order;
   ResetLastError();
   if(!OrderSelect(ticket))
     {
      PrintFormat("OrderSelect(%I64u) failed. Error %d", ticket, GetLastError());
      return;
     }
 
//--- display the data of the order, selected by ticket, in the journal
   ENUM_ORDER_TYPE   type  = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
   long              time  = OrderGetInteger(ORDER_TIME_SETUP_MSC);
   double            price = OrderGetDouble(ORDER_PRICE_OPEN);
   double            volume= OrderGetDouble(ORDER_VOLUME_CURRENT);
   string            symbol= OrderGetString(ORDER_SYMBOL);
   int               digits= (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   PrintFormat("Current selected order: %s %.2f %s #%I64u at %.*f, %s",
               symbol, volume, OrderTypeDescription(type), ticket, digits, price, TimeMscToString(time));
   /*
   result:
   Trade request result: retcode=10009, order=2811006719
   Current selected order: EURUSD 1.00 Buy Limit #2811006719 at 1.10550, 2024.09.04 10:38:28.563
   */
  }
//+------------------------------------------------------------------+
//| Return time with milliseconds                                    |
//+------------------------------------------------------------------+
string TimeMscToString(const long time_msc, int flags=TIME_DATE|TIME_MINUTES|TIME_SECONDS)
  {
   return(TimeToString(time_msc/1000, flags) + "." + IntegerToString(time_msc %1000, 3, '0'));
  }
//+------------------------------------------------------------------+
//| Return the order type description                                |
//+------------------------------------------------------------------+
string OrderTypeDescription(const ENUM_ORDER_TYPE type)
  {
   switch(type)
     {
      case ORDER_TYPE_BUY              :  return("Buy");
      case ORDER_TYPE_SELL             :  return("Sell");
      case ORDER_TYPE_BUY_LIMIT        :  return("Buy Limit");
      case ORDER_TYPE_SELL_LIMIT       :  return("Sell Limit");
      case ORDER_TYPE_BUY_STOP         :  return("Buy Stop");
      case ORDER_TYPE_SELL_STOP        :  return("Sell Stop");
      case ORDER_TYPE_BUY_STOP_LIMIT   :  return("Buy Stop Limit");
      case ORDER_TYPE_SELL_STOP_LIMIT  :  return("Sell Stop Limit");
      default                          :  return("Unknown order type");
     }
  }

```

See also

[OrderGetInteger()](/en/docs/trading/ordergetinteger), [OrderGetDouble()](/en/docs/trading/ordergetdouble), [OrderGetString()](/en/docs/trading/ordergetstring), [OrderCalcProfit()](/en/docs/trading/ordercalcprofit), [OrderGetTicket()](/en/docs/trading/ordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
