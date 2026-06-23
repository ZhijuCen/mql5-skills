# The Trade Request Structure (MqlTradeRequest)

Interaction between the client terminal and a trade server for executing the order placing operation is performed by using trade requests. The trade request is represented by the special predefined [structure](/en/docs/basis/types/classes) of MqlTradeRequest type, which contain all the fields necessary to perform trade deals. The request processing result is represented by the structure of [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) type.

```
struct MqlTradeRequest
  {
   ENUM_TRADE_REQUEST_ACTIONS    action;           // Trade operation type
   ulong                         magic;            // Expert Advisor ID (magic number)
   ulong                         order;            // Order ticket
   string                        symbol;           // Trade symbol
   double                        volume;           // Requested volume for a deal in lots
   double                        price;            // Price
   double                        stoplimit;        // StopLimit level of the order
   double                        sl;               // Stop Loss level of the order
   double                        tp;               // Take Profit level of the order
   ulong                         deviation;        // Maximal possible deviation from the requested price
   ENUM_ORDER_TYPE               type;             // Order type
   ENUM_ORDER_TYPE_FILLING       type_filling;     // Order execution type
   ENUM_ORDER_TYPE_TIME          type_time;        // Order expiration type
   datetime                      expiration;       // Order expiration time (for the orders of ORDER_TIME_SPECIFIED type)
   string                        comment;          // Order comment
   ulong                         position;         // Position ticket
   ulong                         position_by;      // The ticket of an opposite position
  };

```

Fields description

| Field | Description |
| --- | --- |
| action | Trade operation type. Can be one of the  ENUM_TRADE_REQUEST_ACTIONS  enumeration values. |
| magic | Expert Advisor ID. It allows organizing analytical processing of trade orders. Each Expert Advisor can set its own unique ID when sending a trade request. |
| order | Order ticket. It is used for modifying pending orders. |
| symbol | Symbol of the order. It is not necessary for order modification and position close operations. |
| volume | Requested order volume in lots. Note that the real volume of a deal will depend on the  order execution type . |
| price | Price, reaching which the order must be executed. Market orders of symbols, whose execution type is "Market Execution" ( SYMBOL_TRADE_EXECUTION_MARKET ), of  TRADE_ACTION_DEAL  type , do not require specification of price. |
| stoplimit | The price value, at which the Limit pending order will be placed, when price reaches the  price  value  (this condition is obligatory). Until then the pending order is not placed. |
| sl | Stop Loss price in case of the unfavorable price movement |
| tp | Take Profit price in the case of the favorable price movement |
| deviation | The maximal price deviation, specified in  points |
| type | Order type. Can be one of the  ENUM_ORDER_TYPE  enumeration values. |
| type_filling | Order execution type. Can be one of the enumeration  ENUM_ORDER_TYPE_FILLING  values. |
| type_time | Order expiration type. Can be one of the enumeration  ENUM_ORDER_TYPE_TIME  values. |
| expiration | Order expiration time (for orders of  ORDER_TIME_SPECIFIED  type ) |
| comment | Order comment |
| position | Ticket of a position. Should be filled in when a position is modified or closed to identify the position. As a rule it is equal to the ticket of the order, based on which the position was opened. |
| position_by | Ticket of an opposite position. Used when a position is closed by an opposite one open for the same symbol in the opposite direction. |

```
When modifying or closing a position in the hedging system, make sure to specify its ticket (MqlTradeRequest::position). The ticket can also be specified in the netting system, though a position is identified by the symbol name.

```

For sending orders to perform [trade operations](/en/docs/constants/tradingconstants/enum_trade_request_actions) it is necessary to use the [OrderSend()](/en/docs/trading/ordersend) function. For each trade operation it is necessary to specify obligatory fields; optional fields also may be filled. There are seven possible cases to send a trade order:

Request Execution

This is a trade order to open a position in the Request Execution mode (trade upon requested prices). It requires to specify the following 9 fields:

- action
- symbol
- volume
- price
- sl
- tp
- deviation
- type
- type_filling

Also it is possible to specify the "magic" and "comment" field values.

Instant Execution

This is a trade order to open a position in the Instant Execution mode (trade by current prices). It requires specification of the following 9 fields:

- action
- symbol
- volume
- price
- sl
- tp
- deviation
- type
- type_filling

Also it is possible to specify the "magic" and "comment" field values.

