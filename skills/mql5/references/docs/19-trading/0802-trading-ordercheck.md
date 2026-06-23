# OrderCheck

The OrderCheck() function checks if there are enough money to execute a required [trade operation](/en/docs/constants/tradingconstants/enum_trade_request_actions). The check results are placed to the fields of the [MqlTradeCheckResult](/en/docs/constants/structures/mqltradecheckresult) structure.

```
bool  OrderCheck(
   MqlTradeRequest&       request,      // request structure
   MqlTradeCheckResult&   result        // result structure
   );

```

Parameters

request

[in]  Pointer to the structure of the [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type, which describes the required trade action.

result

[in,out]  Pointer to the structure of the [MqlTradeCheckResult](/en/docs/constants/structures/mqltradecheckresult) type, to which the check result will be placed.

Return Value

If funds are not enough for the operation, or parameters are filled out incorrectly, the function returns false. In case of a successful basic check of structures (check of pointers), it returns true. However, this is not an indication that the requested trade operation is sure to be successfully executed. For a more detailed description of the function execution result, analyze the fields of the result structure.

In order to obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
#define   DEVIATION     5              // allowed deviation from the price
#define   VOLUME        1.0            // order volume
#define   EXPERT_MAGIC  123            // MagicNumber
#define   DIRECTION     ORDER_TYPE_BUY // opened position direction (ORDER_TYPE_BUY or ORDER_TYPE_SELL)
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the request, verification and result structures
   MqlTradeRequest     request={};
   MqlTradeCheckResult check  ={};
   MqlTradeResult      result ={};
   
//--- prepare trade request parameters
   PrepareRequest(_Symbol, DIRECTION, VOLUME, request);
   
//--- check trade request parameters
   ResetLastError();
   bool res=OrderCheck(request, check);
   if(!res)
     {
      PrintFormat("Trade request verification completed with error %d\nServer retcode: %u, comment: %s", GetLastError(), check.retcode, check.comment);
      return;
     }
     
//--- trade request check was successful - display the description of the trade request verification structure fields
   Print("Trade request verification completed successfully");
   MqlTradeCheckResultPrint(check, 14);
   
//--- send a trade request
   if(!OrderSend(request, result))
      Print("OrderSend error ", GetLastError());    // if unable to send the request, display the error code
      
//--- information about the operation
   PrintFormat("Trade request result: retcode=%u, deal=%I64u, order=%I64u", result.retcode, result.deal, result.order);
   /*
   result with disabled auto trading in the client terminal:
   Trade request verification completed with error 4752
   Server retcode: 10027, comment: AutoTrading disabled by client
   
   enable auto trading and check again on a closed market:
   Experts   automated trading is enabled
   Trade request verification completed successfully
   Retcode:      0
   Balance:      10779.50 USD
   Equity:       10779.50 USD
   Profit:       0.00 USD
   Margin:       1104.79 USD
   Margin free:  9674.71 USD
   Margin level: 975.71 %
   Comment:      Done
   OrderSend error 4756
   Trade request result: retcode=10018, deal=0, order=0
   
   check on the open market:
   Trade request verification completed successfully
   Retcode:      0
   Balance:      10779.50 USD
   Equity:       10779.50 USD
   Profit:       0.00 USD
   Margin:       110.46 USD
   Margin free:  10669.04 USD
   Margin level: 9758.74 %
   Comment:      Done
   Trade request result: retcode=10009, deal=2777010968, order=2802818813
   */
  }
//+------------------------------------------------------------------+
//| Prepare parameters for a trade request                           |
//+------------------------------------------------------------------+
void PrepareRequest(const string symbol, const ENUM_ORDER_TYPE order_type, const double volume, MqlTradeRequest &request)
  {
   ENUM_ORDER_TYPE type=(DIRECTION !=ORDER_TYPE_BUY ? ORDER_TYPE_SELL : DIRECTION);
   double price=(DIRECTION==ORDER_TYPE_BUY ? SymbolInfoDouble(Symbol(), SYMBOL_ASK) : SymbolInfoDouble(Symbol(), SYMBOL_BID));
//--- request parameters
   request.action    = TRADE_ACTION_DEAL; // trading operation type
   request.symbol    = symbol;            // symbol
   request.volume    = volume;            // volume
   request.type      = type;              // order type
   request.price     = price;             // open price
   request.deviation = DEVIATION;         // allowed deviation from the price
   request.magic     = EXPERT_MAGIC;      // order MagicNumber
  }
//+------------------------------------------------------------------+
//| Print the fields of the trade request                            |
//| verification result in the journal                               |
//+------------------------------------------------------------------+
void MqlTradeCheckResultPrint(const MqlTradeCheckResult &check, const uint header_width=0)
  {
//--- get the account currency and the number of decimal places for the account currency
   string currency=AccountInfoString(ACCOUNT_CURRENCY);
   int    digits  =(int)AccountInfoInteger(ACCOUNT_CURRENCY_DIGITS);
   
//--- define the header text and the width of the header field
//--- if the header width is passed to the function equal to zero, then the width will be the size of the header line + 1
   string header="Retcode:";
   uint w=(header_width==0 ? header.Length()+1 : header_width);
//--- display the return code with the header of the specified width in the journal
   PrintFormat("%-*s%-u", w, header, check.retcode);
   
//--- display the balance value after executing a trade operation in the journal
   header="Balance:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.*f %s", w, header, digits, check.balance, currency);
   
//--- display the equity value after executing a trade operation in the journal
   header="Equity:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.*f %s", w, header, digits, check.equity, currency);
      
//--- display the floating profit value after executing a trading operation in the journal
   header="Profit:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.*f %s", w, header, digits, check.profit, currency);      
      
//--- display the amount of margin, required for the necessary trading operation, in the journal
   header="Margin:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.*f %s", w, header, digits, check.margin, currency);      
      
//--- display the value of equity to be left after conducting a trading operation in the journal
   header="Margin free:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.*f %s", w, header, digits, check.margin_free, currency);      
      
//--- display the margin level to be set after completing the required trading operation in the journal
   header="Margin level:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-.2f %%", w, header, check.margin_level);      
      
//--- display the comment on the response code and error description in the journal
   header="Comment:";
   w=(header_width==0 ? header.Length()+1 : header_width);
   PrintFormat("%-*s%-s", w, header, check.comment);      
  }

```

See also

[OrderSend()](/en/docs/trading/ordersend), [Trade Operation Types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Trade Request Structure](/en/docs/constants/structures/mqltraderequest), [Structure of Request Check Results](/en/docs/constants/structures/mqltradecheckresult), [Structure of a Trade Request Result](/en/docs/constants/structures/mqltraderesult)
