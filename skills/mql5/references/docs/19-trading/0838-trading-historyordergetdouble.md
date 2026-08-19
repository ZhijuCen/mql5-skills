# HistoryOrderGetDouble

Returns the requested order property. The order property must be of the double type. There are 2 variants of the function.

1. Immediately returns the property value.

```
double  HistoryOrderGetDouble(
   ulong                       ticket_number,     // Ticket
   ENUM_ORDER_PROPERTY_DOUBLE  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  HistoryOrderGetDouble(
   ulong                       ticket_number,     // Ticket
   ENUM_ORDER_PROPERTY_DOUBLE  property_id,       // Property identifier
   double&                     double_var         // Here we accept the property value
   );

```

Parameters

ticket_number

[in]  Order ticket.

property_id

[in]  Identifier of the order property. The value can be one of the values of the [ENUM_ORDER_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/orderproperties#enum_order_property_double) enumeration.

double_var

[out]  Variable of the double type that accepts the value of the requested property.

Return Value

Value of the [double](/en/docs/basis/types/double) type.

Note

Do not confuse orders of a trading history with current [pending orders](/en/docs/trading/orderstotal) that appear on the "Trade" tab of the "Toolbox" bar. The list of [orders](/en/docs/constants/tradingconstants/orderproperties) that were canceled or have led to a transaction, can be viewed in the "History" tab of "Toolbox" of the client terminal.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- request deal and order history
   if(!HistorySelect(0, TimeCurrent()))
     {
      Print("HistorySelect() failed. Error ", GetLastError());
      return;
     }
     
//--- in a loop by the list of all historical orders on the account
   int total=HistoryOrdersTotal();
   for(int i=0; i<total; i++)
     {
      //--- get the order ticket in the list by the loop index
      ulong ticket=HistoryOrderGetTicket(i);
      if(ticket==0)
         continue;
      
      //--- get the order type and display the header for the list of real properties of the selected order
      string type=OrderTypeDescription((ENUM_ORDER_TYPE)HistoryOrderGetInteger(ticket, ORDER_TYPE));
      PrintFormat("Double properties of an history order %s #%I64u:", type, ticket);
      
      //--- print all the real properties of the selected order under the header
      HistoryOrderPropertiesDoublePrint(ticket, 16);
     }
   /*
   result:
   Double properties of an history order Sell #2810847541:
   Volume initial: 0.50
   Volume current: 0.00
   Price open:     1.10491
   StopLoss:       0.00000
   TakeProfit:     0.00000
   Price current:  1.10491
   StopLimit:      0.00000
   Double properties of an history order Buy Limit #2811003507:
   Volume initial: 1.00
   Volume current: 1.00
   Price open:     1.10547
   StopLoss:       0.00000
   TakeProfit:     0.00000
   Price current:  1.10591
   StopLimit:      0.00000
   */
  }
//+------------------------------------------------------------------+
//| Display real properties of the                                   |
//| selected historical order in the journal                         |
//+------------------------------------------------------------------+
void HistoryOrderPropertiesDoublePrint(const long ticket, const uint header_width=0)
  {
   uint   w=0;
   string header="";
   double value=0;
   
//--- get the order symbol and the number of decimal places for the symbol
   string symbol = HistoryOrderGetString(ticket, ORDER_SYMBOL);
   int    digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   header="Volume initial:";
   w=(header_width==0 ? header.Length()+1 : header_width);
//--- get and display the initial volume when placing an order with a header of the specified width in the journal
   if(!HistoryOrderGetDouble(ticket, ORDER_VOLUME_INITIAL, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the unfulfilled order volume in the journal
   header="Volume current:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_VOLUME_CURRENT, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the price, specified in the order, in the journal
   header="Price open:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_PRICE_OPEN, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
   
//--- display the StopLoss level in the journal
   header="StopLoss:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_SL, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the TakeProfit level in the journal
   header="TakeProfit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_TP, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the current price by the order symbol in the journal
   header="Price current:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_PRICE_CURRENT, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the Limit order price, when StopLimit order is activated, in the journal
   header="StopLimit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryOrderGetDouble(ticket, ORDER_PRICE_STOPLIMIT, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
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

[HistorySelect()](/en/docs/trading/historyselect), [HistoryOrdersTotal()](/en/docs/trading/historyorderstotal), [HistoryOrderSelect()](/en/docs/trading/historyorderselect), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
