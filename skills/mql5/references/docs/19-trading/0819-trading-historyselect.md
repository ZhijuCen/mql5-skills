# HistorySelect

Retrieves the history of deals and orders for the specified period of server time.

```
bool  HistorySelect(
   datetime  from_date,     // From date
   datetime  to_date        // To date
   );

```

Parameters

from_date

[in]  Start date of the request.

to_date

[in]  End date of the request.

Return Value

It returns true if successful, otherwise returns false.

Note

HistorySelect() creates a list of orders and a list of trades in a mql5-program, for further referring to the list elements using corresponding functions. The deals list size can be returned using the [HistoryDealsTotal()](/en/docs/trading/historydealstotal) function; the size of the list of orders in the history can be obtained using [HistoryOrdersTotal()](/en/docs/trading/historyorderstotal). Selection in the list of orders should be better performed by [HistoryOrderGetTicket()](/en/docs/trading/historyordergetticket), for items in the list of deals [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket) suits better.

After using [HistoryOrderSelect()](/en/docs/trading/historyorderselect), the list of history orders available to the mql5 program is reset and filled again by the found order, if [the search of an order by the ticket](/en/docs/trading/historyorderselect) has been completed successfully. The same applies to the list of deals available to the mql5 program - it is reset by [HistoryDealSelect()](/en/docs/trading/historydealselect) and filled again in case of a successful receipt of a deal by ticket number.

Example:

```
void OnStart()
  {
   color BuyColor =clrBlue;
   color SellColor=clrRed;
//--- request trade history
   HistorySelect(0,TimeCurrent());
//--- create objects
   string   name;
   uint     total=HistoryDealsTotal();
   ulong    ticket=0;
   double   price;
   double   profit;
   datetime time;
   string   symbol;
   long     type;
   long     entry;
//--- for all deals
   for(uint i=0;i<total;i++)
     {
      //--- try to get deals ticket
      if((ticket=HistoryDealGetTicket(i))>0)
        {
         //--- get deals properties
         price =HistoryDealGetDouble(ticket,DEAL_PRICE);
         time  =(datetime)HistoryDealGetInteger(ticket,DEAL_TIME);
         symbol=HistoryDealGetString(ticket,DEAL_SYMBOL);
         type  =HistoryDealGetInteger(ticket,DEAL_TYPE);
         entry =HistoryDealGetInteger(ticket,DEAL_ENTRY);
         profit=HistoryDealGetDouble(ticket,DEAL_PROFIT);
         //--- only for current symbol
         if(price && time && symbol==Symbol())
           {
            //--- create price object
            name="TradeHistory_Deal_"+string(ticket);
            if(entry) ObjectCreate(0,name,OBJ_ARROW_RIGHT_PRICE,0,time,price,0,0);
            else      ObjectCreate(0,name,OBJ_ARROW_LEFT_PRICE,0,time,price,0,0);
            //--- set object properties
            ObjectSetInteger(0,name,OBJPROP_SELECTABLE,0);
            ObjectSetInteger(0,name,OBJPROP_BACK,0);
            ObjectSetInteger(0,name,OBJPROP_COLOR,type?BuyColor:SellColor);
            if(profit!=0) ObjectSetString(0,name,OBJPROP_TEXT,"Profit: "+string(profit));
           }
        }
     }
//--- apply on chart
   ChartRedraw();
  }

```

See also

[HistoryOrderSelect()](/en/docs/trading/historyorderselect), [HistoryDealSelect()](/en/docs/trading/historydealselect)
