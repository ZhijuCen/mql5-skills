# TesterWithdrawal

The special function to emulate the operation of money withdrawal in the process of testing. Can be used in some asset management systems.

```
bool  TesterWithdrawal(
   double money      // the sum to withdraw
   );

```

Parameters

money

[in]  The sum of money that we need to withdraw (in the deposit currency).

Return Value

If successful, returns true, otherwise - false.

Example:

```
//--- defines
#define BALANCE_PROFIT_WITHDRAWAL   5  // the value of the balance profit, at which funds are withdrawn from the account in the tester
 
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
double      balance_op_sum;            // total amount of balance operations
uint        balance_op_total;          // number of balance operations
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   ...
//--- save the initial balance values
   balance_prev=account.Balance();
   balance_op_sum=0;
   balance_op_total=0;
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
 
//--- if the balance profit exceeds the current balance by the value specified in the BALANCE_PROFIT_WITHDRAWAL macro substitution,
//--- it is necessary to withdraw these funds from the account. Call the TesterWithdrawal() function.
//--- check the balance profit for exceeding BALANCE_PROFIT_WITHDRAWAL
   if(balance_prev!=account.Balance())
     {
      if(account.Balance()>balance_prev+BALANCE_PROFIT_WITHDRAWAL)
        {
         double profit=account.Balance()-balance_prev;
         PrintFormat("The account balance has been increased by %.2f %s. Need to withdraw these funds from the account.",profit,account.Currency());
         if(TesterWithdrawal(profit))
           {
            balance_op_total++;
            balance_op_summ+=profit;
            balance_prev=account.Balance();
            PrintFormat("Funds have been withdrawn from the account. Account balance: %.2f %s.",account.Balance(),account.Currency());
            PrintFormat("Total withdrawals: %lu. Amount of withdrawals: %.2f %s.",balance_op_total,balance_op_summ,account.Currency());
           }
         /*
         Result:
         The account balance has been increased by 21.00 USD. Need to withdraw these funds from the account.
         deal #13 balance -21.00 [withdrawal] done
         Funds have been withdrawn from the account. Account balance: 10000.00 USD.
         Total withdrawals: 1. Amount of withdrawals: 21.00 USD.
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
//--- display a message about the drawdown, the number of withdrawals and their total amount in the log
   PrintFormat("%s: Maximum balance drawdown in money: %.2f %s. Total withdrawals: %lu. Amount of withdrawals: %.2f %s.",__FUNCTION__,ret,account.Currency(),balance_op_total,balance_op_summ,account.Currency());
//--- return the result
   return(ret);
   /*
   Result:
   OnTester: Maximum balance drawdown in money: 5188.50 USD. Total withdrawals: 2. Amount of withdrawals: 36.00 USD.
   final balance 4867.50 USD
   OnTester result 5188.5
   */
  }

```

See also

[TesterDeposit](/en/docs/common/testerdeposit)
