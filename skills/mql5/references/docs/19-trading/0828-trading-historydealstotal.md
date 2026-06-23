# HistoryDealsTotal

Returns the number of deal in history. Prior to calling HistoryDealsTotal(), first it is necessary to receive the history of deals and orders using the [HistorySelect()](/en/docs/trading/historyselect) or [HistorySelectByPosition()](/en/docs/trading/historyselectbyposition) function.

```
int  HistoryDealsTotal();

```

Return Value

Value of the [int](/en/docs/basis/types/integer/integertypes) type.

Note

Do not confuse [orders](/en/docs/constants/tradingconstants/orderproperties), [deals](/en/docs/constants/tradingconstants/dealproperties) and [positions](/en/docs/constants/tradingconstants/positionproperties). Each deal is the result of the execution of an order, each position is the summary result of one or more deals.

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
 
//--- get the number of deals in the list and display it in the journal
   int total=HistoryDealsTotal();
   Print("Number of historical deals on the account: ", total);
   /*
   result:
   Number of historical deals on the account: 339
   */
  }

```

See also

[HistorySelect()](/en/docs/trading/historyselect), [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket), [Deal Properties](/en/docs/constants/tradingconstants/dealproperties)
