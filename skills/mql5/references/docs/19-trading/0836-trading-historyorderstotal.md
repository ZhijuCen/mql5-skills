# HistoryOrdersTotal

Returns the number of orders in the history. Prior to calling HistoryOrdersTotal(), first it is necessary to receive the history of deals and orders using the [HistorySelect()](/en/docs/trading/historyselect) or [HistorySelectByPosition()](/en/docs/trading/historyselectbyposition) function.

```
int  HistoryOrdersTotal();

```

Return Value

Value of the [int](/en/docs/basis/types/integer/integertypes) type.

Note

Do not confuse orders of a trading history with current [pending orders](/en/docs/trading/orderstotal) that appear on the "Trade" tab of the "Toolbox" bar. The list of [orders](/en/docs/constants/tradingconstants/orderproperties) that were canceled or have led to a transaction, can be viewed in the "History" tab of "Toolbox" of the client terminal.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- request all the existing history on the account
   if(!HistorySelect(0, TimeCurrent()))
     {
      Print("HistorySelect() failed. Error ", GetLastError());
      return;
     }
 
//--- get the number of orders in the list and display it in the journal
   int total=HistoryOrdersTotal();
   Print("Number of historical orders on the account: ", total);
   /*
   result:
   Number of historical orders on the account: 496
   */
  }

```

See also

[HistorySelect()](/en/docs/trading/historyselect), [HistoryOrderSelect()](/en/docs/trading/historyorderselect), [HistoryOrderGetTicket()](/en/docs/trading/historyordergetticket), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