Market Execution

This is a trade order to open a position in the Market Execution mode. It requires to specify the following 5 fields:

- action
- symbol
- volume
- type
- type_filling

Also it is possible to specify the "magic" and "comment" field values.

Exchange Execution

This is a trade order to open a position in the Exchange Execution mode. It requires to specify the following 5 fields:

- action
- symbol
- volume
- type
- type_filling

Also it is possible to specify the "magic" and "comment" field values.

Example of the TRADE_ACTION_DEAL trade operation for opening a Buy position:

```
#define EXPERT_MAGIC 123456   // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Opening Buy position                                             |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};
//--- parameters of request
   request.action   =TRADE_ACTION_DEAL;                     // type of trade operation
   request.symbol   =Symbol();                              // symbol
   request.volume   =0.1;                                   // volume of 0.1 lot
   request.type     =ORDER_TYPE_BUY;                        // order type
   request.price    =SymbolInfoDouble(Symbol(),SYMBOL_ASK); // price for opening
   request.deviation=5;                                     // allowed deviation from the price
   request.magic    =EXPERT_MAGIC;                          // MagicNumber of the order
//--- send the request
   if(!OrderSend(request,result))
      PrintFormat("OrderSend error %d",GetLastError());     // if unable to send the request, output the error code
//--- information about the operation
   PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
  }
//+------------------------------------------------------------------+

```

Example of the TRADE_ACTION_DEAL trade operation for opening a Sell position:

```
#define EXPERT_MAGIC 123456   // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Opening Sell position                                            |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};
//--- parameters of request
   request.action   =TRADE_ACTION_DEAL;                     // type of trade operation
   request.symbol   =Symbol();                              // symbol
   request.volume   =0.2;                                   // volume of 0.2 lot
   request.type     =ORDER_TYPE_SELL;                       // order type
   request.price    =SymbolInfoDouble(Symbol(),SYMBOL_BID); // price for opening
   request.deviation=5;                                     // allowed deviation from the price
   request.magic    =EXPERT_MAGIC;                          // MagicNumber of the order
//--- send the request
   if(!OrderSend(request,result))
      PrintFormat("OrderSend error %d",GetLastError());     // if unable to send the request, output the error code
//--- information about the operation
   PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
  }
//+------------------------------------------------------------------+

```

Example of the TRADE_ACTION_DEAL trade operation for closing positions:

```
#define EXPERT_MAGIC 123456   // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Closing all positions                                            |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request;
   MqlTradeResult  result;
   int total=PositionsTotal(); // number of open positions   
//--- iterate over all open positions
   for(int i=total-1; i>=0; i--)
     {
      //--- parameters of the order
      ulong  position_ticket=PositionGetTicket(i);                                      // ticket of the position
      string position_symbol=PositionGetString(POSITION_SYMBOL);                        // symbol 
      int    digits=(int)SymbolInfoInteger(position_symbol,SYMBOL_DIGITS);              // number of decimal places
      ulong  magic=PositionGetInteger(POSITION_MAGIC);                                  // MagicNumber of the position
      double volume=PositionGetDouble(POSITION_VOLUME);                                 // volume of the position
      ENUM_POSITION_TYPE type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);    // type of the position
      //--- output information about the position
      PrintFormat("#%I64u %s  %s  %.2f  %s [%I64d]",
                  position_ticket,
                  position_symbol,
                  EnumToString(type),
                  volume,
                  DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                  magic);
      //--- if the MagicNumber matches
      if(magic==EXPERT_MAGIC)
        {
         //--- zeroing the request and result values
         ZeroMemory(request);
         ZeroMemory(result);
         //--- setting the operation parameters
         request.action   =TRADE_ACTION_DEAL;        // type of trade operation
         request.position =position_ticket;          // ticket of the position
         request.symbol   =position_symbol;          // symbol 
         request.volume   =volume;                   // volume of the position
         request.deviation=5;                        // allowed deviation from the price
         request.magic    =EXPERT_MAGIC;             // MagicNumber of the position
         //--- set the price and order type depending on the position type
         if(type==POSITION_TYPE_BUY)
           {
            request.price=SymbolInfoDouble(position_symbol,SYMBOL_BID);
            request.type =ORDER_TYPE_SELL;
           }
         else
           {
            request.price=SymbolInfoDouble(position_symbol,SYMBOL_ASK);
            request.type =ORDER_TYPE_BUY;
           }
         //--- output information about the closure
         PrintFormat("Close #%I64d %s %s",position_ticket,position_symbol,EnumToString(type));
         //--- send the request
         if(!OrderSend(request,result))
            PrintFormat("OrderSend error %d",GetLastError());  // if unable to send the request, output the error code
         //--- information about the operation   
         PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
         //---
        }
     }
  }
//+------------------------------------------------------------------+

```

