# The Structure of a Trade Request Result (MqlTradeResult)

As result of a [trade request](/en/docs/constants/structures/mqltraderequest), a trade server returns data about the trade request processing result as a special predefined structure of MqlTradeResult type.

```
struct MqlTradeResult
  {
   uint     retcode;          // Operation return code
   ulong    deal;             // Deal ticket, if it is performed
   ulong    order;            // Order ticket, if it is placed
   double   volume;           // Deal volume, confirmed by broker
   double   price;            // Deal price, confirmed by broker
   double   bid;              // Current Bid price
   double   ask;              // Current Ask price
   string   comment;          // Broker comment to operation (by default it is filled by description of trade server return code)
   uint     request_id;       // Request ID set by the terminal during the dispatch 
   int      retcode_external; // Return code of an external trading system
  };

```

Fields description

| Field | Description |
| --- | --- |
| retcode | Return code  of a trade server |
| deal | Deal  ticket,  if a deal has been performed. It is available for a trade operation of  TRADE_ACTION_DEAL  type |
| order | Order  ticket, if a ticket has been placed. It is available for a trade operation of   TRADE_ACTION_PENDING  type |
| volume | Deal volume, confirmed by broker. It depends on the  order filling type |
| price | Deal price, confirmed by broker. It depends on the  deviation  field of the  trade request  and/or on the  trade operation |
| bid | The current market Bid price (requote price) |
| ask | The current market Ask price (requote price) |
| comment | The broker comment to operation (by default it is filled by description of trade server return code) |
| request_id | Request ID set by the terminal when sending to the trade server |
| retcode_external | The code of the error returned by an external trading system. The use and types of these errors depend on the broker and the external trading system, to which trading operations are sent. |

The trade operation result is returned to a variable of the MqlTradeResult type, which is passed as the second parameter to [OrderSend()](/en/docs/trading/ordersend) to perform [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions).

The terminal fixes [request](/en/docs/constants/structures/mqltraderequest) ID in request_id field when sending it to the trade server using [OrdersSend(](/en/docs/trading/ordersend)) and [OrderSendAsync()](/en/docs/trading/ordersendasync) functions. The terminal receives messages about performed transactions from the trade server and submits them for processing by [OnTradeTransaction()](/en/docs/event_handlers/ontradetransaction) function containing the following components as parameters:

- description of the trade transaction in [MqlTradeTransaction](/en/docs/constants/structures/mqltradetransaction) structure;
- description of the [trade request](/en/docs/constants/structures/mqltraderequest) sent from OrderSend() or OrdersSendAsync() function. Request ID is sent by the terminal to the trade server, while the request itself and its request_id are stored in the terminal memory;
- the trade request execution result as MqlTradeResult structure with request_id field containing ID of this request.

OnTradeTransaction() function receives three input parameters but the last two should be analyzed only for transactions having [TRADE_TRANSACTION_REQUEST](/en/docs/constants/structures/mqltradetransaction) type. In all other cases, data on the trade request and its execution result are not filled. Example of parameters analysis can be found at [Structure of a Trade Request](/en/docs/constants/structures/mqltradetransaction).

Setting request_id by the terminal for the trade request when sending it to the server is mainly introduced for working with OrderSendAsync() asynchronous function. This identifier allows to associate the performed action (OrderSend or OrderSendAsync functions call) with the result of this action sent to [OnTradeTransaction()](/en/docs/event_handlers/ontradetransaction).

Example:

```
//+------------------------------------------------------------------+
//| Sending a trade request with the result processing               |
//+------------------------------------------------------------------+
bool MyOrderSend(MqlTradeRequest request,MqlTradeResult result)
  {
//--- reset the last error code to zero
   ResetLastError();
//--- send request
   bool success=OrderSend(request,result);
//--- if the result fails - try to find out why
   if(!success)
     {
      int answer=result.retcode;
      Print("TradeLog: Trade request failed. Error = ",GetLastError());
      switch(answer)
        {
         //--- requote
         case 10004:
           {
            Print("TRADE_RETCODE_REQUOTE");
            Print("request.price = ",request.price,"   result.ask = ",
                  result.ask," result.bid = ",result.bid);
            break;
           }
         //--- order is not accepted by the server
         case 10006:
           {
            Print("TRADE_RETCODE_REJECT");
            Print("request.price = ",request.price,"   result.ask = ",
                  result.ask," result.bid = ",result.bid);
            break;
           }
         //--- invalid price
         case 10015:
           {
            Print("TRADE_RETCODE_INVALID_PRICE");
            Print("request.price = ",request.price,"   result.ask = ",
                  result.ask," result.bid = ",result.bid);
            break;
           }
         //--- invalid SL and/or TP
         case 10016:
           {
            Print("TRADE_RETCODE_INVALID_STOPS");
            Print("request.sl = ",request.sl," request.tp = ",request.tp);
            Print("result.ask = ",result.ask," result.bid = ",result.bid);
            break;
           }
         //--- invalid volume
         case 10014:
           {
            Print("TRADE_RETCODE_INVALID_VOLUME");
            Print("request.volume = ",request.volume,"   result.volume = ",
                  result.volume);
            break;
           }
         //--- not enough money for a trade operation 
         case 10019:
           {
            Print("TRADE_RETCODE_NO_MONEY");
            Print("request.volume = ",request.volume,"   result.volume = ",
                  result.volume,"   result.comment = ",result.comment);
            break;
           }
         //--- some other reason, output the server response code 
         default:
           {
            Print("Other answer = ",answer);
           }
        }
      //--- notify about the unsuccessful result of the trade request by returning false
      return(false);
     }
//--- OrderSend() returns true - repeat the answer
   return(true);
  }

```
