# MessageBox

It creates and shows a message box and manages it. A message box contains a message and header, any combination of predefined signs and command buttons.

```
int  MessageBox(
   string  text,             // message text
   string  caption=NULL,     // box header
   int     flags=0           // defines set of buttons in the box
   );

```

Parameters

text

[in]  Text, containing message to output.

caption=[NULL](/en/docs/basis/types/void)

[in]  Optional text to be displayed in the box header. If the parameter is empty, Expert Advisor name is shown in the box header.

flags=0

[in]  Optional [flags](/en/docs/constants/io_constants/messbconstants#messageboxflags) defining appearance and behavior of a message box. Flags can be a combination of a special group of flags.

Return Value

If the function is successfully performed, the returned value is one of values of [MessageBox()](/en/docs/constants/io_constants/messbconstants) return codes.

Note

The function cannot be used in custom indicators since calling MessageBox() suspends the [thread of execution](/en/docs/runtime/running) for the whole time while waiting for the user's response. Since all indicators for each symbol are executed in a single thread, such suspension makes the operation of all charts on all timeframes for this symbol impossible.

MessageBox() function does not work in the [Strategy Tester](/en/docs/runtime/testing#alert_etc).

Example:

```
//+------------------------------------------------------------------+
//| The EA displays MessageBox window with a request for further work|
//| upon reaching specified number of series of unprofitable trades  |
//| Wait for the specified number of bars and display MessageBox     |
//| with a request to continue work.                                 |
//| To check, we need to manually open and close several positions   |
//| with a loss, since the EA does not control                       |
//| its own "positions" by magic number for simplicity.              |
//+------------------------------------------------------------------+
 
//--- input parameters
input uint InpMaxLossDeals      =  3;    // Max Loss deals
input uint InpInactivityNumBars =  5;    // Number of bars of advisor inactivity
 
//--- global variables
bool     ExtFirstStart=true;             // First launch flag
bool     ExtFlag=true;                   // Flag for allowing the EA to work
uint     ExtNumLoss;                     // Number of consecutive unprofitable trades
datetime ExtTimeLastLoss;                // Time of the last trade to close a losing position
 
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- get the number of losing trades in a row and the time of the last trade to close the position
   ExtNumLoss=GetNumLosingTradesInRow(ExtTimeLastLoss);
 
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   Comment("");
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- determine how many bars have passed since the last closed losing position in the series
   int bars_remaining=iBarShift(Symbol(),PERIOD_CURRENT,ExtTimeLastLoss);
 
//--- if this is the first launch
   if(ExtFirstStart)
     {
      //--- If a specified number of bars have already passed after a series of unprofitable positions, set the EA operation flag
      if(bars_remaining>(int)InpInactivityNumBars)
         ExtFlag=true;
      ExtFirstStart=false;
     }
 
//--- if the EA operation flag is disabled
   if(!ExtFlag)
     {
      Comment(StringFormat("The advisor is stopped for %d bars. Num Loss positions: %u, Time last loss: %s",
                          (InpInactivityNumBars-bars_remaining),ExtNumLoss,TimeToString(ExtTimeLastLoss,TIME_DATE|TIME_MINUTES|TIME_SECONDS)));
      //--- if a specified number of bars have passed after a series of unprofitable positions
      if(bars_remaining>(int)InpInactivityNumBars)
        {
         //--- display MessageBox window with the specified text and window title
         //--- the request window has two Yes/No buttons and an icon with a question mark.
         //--- the Yes button is selected by default.
         string mb_text="The specified number of bars of EA inactivity have passed.\n Continue its work?";
         string mb_caption="Please note";
         int    mb_id=MessageBox(mb_text,mb_caption,MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON1);
         //--- if the return code from MessageBox is the Yes button pressed, set the EA operation flag
         if(mb_id==IDYES)
           {
            ExtFlag=true;
            return;
           }
        }
      //--- the EA operation flag is disabled, exit OnTick()
      return;
     }
 
//---  the EA operation flag is set - the EA works as provided by the code below
   Comment(StringFormat("The advisor is working. Num Loss positions: %u, Time last loss: %s, Elapsed Bars: %d",
           ExtNumLoss,TimeToString(ExtTimeLastLoss,TIME_DATE|TIME_MINUTES|TIME_SECONDS),bars_remaining));
  }
//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
  {
//--- if the transaction type is adding a transaction to history
   if(trans.type==TRADE_TRANSACTION_DEAL_ADD)
     {
      //--- get a deal ticket and select a deal from the list by ticket
      ulong deal_ticket=trans.deal;
      if(HistoryDealSelect(deal_ticket))
        {
         //--- if this is a market exit trade, get the number of losing trades in a row and the time of the last trade
         ENUM_DEAL_ENTRY entry=(ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal_ticket,DEAL_ENTRY);
         if(entry==DEAL_ENTRY_OUT || entry==DEAL_ENTRY_INOUT || entry==DEAL_ENTRY_OUT_BY)
            ExtNumLoss=GetNumLosingTradesInRow(ExtTimeLastLoss);
        }
     }
 
//--- if the number of losing trades in a row is greater than the specified value and the EA operation flag is enabled
   if(ExtNumLoss>=InpMaxLossDeals && ExtFlag)
     {
      //--- display MessageBox window with the specified text and window title
      //--- the request window has two Yes/No buttons and an icon with an exclamation mark.
      //--- the No button is selected by default.
      string mb_text="The number of losing trades has reached the specified maximum. The advisor is stopped.\n Continue its work?";
      string mb_caption="Attention!";
      int    mb_id=MessageBox(mb_text,mb_caption,MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON2);
      //--- if the return code from MessageBox is the No button pressed, disable the EA operation flag
      if(mb_id==IDNO)
         ExtFlag=false;
     }
  }
//+------------------------------------------------------------------+
//| Return the number of consecutive unprofitable trades             |
//| and the time of the last trade to close a losing position        |
//+------------------------------------------------------------------+
uint GetNumLosingTradesInRow(datetime &time_last_deal)
  {
//--- select the entire history
   if(!HistorySelect(0,TimeCurrent()))
      return(0);
 
//--- get the next trade ticket by the list of historical deals in a loop
   uint res=0;
   uint total=HistoryDealsTotal();
   for(int i=(int)total-1; i>=0; i--)
     {
      ulong deal_ticket=HistoryDealGetTicket(i);
      if(deal_ticket>0)
        {
         //--- if the deal is not for exiting the position, move on to the next one
         ENUM_DEAL_ENTRY entry=(ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal_ticket,DEAL_ENTRY);
         if(entry!=DEAL_ENTRY_OUT && entry!=DEAL_ENTRY_OUT_BY && entry!=DEAL_ENTRY_INOUT)
            continue;
         //--- if the result of closing a position has a profit, interrupt the loop
         if(!IsClosePositionWithLoss(deal_ticket))
            break;
         //--- increase the counter of consecutive loss-making trades
         res++;
         //--- write the maximum trade time into a variable (looking for the last one)
         datetime deal_time=(datetime)HistoryDealGetInteger(deal_ticket,DEAL_TIME);
         if(deal_time>time_last_deal)
            time_last_deal=deal_time;
        }
     }
 
//--- return the number of consecutive losses
   return(res);
  }
//+------------------------------------------------------------------+
//| Return the flag of closing a position with a loss                |
//+------------------------------------------------------------------+
bool IsClosePositionWithLoss(const ulong deal_ticket)
  {
//--- get the values of the properties affecting profit from the trade
   double profit=HistoryDealGetDouble(deal_ticket,DEAL_PROFIT);
   double comission=HistoryDealGetDouble(deal_ticket,DEAL_COMMISSION);
   double swap=HistoryDealGetDouble(deal_ticket,DEAL_SWAP);
   double fee=HistoryDealGetDouble(deal_ticket,DEAL_FEE);
 
//--- return the flag indicating that the total value of the received properties is negative
   return(profit+comission+swap+fee<0);
  }

```