SL & TP Modification

Trade order to modify the StopLoss and/or TakeProfit price levels. It requires to specify the following 4 fields:

- action
- symbol
- sl
- tp
- position

Example of the TRADE_ACTION_SLTP trade operation for modifying the Stop Loss and Take Profit values of an open position:

```
#define EXPERT_MAGIC 123456  // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Modification of Stop Loss and Take Profit of position            |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request;
   MqlTradeResult  result;
   int total=PositionsTotal(); // number of open positions   
//--- iterate over all open positions
   for(int i=0; i<total; i++)
     {
      //--- parameters of the order
      ulong  position_ticket=PositionGetTicket(i);// ticket of the position
      string position_symbol=PositionGetString(POSITION_SYMBOL); // symbol 
      int    digits=(int)SymbolInfoInteger(position_symbol,SYMBOL_DIGITS); // number of decimal places
      ulong  magic=PositionGetInteger(POSITION_MAGIC); // MagicNumber of the position
      double volume=PositionGetDouble(POSITION_VOLUME);    // volume of the position
      double sl=PositionGetDouble(POSITION_SL);  // Stop Loss of the position
      double tp=PositionGetDouble(POSITION_TP);  // Take Profit of the position
      ENUM_POSITION_TYPE type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);  // type of the position
      //--- output information about the position
      PrintFormat("#%I64u %s  %s  %.2f  %s  sl: %s  tp: %s  [%I64d]",
                  position_ticket,
                  position_symbol,
                  EnumToString(type),
                  volume,
                  DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                  DoubleToString(sl,digits),
                  DoubleToString(tp,digits),
                  magic);
      //--- if the MagicNumber matches, Stop Loss and Take Profit are not defined
      if(magic==EXPERT_MAGIC && sl==0 && tp==0)
        {
         //--- calculate the current price levels
         double price=PositionGetDouble(POSITION_PRICE_OPEN);
         double bid=SymbolInfoDouble(position_symbol,SYMBOL_BID);
         double ask=SymbolInfoDouble(position_symbol,SYMBOL_ASK);
         int    stop_level=(int)SymbolInfoInteger(position_symbol,SYMBOL_TRADE_STOPS_LEVEL);
         double price_level;
         //--- if the minimum allowed offset distance in points from the current close price is not set
         if(stop_level<=0)
            stop_level=150; // set the offset distance of 150 points from the current close price
         else
            stop_level+=50; // set the offset distance to (SYMBOL_TRADE_STOPS_LEVEL + 50) points for reliability
 
         //--- calculation and rounding of the Stop Loss and Take Profit values
         price_level=stop_level*SymbolInfoDouble(position_symbol,SYMBOL_POINT);
         if(type==POSITION_TYPE_BUY)
           {
            sl=NormalizeDouble(bid-price_level,digits);
            tp=NormalizeDouble(bid+price_level,digits);
           }
         else
           {
            sl=NormalizeDouble(ask+price_level,digits);
            tp=NormalizeDouble(ask-price_level,digits);
           }
         //--- zeroing the request and result values
         ZeroMemory(request);
         ZeroMemory(result);
         //--- setting the operation parameters
         request.action  =TRADE_ACTION_SLTP; // type of trade operation
         request.position=position_ticket;   // ticket of the position
         request.symbol=position_symbol;     // symbol 
         request.sl      =sl;                // Stop Loss of the position
         request.tp      =tp;                // Take Profit of the position
         request.magic=EXPERT_MAGIC;         // MagicNumber of the position
         //--- output information about the modification
         PrintFormat("Modify #%I64d %s %s",position_ticket,position_symbol,EnumToString(type));
         //--- send the request
         if(!OrderSend(request,result))
            PrintFormat("OrderSend error %d",GetLastError());  // if unable to send the request, output the error code
         //--- information about the operation   
         PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
        }
     }
  }
//+------------------------------------------------------------------+

```

Pending Order

