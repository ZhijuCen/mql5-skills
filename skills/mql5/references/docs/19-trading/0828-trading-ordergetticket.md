# OrderGetTicket

Returns ticket of a corresponding order and automatically selects the order for further working with it using functions.

```
ulong  OrderGetTicket(
   int  index      // Number in the list of orders
   );

```

Parameters

index

[in]  Number of an order in the list of current orders.

Return Value

Value of the [ulong](/en/docs/basis/types/integer/integertypes) type. If the function fails, 0 is returned.

Note

Do not confuse current [pending orders](/en/docs/constants/tradingconstants/orderproperties) with positions, which are also displayed on the "Trade" tab of the "Toolbox" of the client terminal. An order is a request to conduct a [transaction](/en/docs/constants/tradingconstants/enum_trade_request_actions), while a position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties).

For the "netting" interpretation of positions ([ACCOUNT_MARGIN_MODE_RETAIL_NETTING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer) and [ACCOUNT_MARGIN_MODE_EXCHANGE](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), only one [position](/en/docs/constants/tradingconstants/positionproperties) can exist for a [symbol](/en/docs/check/symbol) at any moment of time. This position is a result of one or more [deals](/en/docs/constants/tradingconstants/dealproperties). Do not confuse positions with valid [pending orders](/en/docs/constants/tradingconstants/orderproperties), which are also displayed on the Trading tab of the Toolbox window.

If individual positions are allowed ([ACCOUNT_MARGIN_MODE_RETAIL_HEDGING](/en/docs/constants/environment_state/accountinformation#enum_account_info_integer)), multiple positions can be open for one symbol.

Function OrderGetTicket() copies data about an order into the program environment, and further calls of [OrderGetDouble()](/en/docs/trading/ordergetdouble), [OrderGetInteger()](/en/docs/trading/ordergetinteger), [OrderGetString()](/en/docs/trading/ordergetstring) return the earlier copied data. This means that the order itself may no longer exist (or its open price, Stop Loss/Take Profit levels or expiration has changed), but data of this order still can be obtained. To ensure receipt of fresh data about an order, it is recommended to call OrderGetTicket() right before referring to them.

Example:

```
void OnStart()
  {
//--- variables for returning values from order properties
   ulong    ticket;
   double   open_price;
   double   initial_volume;
   datetime time_setup;
   string   symbol;
   string   type;
   long     order_magic;
   long     positionID;
//--- number of current pending orders
   uint     total=OrdersTotal();
//--- go through orders in a loop
   for(uint i=0;i<total;i++)
     {
      //--- return order ticket by its position in the list
      if((ticket=OrderGetTicket(i))>0)
        {
         //--- return order properties
         open_price    =OrderGetDouble(ORDER_PRICE_OPEN);
         time_setup    =(datetime)OrderGetInteger(ORDER_TIME_SETUP);
         symbol        =OrderGetString(ORDER_SYMBOL);
         order_magic   =OrderGetInteger(ORDER_MAGIC);
         positionID    =OrderGetInteger(ORDER_POSITION_ID);
         initial_volume=OrderGetDouble(ORDER_VOLUME_INITIAL);
         type          =EnumToString(ENUM_ORDER_TYPE(OrderGetInteger(ORDER_TYPE)));
         //--- prepare and show information about the order
         printf("#ticket %d %s %G %s at %G was set up at %s",
                ticket,                 // order ticket
                type,                   // type
                initial_volume,         // placed volume
                symbol,                 // symbol
                open_price,             // specified open price
                TimeToString(time_setup)// time of order placing
                );
        }
     }
//---
  }

```

See also

[OrdersTotal()](/en/docs/trading/orderstotal), [OrderSelect()](/en/docs/trading/orderselect), [OrderGetInteger()](/en/docs/trading/ordergetinteger)
