# OnTester

The function is called in Expert Advisors when the [Tester](/en/docs/runtime/event_fire#tester) event occurs to perform necessary actions after testing.

```
double  OnTester(void);

```

Return Value

Value of the custom criterion optimization for assessing test results.

Note

The OnTester() function can be used only when testing EAs and is intended primarily for the calculation of a value that is used as a 'Custom max' criterion when optimizing input parameters.

During the genetic optimization, sorting results within one generation is performed in descending order. This means that the results with the highest value are deemed the best from the optimization criterion point of view. The worst values ​​for such sorting are placed at the end and are subsequently discarded. Therefore, they do not take part in forming the next generation.

Thus, the OnTester() function allows you not only to create and save your own test results reports, but also control the optimization process to find the best parameters of the trading strategy.

Below is an example of calculating the custom criterion optimization. The idea is to calculate the linear regression of the balance graph. It is described in the article [Optimizing a strategy using balance graph and comparing results with "Balance + max Sharpe Ratio" criterion](https://www.mql5.com/en/articles/3642).

```
//+------------------------------------------------------------------+
//|                                              OnTester_Sample.mq5 |
//|                        Copyright 2018, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "Sample EA with the OnTester() handler"
#property description "As a custom optimization criterion, "
#property description "the ratio of the balance graph linear regression"
#property description "divided by the deviation mean-square error is returned"
//--- include the class for trading operations
#include <Trade\Trade.mqh>
//--- EA input parameters
input double Lots               = 0.1;     // Volume
input int    Slippage           = 10;      // Allowable slippage
input int    MovingPeriod       = 80;      // Moving average period
input int    MovingShift        = 6;       // Moving average shift
//--- global variables
int    IndicatorHandle=0;  // indicator handle
bool   IsHedging=false;    // flag of the account
CTrade trade;              // for performing trading operations
//--- 
#define EA_MAGIC 18052018
//+------------------------------------------------------------------+
//| Check for position opening conditions                            |
//+------------------------------------------------------------------+
void CheckForOpen(void)
  {
   MqlRates rt[2];
//--- trade only at the start of a new bar
   if(CopyRates(_Symbol,_Period,0,2,rt)!=2)
     {
      Print("CopyRates of ",_Symbol," failed, no history");
      return;
     }
//--- tick volume
   if(rt[1].tick_volume>1)
      return;
//--- receive moving average values
   double   ma[1];
   if(CopyBuffer(IndicatorHandle,0,1,1,ma)!=1)
     {
      Print("CopyBuffer from iMA failed, no data");
      return;
     }
//--- check for a signal presence
   ENUM_ORDER_TYPE signal=WRONG_VALUE;
//--- candle opened higher but closed below the moving average
   if(rt[0].open>ma[0] && rt[0].close<ma[0])
      signal=ORDER_TYPE_BUY;    // buy signal
   else // candle opened lower but closed above the moving average
     {
      if(rt[0].open<ma[0] && rt[0].close>ma[0])
         signal=ORDER_TYPE_SELL;// sell signal
     }
//--- additional checks
   if(signal!=WRONG_VALUE)
     {
      if(TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) && Bars(_Symbol,_Period)>100)
        {
         double price=SymbolInfoDouble(_Symbol,signal==ORDER_TYPE_SELL ? SYMBOL_BID:SYMBOL_ASK);
         trade.PositionOpen(_Symbol,signal,Lots,price,0,0);
        }
     }
//---
  }
//+------------------------------------------------------------------+
//| Check for position closing conditions                            |
//+------------------------------------------------------------------+
void CheckForClose(void)
  {
   MqlRates rt[2];
//--- trade only at the start of a new bar
   if(CopyRates(_Symbol,_Period,0,2,rt)!=2)
     {
      Print("CopyRates of ",_Symbol," failed, no history");
      return;
     }
   if(rt[1].tick_volume>1)
      return;
//--- receive moving average values
   double   ma[1];
   if(CopyBuffer(IndicatorHandle,0,1,1,ma)!=1)
     {
      Print("CopyBuffer from iMA failed, no data");
      return;
     }
//--- position has already been selected earlier using PositionSelect()
   bool signal=false;
   long type=PositionGetInteger(POSITION_TYPE);
//--- candle opened higher but closed below the moving average - close a short position
   if(type==(long)POSITION_TYPE_SELL && rt[0].open>ma[0] && rt[0].close<ma[0])
      signal=true;
//--- candle opened lower but closed above the moving average - close a long position
   if(type==(long)POSITION_TYPE_BUY && rt[0].open<ma[0] && rt[0].close>ma[0])
      signal=true;
//--- additional checks
   if(signal)
     {
      if(TerminalInfoInteger(TERMINAL_TRADE_ALLOWED) && Bars(_Symbol,_Period)>100)
         trade.PositionClose(_Symbol,Slippage);
     }
//---
  }
//+-------------------------------------------------------------------+
//| Select a position considering an account type: Netting or Hedging |
//+-------------------------------------------------------------------+
bool SelectPosition()
  {
   bool res=false;
//--- select a position for a Hedging account
   if(IsHedging)
     {
      uint total=PositionsTotal();
      for(uint i=0; i<total; i++)
        {
         string position_symbol=PositionGetSymbol(i);
         if(_Symbol==position_symbol && EA_MAGIC==PositionGetInteger(POSITION_MAGIC))
           {
            res=true;
            break;
           }
        }
     }
//--- select a position for a Netting account
   else
     {
      if(!PositionSelect(_Symbol))
         return(false);
      else
         return(PositionGetInteger(POSITION_MAGIC)==EA_MAGIC); //---check Magic number
     }
//--- execution result
   return(res);
  }
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit(void)
  {
//--- set a trading type: Netting or Hedging
   IsHedging=((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)==ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
//--- initialize an object for correct position control
   trade.SetExpertMagicNumber(EA_MAGIC);
   trade.SetMarginMode();
   trade.SetTypeFillingBySymbol(Symbol());
   trade.SetDeviationInPoints(Slippage);
//--- create Moving Average indicator
   IndicatorHandle=iMA(_Symbol,_Period,MovingPeriod,MovingShift,MODE_SMA,PRICE_CLOSE);
   if(IndicatorHandle==INVALID_HANDLE)
     {
      printf("Error creating iMA indicator");
      return(INIT_FAILED);
     }
//--- ok
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick(void)
  {
//--- if a position is already opened, check the closing condition
   if(SelectPosition())
      CheckForClose();
// check the position opening condition
   CheckForOpen();
//---
  }
//+------------------------------------------------------------------+
//| Tester function                                                  |
//+------------------------------------------------------------------+
double OnTester()
  {
//--- custom criterion optimization value (the higher, the better)
   double ret=0.0;
//--- get trade results to the array
   double array[];
   double trades_volume;
   GetTradeResultsToArray(array,trades_volume);
   int trades=ArraySize(array);
//--- if there are less than 10 trades, test yields no positive results
   if(trades<10)
      return (0);
//--- average result per trade
   double average_pl=0;
   for(int i=0;i<ArraySize(array);i++)
      average_pl+=array[i];
   average_pl/=trades;
//--- display the message for the single-test mode
   if(MQLInfoInteger(MQL_TESTER) && !MQLInfoInteger(MQL_OPTIMIZATION))
      PrintFormat("%s: Trades=%d, Average profit=%.2f",__FUNCTION__,trades,average_pl);
//--- calculate linear regression ratios for the profit graph
   double a,b,std_error;
   double chart[];
   if(!CalculateLinearRegression(array,chart,a,b))
      return (0);
//--- calculate the error of the chart deviation from the regression line
   if(!CalculateStdError(chart,a,b,std_error))
      return (0);
//--- calculate the ratio of trend profits to the standard deviation
   ret=(std_error == 0.0) ? a*trades : a*trades/std_error;
//--- return custom criterion optimization value
   return(ret);
  }
//+------------------------------------------------------------------+
//| Get the array of profits/losses from deals                       |
//+------------------------------------------------------------------+
bool GetTradeResultsToArray(double &pl_results[],double &volume)
  {
//--- request the complete trading history
   if(!HistorySelect(0,TimeCurrent()))
      return (false);
   uint total_deals=HistoryDealsTotal();
   volume=0;
//--- set the initial size of the array with a margin - by the number of deals in history
   ArrayResize(pl_results,total_deals);
//--- counter of deals that fix the trading result - profit or loss
   int counter=0;
   ulong ticket_history_deal=0;
//--- go through all deals
   for(uint i=0;i<total_deals;i++)
     {
      //--- select a deal 
      if((ticket_history_deal=HistoryDealGetTicket(i))>0)
        {
         ENUM_DEAL_ENTRY deal_entry  =(ENUM_DEAL_ENTRY)HistoryDealGetInteger(ticket_history_deal,DEAL_ENTRY);
         long            deal_type   =HistoryDealGetInteger(ticket_history_deal,DEAL_TYPE);
         double          deal_profit =HistoryDealGetDouble(ticket_history_deal,DEAL_PROFIT);
         double          deal_volume =HistoryDealGetDouble(ticket_history_deal,DEAL_VOLUME);
         //--- we are only interested in trading operations        
         if((deal_type!=DEAL_TYPE_BUY) && (deal_type!=DEAL_TYPE_SELL))
            continue;
         //--- only deals that fix profits/losses
         if(deal_entry!=DEAL_ENTRY_IN)
           {
            //--- write the trading result to the array and increase the counter of deals
            pl_results[counter]=deal_profit;
            volume+=deal_volume;
            counter++;
           }
        }
     }
//--- set the final size of the array
   ArrayResize(pl_results,counter);
   return (true);
  }
//+------------------------------------------------------------------+
//| Calculate the linear regression y=a*x+b                          |
//+------------------------------------------------------------------+
bool CalculateLinearRegression(double  &change[],double &chartline[],
                               double  &a_coef,double  &b_coef)
  {
//--- check for data sufficiency
   if(ArraySize(change)<3)
      return (false);
//--- create a chart array with an accumulation
   int N=ArraySize(change);
   ArrayResize(chartline,N);
   chartline[0]=change[0];
   for(int i=1;i<N;i++)
      chartline[i]=chartline[i-1]+change[i];
//--- now, calculate regression ratios
   double x=0,y=0,x2=0,xy=0;
   for(int i=0;i<N;i++)
     {
      x=x+i;
      y=y+chartline[i];
      xy=xy+i*chartline[i];
      x2=x2+i*i;
     }
   a_coef=(N*xy-x*y)/(N*x2-x*x);
   b_coef=(y-a_coef*x)/N;
//---
   return (true);
  }
//+------------------------------------------------------------------+
//|  Calculate mean-square deviation error for specified a and b     |
//+------------------------------------------------------------------+
bool  CalculateStdError(double  &data[],double  a_coef,double  b_coef,double &std_err)
  {
//--- sum of error squares
   double error=0;
   int N=ArraySize(data);
   if(N<=2)
      return (false);
   for(int i=0;i<N;i++)
      error+=MathPow(a_coef*i+b_coef-data[i],2);
   std_err=MathSqrt(error/(N-2));
//--- 
   return (true);
  }

```

See also

[Testing trading strategies](/en/docs/runtime/testing), [TesterHideIndicators](/en/docs/common/testerhideindicators), [Working with optimization results](/en/docs/optimization_frames), [TesterStatistics](/en/docs/common/testerstatistics), [OnTesterInit](/en/docs/event_handlers/ontesterinit), [OnTesterDeinit](/en/docs/event_handlers/ontesterdeinit), [OnTesterPass](/en/docs/event_handlers/ontesterpass), [MQL_TESTER](/en/docs/constants/environment_state/mql5_programm_info#enum_mql_info_integer), [MQL_OPTIMIZATION](/en/docs/constants/environment_state/mql5_programm_info#enum_mql_info_integer), [FileOpen](/en/docs/files/fileopen), [FileWrite](/en/docs/files/filewrite), [FileLoad](/en/docs/files/fileload), [FileSave](/en/docs/files/filesave)