Trade order to place a pending order. It requires to specify the following 11 fields:

- action
- symbol
- volume
- price
- stoplimit
- sl
- tp
- type
- type_filling
- type_time
- expiration

Also it is possible to specify the "magic" and "comment" field values.

Example of the TRADE_ACTION_PENDING trade operation for placing a pending order:

```
#property description "Example of placing pending orders"
#property script_show_inputs
#define EXPERT_MAGIC 123456                             // MagicNumber of the expert
input ENUM_ORDER_TYPE orderType=ORDER_TYPE_BUY_LIMIT;   // order type
//+------------------------------------------------------------------+
//| Placing pending orders                                           |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};
//--- parameters to place a pending order
   request.action   =TRADE_ACTION_PENDING;                             // type of trade operation
   request.symbol   =Symbol();                                         // symbol
   request.volume   =0.1;                                              // volume of 0.1 lot
   request.deviation=2;                                                // allowed deviation from the price
   request.magic    =EXPERT_MAGIC;                                     // MagicNumber of the order
   int offset = 50;                                                    // offset from the current price to place the order, in points
   double price;                                                       // order triggering price
   double point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);                // value of point
   int digits=SymbolInfoInteger(_Symbol,SYMBOL_DIGITS);                // number of decimal places (precision)
   //--- checking the type of operation
   if(orderType==ORDER_TYPE_BUY_LIMIT)
     {
      request.type     =ORDER_TYPE_BUY_LIMIT;                          // order type
      price=SymbolInfoDouble(Symbol(),SYMBOL_ASK)-offset*point;        // price for opening 
      request.price    =NormalizeDouble(price,digits);                 // normalized opening price 
     }
   else if(orderType==ORDER_TYPE_SELL_LIMIT)
     {
      request.type     =ORDER_TYPE_SELL_LIMIT;                          // order type
      price=SymbolInfoDouble(Symbol(),SYMBOL_BID)+offset*point;         // price for opening 
      request.price    =NormalizeDouble(price,digits);                  // normalized opening price 
     }
   else if(orderType==ORDER_TYPE_BUY_STOP)
     {
      request.type =ORDER_TYPE_BUY_STOP;                                // order type
      price        =SymbolInfoDouble(Symbol(),SYMBOL_ASK)+offset*point; // price for opening 
      request.price=NormalizeDouble(price,digits);                      // normalized opening price 
     }
   else if(orderType==ORDER_TYPE_SELL_STOP)
     {
      request.type     =ORDER_TYPE_SELL_STOP;                           // order type
      price=SymbolInfoDouble(Symbol(),SYMBOL_BID)-offset*point;         // price for opening 
      request.price    =NormalizeDouble(price,digits);                  // normalized opening price 
     }
   else Alert("This example is only for placing pending orders");   // if not pending order is selected
//--- send the request
   if(!OrderSend(request,result))
      PrintFormat("OrderSend error %d",GetLastError());                 // if unable to send the request, output the error code
//--- information about the operation
   PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
  }
//+------------------------------------------------------------------+

```

Modify Pending Order

Trade order to modify the prices of a pending order. It requires to specify the following 7 fields:

- action
- order
- price
- sl
- tp
- type_time
- expiration

Example of the TRADE_ACTION_MODIFY trade operation for modifying the price levels of pending orders:

