# TesterStatistics

The function returns the value of the specified statistical parameter calculated based on testing results.

```
double  TesterStatistics(
   ENUM_STATISTICS statistic_id      // ID
   );

```

Parameters

statistic_id

[in]   The ID of the statistical parameter from the [ENUM_STATISTICS](/en/docs/constants/environment_state/statistics#enum_statistics) enumeration.

Return Value

The value of the statistical parameter from testing results.

Note

The function can be called inside [OnTester()](/en/docs/event_handlers/ontester) or [OnDeinit()](/en/docs/basis/function/events) in the tester. In other cases the result is undefined.

Example:

```
// The EA based on standard "MACD Sample.mq5" file
// shows the result of TesterStatistics() in the Tester event handler
#define MACD_MAGIC 1234502
//---
#include <Trade\Trade.mqh>
#include <Trade\SymbolInfo.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\AccountInfo.mqh>
//---
input double InpLots          =0.1; // Lots
input int    InpTakeProfit    =50;  // Take Profit (in pips)
input int    InpTrailingStop  =30;  // Trailing Stop Level (in pips)
input int    InpMACDOpenLevel =3;   // MACD open level (in pips)
input int    InpMACDCloseLevel=2;   // MACD close level (in pips)
input int    InpMATrendPeriod =26;  // MA trend period
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit(void)
  {
//--- create all the necessary objects
   if(!ExtExpert.Init())
      return(INIT_FAILED);
//--- successful initialization
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert new tick handling function                                |
//+------------------------------------------------------------------+
void OnTick(void)
  {
   static datetime limit_time=0; // last call time considering 'timeout'
//--- if the time exceeds the specified limit_time value
   if(TimeCurrent()>=limit_time)
     {
      //--- check the data
      if(Bars(Symbol(),Period())>2*InpMATrendPeriod)
        {
         //--- if successful, increase limit_time by 'timeout' seconds
         if(ExtExpert.Processing())
            limit_time=TimeCurrent()+ExtTimeOut;
        }
     }
  }
//+------------------------------------------------------------------+
//| Expert tester handling function                                  |
//+------------------------------------------------------------------+
double OnTester(void)
  {
   double ret=TesterStatistics(STAT_PROFIT_FACTOR);
   double profit=TesterStatistics(STAT_PROFIT);
   int    trades_total=(int)TesterStatistics(STAT_TRADES);
   int    profit_total=(int)TesterStatistics(STAT_PROFIT_TRADES);
   int    loss_total=(int)TesterStatistics(STAT_LOSS_TRADES);
   PrintFormat("%s: Profit = %.2f, trades total: %lu, profit trades total: %lu, loss trades total: %lu, profit factor: %.2f",__FUNCTION__,profit,trades_total,profit_total,loss_total,ret);
   return(ret);
   /*
   Result:
   OnTester: Profit = 209.84, trades total: 13, profit trades total: 11, loss trades total: 2, profit factor: 3.02
   final balance 10209.84 USD
   OnTester result 3.020606644198363
   */
  }  

```
