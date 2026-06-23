# Estimating the profit of a trading operation: OrderCalcProfit

One of the MQL5 API functions, OrderCalcProfit, allows you to pre-evaluate the financial result of a trading operation if the expected conditions are met. For example, using this function you can find out the amount of profit when reaching the Take Profit level, and the amount of loss when Stop Loss is triggered.

bool OrderCalcProfit(ENUM_ORDER_TYPE action, const string symbol, double volume,  

   double openPrice, double closePrice, double &profit)

The function calculates the profit or loss in the account currency for the current market environment based on the passed parameters.

The order type is specified in the action parameter. Only market orders ORDER_TYPE_BUY or ORDER_TYPE_SELL from the ENUM_ORDER_TYPE enumeration are allowed. The name of the financial instrument and its volume are passed in the parameters symbol and volume. The market entry and exit prices are set by the parameters openPrice and closePrice, respectively. The profit variable is passed by reference as the last parameter, and the profit value will be written in it.

The function returns an indicator of success (true) or error (false).

The formula for calculating the financial result used inside OrderCalcProfit depends on the symbol type.

| Identifier | Formula |
| --- | --- |
| SYMBOL_CALC_MODE_FOREX | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_CFD | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_CFDINDEX | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_CFDLEVERAGE | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_EXCH_STOCKS | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX | (ClosePrice - OpenPrice) * ContractSize * Lots |
| SYMBOL_CALC_MODE_FUTURES | (ClosePrice - OpenPrice) * Lots * TickPrice / TickSize |
| SYMBOL_CALC_MODE_EXCH_FUTURES | (ClosePrice - OpenPrice) * Lots * TickPrice / TickSize |
| SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS | (ClosePrice - OpenPrice) * Lots * TickPrice / TickSize |
| SYMBOL_CALC_MODE_EXCH_BONDS | Lots * ContractSize * (ClosePrice * FaceValue + AccruedInterest) |
| SYMBOL_CALC_MODE_EXCH_BONDS_MOEX | Lots * ContractSize * (ClosePrice * FaceValue + AccruedInterest) |
| SYMBOL_CALC_MODE_SERV_COLLATERAL | Lots * ContractSize * MarketPrice * LiqudityRate |

The following notation is used in the formulas:

- Lots — position volume in lots (contract shares)
- ContractSize — contract size (one lot, [SYMBOL_TRADE_CONTRACT_SIZE](/en/book/automation/symbols/symbols_volume))
- TickPrice — tick price ([SYMBOL_TRADE_TICK_VALUE](/en/book/automation/symbols/symbols_point_tick))
- TickSize — tick size ([SYMBOL_TRADE_TICK_SIZE](/en/book/automation/symbols/symbols_point_tick))
- MarketPrice — last known price [Bid/Ask](/en/book/automation/symbols/symbols_tick_parts) depending on the type of transaction
- OpenPrice — position opening price
- ClosePrice — position closing price
- FaceValue — face value of the bond (SYMBOL_TRADE_FACE_VALUE)
- LiqudityRate — liquidity ratio (SYMBOL_TRADE_LIQUIDITY_RATE)
- AccruedInterest — accumulated coupon income (SYMBOL_TRADE_ACCRUED_INTEREST)

The OrderCalcProfit function can only be used in Expert Advisors and scripts. To calculate potential profit/loss in indicators, you need to implement an alternative method, for example, independent calculations using formulas.

To bypass the restriction on the use of the OrderCalcProfit and [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin) functions in indicators, we have developed a set of functions that perform calculations using the formulas from this section, as well as the section [Margin requirements](/en/book/automation/symbols/symbols_margin). The functions are in the header file MarginProfitMeter.mqh, inside the common namespace MPM (from "Margin Profit Meter").

In particular, to calculate the financial result, it is important to have the value of one point of a particular instrument. In the above formulas, it indirectly participates in the difference between the opening and closing prices (ClosePrice - OpenPrice).

The function calculates the value of one price point PointValue.

```
namespace MPM
{
   double PointValue(const string symbol, const bool ask = false,
      const datetime moment = 0)
   {
      const double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
      const double contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE);
      const ENUM_SYMBOL_CALC_MODE m =
         (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);
      ...

```

At the beginning of the function, we request all the symbol properties needed for the calculation. Then, depending on the type of symbol, we obtain profit/loss in the currency of the profit of this instrument. Please note that there are no bonds here, the formulas of which take into account the nominal price and coupon income.

```
      double result = 0;
      switch(m)
      {
      case SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE:
      case SYMBOL_CALC_MODE_FOREX:
      case SYMBOL_CALC_MODE_CFD:
      case SYMBOL_CALC_MODE_CFDINDEX:
      case SYMBOL_CALC_MODE_CFDLEVERAGE:
      case SYMBOL_CALC_MODE_EXCH_STOCKS:
      case SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX:
         result = point * contract;
         break;
   
      case SYMBOL_CALC_MODE_FUTURES:
      case SYMBOL_CALC_MODE_EXCH_FUTURES:
      case SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS:
         result = point * SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
            / SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
         break;
      default:
         PrintFormat("Unsupported symbol %s trade mode: %s", symbol, EnumToString(m));
      }
      ...

```

Finally, we convert the amount to the account currency, if it differs.

