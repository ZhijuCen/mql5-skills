# Getting a list of active orders

Expert Advisor programs often need to enumerate existing active orders and analyze their properties. In particular, in the section on [pending order modifications](/en/book/automation/experts/experts_modify_order), in the example PendingOrderModify.mq5, we have created a special function GetMyOrder to find the orders belonging to the Expert Advisor in to modify this order. There, the analysis was carried out by symbol name and Expert Advisor ID (Magic). In theory, the same approach should have been applied in the example of deleting a pending order PendingOrderDelete.mq5 from the previous section.

In the latter case, for simplicity, we created an order and stored its ticket in a global variable. But this cannot be done in the general case because the Expert Advisor and the entire terminal can be stopped or restarted at any time. Therefore, the Expert Advisor must contain an algorithm for restoring the internal state, including the analysis of the entire trading environment, along with orders, deals, positions, account balance, and so on.

In this section, we will study the MQL5 functions for obtaining a list of active orders and selecting any of them in the trading environment, which makes it possible to read all its properties.

int OrdersTotal()

The OrdersTotal function returns the number of currently active orders. These include pending orders, as well as market orders that have not yet been executed. As a rule, a market order is executed promptly, and therefore it is not often possible to catch it in the active phase, but if there is not enough liquidity in the market, this can happen. As soon as the order is executed (a deal is concluded), it is transferred from the category of active ones to history. We will talk about working with order history in a separate section.

Please note that only orders can be active and historical. This significantly distinguishes orders from deals which are always created in history and from positions that exist only online. To restore the history of positions, you should analyze the [history of deals](/en/book/automation/experts/experts_history_select).

ulong OrderGetTicket(uint index)

The OrderGetTicket function returns the order ticket by its number in the list of orders in the terminal's trading environment. The index parameter must be between 0 and the OrdersTotal()-1 value inclusive. The way in which orders are organized is not regulated.

The OrderGetTicket function selects an order, that is, copies data about it to some internal cache so that the MQL program can read all its properties using the subsequent calls of the OrderGetDouble, OrderGetInteger, or OrderGetString function, which will be discussed in a [separate section](/en/book/automation/experts/experts_orderget_funcs).

The presence of such a cache indicates that the data received from it can become obsolete: the order may no longer exist or may have been modified (for example, it may have a different status, open price, Stop Loss or Take Profit levels and expiration). Therefore, to guarantee the receipt of relevant data about the order, it is recommended to call the OrderGetTicket function immediately prior to requesting the data. Here is how this is done in the example of PendingOrderModify.mq5.

```
ulong GetMyOrder(const string name, const ulong magic)
{
   for(int i = 0; i < OrdersTotal(); ++i)
   {
      ulong t = OrderGetTicket(i);
      if(OrderGetInteger(ORDER_MAGIC) == magic
      && OrderGetString(ORDER_SYMBOL) == name)
      {
         return t;
      }
   }
   return 0;
}

```

Each MQL program maintains its own cache (trading environment context), which includes the selected order. In the following sections, we will learn that in addition to orders, an MQL program can select positions and history fragments with deals and orders into the active context.

The OrderSelect function performs a similar selection of an order with copying of its data to the internal cache.

bool OrderSelect(ulong ticket)

The function checks for the presence of an order and prepares the possibility of further reading its properties. In this case, the order is specified not by a serial number but by a ticket which must be received by the MQL program earlier in one way or another, in particular, as a result of executing OrderSend/OrderSendAsync.

The function returns true in case of success. If false is received, it usually means that there is no order with the specified ticket. The most common reason for this is when order status has changed from active to history, for example, as a result of execution or cancellation (we will learn how to determine the exact status later). Orders can be selected in history using the [relevant functions](/en/book/automation/experts/experts_history_select).

Previously we used the OrderSelect function in the MqlTradeResultSync structure for tracking [creation](/en/book/automation/experts/experts_pending) and [removal](/en/book/automation/experts/experts_remove_order) of pending orders.
