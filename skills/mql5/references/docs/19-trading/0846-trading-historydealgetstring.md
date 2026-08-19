# HistoryDealGetString

Returns the requested property of a deal. The deal property must be of the string type. There are 2 variants of the function.

1. Immediately returns the property value.

```
string  HistoryDealGetString(
   ulong                      ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_STRING  property_id        // Property identifier
   );

```

2. Returns true or false, depending on the success of the function. If successful, the value of the property is placed into a target variable passed by reference by the last parameter.

```
bool  HistoryDealGetString(
   ulong                      ticket_number,     // Ticket
   ENUM_DEAL_PROPERTY_STRING  property_id,       // Property identifier
   string&                    string_var         // Here we accept the property value
   );

```

Parameters

ticket_number

[in]  Deal ticket.

property_id

[in]  Identifier of the deal property. The value can be one of the values of the [ENUM_DEAL_PROPERTY_STRING](/en/docs/constants/tradingconstants/dealproperties#enum_deal_property_string) enumeration.

string_var

[out]  Variable of the string type that accepts the value of the requested property.

Return Value

Value of the [string](/en/docs/basis/types/stringconst) type.

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
      PrintFormat("String properties of an deal %s entry %s #%I64u:", type, entry, ticket);
      
      //--- print all the real properties of the selected deal under the header
      HistoryDealPropertiesStringPrint(ticket, 13);
     }
   /*
   result:
   String properties of an deal Buy entry In #2785021084:
   Symbol:      EURUSD
   Comment:     Test PositionGetString
   Extarnal ID:
   String properties of an deal Buy entry Out #2497993663:
   Symbol:      EURUSD
   Comment:     [tp 1.08639]
   Extarnal ID: 
   */
  }
//+------------------------------------------------------------------+
//| Display string properties of the selected deal in the journal    |
//+------------------------------------------------------------------+
void HistoryDealPropertiesStringPrint(const ulong ticket, const uint header_width=0)
  {
   uint   w=0;
   string header="";
   string value ="";
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   header="Symbol:";
   w=(header_width==0 ? header.Length()+1 : header_width);
//--- get and display the deal symbol with the specified header width in the journal
   if(!HistoryDealGetString(ticket, DEAL_SYMBOL, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
   
//--- display the deal comment in the journal
   header="Comment:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetString(ticket, DEAL_COMMENT, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
   
//--- display the deal ID in an external trading system 
   header="Extarnal ID:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   if(!HistoryDealGetString(ticket, DEAL_EXTERNAL_ID, value))
      return;
   PrintFormat("%-*s%-s", w, header, value);
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

[HistoryDealsTotal()](/en/docs/trading/historydealstotal), [HistorySelect()](/en/docs/trading/historyselect), [HistoryDealGetTicket()](/en/docs/trading/historydealgetticket),  [Deal Properties](/en/docs/constants/tradingconstants/dealproperties)
