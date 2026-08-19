# OrderGetDouble

Returns the requested property of an order, pre-selected using [OrderGetTicket](/en/docs/trading/ordergetticket) or [OrderSelect](/en/docs/trading/orderselect). The order property must be of the double type. There are 2 variants of the function.

1. Immediately returns the property value.

```
double  OrderGetDouble(
   ENUM_ORDER_PROPERTY_DOUBLE  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of a function. If successful, the value of the property is placed in a target variable passed by reference by the last parameter.

```
bool  OrderGetDouble(
   ENUM_ORDER_PROPERTY_DOUBLE  property_id,       // Property identifier
   double&                        double_var         // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of the order property. The value can be one of the values of the [ENUM_ORDER_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_double) enumeration.

double_var

[out]  Variable of the double type that accepts the value of the requested property.

Return Value

Value of the [double](/en/docs/basis/types/double) type. If the function fails, 0 is returned.

Note

Do not confuse current [pending orders](/en/docs/constants/tradingconstants/orderproperties) with positions, which are also displayed on the "Trade" tab of the "Toolbox" of the client terminal.

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

To ensure receipt of fresh data about an order, it is recommended to call [OrderSelect()](/en/docs/trading/orderselect) right before referring to them.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- in a loop by the list of all account orders
   int total=OrdersTotal();
   for(int i=0; i<total; i++)
     {
      //--- get the order ticket in the list by the loop index
      ulong ticket=OrderGetTicket(i);
      if(ticket==0)
         continue;
      
      //--- get the order type and display the header for the list of real properties of the selected order
      string type=OrderTypeDescription((ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE));
      PrintFormat("Double properties of an active pending order %s #%I64u:", type, ticket);
      
      //--- print all the real properties of the selected order under the header
      OrderPropertiesDoublePrint(16);
     }
   /*
   result:
   Double properties of an active pending order Sell Limit #2812000714:
   Volume initial: 1.00
   Volume current: 1.00
   Price open:     145.282
   StopLoss:       0.000
   TakeProfit:     0.000
   Price current:  145.044
   StopLimit:      0.000
   Double properties of an active pending order Buy Limit #2812001112:
   Volume initial: 1.00
   Volume current: 1.00
   Price open:     144.836
   StopLoss:       0.000
   TakeProfit:     0.000
   Price current:  145.051
   StopLimit:      0.000
   Double properties of an active pending order Buy Stop #2812001488:
   Volume initial: 0.50
   Volume current: 0.50
   Price open:     1.10642
   StopLoss:       0.00000
   TakeProfit:     0.00000
   Price current:  1.10530
   StopLimit:      0.00000
   Double properties of an active pending order Sell Stop #2812001712:
   Volume initial: 0.50
   Volume current: 0.50
   Price open:     1.10374
   StopLoss:       0.00000
   TakeProfit:     0.00000
   Price current:  1.10525
   StopLimit:      0.00000
   */
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
//+------------------------------------------------------------------+
//| Display real properties of the selected order in the journal     |
//+------------------------------------------------------------------+
void OrderPropertiesDoublePrint(const uint header_width=0)
  {
//--- get the order symbol and the number of decimal places for the symbol
   string symbol = OrderGetString(ORDER_SYMBOL);
   int    digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   
//--- display the initial volume when placing an order with a header of the specified width in the journal
   OrderPropertyPrint("Volume initial:",header_width,2,ORDER_VOLUME_INITIAL);
   
//--- display the unfulfilled order volume in the journal
   OrderPropertyPrint("Volume current:",header_width,2,ORDER_VOLUME_CURRENT);
   
//--- display the price, specified in the order, in the journal
   OrderPropertyPrint("Price open:",header_width,digits,ORDER_PRICE_OPEN);
   
//--- display the StopLoss level in the journal
   OrderPropertyPrint("StopLoss:",header_width,digits,ORDER_SL);
 
//--- display the TakeProfit level in the journal
   OrderPropertyPrint("TakeProfit:",header_width,digits,ORDER_TP);
 
//--- display the current price by the order symbol in the journal
   OrderPropertyPrint("Price current:",header_width,digits,ORDER_PRICE_CURRENT);
 
//--- display the Limit order price, when StopLimit order is activated, in the journal
   OrderPropertyPrint("StopLimit:",header_width,digits,ORDER_PRICE_STOPLIMIT);
  }
//+------------------------------------------------------------------+
//| Display the order real property value in the journal             |
//+------------------------------------------------------------------+
void OrderPropertyPrint(const string header, uint header_width, int digits, ENUM_ORDER_PROPERTY_DOUBLE property)
  {
   double value=0;
   if(!OrderGetDouble(property, value))
      PrintFormat("Cannot get property %s, error=%d", EnumToString(property), GetLastError());
   else
     {
      //--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
      uint w=(header_width==0 ? header.Length()+1 : header_width);
      PrintFormat("%-*s%-.*f", w, header, digits, value);
     }
  }

```

See also

[OrdersTotal()](/en/docs/trading/orderstotal), [OrderGetTicket()](/en/docs/trading/ordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
