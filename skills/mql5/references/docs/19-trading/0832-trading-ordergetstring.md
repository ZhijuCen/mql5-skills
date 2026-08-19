# OrderGetString

Returns the requested order property, pre-selected using [OrderGetTicket](/en/docs/trading/ordergetticket) or [OrderSelect](/en/docs/trading/orderselect). The order property must be of the string type. There are 2 variants of the function.

1. Immediately returns the property value.

```
string  OrderGetString(
   ENUM_ORDER_PROPERTY_STRING  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  OrderGetString(
   ENUM_ORDER_PROPERTY_STRING  property_id,       // Property identifier
   string&                     string_var         // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of the order property. The value can be one of the values of the [ENUM_ORDER_PROPERTY_STRING](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_string) enumeration.

string_var

[out]  Variable of the string type that accepts the value of the requested property.

Return Value

Value of the [string](/en/docs/basis/types/stringconst) type.

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
      
      //--- get the order type and display the header for the list of string properties of the selected order
      string type=OrderTypeDescription((ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE));
      PrintFormat("String properties of an active pending order %s #%I64u:", type, ticket);
      
      //--- print all the string properties of the selected order under the header
      OrderPropertiesStringPrint(13);
     }
   /*
   result:
   String properties of an active pending order Sell Limit #2813781342:
   Comment:     Test OrderGetString
   Symbol:      EURUSD
   External ID: 
   */
  }
//+------------------------------------------------------------------+
//| Display string properties of the selected order in the journal   |
//+------------------------------------------------------------------+
void OrderPropertiesStringPrint(const uint header_width=0)
  {
//--- display the comment in the journal
   OrderPropertyPrint("Comment:", header_width, ORDER_COMMENT);
   
//--- display a symbol the order has been placed for in the journal
   OrderPropertyPrint("Symbol:", header_width, ORDER_SYMBOL);
   
//--- display the order ID in an external system in the journal 
   OrderPropertyPrint("External ID:", header_width, ORDER_EXTERNAL_ID);
  }
//+------------------------------------------------------------------+
//| Display the order string property value in the journal           |
//+------------------------------------------------------------------+
void OrderPropertyPrint(const string header, uint header_width, ENUM_ORDER_PROPERTY_STRING property)
  {
   string value="";
   if(!OrderGetString(property, value))
      PrintFormat("Cannot get property %s, error=%d", EnumToString(property), GetLastError());
   else
     {
      //--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
      uint w=(header_width==0 ? header.Length()+1 : header_width);
      PrintFormat("%-*s%-s", w, header, value);
     }
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
      default                          :  return("Unknown order type: "+(string)type);
     }
  }

```

See also

[OrdersTotal()](/en/docs/trading/orderstotal), [OrderGetTicket()](/en/docs/trading/ordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
