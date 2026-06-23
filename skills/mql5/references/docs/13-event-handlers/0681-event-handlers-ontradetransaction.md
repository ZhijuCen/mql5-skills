# OnTradeTransaction

The function is called in EAs when the [TradeTransaction](/en/docs/runtime/event_fire#tradetransaction) event occurs. The function is meant for handling trade request execution results.

```
void  OnTradeTransaction()
   const MqlTradeTransaction&    trans,     // trade transaction structure
   const MqlTradeRequest&        request,   // request structure
   const MqlTradeResult&         result     // response structure
   );

```

Parameters

trans

[in]  [MqlTradeTransaction](/en/docs/constants/structures/mqltradetransaction) type variable describing a transaction made on a trading account.

request

[in]  [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type variable describing a trade request that led to a transaction. It contains the values for [TRADE_TRANSACTION_REQUEST](/en/docs/constants/tradingconstants/enum_trade_request_actions) type transaction only.

result

[in]  [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) type variable containing an execution result of a trade request that led to a transaction. It contains the values for [TRADE_TRANSACTION_REQUEST](/en/docs/constants/tradingconstants/enum_trade_request_actions) type transaction only.

Return Value

No return value

Note

OnTradeTransaction() is called to handle the [TradeTransaction](/en/docs/event_handlers/ontradetransaction) event sent by the trade server to the terminal in the following cases:

- sending a trade request from an MQL5 program using the [OrderSend()](/en/docs/trading/ordersend)/[OrderSendAsync()](/en/docs/trading/ordersendasync) functions and its subsequent execution;
- sending a trade request manually via the GUI and its subsequent execution;
- activations of pending and stop orders on the server;
- performing operations on the trade server side.

Data on transaction type is contained in the type field of the trans variable. Types of trade transactions are described in the [ENUM_TRADE_TRANSACTION_TYPE](/en/docs/constants/tradingconstants/enum_trade_transaction_type) enumeration:

- TRADE_TRANSACTION_ORDER_ADD – adding a new active order
- TRADE_TRANSACTION_ORDER_UPDATE – changing an existing order
- TRADE_TRANSACTION_ORDER_DELETE – deleting an order from the list of active ones
- TRADE_TRANSACTION_DEAL_ADD – adding a deal to history
- TRADE_TRANSACTION_DEAL_UPDATE – changing a deal in history
- TRADE_TRANSACTION_DEAL_DELETE – deleting a deal from history
- TRADE_TRANSACTION_HISTORY_ADD – adding an order to history as a result of execution or cancelation
- TRADE_TRANSACTION_HISTORY_UPDATE – changing an order in the order history
- TRADE_TRANSACTION_HISTORY_DELETE – deleting an order from the order history
- TRADE_TRANSACTION_POSITION – position change not related to a trade execution
- TRADE_TRANSACTION_REQUEST – notification that a trade request has been processed by the server and the result of its processing has been received.

When handling transactions of TRADE_TRANSACTION_REQUEST type, it is necessary to analyze the second and third parameters of the OnTradeTransaction() function – request and result – to receive additional information.

Sending a buy trade request leads to a chain of trade transactions on a trading account: 1) request is accepted for processing, 2) an appropriate purchase order is created for the account, 3) the order is then executed, 4) the executed order is removed from the list of active ones, 5) adding to the history of orders, 6) the subsequent transaction is added to history and 7) a new position is created. All these stages are [trade transactions](/en/docs/constants/tradingconstants/enum_trade_transaction_type). The arrival of each such transaction to the terminal is the [TradeTransaction](/en/docs/event_handlers/ontradetransaction) event. Priority of these transactions' arrival at the terminal is not guaranteed. Thus, you should not expect that one group of transactions will arrive after another one when developing your trading algorithm.

When transactions are processed by the EA's OnTradeTransaction() handler, the terminal goes on handling the incoming trade transactions. Thus, the trading account status may change at the course of OnTradeTransaction() operation. For example, while an MQL5 program handles adding a new order, it can be executed, deleted from the list of open orders and moved to history. The program is notified of all these events.

Transactions queue length comprises 1024 elements. If OnTradeTransaction() handles yet another transaction for too long, the previous ones can be superseded by new transactions in the queue.

