# Modifying Stop Loss and/or Take Profit levels of a position

An MQL program can change protective Stop Loss and Take Profit price levels for an open position. The TRADE_ACTION_SLTP element in the [ENUM_TRADE_REQUEST_ACTIONS](/en/book/automation/experts/experts_request_types) enumeration is intended for this purpose, that is, when filling the [MqlTradeRequest](/en/book/automation/experts/experts_mqltraderequest) structure, we should write TRADE_ACTION_SLTP in the action field.

This is the only required field. The need to fill in other fields is determined by the account operation mode [ENUM_ACCOUNT_MARGIN_MODE](/en/book/automation/account/account_netting_hedge). On hedging accounts, you should fill in the symbol field, but you can omit the position ticket. On hedging accounts, on the contrary, it is mandatory to indicate the position position ticket, but you can omit the symbol. This is due to the specifics of position identification on accounts of different types. During netting, only one position can exist for each symbol.

In order to unify the code, it is recommended to fill in both fields if information is available.

Protective price levels are set in the sl and tp fields. It is possible to est only one of the fields. To remove protective levels, assign zero values to them.

The following table summarizes the requirements for filling in the fields depending on the counting modes. Required fields are marked with an asterisk, optional fields are marked with a plus.

| Field | Netting | Hedging |
| --- | --- | --- |
| action | * | * |
| symbol | * | + |
| position | + | * |
| sl | + | + |
| tp | + | + |

To perform the operation of modifying protective levels, we introduce several overloads of the adjust method in the MqlTradeRequestSync structure.

```
struct MqlTradeRequestSync: public MqlTradeRequest
{
   ...
   bool adjust(const ulong pos, const double stop = 0, const double take = 0);
   bool adjust(const string name, const double stop = 0, const double take = 0);
   bool adjust(const double stop = 0, const double take = 0);
   ...
};

```

As we saw above, depending on the environment, modification can be done only by ticket or only by position symbol. These options are taken into account in the first two prototypes.

In addition, since the structure may have already been used for previous requests, it may have filled position and symbols fields. Then you can call the method with the last prototype.

We do not yet show the implementation of these three methods, because it is clear that it must have a common body with sending a request. This part is framed as a private helper method _adjust with a full set of options. Here its code is given with some abbreviations that do not affect the logic of work.

```
private:
   bool _adjust(const ulong pos, const string name,
      const double stop = 0, const double take = 0)
   {
      action = TRADE_ACTION_SLTP;
      position = pos;
      type = (ENUM_ORDER_TYPE)PositionGetInteger(POSITION_TYPE);
      if(!setSymbol(name)) return false;
      if(!setSLTP(stop, take)) return false;
      ZeroMemory(result);
      return OrderSend(this, result);
   }

```

We fill in all the fields of the structure according to the above rules, calling the previously described setSymbol and setSLTP methods, and then send a request to the server. The result is a success status (true) or errors (false).

Each of the overloaded adjust methods separately prepares source parameters for the request. This is how it is done in the presence of a position ticket.

```
public:
   bool adjust(const ulong pos, const double stop = 0, const double take = 0)
   {
      if(!PositionSelectByTicket(pos))
      {
         Print("No position: P=" + (string)pos);
         return false;
      }
      return _adjust(pos, PositionGetString(POSITION_SYMBOL), stop, take);
   }

```

Here, using the built-in PositionSelectByTicket function, we check for the presence of a position and its selection in the trading environment of the terminal, which is necessary for the subsequent reading of its properties, in this case, the symbol (PositionGetString(POSITION_SYMBOL)). Then the universal variant is called adjust.

When modifying a position by symbol name (which is only available on a netting account), you can use another option adjust.

```
   bool adjust(const string name, const double stop = 0, const double take = 0)
   {
      if(!PositionSelect(name))
      {
         Print("No position: " + s);
         return false;
      }
      
      return _adjust(PositionGetInteger(POSITION_TICKET), name, stop, take);
   }

```

Here, position selection is done using the built-in PositionSelect function, and the ticket number is obtained from its properties (PositionGetInteger(POSITION_TICKET)).

All of these features will be discussed in detail in their respective sections on [working with positions](/en/book/automation/experts/experts_position_list) and [position properties](/en/book/automation/experts/experts_position_properties).

The adjust method version with the most minimalist set of parameters, i.e. with only stop and take levels, is as follows.

