# HistorySelectByPosition

Retrieves the history of deals and orders having the specified position identifier.

```
bool  HistorySelectByPosition(
   ulong   position_id     // position identifier - POSITION_IDENTIFIER
   );

```

Parameters

position_id

[in]  Position identifier that is set to every executed order and every deal.

Return Value

It returns true if successful, otherwise returns false.

Note

Do not confuse orders of a trading history with current [pending orders](/en/docs/trading/orderstotal) that appear on the "Trade" tab of the "Toolbox" bar. The list of [orders](/en/docs/constants/tradingconstants/orderproperties) that were canceled or have led to a transaction, can be viewed in the "History" tab of "Toolbox" of the client terminal.

HistorySelectByPosition() creates in a mql5 program a list of orders and a list of deals with a specified [position identifier](/en/docs/constants/tradingconstants/positionproperties#enum_position_property_integer) for further reference to the elements of the list using the appropriate functions. To know the size of the list of deals, use function [HistoryDealsTotal()](/en/docs/trading/historydealstotal), the size of the list of orders in the history can be obtained using [HistoryOrdersTotal()](/en/docs/trading/historyorderstotal). To run through elements of the orders list, use [HistoryOrderGetTicket()](/en/docs/trading/historyordergetticket), for elements of the deals list - [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket).

After using [HistoryOrderSelect()](/en/docs/trading/historyorderselect), list of history orders available to the mql5 program is reset and filled again with the found order, if [search of an order by its ticket](/en/docs/trading/historyorderselect) was successful. The same refers to the list of deals available to the mql5 program - it is reset by function [HistoryDealSelect()](/en/docs/trading/historydealselect) and is filled out again if a deal was found successfully by the ticket number.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   long  pos_id_array[];         // array for storing position IDs
 
//--- request the entire history
   if(!HistorySelect(0, TimeCurrent()))
     {
      Print("HistorySelect() failed. Error ", GetLastError());
      return;
     }
     
//--- collect all Position IDs from pending orders only in the array
   int total=HistoryOrdersTotal();
   for(int i=0; i<total; i++)
     {
      ulong ticket=HistoryOrderGetTicket(i);
      if(ticket==0)
         continue;
      ENUM_ORDER_TYPE type=(ENUM_ORDER_TYPE)HistoryOrderGetInteger(ticket, ORDER_TYPE);
      long pos_id=HistoryOrderGetInteger(ticket, ORDER_POSITION_ID);
      if(type<=ORDER_TYPE_SELL || pos_id==0)
         continue;
      
      int size=ArraySize(pos_id_array);
      if(ArrayResize(pos_id_array, size+1)==size+1)
         pos_id_array[size]=pos_id;
     }
   
//--- by list of position IDs in the array
   total=ArraySize(pos_id_array);
   for(int i=0; i<total; i++)
     {
      //--- print the header, as well as the position order and deal list
      long position_id=pos_id_array[i];
      Print("List of orders and deals for position with ID: ", position_id);
      HistorySelectByPositionProcess(position_id);
     }
   /*
   result:
   List of orders and deals for position with ID: 1819629924
     [0] Order Sell Limit #1819629924
     [1] Order Buy #1819633194
     [0] Entry In Deal Sell #1794972472
     [1] Entry Out Deal Buy #1794975589
   List of orders and deals for position with ID: 1841753970
     [0] Order Sell Stop #1841753970
     [1] Order Buy #1842322160
     [0] Entry In Deal Sell #1817242142
     [1] Entry Out Deal Buy #1817765341
   */
  }
//+------------------------------------------------------------------+
//| Select history of orders and deals by position ID and            |
//| prints a list of orders and deals for the position in the journal|
//+------------------------------------------------------------------+
bool HistorySelectByPositionProcess(const long position_id)
  {
//--- request the history of deals and orders having the specified position ID
   if(!HistorySelectByPosition(position_id))
     {
      PrintFormat("HistorySelectByPosition(%I64d) failed. Error %d", position_id, GetLastError());
      return(false);
     }
     
//--- print a list of position orders
   int orders_total=HistoryOrdersTotal();
   for(int i=0; i<orders_total; i++)
     {
      ulong ticket=HistoryOrderGetTicket(i);
      if(ticket==0)
         continue;
      ENUM_ORDER_TYPE order_type=(ENUM_ORDER_TYPE)HistoryOrderGetInteger(ticket, ORDER_TYPE);
      PrintFormat("  [%d] Order %s #%I64u", i, OrderTypeDescription(order_type), ticket);
     }
     
//--- print a list of position deals in the journal
   int deals_total =HistoryDealsTotal();
   for(int i=0; i<deals_total; i++)
     {
      ulong ticket=HistoryDealGetTicket(i);
      if(ticket==0)
         continue;
      ENUM_DEAL_ENTRY deal_entry=(ENUM_DEAL_ENTRY)HistoryDealGetInteger(ticket, DEAL_ENTRY);
      ENUM_DEAL_TYPE  deal_type= (ENUM_DEAL_TYPE)HistoryDealGetInteger(ticket, DEAL_TYPE);
      if(deal_type!=DEAL_TYPE_BUY && deal_type!=DEAL_TYPE_SELL)
         continue;
      PrintFormat("  [%d] Entry %s Deal %s #%I64u", i, DealEntryDescription(deal_entry), DealTypeDescription(deal_type), ticket);
     }
   return(true);
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
//| Return the position deal type description                        |
//+------------------------------------------------------------------+
string DealTypeDescription(const ENUM_DEAL_TYPE type)
  {
   switch(type)
     {
      //--- return the description of the Buy and Sell deals only,
      //--- since all other types do not apply to the position
      case DEAL_TYPE_BUY   :  return("Buy");
      case DEAL_TYPE_SELL  :  return("Sell");
      default              :  return("Unknown deal type: "+(string)type);
     }
  }
//+------------------------------------------------------------------+
//| Return position change method                                    |
//+------------------------------------------------------------------+
string DealEntryDescription(const ENUM_DEAL_ENTRY entry)
  {
   switch(entry)
     {
      case DEAL_ENTRY_IN      :  return("In");
      case DEAL_ENTRY_OUT     :  return("Out");
      case DEAL_ENTRY_INOUT   :  return("InOut");
      case DEAL_ENTRY_OUT_BY  :  return("Out by");
      case DEAL_ENTRY_STATE   :  return("Status record");
      default                 :  return("Unknown deal entry: "+(string)entry);
     }
  }

```

See also

[HistorySelect()](/en/docs/trading/historyselect), [HistoryOrderGetTicket()](/en/docs/trading/historyordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