[OnTrade()](/en/docs/event_handlers/ontrade) handler is called after the appropriate OnTradeTransaction() calls. In general, there is no exact correlation in the number of OnTrade () and OnTradeTransaction () calls. One OnTrade() call corresponds to one or several OnTradeTransaction calls.

Each [Trade](/en/docs/runtime/event_fire#trade) event may appear as a result of one or several trade requests. Trade requests are sent to the server using [OrderSend()](/en/docs/trading/ordersend) or [OrderSendAsync()](/en/docs/trading/ordersendasync). Each request can lead to several trade events. You cannot rely on the statement "One request - one Trade event", since the processing of events may be performed in several stages and each operation may change the state of orders, positions and the trade history.

Sample EA with OnTradeTransaction() handler

```
//+------------------------------------------------------------------+
//|                                    OnTradeTransaction_Sample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Sample listener of TradeTransaction events"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   PrintFormat("LAST PING=%.f ms",
               TerminalInfoInteger(TERMINAL_PING_LAST)/1000.);
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
 
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
  {
//---
   static int counter=0;   // counter of OnTradeTransaction() calls
   static uint lasttime=0; // time of the OnTradeTransaction() last call
//---
   uint time=GetTickCount();
//--- if the last transaction was performed more than 1 second ago,
   if(time-lasttime>1000)
     {
      counter=0; // then this is a new trade operation, an the counter can be reset
      if(IS_DEBUG_MODE)
         Print(" New trade operation");
     }
   lasttime=time;
   counter++;
   Print(counter,". ",__FUNCTION__);
//--- result of trade request execution
   ulong            lastOrderID   =trans.order;
   ENUM_ORDER_TYPE  lastOrderType =trans.order_type;
   ENUM_ORDER_STATE lastOrderState=trans.order_state;
//--- the name of the symbol, for which a transaction was performed
   string trans_symbol=trans.symbol;
//--- type of transaction
   ENUM_TRADE_TRANSACTION_TYPE  trans_type=trans.type;
   switch(trans.type)
     {
      case  TRADE_TRANSACTION_POSITION:   // position modification
        {
         ulong pos_ID=trans.position;
         PrintFormat("MqlTradeTransaction: Position  #%I64u %s modified: SL=%.5f TP=%.5f",
                     pos_ID,trans_symbol,trans.price_sl,trans.price_tp);
        }
      break;
      case TRADE_TRANSACTION_REQUEST:     // sending a trade request
         PrintFormat("MqlTradeTransaction: TRADE_TRANSACTION_REQUEST");
         break;
      case TRADE_TRANSACTION_DEAL_ADD:    // adding a trade
        {
         ulong          lastDealID   =trans.deal;
         ENUM_DEAL_TYPE lastDealType =trans.deal_type;
         double        lastDealVolume=trans.volume;
         //--- Trade ID in an external system - a ticket assigned by an exchange
         string Exchange_ticket="";
         if(HistoryDealSelect(lastDealID))
            Exchange_ticket=HistoryDealGetString(lastDealID,DEAL_EXTERNAL_ID);
         if(Exchange_ticket!="")
            Exchange_ticket=StringFormat("(Exchange deal=%s)",Exchange_ticket);
 
         PrintFormat("MqlTradeTransaction: %s deal #%I64u %s %s %.2f lot   %s",EnumToString(trans_type),
                     lastDealID,EnumToString(lastDealType),trans_symbol,lastDealVolume,Exchange_ticket);
        }
      break;
      case TRADE_TRANSACTION_HISTORY_ADD: // adding an order to the history
        {
         //--- order ID in an external system - a ticket assigned by an Exchange
         string Exchange_ticket="";
         if(lastOrderState==ORDER_STATE_FILLED)
           {
            if(HistoryOrderSelect(lastOrderID))
               Exchange_ticket=HistoryOrderGetString(lastOrderID,ORDER_EXTERNAL_ID);
            if(Exchange_ticket!="")
               Exchange_ticket=StringFormat("(Exchange ticket=%s)",Exchange_ticket);
           }
         PrintFormat("MqlTradeTransaction: %s order #%I64u %s %s %s   %s",EnumToString(trans_type),
                     lastOrderID,EnumToString(lastOrderType),trans_symbol,EnumToString(lastOrderState),Exchange_ticket);
        }
      break;
      default: // other transactions  
        {
         //--- order ID in an external system - a ticket assigned by Exchange
         string Exchange_ticket="";
         if(lastOrderState==ORDER_STATE_PLACED)
           {
            if(OrderSelect(lastOrderID))
               Exchange_ticket=OrderGetString(ORDER_EXTERNAL_ID);
            if(Exchange_ticket!="")
               Exchange_ticket=StringFormat("Exchange ticket=%s",Exchange_ticket);
           }
         PrintFormat("MqlTradeTransaction: %s order #%I64u %s %s   %s",EnumToString(trans_type),
                     lastOrderID,EnumToString(lastOrderType),EnumToString(lastOrderState),Exchange_ticket);
        }
      break;
     }
//--- order ticket    
   ulong orderID_result=result.order;
   string retcode_result=GetRetcodeID(result.retcode);
   if(orderID_result!=0)
      PrintFormat("MqlTradeResult: order #%d retcode=%s ",orderID_result,retcode_result);
//---   
  }
//+------------------------------------------------------------------+
//| convert numeric response codes to string mnemonics               |
//+------------------------------------------------------------------+
string GetRetcodeID(int retcode)
  {
   switch(retcode)
     {
      case 10004: return("TRADE_RETCODE_REQUOTE");             break;
      case 10006: return("TRADE_RETCODE_REJECT");              break;
      case 10007: return("TRADE_RETCODE_CANCEL");              break;
      case 10008: return("TRADE_RETCODE_PLACED");              break;
      case 10009: return("TRADE_RETCODE_DONE");                break;
      case 10010: return("TRADE_RETCODE_DONE_PARTIAL");        break;
      case 10011: return("TRADE_RETCODE_ERROR");               break;
      case 10012: return("TRADE_RETCODE_TIMEOUT");             break;
      case 10013: return("TRADE_RETCODE_INVALID");             break;
      case 10014: return("TRADE_RETCODE_INVALID_VOLUME");      break;
      case 10015: return("TRADE_RETCODE_INVALID_PRICE");       break;
      case 10016: return("TRADE_RETCODE_INVALID_STOPS");       break;
      case 10017: return("TRADE_RETCODE_TRADE_DISABLED");      break;
      case 10018: return("TRADE_RETCODE_MARKET_CLOSED");       break;
      case 10019: return("TRADE_RETCODE_NO_MONEY");            break;
      case 10020: return("TRADE_RETCODE_PRICE_CHANGED");       break;
      case 10021: return("TRADE_RETCODE_PRICE_OFF");           break;
      case 10022: return("TRADE_RETCODE_INVALID_EXPIRATION");  break;
      case 10023: return("TRADE_RETCODE_ORDER_CHANGED");       break;
      case 10024: return("TRADE_RETCODE_TOO_MANY_REQUESTS");   break;
      case 10025: return("TRADE_RETCODE_NO_CHANGES");          break;
      case 10026: return("TRADE_RETCODE_SERVER_DISABLES_AT");  break;
      case 10027: return("TRADE_RETCODE_CLIENT_DISABLES_AT");  break;
      case 10028: return("TRADE_RETCODE_LOCKED");              break;
      case 10029: return("TRADE_RETCODE_FROZEN");              break;
      case 10030: return("TRADE_RETCODE_INVALID_FILL");        break;
      case 10031: return("TRADE_RETCODE_CONNECTION");          break;
      case 10032: return("TRADE_RETCODE_ONLY_REAL");           break;
      case 10033: return("TRADE_RETCODE_LIMIT_ORDERS");        break;
      case 10034: return("TRADE_RETCODE_LIMIT_VOLUME");        break;
      case 10035: return("TRADE_RETCODE_INVALID_ORDER");       break;
      case 10036: return("TRADE_RETCODE_POSITION_CLOSED");     break;
      default:
         return("TRADE_RETCODE_UNKNOWN="+IntegerToString(retcode));
         break;
     }
//---
  }

```

See also

[OrderSend](/en/docs/trading/ordersend), [OrderSendAsync](/en/docs/trading/ordersendasync), [OnTradeTransaction](/en/docs/event_handlers/ontradetransaction), [Trade request structure](/en/docs/constants/structures/mqltraderequest), [Trade transaction structure](/en/docs/constants/structures/mqltradetransaction), [Trade transaction types](/en/docs/constants/tradingconstants/enum_trade_transaction_type), [Trade operation types](/en/docs/constants/tradingconstants/enum_trade_request_actions), [Client terminal events](/en/docs/runtime/event_fire)