```
      string account = AccountInfoString(ACCOUNT_CURRENCY);
      string current = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
   
      if(current != account)
      {
         if(!Convert(current, account, ask, result, moment)) return 0;
      }
     
      return result;
   }
   ...
};

```

The helper function Convert is used to convert amounts. It, in turn, depends on the FindExchangeRate function, which searches among all available symbols for one that contains the rate from the current currency into the account currency.

```
   bool Convert(const string current, const string account,
      const bool ask, double &margin, const datetime moment = 0)
   {
      string rate;
      int dir = FindExchangeRate(current, account, rate);
      if(dir == +1)
      {
         margin *= moment == 0 ?
            SymbolInfoDouble(rate, ask ? SYMBOL_BID : SYMBOL_ASK) :
            GetHistoricPrice(rate, moment, ask);
      }
      else if(dir == -1)
      {
         margin /= moment == 0 ?
            SymbolInfoDouble(rate, ask ? SYMBOL_ASK : SYMBOL_BID) :
            GetHistoricPrice(rate, moment, ask);
      }
      else
      {
         static bool once = false;
         if(!once)
         {
            Print("Can't convert ", current, " -> ", account);
            once = true;
         }
      }
      return true;
   }

```

The FindExchangeRate function looks up characters in Market Watch and returns the name of the first matching Forex symbol, if there are several of them, in the result parameter. If the quote corresponds to the direct order of currencies "current/account", the function will return +1, and if the opposite, it will be "account/current", i.e. -1.

```
   int FindExchangeRate(const string current, const string account, string &result)
   {
      for(int i = 0; i < SymbolsTotal(true); i++)
      {
         const string symbol = SymbolName(i, true);
         const ENUM_SYMBOL_CALC_MODE m =
            (ENUM_SYMBOL_CALC_MODE)SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE);
         if(m == SYMBOL_CALC_MODE_FOREX || m == SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE)
         {
            string base = SymbolInfoString(symbol, SYMBOL_CURRENCY_BASE);
            string profit = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT);
            if(base == current && profit == account)
            {
               result = symbol;
               return +1;
            }
            else
            if(base == account && profit == current)
            {
               result = symbol;
               return -1;
            }
         }
      }
      return 0;
   }

```

The full code of the functions can be found in the attached file MarginProfitMeter.mqh.

Let's check the performance of the OrderCalcProfit function and the group of functions MPM with a test script ProfitMeter.mq5: we will calculate the profit/loss estimate for virtual trades for all symbols of the Market Watch, and we will do it using two methods: built-in and ours.

In the input parameters of the script, you can select the type of operation Action (buy or sell), lot size Lot and the position holding time in bars Duration. The financial result is calculated for the quotes of the last Duration bars of the current timeframe.

```
#property script_show_inputs
   
input ENUM_ORDER_TYPE Action = ORDER_TYPE_BUY; // Action (only Buy/Sell allowed)
input float Lot = 1;
input int Duration = 20; // Duration (bar number in past)

```

In the body of the script, we connect the header files and display the header with the parameters.

```
#include <MQL5Book/MarginProfitMeter.mqh>
#include <MQL5Book/Periods.mqh>
   
void OnStart()
{
   // guarantee that the operation will only be a buy or a sell
   ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)(Action % 2);
   const string text[] = {"buying", "selling"};
   PrintFormat("Profits/Losses for %s %s lots"
      " of %d symbols in Market Watch on last %d bars %s",
      text[type], (string)Lot, SymbolsTotal(true),
      Duration, PeriodToString(_Period));
   ...

```

Then, in a loop through symbols, we perform the calculations in two ways and print the results for comparison.

```
   for(int i = 0; i < SymbolsTotal(true); i++)
   {
      const string symbol = SymbolName(i, true);
      const double enter = iClose(symbol, _Period, Duration);
      const double exit = iClose(symbol, _Period, 0);
      
      double profit1, profit2; // 2 adopted variables
      
      // standard method 
      if(!OrderCalcProfit(type, symbol, Lot, enter, exit, profit1))
      {
         PrintFormat("OrderCalcProfit(%s) failed: %d", symbol, _LastError);
         continue;
      }
      
      // our own method 
      const int points = (int)MathRound((exit - enter)
         / SymbolInfoDouble(symbol, SYMBOL_POINT));
      profit2 = Lot * points * MPM::PointValue(symbol);
      profit2 = NormalizeDouble(profit2,
         (int)AccountInfoInteger(ACCOUNT_CURRENCY_DIGITS));
      if(type == ORDER_TYPE_SELL) profit2 *= -1;
      
      // output to the log for comparison
      PrintFormat("%s: %f %f", symbol, profit1, profit2);
   }
}

```

Try running the script for different accounts and instrument sets.

```
Profits/Losses for buying 1.0 lots of 13 symbols in Market Watch on last 20 bars H1
EURUSD: 390.000000 390.000000
GBPUSD: 214.000000 214.000000
USDCHF: -254.270000 -254.270000
USDJPY: -57.930000 -57.930000
USDCNH: -172.570000 -172.570000
USDRUB: 493.360000 493.360000
AUDUSD: 84.000000 84.000000
NZDUSD: 13.000000 13.000000
USDCAD: -97.480000 -97.480000
USDSEK: -682.910000 -682.910000
XAUUSD: -1706.000000 -1706.000000
SP500m: 5300.000000 5300.000000
XPDUSD: -84.030000 -84.030000

```

Ideally, the numbers in each line should match.