```
   bool adjust(const double stop = 0, const double take = 0)
   {
      if(position != 0)
      {
         if(!PositionSelectByTicket(position))
         {
            Print("No position with ticket P=" + (string)position);
            return false;
         }
         const string s = PositionGetString(POSITION_SYMBOL);
         if(symbol != NULL && symbol != s)
         {
            Print("Position symbol is adjusted from " + symbol + " to " + s);
         }
         symbol = s;
      }
      else if(AccountInfoInteger(ACCOUNT_MARGIN_MODE)
         != ACCOUNT_MARGIN_MODE_RETAIL_HEDGING
         && StringLen(symbol) > 0)
      {
         if(!PositionSelect(symbol))
         {
            Print("Can't select position for " + symbol);
            return false;
         }
         position = PositionGetInteger(POSITION_TICKET);
      }
      else
      {
         Print("Neither position ticket nor symbol was provided");
         return false;
      }
      return _adjust(position, symbol, stop, take);
   }

```

This code ensures that the position and symbols fields are filled correctly in various modes or that it exits early with an error message in the log. At the end, the private version of _adjust is called, which sends the request via OrderSend.

Similar to buy/sell methods, the set of adjust methods works "asynchronously": upon their completion, only the request sending status is known, but there is no confirmation of the modification of the levels. As we know, for the stock exchange, the Take Profit level can be forwarded as a limit order. Therefore, in the MqlTradeResultSync structure, we should provide a "synchronous" wait until the changes take effect.

The general wait mechanism formed as the MqlTradeResultSync::wait method is already ready and has been used to wait for the opening of a position. The wait method receives as the first parameter a pointer to another method with a predefined prototype condition to poll in a loop until the required condition is met or a timeout occurs. In this case, this condition-compatible method should perform an applied check of the stop levels in the position.

Let's add such a new method called adjusted.

```
struct MqlTradeResultSync: public MqlTradeResult
{
   ...
   bool adjusted(const ulong msc = 1000)
   {
      if(retcode != TRADE_RETCODE_DONE || retcode != TRADE_RETCODE_PLACED)
      {
         return false;
      }
   
      if(!wait(checkSLTP, msc))
      {
         Print("SL/TP modification timeout: P=" + (string)position);
         return false;
      }
      
      return true;
   }

```

First of all, of course, we check the status in the field retcode. If there is a standard status, we continue checking the levels themselves, passing to wait an auxiliary method checkSLTP.

```
struct MqlTradeResultSync: public MqlTradeResult
{
   ...
   static bool checkSLTP(MqlTradeResultSync &ref)
   {
      if(PositionSelectByTicket(ref.position))
      {
         return TU::Equal(PositionGetDouble(POSITION_SL), /*.?.*/)
            && TU::Equal(PositionGetDouble(POSITION_TP), /*.?.*/);
      }
      else
      {
         Print("PositionSelectByTicket failed: P=" + (string)ref.position);
      }
      return false;
   }

```

This code ensures that the position is selected by ticket in the trading environment of the terminal using [PositionSelectByTicket](/en/book/automation/experts/experts_position_list) and reads the position properties POSITION_SL and POSITION_TP, which should be compared with what was in the request. The problem is that here we don't have access to the request object and we must somehow pass here a couple of values for the places marked with '.?.'.

Basically, since we are designing the MqlTradeResultSync structure, we can add sl and tp fields to it and fill them with values from MqlTradeRequestSync before sending the request (the kernel does not "know" about our added fields and will leave them untouched during theOrderSend call). But for simplicity, we will use what is already available. The bid and ask fields in the MqlTradeResultSync structure are only used to report requote prices (TRADE_RETCODE_REQUOTE status), which is not related to the TRADE_ACTION_SLTP request, so we can store the sl and tp from the completed MqlTradeRequestSync in them.

It is logical to make this in the completed method of the MqlTradeRequestSync structure which starts a blocking wait for the trading operation results with a predefined timeout. So far, its code has only had one branch for the TRADE_ACTION_DEAL action. To continue, let's add a branch for TRADE_ACTION_SLTP.

```
struct MqlTradeRequestSync: public MqlTradeRequest
{
   ...
   bool completed()
   {
      if(action == TRADE_ACTION_DEAL)
      {
         const bool success = result.opened(timeout);
         if(success) position = result.position;
         return success;
      }
      else if(action == TRADE_ACTION_SLTP)
      {
         // pass the original request data for comparison with the position properties,
         // by default they are not in the result structure
         result.position = position;
         result.bid = sl; // bid field is free in this result type, use under StopLoss
         result.ask = tp; // ask field is free in this type of result, we use it under TakeProfit
         return result.adjusted(timeout);
      }
      return false;
   }

```

As you can see, after setting the position ticket and price levels from the request, we call the adjusted method discussed above which checks wait(checkSLTP). Now we can return to the helper method checkSLTP in the MqlTradeResultSync structure and bring it to its final form.

