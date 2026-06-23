# Margin requirements

Among the most important information about a financial instrument for a trader is the amount of funds required to open a position. Without knowing how much money is needed to buy or sell a given number of lots, it is impossible to implement a money management system within an Expert Advisor and control the account balance.

Since MetaTrader 5 is used to trade various instruments (currencies, commodities, stocks, bonds, options, and futures), the margin calculation principles differ significantly. The documentation provides details, in particular for [Forex and futures](https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_forex), as well as [exchanges](https://www.metatrader5.com/en/terminal/help/trading_advanced/margin_exchange).

Several properties of the MQL5 API allow you to define the type of market and the method of calculating the margin for a specific instrument.

Looking ahead, let's say that for a given combination of parameters such as the trading operation type, instrument, volume, and price, MQL5 allows you to calculate the margin using the [OrderCalcMargin](/en/book/automation/experts/experts_ordercalcmargin) function. This is the simplest method, but it has a significant limitation: the function does not take into account current open positions and pending orders. This, in particular, ignores possible adjustments for overlapping volumes when opposite positions are allowed on the account.

Thus, in order to obtain a breakdown of the account funds currently used as a margin for open positions and orders, an MQL program may need to analyze the following properties and calculations using formulas. Furthermore, the OrderCalcMargin function is prohibited for use in indicators. You can estimate the free margin in advance after the proposed transaction is completed using [OrderCheck](/en/book/automation/experts/experts_ordercheck).

| Identifier | Description |
| --- | --- |
| SYMBOL_TRADE_CALC_MODE | The method for calculating margin and profit (see ENUM_SYMBOL_CALC_MODE) |
| SYMBOL_MARGIN_HEDGED_USE_LEG | Boolean flag to enable (true) or disable (false) the hedged margin calculation mode for the largest of the overlapped positions (buy and sell) |
| SYMBOL_MARGIN_INITIAL | Initial margin for an exchange instrument |
| SYMBOL_MARGIN_MAINTENANCE | Maintenance margin for an exchange instrument |
| SYMBOL_MARGIN_HEDGED | Contract size or margin for one lot of covered positions (opposite positions for one symbol) |

The first two properties are included in the ENUM_SYMBOL_INFO_INTEGER enumeration, and the last three are in ENUM_SYMBOL_INFO_DOUBLE, and they can be read, respectively, by functions [SymbolInfoInteger](/en/book/automation/symbols/symbols_info) and [SymbolInfoDouble](/en/book/automation/symbols/symbols_info).

Specific margin calculation formulas depend on the SYMBOL_TRADE_CALC_MODE property and are shown in the table below. More complete information can be found in [MQL5 documentation](https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants#enum_symbol_calc_mode).

Please note that initial and maintenance margins are not used for Forex instruments, and these properties are always 0 for them.

The initial margin indicates the amount of required security deposit in [margin currency](/en/book/automation/symbols/symbols_currencies) to open a position with a volume of one [lot](/en/book/automation/symbols/symbols_volume). It is used when checking the sufficiency of the client's funds before entering the market. To get the final amount of margin charged depending on the type and direction of the order, check the margin ratios using the [SymbolInfoMarginRate](/en/book/automation/symbols/symbols_margin_rates) function. Thus, the broker can set an individual leverage or discount for each instrument.

The maintenance margin indicates the minimum value of funds in the instrument's margin currency to maintain an open position of one lot. It is used when checking the sufficiency of the client's funds when the account status (trading conditions) changes. If the level of funds falls below the amount of the maintenance margin of all positions, the broker will start to close them forcibly.

If the maintenance margin property is 0, then the initial margin is used. As in the case of the initial margin, to obtain the final amount of margin charged depending on the type and direction, you should check the margin ratios using the SymbolInfoMarginRate function.

Hedged positions, that is, multidirectional positions for the same symbol, can only exist on [hedging](/en/book/automation/account/account_netting_hedge) trading accounts. Obviously, the calculation of the hedged margin together with the properties SYMBOL_MARGIN_HEDGED_USE_LEG, SYMBOL_MARGIN_HEDGED make sense only on such accounts. The hedged margin is applied for the covered volume.

The broker can choose for each instrument one of the two existing methods for calculating the margin for covered positions:

- The base calculation is applied when the longest side calculation mode is disabled, i.e. the SYMBOL_MARGIN_HEDGED_USE_LEG property is equal to false. In this case, the margin consists of three components: the margin for the uncovered volume of the existing position, the margin for the covered volume (if there are opposite positions and the SYMBOL_MARGIN_HEDGED property is non-zero), the margin for pending orders. If the initial margin is set for the instrument (the SYMBOL_MARGIN_INITIAL property is non-zero), then the hedged margin is specified as an absolute value (in money). If the initial margin is not set (equal to 0), then SYMBOL_MARGIN_HEDGED specifies the contract size that will be used when calculating the margin according to the formula corresponding to the type of trading instrument (SYMBOL_TRADE_CALC_MODE).
- The highest position calculation is applied when the SYMBOL_MARGIN_HEDGED_USE_LEG property is equal to true. The value of SYMBOL_MARGIN_HEDGED is ignored in this case. Instead, the volume of all short and long positions on the instrument is calculated, and the weighted average opening price is calculated for each side. Further, using the formulas corresponding to the instrument type (SYMBOL_TRADE_CALC_MODE), the margin for the short side and the long side is calculated. The largest value is used as the final value.

The following table lists the ENUM_SYMBOL_CALC_MODE elements and their respective margin calculation methods. The same property (SYMBOL_TRADE_CALC_MODE) is also responsible for calculating the profit/loss of a position, but we will consider this aspect later, in the chapter on MQL5 trading functions.

| Identifier | Formula |
| --- | --- |
| SYMBOL_CALC_MODE_FOREX 
 Forex | Lots * ContractSize * MarginRate / Leverage |
| SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE 
 Forex without leverage | Lots * ContractSize * MarginRate |
| SYMBOL_CALC_MODE_CFD 
 CFD | Lots * ContractSize * MarketPrice * MarginRate |
| SYMBOL_CALC_MODE_CFDLEVERAGE 
 CFD with leverage | Lots * ContractSize * MarketPrice * MarginRate / Leverage |
| SYMBOL_CALC_MODE_CFDINDEX 
 CFDs on indices | Lots * ContractSize * MarketPrice * TickPrice / TickSize * MarginRate |
| SYMBOL_CALC_MODE_EXCH_STOCKS 
 Securities on the stock exchange | Lots * ContractSize * LastPrice * MarginRate |
| SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX 
 Securities on MOEX | Lots * ContractSize * LastPrice * MarginRate |
| SYMBOL_CALC_MODE_FUTURES 
 Futures | Lots * InitialMargin * MarginRate |
| SYMBOL_CALC_MODE_EXCH_FUTURES 
 Futures on the stock exchange | Lots * InitialMargin * MarginRate                  or  
 Lots * MaintenanceMargin * MarginRate |
| SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS 
 Futures on FORTS | Lots * InitialMargin * MarginRate                  or  
 Lots * MaintenanceMargin * MarginRate |
| SYMBOL_CALC_MODE_EXCH_BONDS 
 Bonds on the stock exchange | Lots * ContractSize * FaceValue * OpenPrice / 100 |
| SYMBOL_CALC_MODE_EXCH_BONDS_MOEX 
 Bonds on MOEX | Lots * ContractSize * FaceValue * OpenPrice / 100 |
| SYMBOL_CALC_MODE_SERV_COLLATERAL | Non-tradable asset (margin not applicable) |

The following notation is used in the formulas:

- Lots — position or order volume in lots (shares of the contract)
- ContractSize — contract size (one lot, [SYMBOL_TRADE_CONTRACT_SIZE](/en/book/automation/symbols/symbols_volume))
- Leverage — trading account leverage ([ACCOUNT_LEVERAGE](/en/book/automation/account/account_margin))
- InitialMargin — initial margin (SYMBOL_MARGIN_INITIAL)
- MaintenanceMargin — maintenance margin (SYMBOL_MARGIN_MAINTENANCE)
- TickPrice — tick price ([SYMBOL_TRADE_TICK_VALUE](/en/book/automation/symbols/symbols_point_tick))
- TickSize —  tick size ([SYMBOL_TRADE_TICK_SIZE](/en/book/automation/symbols/symbols_point_tick))
- MarketPrice — last known [Bid/Ask](/en/book/automation/symbols/symbols_tick_parts) price depending on the type of transaction
- LastPrice — last known [Last](/en/book/automation/symbols/symbols_tick_parts) price
- OpenPrice — weighted average price of a position or order opening
- FaceValue — face value of the bond
- MarginRate — margin ratio according to the [SymbolInfoMarginRate](/en/book/automation/symbols/symbols_margin_rates) function, can also have 2 different values: for initial and maintenance margin

An alternative implementation of formula calculations for most types of symbols is given in the file MarginProfitMeter.mqh (see section [Estimating the profit of a trading operation](/en/book/automation/experts/experts_ordercalcprofit)). It can also be used in indicators.

Let's make a couple of comments on some modes.

In the table above, only three of the futures formulas use the initial margin (SYMBOL_MARGIN_INITIAL). However, if this property has a non-zero value in the specification of any other symbol, then it determines the margin.

Some exchanges may impose their own specifics on margin adjustment, such as the discount system for FORTS (SYMBOL_CALC_MODE_EXCH_FUTURES_FORTS). See the MQL5 documentation and your broker for details.

In the SYMBOL_CALC_MODE_SERV_COLLATERAL mode, the value of an instrument is taken into account in Assets, which are added to Equity. Thus, open positions on such an instrument increase the amount of Free Margin and serve as an additional collateral for open positions on traded instruments. The market value of an open position is calculated based on the volume, contract size, current market price, and liquidity ratio: Lots * ContractSize * MarketPrice * LiquidityRate (the latter value can be obtained as the SYMBOL_TRADE_LIQUIDITY_RATE property).

As an example of working with margin-related properties, consider the script SymbolFilterMarginStats.mq5. Its purpose will be to calculate statistics on margin calculation methods in the list of selected symbols, as well as optionally log these properties for each symbol. We will select symbols for analysis using the already known filter class SymbolFilter and conditions for it supplied from the input variables.

```
#include <MQL5Book/SymbolFilter.mqh>
   
input bool UseMarketWatch = false;
input bool ShowPerSymbolDetails = false;
input bool ExcludeZeroInitMargin = false;
input bool ExcludeZeroMainMargin = false;
input bool ExcludeZeroHedgeMargin = false;

```

By default, information is requested for all available symbols. To limit the context to the market overview only, we should set UseMarketWatch to true.

Parameter ShowPerSymbolDetails allows you to enable the output of detailed information about each symbol (by default, the parameter is false, and only statistics are displayed).

The last three parameters are intended for filtering symbols according to the conditions of zero margin values (initial, maintenance, and hedging, respectively).

To collect and conveniently display in the log a complete set of properties for each symbol (when the ShowPerSymbolDetails is on), the structure MarginSettings is defined in the code.

```
struct MarginSettings
{
   string name;
   ENUM_SYMBOL_CALC_MODE calcMode;
   bool hedgeLeg;
   double initial;
   double maintenance;
   double hedged;
};

```

Since some of the properties are integer (SYMBOL_TRADE_CALC_MODE, SYMBOL_MARGIN_HEDGED_USE_LEG), and some are real (SYMBOL_MARGIN_INITIAL, SYMBOL_MARGIN_MAINTENANCE, SYMBOL_MARGIN_HEDGED), they will have to be requested by the filter object separately.

Now let's go directly to the working code in OnStart. Here, as usual, we define the filter object (f), output arrays for character names (symbols), and values of requested properties (flags,values). In addition to them, we add an array of structures MarginSettings.

```
void OnStart()
{
   SymbolFilter f;                // filter object
   string symbols[];              // array for names
   long flags[][2];               // array for integer vectors
   double values[][3];            // array for real vectors
   MarginSettings margins[];      // composite output array
   ...

```

The stats array map has been introduced to calculate statistics with a key like ENUM_SYMBOL_CALC_MODE and the int integer value for the number of times each method was encountered. Also, all cases of zero margin and the enabled calculation mode on the longer leg should be recorded in the corresponding counter variables.

```
   MapArray<ENUM_SYMBOL_CALC_MODE,int> stats; // counters for each method/mode
   int hedgeLeg = 0;                          // and other counters
   int zeroInit = 0;                          // ...
   int zeroMaintenance = 0;
   int zeroHedged = 0;
   ...

```

Next, we specify the properties of interest to us which are related to the margin, which will be read from the symbol settings. First, integers in the ints array and then the real ones in the doubles array.

```
   ENUM_SYMBOL_INFO_INTEGER ints[] =
   {
      SYMBOL_TRADE_CALC_MODE,
      SYMBOL_MARGIN_HEDGED_USE_LEG
   };
   
   ENUM_SYMBOL_INFO_DOUBLE doubles[] =
   {
      SYMBOL_MARGIN_INITIAL,
      SYMBOL_MARGIN_MAINTENANCE,
      SYMBOL_MARGIN_HEDGED
   };
   ...

```

Depending on the input parameters, we will set the filtering conditions.

```
   if(ExcludeZeroInitMargin) f.let(SYMBOL_MARGIN_INITIAL, 0, SymbolFilter::IS::GREATER);
   if(ExcludeZeroMainMargin) f.let(SYMBOL_MARGIN_MAINTENANCE, 0, SymbolFilter::IS::GREATER);
   if(ExcludeZeroHedgeMargin) f.let(SYMBOL_MARGIN_HEDGED, 0, SymbolFilter::IS::GREATER);
   ...

```

Now everything is ready for selecting symbols by conditions and getting their properties into arrays. We do this twice, separately for integer and real properties.

```
   f.select(UseMarketWatch, ints, symbols, flags);
   const int n = ArraySize(symbols);
   ArrayResize(symbols, 0, n);
   f.select(UseMarketWatch, doubles, symbols, values);
   ...

```

An array with symbols has to be zeroed out after the first application of the filter so that the names do not double up. Despite two separate queries, the order of elements in all output arrays (ints and doubles) is the same, since the filtering conditions do not change.

If a detailed log is enabled by the user, we allocate memory for the margins array of structures.

```
   if(ShowPerSymbolDetails) ArrayResize(margins, n);

```

Finally, we calculate the statistics by iterating over all the elements of the resulting arrays and optionally populate the array of structures.

```
   for(int i = 0; i < n; ++i)
   {
      stats.inc((ENUM_SYMBOL_CALC_MODE)flags[i].value[0]);
      hedgeLeg += (int)flags[i].value[1];
      if(values[i].value[0] == 0) zeroInit++;
      if(values[i].value[1] == 0) zeroMaintenance++;
      if(values[i].value[2] == 0) zeroHedged++;
      
      if(ShowPerSymbolDetails)
      {
         margins[i].name = symbols[i];
         margins[i].calcMode = (ENUM_SYMBOL_CALC_MODE)flags[i][0];
         margins[i].hedgeLeg = (bool)flags[i][1];
         margins[i].initial = values[i][0];
         margins[i].maintenance = values[i][1];
         margins[i].hedged = values[i][2];
      }
   }
   ...

```

Now we display the statistics in the log.

```
   PrintFormat("===== Margin calculation modes for %s symbols %s=====",
      (UseMarketWatch ? "Market Watch" : "all available"),
      (ExcludeZeroInitMargin || ExcludeZeroMainMargin || ExcludeZeroHedgeMargin
         ? "(with conditions) " : ""));
   PrintFormat("Total symbols: %d", n);
   PrintFormat("Hedge leg used in: %d", hedgeLeg);
   PrintFormat("Zero margin counts: initial=%d, maintenance=%d, hedged=%d",
      zeroInit, zeroMaintenance, zeroHedged);
   
   Print("Stats per calculation mode:");
   stats.print();
   ...

```

Since the members of the ENUM_SYMBOL_CALC_MODE enumeration are displayed as integers (which is not very informative), we also display a text where each value has a name (from EnumToString).

```
   Print("Legend: key=calculation mode, value=count");
   for(int i = 0; i < stats.getSize(); ++i)
   {
      PrintFormat("%d -> %s", stats.getKey(i), EnumToString(stats.getKey(i)));
   }
   ...

```

If detailed information on the selected characters is required, we output the margins array of structures.

```
   if(ShowPerSymbolDetails)
   {
      Print("Settings per symbol:");
      ArrayPrint(margins);
   }
}

```

Let's run the script a couple of times with different settings. Let's start with the default settings.

```
===== Margin calculation modes for all available symbols =====
Total symbols: 131
Hedge leg used in: 14
Zero margin counts: initial=123, maintenance=130, hedged=32
Stats per calculation mode:
    [key] [value]
[0]     0     101
[1]     4      16
[2]     1       1
[3]     2      11
[4]     5       2
Legend: key=calculation mode, value=count
0 -> SYMBOL_CALC_MODE_FOREX
4 -> SYMBOL_CALC_MODE_CFDLEVERAGE
1 -> SYMBOL_CALC_MODE_FUTURES
2 -> SYMBOL_CALC_MODE_CFD
5 -> SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE

```

For the second run, let's set ShowPerSymbolDetails and ExcludeZeroInitMargin to true. This requests detailed information about all symbols that have a non-zero value of the initial margin.

```
===== Margin calculation modes for all available symbols (with conditions) =====
Total symbols: 8
Hedge leg used in: 0
Zero margin counts: initial=0, maintenance=7, hedged=0
Stats per calculation mode:
    [key] [value]
[0]     0       5
[1]     1       1
[2]     5       2
Legend: key=calculation mode, value=count
0 -> SYMBOL_CALC_MODE_FOREX
1 -> SYMBOL_CALC_MODE_FUTURES
5 -> SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE
Settings per symbol:
      [name] [calcMode] [hedgeLeg]    [initial] [maintenance]    [hedged]
[0] "XAUEUR"          0      false    100.00000       0.00000    50.00000
[1] "XAUAUD"          0      false    100.00000       0.00000   100.00000
[2] "XAGEUR"          0      false   1000.00000       0.00000  1000.00000
[3] "USDGEL"          0      false 100000.00000  100000.00000 50000.00000
[4] "SP500m"          1      false   6600.00000       0.00000  6600.00000
[5] "XBRUSD"          5      false    100.00000       0.00000    50.00000
[6] "XNGUSD"          0      false  10000.00000       0.00000 10000.00000
[7] "XTIUSD"          5      false    100.00000       0.00000    50.00000

```