```
#define EXPERT_MAGIC 123456  // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Modification of pending orders                                   |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};
   int total=OrdersTotal(); // total number of placed pending orders
//--- iterate over all placed pending orders
   for(int i=0; i<total; i++)
     {
      //--- parameters of the order
      ulong  order_ticket=OrderGetTicket(i);                             // order ticket
      string order_symbol=Symbol();                                      // symbol
      int    digits=(int)SymbolInfoInteger(order_symbol,SYMBOL_DIGITS);  // number of decimal places
      ulong  magic=OrderGetInteger(ORDER_MAGIC);                         // MagicNumber of the order
      double volume=OrderGetDouble(ORDER_VOLUME_CURRENT);                // current volume of the order
      double sl=OrderGetDouble(ORDER_SL);                                // current Stop Loss of the order
      double tp=OrderGetDouble(ORDER_TP);                                // current Take Profit of the order
      ENUM_ORDER_TYPE type=(ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE); // type of the order
      int offset = 50;                                                   // offset from the current price to place the order, in points
      double price;                                                      // order triggering price
      double point=SymbolInfoDouble(order_symbol,SYMBOL_POINT);          // value of point
      //--- output information about the order
      PrintFormat("#%I64u %s  %s  %.2f  %s  sl: %s  tp: %s  [%I64d]",
                  order_ticket,
                  order_symbol,
                  EnumToString(type),
                  volume,
                  DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                  DoubleToString(sl,digits),
                  DoubleToString(tp,digits),
                  magic);
      //--- if the MagicNumber matches, Stop Loss and Take Profit are not defined
      if(magic==EXPERT_MAGIC && sl==0 && tp==0)
        {
         request.action=TRADE_ACTION_MODIFY;                           // type of trade operation
         request.order = OrderGetTicket(i);                            // order ticket
         request.symbol   =Symbol();                                   // symbol
         request.deviation=5;                                          // allowed deviation from the price
        //--- setting the price level, Take Profit and Stop Loss of the order depending on its type
         if(type==ORDER_TYPE_BUY_LIMIT)
           {
            price = SymbolInfoDouble(Symbol(),SYMBOL_ASK)-offset*point; 
            request.tp = NormalizeDouble(price+offset*point,digits);
            request.sl = NormalizeDouble(price-offset*point,digits);
            request.price    =NormalizeDouble(price,digits);                // normalized opening price
           }
         else if(type==ORDER_TYPE_SELL_LIMIT)
           {
           price = SymbolInfoDouble(Symbol(),SYMBOL_BID)+offset*point; 
            request.tp = NormalizeDouble(price-offset*point,digits);
            request.sl = NormalizeDouble(price+offset*point,digits);
            request.price    =NormalizeDouble(price,digits);                 // normalized opening price
           }
         else if(type==ORDER_TYPE_BUY_STOP)
           {
           price = SymbolInfoDouble(Symbol(),SYMBOL_ASK)+offset*point; 
            request.tp = NormalizeDouble(price+offset*point,digits);
            request.sl = NormalizeDouble(price-offset*point,digits);
            request.price    =NormalizeDouble(price,digits);                 // normalized opening price
           }
         else if(type==ORDER_TYPE_SELL_STOP)
           {
           price = SymbolInfoDouble(Symbol(),SYMBOL_BID)-offset*point; 
            request.tp = NormalizeDouble(price-offset*point,digits);
            request.sl = NormalizeDouble(price+offset*point,digits);
            request.price    =NormalizeDouble(price,digits);                 // normalized opening price
           }
         //--- send the request
         if(!OrderSend(request,result))
            PrintFormat("OrderSend error %d",GetLastError());  // if unable to send the request, output the error code
         //--- information about the operation   
         PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
         //--- zeroing the request and result values
         ZeroMemory(request);
         ZeroMemory(result);
        }
     }
  }
//+------------------------------------------------------------------+

```

Delete Pending Order

Trade order to delete a pending order. It requires to specify the following 2 fields:

- action
- order

Example of the TRADE_ACTION_REMOVE trade operation for deleting pending orders:

```
#define EXPERT_MAGIC 123456  // MagicNumber of the expert
//+------------------------------------------------------------------+
//| Deleting pending orders                                          |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the trade request and result of trade request
   MqlTradeRequest request={};
   MqlTradeResult  result={};
   int total=OrdersTotal(); // total number of placed pending orders
//--- iterate over all placed pending orders
   for(int i=total-1; i>=0; i--)
     {
      ulong  order_ticket=OrderGetTicket(i);                   // order ticket
      ulong  magic=OrderGetInteger(ORDER_MAGIC);               // MagicNumber of the order
      //--- if the MagicNumber matches
      if(magic==EXPERT_MAGIC)
        {
         //--- zeroing the request and result values
         ZeroMemory(request);
         ZeroMemory(result);
         //--- setting the operation parameters     
         request.action=TRADE_ACTION_REMOVE;                   // type of trade operation
         request.order = order_ticket;                         // order ticket
         //--- send the request
         if(!OrderSend(request,result))
            PrintFormat("OrderSend error %d",GetLastError());  // if unable to send the request, output the error code
         //--- information about the operation   
         PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
        }
     }
  }
//+------------------------------------------------------------------+

```

See also

[Structures and Classes](/en/docs/basis/types/classes), [Trade Functions](/en/docs/trading), [Order Properties](/en/docs/constants/tradingconstants/orderproperties)
