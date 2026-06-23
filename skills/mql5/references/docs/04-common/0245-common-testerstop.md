# TesterStop

Gives program operation completion command when [testing](https://www.metatrader5.com/en/terminal/help/algotrading/testing).

```
void  TesterStop();

```

Return Value

No return value.

Note

The TesterStop() function is designed for a routine early shutdown of an EA on a [test agent](https://www.metatrader5.com/en/terminal/help/algotrading/strategy_optimization#agents) – for example, when reaching a specified number of losing trades or a preset drawdown level.

TesterStop() call is considered a normal completion of a test, therefore the [OnTester(](/en/docs/event_handlers/ontester)) function is called, and the entire accumulated trading statistics and [optimization criterion](/en/docs/event_handlers/ontester) value are submitted to the strategy tester.

Calling [ExpertRemove()](/en/docs/common/expertremove) in the strategy tester also means normal test completion and allows for obtaining trading statistics, but the EA is unloaded from the agent’s memory. In this case, performing a pass on the next set of parameters requires time in order to reload the program. Therefore, TesterStop() is a preferred option for an early routine completion of a test.

Example:

```
//--- defines
#define BALANCE_LOSS_STOP  100.0       // value of the balance drawdown, at which testing is stopped
#define EQUITY_LOSS_STOP   100.0       // value of the equity drawdown, at which testing is stopped
 
//--- input parameters
input  double  InpLots        =  0.1;  // lots
input  uint    InpStopLoss    =  50;   // Stop loss in points
input  uint    InpTakeProfit  =  150;  // Take Profit in points
sinput ulong   InpMagic       =  123;  // MagicNumber
sinput ulong   InpDeviation   =  5;    // deviation
//--- global variables
CTrade      trade;                     // trade class instance
CSymbolInfo symb;                      // symbol class instance
CAccountInfo account;                  // trading account class instance
...
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   ...
//--- successful initialization
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//--- update current quotes
   if(!symb.RefreshRates())
      return;
   ...
 
//--- if the balance or equity have dropped more than indicated in the BALANCE_LOSS_STOP and EQUITY_LOSS_STOP macro substitutions,
//--- the test is considered unsuccessful and the TesterStop() function is called
//--- check for loss of balance by more than BALANCE_LOSS_STOP
   if(balance_prev!=account.Balance())
     {
      if(account.Balance()<balance_prev-BALANCE_LOSS_STOP)
        {
         PrintFormat("The initial balance of %.2f %s decreased by %.2f %s, and now has a value of %.2f %s. Stop testing.",balance_prev,account.Currency(),balance_prev-account.Balance(),account.Currency(),account.Balance(),account.Currency());
         TesterStop();
         /*
         Result:
         The initial balance of 10000.00 USD decreased by 100.10 USD, and now has a value of 9899.90 USD. Stop testing.
         TesterStop() called on 9% of testing interval
         */
        }
     }
//--- check the loss of equity by more than EQUITY_LOSS_STOP
   if(equity_prev!=account.Equity())
     {
      if(account.Equity()<equity_prev-EQUITY_LOSS_STOP)
        {
         PrintFormat("The initial equity of %.2f %s decreased by %.2f %s, and now has a value of %.2f %s. Stop testing.",equity_prev,account.Currency(),equity_prev-account.Equity(),account.Currency(),account.Equity(),account.Currency());
         TesterStop();
         /*
         Result:
         The initial equity of 10000.00 USD decreased by 100.10 USD, and now has a value of 9899.90 USD. Stop testing.
         TesterStop() called on 9% of testing interval
         */
        }
     }
  }

```

See also

[Program Running](/en/docs/runtime/running), [Testing Trading Strategies](/en/docs/runtime/testing), [ExpertRemove](/en/docs/common/expertremove), [SetReturnError](/en/docs/common/setreturnerror)
