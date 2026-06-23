# TesterDeposit

The special function that emulates depositing funds during a test. It can be used in some money management systems.

```
bool  TesterDeposit(
   double money      // deposited sum
   );

```

Parameters

money

[in]  Money to be deposited to an account in the deposit currency.

Return Value

Returns true if successful, otherwise - false.

Example:

```
//--- defines
#define BALANCE_LOSS_DEPOSIT  100.0    // value of the balance drawdown, at which funds will be deposited into the account in the tester
 
//--- input parameters
input  double  InpLots        =  0.1;  // Lots
input  uint    InpStopLoss    =  50;   // Stop loss in points
input  uint    InpTakeProfit  =  150;  // Take Profit in points
sinput ulong   InpMagic       =  123;  // Magic number
sinput ulong   InpDeviation   =  5;    // Deviation
//--- global variables
CTrade      trade;                     // trade class instance
CSymbolInfo symb;                      // symbol class instance
CAccountInfo account;                  // trading account class instance
...
double      balance_dep_summ;          // total amount of balance top-ups
uint        balance_dep_total;         // number of balance top-ups
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   ...
//--- save the initial balance values
   balance_prev=account.Balance();
   balance_dep_summ=0;
   balance_dep_total=0;
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
 
//--- if the balance has dropped more than indicated in the BALANCE_LOSS_DEPOSIT macro substitution,
//--- it is necessary to top up the account and call the TesterDeposit() function
//--- check for loss of balance by more than BALANCE_LOSS_DEPOSIT
   if(balance_prev!=account.Balance())
     {
      if(account.Balance()<balance_prev-BALANCE_LOSS_DEPOSIT)
        {
         double loss=balance_prev-account.Balance();
         PrintFormat("The initial balance of %.2f %s decreased by %.2f %s. It is necessary to make a deposit to the account for %.2f %s.",balance_prev,account.Currency(),loss,account.Currency(),loss,account.Currency());
         if(TesterDeposit(loss))
           {
            balance_dep_total++;
            balance_dep_summ+=loss;
            balance_prev=account.Balance();
            PrintFormat("Funds have been deposited into the account. Account balance: %.2f %s.",account.Balance(),account.Currency());
            PrintFormat("Total deposits: %lu. Amount of deposits: %.2f %s.",balance_dep_total,balance_dep_summ,account.Currency());
           }
         /*
         Result:
         The initial balance of 10000.00 USD decreased by 116.00 USD. It is necessary to make a deposit to the account for 116.00 USD.
         deal #45 balance 116.00 [deposit] done
         Funds have been deposited into the account. Account balance: 10000.00 USD.
         Total deposits: 1. Amount of deposits: 116.00 USD.
         */
        }
     }
  }
//+------------------------------------------------------------------+
//| Tester function                                                  |
//+------------------------------------------------------------------+
double OnTester()
  {
//--- set the maximum balance drawdown in monetary terms as the output handler value
   double ret=TesterStatistics(STAT_BALANCE_DD);
//--- display a message about the drawdown, the number of deposits and their total amount in the log
   PrintFormat("%s: Maximum balance drawdown in money: %.2f %s. Total deposits: %lu. Amount of deposits: %.2f %s.",__FUNCTION__,ret,account.Currency(),balance_dep_total,balance_dep_summ,account.Currency());
//--- return the result
   return(ret);
   /*
   Result:
   OnTester: Maximum balance drawdown in money: 5188.50 USD. Total deposits: 46. Amount of deposits: 5128.50 USD.
   final balance 4867.50 USD
   OnTester result 5188.5
   */
  }

```

See also

[TesterWithdrawal](/en/docs/common/testerwithdrawal)
