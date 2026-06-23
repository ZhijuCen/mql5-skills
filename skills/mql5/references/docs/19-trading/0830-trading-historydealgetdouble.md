# HistoryDealGetDouble

Returns the requested property of a deal. The deal property must be of the double type. There are 2 variants of the function.

1. Immediately returns the property value.

```
double  HistoryDealGetDouble(
   ulong                      ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_DOUBLE  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  HistoryDealGetDouble(
   ulong                      ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_DOUBLE  property_id,       // Property identifier
   double&                    double_var         // Here we accept the property value
   );

```

Parameters

ticket_number

[in]  Deal ticket.

property_id

[in]  Identifier of a deal property. The value can be one of the values of the [ENUM_DEAL_PROPERTY_DOUBLE](/en/docs/constants/tradingconstants/dealproperties#enum_deal_property_double) enumeration.

double_var

[out]  Variable of the double type that accepts the value of the requested property.

Return Value

Value of the [double](/en/docs/basis/types/double) type.

Note

Do not confuse [orders](/en/docs/constants/tradingconstants/orderproperties), [deals](/en/docs/constants/tradingconstants/dealproperties) and [positions](/en/docs/constants/tradingconstants/positionproperties). Each deal is the result of the execution of an order, each position is the summary result of one or more deals.

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
 
//--- in a loop by the list of deals in the account history
   int total=HistoryDealsTotal();
   for(int i=0; i<total; i++)
     {
      //--- get the ticket of the next deal (the deal is automatically selected to get its properties)
      ulong ticket=HistoryDealGetTicket(i);
      if(ticket==0)
         continue;
      
      //--- get the type and direction of the deal and display the header for the list of real properties of the selected deal
      string type=DealTypeDescription((ENUM_DEAL_TYPE)HistoryDealGetInteger(ticket, DEAL_TYPE));
      string entry=DealEntryDescription((ENUM_DEAL_ENTRY)HistoryDealGetInteger(ticket, DEAL_ENTRY));
      PrintFormat("Double properties of an deal %s entry %s #%I64u:", type, entry, ticket);
      
      //--- print all the real properties of the selected deal under the header
      HistoryDealPropertiesDoublePrint(ticket, 12);
     }
   /*
   real:
   Double properties of an deal Buy entry In #2785070622:
   Volume:     0.50
   Price:      1.10480
   Commission: 0.00
   Swap:       0.00
   Profit:     0.00 USD
   Fee:        0.00
   StopLoss:   0.00000
   TakeProfit: 0.00000
   Double properties of an deal Sell entry Out #2785071538:
   Volume:     0.50
   Price:      1.10491
   Commission: 0.00
   Swap:       0.00
   Profit:     5.50 USD
   Fee:        0.00
   StopLoss:   0.00000
   TakeProfit: 0.00000
   */
  }
//+------------------------------------------------------------------+
//| Display real properties of the selected deal in the journal      |
//+------------------------------------------------------------------+
void HistoryDealPropertiesDoublePrint(const ulong ticket, const uint header_width=0)
  {
   uint   w=0;
   string header="";
   double value=0;
   
//--- get the deal symbol, profit currency and the number of decimal places for the symbol
   string symbol  = HistoryDealGetString(ticket, DEAL_SYMBOL);
   string currency= SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
   int    digits  = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   header="Volume:";
   w=(header_width==0 ? header.Length()+1 : header_width);
//--- get and display the deal volume with the specified header width in the journal
   if(!HistoryDealGetDouble(ticket, DEAL_VOLUME, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the deal price in the journal
   header="Price:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_PRICE, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
   
//--- display the deal commission in the journal
   header="Commission:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_COMMISSION, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the accumulated swap in the journal when closing
   header="Swap:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_SWAP, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the deal financial result in the journal
   header="Profit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_PROFIT, value))
      return;
   PrintFormat("%-*s%-.2f %s", w, header, value, currency);
   
//--- display the deal fee in the journal
   header="Fee:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_FEE, value))
      return;
   PrintFormat("%-*s%-.2f", w, header, value);
   
//--- display the StopLoss level in the journal
   header="StopLoss:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_SL, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
 
//--- display the TakeProfit level in the journal
   header="TakeProfit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetDouble(ticket, DEAL_TP, value))
      return;
   PrintFormat("%-*s%-.*f", w, header, digits, value);
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

```

See also

[HistorySelect()](/en/docs/trading/historyselect), [HistoryDealsTotal()](/en/docs/trading/historydealstotal), [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket), [Deal Properties](/en/docs/constants/tradingconstants/dealproperties)
