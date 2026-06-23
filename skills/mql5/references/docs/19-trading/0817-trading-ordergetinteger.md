# OrderGetInteger

Returns the requested order property, pre-selected using [OrderGetTicket](/en/docs/trading/ordergetticket) or [OrderSelect](/en/docs/trading/orderselect). Order property must be of the datetime, int type. There are 2 variants of the function.

1. Immediately returns the property value.

```
long  OrderGetInteger(
   ENUM_ORDER_PROPERTY_INTEGER  property_id        // Property identifier
   );

```

2. Returns true or false depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  OrderGetInteger(
   ENUM_ORDER_PROPERTY_INTEGER  property_id,       // Property identifier
   long&                        long_var           // Here we accept the property value
   );

```

Parameters

property_id

[in]  Identifier of the order property. The value can be one of the values of the [ENUM_ORDER_PROPERTY_INTEGER](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer) enumeration.

long_var

[out]  Variable of the long type that accepts the value of the requested property.

Return Value

Value of the [long](/en/docs/basis/types/integer/integertypes#long) type. If the function fails, 0 is returned.

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
      PrintFormat("Integer properties of an active pending order %s #%I64u:", type, ticket);
      
      //--- print all the integer properties of the selected order under the header
      OrderPropertiesIntegerPrint(17);
     }
   /*
   result:
   Integer properties of an active pending order Buy Limit #2812945317:
   Ticket:          2812945317
   Time setup:      2024.09.04 19:17:16
   Type:            Buy Limit
   State:           Placed
   Time expiration: 0
   Time done:       0
   Time setup msc:  2024.09.04 19:17:16.686
   Time done msc:   0
   Type filling:    Return
   Type time:       Time GTC
   Magic:           0
   Reason:          Client
   Position ID:     0
   Position By ID:  0
   */
  }
//+------------------------------------------------------------------+
//| Display integer properties of the selected order in the journal  |
//+------------------------------------------------------------------+
void OrderPropertiesIntegerPrint(const uint header_width=0)
  {
   uint   w=0;
   string header="";
   long   value=0;
   
//--- display order ticket in the journal
   OrderPropertyPrint("Ticket:", header_width, ORDER_TICKET);
   
//--- display the order placement time in the journal
   OrderPropertyPrint("Time setup:", header_width, ORDER_TIME_SETUP);
   
//--- display the order type in the journal
   OrderPropertyPrint("Type:", header_width, ORDER_TYPE);
   
//--- display the order status in the journal
   OrderPropertyPrint("State:", header_width, ORDER_STATE);
   
//--- display the order expiration time in the journal
   OrderPropertyPrint("Time expiration:", header_width, ORDER_TIME_EXPIRATION);
   
//--- display the order execution/expiration time in the journal
   OrderPropertyPrint("Time done:", header_width, ORDER_TIME_DONE);
   
//--- display the time of placing an order for execution in milliseconds since 01.01.1970 in the journal
   OrderPropertyPrint("Time setup msc:", header_width, ORDER_TIME_SETUP_MSC);
   
//--- display the order execution/expiration time in milliseconds since 01.01.1970 in the journal
   OrderPropertyPrint("Time done msc:", header_width, ORDER_TIME_DONE_MSC);
   
//--- display the execution type by residue in the journal
   OrderPropertyPrint("Type filling:", header_width, ORDER_TYPE_FILLING);
   
//--- display the order lifetime in the journal
   OrderPropertyPrint("Type time:", header_width, ORDER_TYPE_TIME);
   
//--- display the ID of the EA, that placed an order, in the journal
   OrderPropertyPrint("Magic:", header_width, ORDER_MAGIC);
   
//--- display order reason or source in the journal
   OrderPropertyPrint("Reason:", header_width, ORDER_REASON);
   
//--- display the ID of the position, set on the order during its execution, in the journal
   OrderPropertyPrint("Position ID:", header_width, ORDER_POSITION_ID);
   
//--- display the opposite position ID for ORDER_TYPE_CLOSE_BY type orders in the journal
   OrderPropertyPrint("Position By ID:", header_width, ORDER_POSITION_BY_ID);
  }
//+------------------------------------------------------------------+
//| Display the order integer property value in the journal          |
//+------------------------------------------------------------------+
void OrderPropertyPrint(const string header, uint header_width, ENUM_ORDER_PROPERTY_INTEGER property)
  {
   string svalue="";
   long   lvalue=0;
   if(!OrderGetInteger(property, lvalue))
      PrintFormat("Cannot get property %s, error=%d", EnumToString(property), GetLastError());
   else
     {
      switch(property)
        {
         case ORDER_TICKET          :
         case ORDER_MAGIC           :
         case ORDER_POSITION_ID     :
         case ORDER_POSITION_BY_ID  :
           svalue=(string)lvalue;
           break;
           
         case ORDER_TIME_SETUP      :
         case ORDER_TIME_EXPIRATION :
         case ORDER_TIME_DONE       :
           svalue=(lvalue!=0 ? TimeToString((datetime)lvalue, TIME_DATE|TIME_MINUTES|TIME_SECONDS) : "0");
           break;
           
         case ORDER_TIME_SETUP_MSC  :
         case ORDER_TIME_DONE_MSC   :
           svalue=(lvalue!=0 ? TimeMscToString(lvalue) : "0");
           break;
           
         case ORDER_TYPE            :
           svalue=OrderTypeDescription((ENUM_ORDER_TYPE)lvalue);
           break;
         case ORDER_STATE           :
           svalue=OrderStateDescription((ENUM_ORDER_STATE)lvalue);
           break;
         case ORDER_TYPE_FILLING    :
           svalue=OrderTypeFillingDescription((ENUM_ORDER_TYPE_FILLING)lvalue);
           break;
         case ORDER_TYPE_TIME       :
           svalue=OrderTypeTimeDescription((ENUM_ORDER_TYPE_TIME)lvalue);
           break;
         case ORDER_REASON          :
           svalue=OrderReasonDescription((ENUM_ORDER_REASON)lvalue);
           break;
         
         default                    :
           svalue="Unknown property";
           break;
        }
      
      //--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
      uint w=(header_width==0 ? header.Length()+1 : header_width);
      PrintFormat("%-*s%-s", w, header, svalue);
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
//+------------------------------------------------------------------+
//| Return the order status description                              |
//+------------------------------------------------------------------+
string OrderStateDescription(ENUM_ORDER_STATE state)
  {
   switch(state)
     {
      case ORDER_STATE_STARTED         :  return("Started");
      case ORDER_STATE_PLACED          :  return("Placed");
      case ORDER_STATE_CANCELED        :  return("Canceled");
      case ORDER_STATE_PARTIAL         :  return("Partial");
      case ORDER_STATE_FILLED          :  return("Filled");
      case ORDER_STATE_REJECTED        :  return("Rejected");
      case ORDER_STATE_EXPIRED         :  return("Expired");
      case ORDER_STATE_REQUEST_ADD     :  return("Request Add");
      case ORDER_STATE_REQUEST_MODIFY  :  return("Request Modify");
      case ORDER_STATE_REQUEST_CANCEL  :  return("Request Cancel");
      default                          :  return("Unknown state: "+(string)state);
     }
  }
//+------------------------------------------------------------------+
//| Return the description of the order volume filling policy        |
//+------------------------------------------------------------------+
string OrderTypeFillingDescription(const ENUM_ORDER_TYPE_FILLING type)
  {
   switch(type)
     {
      case ORDER_FILLING_FOK     :  return("Fill or Kill");
      case ORDER_FILLING_IOC     :  return("Immediate or Cancel");
      case ORDER_FILLING_BOC     :  return("Book or Cancel");
      case ORDER_FILLING_RETURN  :  return("Return");
      default                    :  return("Unknown type filling: "+(string)type);
     }
  }
//+------------------------------------------------------------------+
//| Return the order expiration date description                     |
//+------------------------------------------------------------------+
string OrderTypeTimeDescription(const ENUM_ORDER_TYPE_TIME type)
  {
   switch(type)
     {
      case ORDER_TIME_GTC           :   return("Time GTC");
      case ORDER_TIME_DAY           :   return("Time Day");
      case ORDER_TIME_SPECIFIED     :   return("Time Specified");
      case ORDER_TIME_SPECIFIED_DAY :   return("Time Specified Day");
      default                       :  return("Unknown type time: "+(string)type);
     }
  }
//+------------------------------------------------------------------+
//| Return the order placement reason description                    |
//+------------------------------------------------------------------+
string OrderReasonDescription(const ENUM_ORDER_REASON reason)
  {
   switch(reason)
     {
      case ORDER_REASON_CLIENT   :  return("Client");
      case ORDER_REASON_MOBILE   :  return("Mobile");
      case ORDER_REASON_WEB      :  return("Web");
      case ORDER_REASON_EXPERT   :  return("Expert");
      case ORDER_REASON_SL       :  return("Stop Loss");
      case ORDER_REASON_TP       :  return("Take Profit");
      case ORDER_REASON_SO       :  return("Stop Out");
      default                    :  return("Unknown reason: "+(string)reason);
     }
  }
//+------------------------------------------------------------------+
//| Return time with milliseconds                                    |
//+------------------------------------------------------------------+
string TimeMscToString(const long time_msc, int flags=TIME_DATE|TIME_MINUTES|TIME_SECONDS)
  {
   return(TimeToString(time_msc/1000, flags) + "." + IntegerToString(time_msc %1000, 3, '0'));
  }

```

See also

[OrdersTotal()](/en/docs/trading/orderstotal), [OrderGetTicket()](/en/docs/trading/ordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
