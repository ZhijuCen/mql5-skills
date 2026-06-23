# PositionSelectByTicket

Selects an open position to work with based on the ticket number specified in the position. If successful, returns true. Returns false if the function failed. Call [GetLastError()](/en/docs/check/getlasterror) for error details.

```
bool  PositionSelectByTicket(
   ulong   ticket     // Position ticket
   );

```

Parameters

ticket

[in]  Position ticket.

Return Value

A value of the bool type.

Note

The PositionSelectByTicket() function copies position data to the program environment. Further calls of [PositionGetDouble()](/en/docs/trading/positiongetdouble), [PositionGetInteger()](/en/docs/trading/positiongetinteger) and [PositionGetString()](/en/docs/trading/positiongetstring) return the previously copied data. Even if a position does not exist already (or its size, direction etc. has changed), the data may still be received sometimes. To make sure that you receive valid position data, it is recommended to call PositionSelectByTicket() before you access the data.

Example:

```
#define   EXPERT_MAGIC  123456   // MagicNumber
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- declare and initialize the request and result structures
   MqlTradeRequest request={};
   MqlTradeResult  result ={};
   
//--- fill in trade request parameters to open a long position
   request.action    = TRADE_ACTION_DEAL;                      // trading operation type
   request.symbol    = Symbol();                               // symbol
   request.volume    = 0.1;                                    // volume of 0.1 lot
   request.type      = ORDER_TYPE_BUY;                         // order type
   request.price     = SymbolInfoDouble(Symbol(), SYMBOL_ASK); // open price
   request.deviation = 5;                                      // allowed deviation from the price
   request.magic     = EXPERT_MAGIC;                           // order MagicNumber
   
//--- send a request. If failed to send a request, display the error code and complete operation
   if(!OrderSend(request, result))
     {
      PrintFormat("OrderSend error ", GetLastError());
      return;
     }
      
//--- display operation data
   PrintFormat("Trade request result: retcode: %u, deal: %I64u, order: %I64u", result.retcode, result.deal, result.order);
   
//--- get the position ticket from the trade operation result and select the position by ticket
//--- the ticket of a newly opened position corresponds to the ticket of the order that generated the deal
   ulong ticket=result.order;
   ResetLastError();
   if(!PositionSelectByTicket(ticket))
     {
      PrintFormat("PositionSelectByTicket(%I64u) failed. Error %d", ticket, GetLastError());
      return;
     }
 
//--- display the data of a position, selected by ticket, in the journal
   ENUM_POSITION_TYPE type  = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
   long               time  = PositionGetInteger(POSITION_TIME_MSC);
   double             price = PositionGetDouble(POSITION_PRICE_OPEN);
   double             volume= PositionGetDouble(POSITION_VOLUME);
   string             symbol= PositionGetString(POSITION_SYMBOL);
   int                digits= (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   PrintFormat("Current selected position: %s %.2f %s #%I64u at %.*f, %s",
               symbol, volume, (type==POSITION_TYPE_BUY ? "Buy" : "Sell"), ticket, digits, price, TimeMscToString(time));
   /*
   result:
   Trade request result: retcode: 10009, deal: 2778100901, order: 2803905975
   Current selected position: EURUSD 0.10 Buy #2803905975 at 1.10672, 2024.09.02 12:09:51.239
   */
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

[PositionGetSymbol()](/en/docs/trading/positiongetsymbol), [PositionsTotal()](/en/docs/trading/positionstotal), [Position Properties](/en/docs/constants/tradingconstants/positionproperties)