```
struct MqlTradeResultSync: public MqlTradeResult
{
   ...
   static bool checkSLTP(MqlTradeResultSync &ref)
   {
      if(PositionSelectByTicket(ref.position))
      {
         return TU::Equal(PositionGetDouble(POSITION_SL), ref.bid) // sl from request
            && TU::Equal(PositionGetDouble(POSITION_TP), ref.ask); // tp from request
      }
      else
      {
         Print("PositionSelectByTicket failed: P=" + (string)ref.position);
      }
      return false;
   }

```

This completes the extension of the functionality of structures MqlTradeRequestSync and MqlTradeResultSync for the of Stop Loss and Take Profit modification operation.

With this in mind, let's continue with the example of the Expert Advisor MarketOrderSend.mq5 which we started in the previous section. Let's add to it an input parameter Distance2SLTP, which allows you to specify the distance in points to the levels Stop Loss and Take Profit.

```
input int Distance2SLTP = 0; // Distance to SL/TP in points (0 = no)

```

When it is zero, no guard levels will be set.

In the working code, after receiving confirmation of opening a position, we calculate the values of the levels in the SL and TP variables and perform a synchronous modification: request.adjust(SL, TP) && request.completed().

```
   ...
   const ulong order = (wantToBuy ?
      request.buy(symbol, volume, Price) :
      request.sell(symbol, volume, Price));
   if(order != 0)
   {
      Print("OK Order: #=", order);
      if(request.completed()) // waiting for position opening
      {
         Print("OK Position: P=", request.result.position);
         if(Distance2SLTP != 0)
         {
            // position "selected" in the trading environment of the terminal inside 'complete',
            // so it is not required to do this explicitly on the ticket
            // PositionSelectByTicket(request.result.position);
            
            // with the selected position, you can find out its properties, but we need the price,
            // to step back from it by a given number of points
            const double price = PositionGetDouble(POSITION_PRICE_OPEN);
            const double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
            // we count the levels using the auxiliary class TradeDirection
            TU::TradeDirection dir((ENUM_ORDER_TYPE)Type);
            // SL is always "worse" and TP is always "better" of the price: the code is the same for buying and selling
            const double SL = dir.negative(price, Distance2SLTP * point);
            const double TP = dir.positive(price, Distance2SLTP * point);
            if(request.adjust(SL, TP) && request.completed())
            {
               Print("OK Adjust");
            }
         }
      }
   }
   Print(TU::StringOf(request));
   Print(TU::StringOf(request.result));
}

```

In the first call of completed after a successful buy or sell operation, the position ticket is saved in the position field of the request structure. Therefore, to modify stops, only price levels are sufficient, and the symbol and ticket of the position are already present in request.

Let's try to execute a buy operation using the Expert Advisor with default settings but with Distance2SLTP set at 500 points.

```
OK Order: #=1273913958
Waiting for position for deal D=1256506526
OK Position: P=1273913958
OK Adjust
TRADE_ACTION_SLTP, EURUSD, ORDER_TYPE_BUY, V=0.01, ORDER_FILLING_FOK, @ 1.10889, »
»  SL=1.10389, TP=1.11389, P=1273913958
DONE, Bid=1.10389, Ask=1.11389, Request executed, Req=26

```

The last two lines correspond to the debug output to the log of the contents of the request and request.result structures, initiated at the end of the function. In these lines, it is interesting that the fields store a symbiosis of values from two queries: first, a position was opened, and then it was modified. In particular, the fields with volume (0.01) and price (1.10889) in the request remained after TRADE_ACTION_DEAL, but did not prevent the execution of TRADE_ACTION_SLTP. In theory, it is easy to get rid of this by resetting the structure between two requests, however, we preferred to leave them as they are, because among the filled fields there are also useful ones: the position field received the ticket we need to request the modification. If we reset the structure, then we would need to introduce a variable for intermediate storage of the ticket.

In general cases, of course, it is desirable to adhere to a strict data initialization policy, but knowing how to use them in specific scenarios (such as two or more related requests of a predefined type) allows you to optimize your code.

Also, one should not be surprised that in the structure with the result, we see the requested levels sl and tp in the fields for the Bid and Ask prices: they were written there by the MqlTradeRequestSync::completed method for the purpose of comparison with the actual position changes. When executing the request, the system kernel filled only retcode (DONE), comment ("Request executed"), and request_id (26) in the result structure.

Next, we will consider another example of level modification that implements the [trailing stop](/en/book/automation/experts/experts_trailing_stop).
