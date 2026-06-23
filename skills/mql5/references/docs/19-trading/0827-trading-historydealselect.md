# HistoryDealSelect

Selects a deal in the history for further calling it through appropriate functions. It returns true if the function has been successfully completed. Returns false if the function has failed. For more details on error call [GetLastError()](/en/docs/check/getlasterror).

```
bool  HistoryDealSelect(
   ulong  ticket      // Deal ticket
   );

```

Parameters

ticket

[in]  Deal ticket.

Return Value

Returns true if successful, otherwise false.

Note

Do not confuse [orders](/en/docs/constants/tradingconstants/orderproperties), [deals](/en/docs/constants/tradingconstants/dealproperties) and [positions](/en/docs/constants/tradingconstants/positionproperties). Each deal is the result of the execution of an order, each position is the summary result of one or more deals.

HistoryDealSelect() clears in a mql5-program the list of deals available for reference, and copies the single deal, if the execution of HistoryDealSelect() has been completed successfully. If you need to go through all deals selected by the [HistorySelect()](/en/docs/trading/historyselect) function, you should better use [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket).

Example:

```
#define   TICKET    2620919264   // ticket of any known deal, for example, from the terminal account history
 
long      ExtTicket=TICKET;      // set the specified ticket to the variable from the macro substitution for the test in the script,
                                 // or handle deals in the OnTradeTransaction() handler in the EA:
//+------------------------------------------------------------------+
//| Expert TradeTransaction handler                                  |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
  {
   //--- if a transaction is adding a deal to history
   if(trans.type==TRADE_TRANSACTION_DEAL_ADD)
     {
      //--- select a deal by ticket, get its data and display the deal description in the journal
      HistoryDealSelectProcess(trans.deal);
     }
  }
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- select a deal by ticket, get its data and display the deal description in the journal
   HistoryDealSelectProcess(ExtTicket);
   /*
   result:
   (Position ID #2645974677) EURUSD Deal Out 0.10 Buy #2620919264 by order #2646028969 at 1.09178, 2024.07.15 18:16:32.570
   */
  }
//+------------------------------------------------------------------+
//| Select a deal by ticket and print the deal data in the journal   |
//+------------------------------------------------------------------+
void HistoryDealSelectProcess(const ulong deal_ticket)
  {
//--- select a historical deal by the ticket specified in deal_ticket
   ResetLastError();
   if(!HistoryDealSelect(deal_ticket))
     {
      PrintFormat("HistoryDealSelect(%I64u) failed. Error %d", deal_ticket, GetLastError());
      return;
     }
 
//--- if a deal is successfully selected, get its data and display the deal description in the journal
   ENUM_DEAL_TYPE    deal_type  = (ENUM_DEAL_TYPE)HistoryDealGetInteger(ExtTicket, DEAL_TYPE);
   ENUM_DEAL_ENTRY   deal_entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(ExtTicket, DEAL_ENTRY);
   ENUM_DEAL_REASON  deal_reason= (ENUM_DEAL_REASON)HistoryDealGetInteger(ExtTicket, DEAL_REASON);
   long              deal_time  = HistoryDealGetInteger(ExtTicket, DEAL_TIME_MSC);
   long              deal_order = HistoryDealGetInteger(ExtTicket, DEAL_ORDER);
   long              deal_pos_id= HistoryDealGetInteger(ExtTicket, DEAL_POSITION_ID);
   string            deal_symbol= HistoryDealGetString(ExtTicket, DEAL_SYMBOL);
   double            deal_volume= HistoryDealGetDouble(ExtTicket, DEAL_VOLUME);
   double            deal_price = HistoryDealGetDouble(ExtTicket, DEAL_PRICE);
   int               digits     = (int)SymbolInfoInteger(deal_symbol, SYMBOL_DIGITS);
   
   PrintFormat("(Position ID #%I64d) %s Deal %s %.2f %s #%I64u by order #%I64d at %.*f, %s",
               deal_pos_id, deal_symbol, DealEntryDescription(deal_entry), deal_volume,
               DealTypeDescription(deal_type), ExtTicket, deal_order, digits, deal_price,
               TimeMscToString(deal_time));
  }
//+------------------------------------------------------------------+
//| Return the deal type description                                 |
//+------------------------------------------------------------------+
string DealTypeDescription(const ENUM_DEAL_TYPE type)
  {
   switch(type)
     {
      case DEAL_TYPE_BUY                     :  return("Buy");
      case DEAL_TYPE_SELL                    :  return("Sell");
      case DEAL_TYPE_BALANCE                 :  return("Balance");
      case DEAL_TYPE_CREDIT                  :  return("Credit");
      case DEAL_TYPE_CHARGE                  :  return("Additional charge");
      case DEAL_TYPE_CORRECTION              :  return("Correction");
      case DEAL_TYPE_BONUS                   :  return("Bonus");
      case DEAL_TYPE_COMMISSION              :  return("Additional commission");
      case DEAL_TYPE_COMMISSION_DAILY        :  return("Daily commission");
      case DEAL_TYPE_COMMISSION_MONTHLY      :  return("Monthly commission");
      case DEAL_TYPE_COMMISSION_AGENT_DAILY  :  return("Daily agent commission");
      case DEAL_TYPE_COMMISSION_AGENT_MONTHLY:  return("Monthly agent commission");
      case DEAL_TYPE_INTEREST                :  return("Interest rate");
      case DEAL_TYPE_BUY_CANCELED            :  return("Canceled buy deal");
      case DEAL_TYPE_SELL_CANCELED           :  return("Canceled sell deal");
      case DEAL_DIVIDEND                     :  return("Dividend operations");
      case DEAL_DIVIDEND_FRANKED             :  return("Franked (non-taxable) dividend operations");
      case DEAL_TAX                          :  return("Tax charges");
      default                                :  return("Unknown deal type: "+(string)type);
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
      case DEAL_ENTRY_INOUT   :  return("Reverce");
      case DEAL_ENTRY_OUT_BY  :  return("Out by");
      case DEAL_ENTRY_STATE   :  return("Status record");
      default                 :  return("Unknown deal entry: "+(string)entry);
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

[HistorySelect()](/en/docs/trading/historyselect), [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket), [Deal Properties](/en/docs/constants/tradingconstants/dealproperties)
