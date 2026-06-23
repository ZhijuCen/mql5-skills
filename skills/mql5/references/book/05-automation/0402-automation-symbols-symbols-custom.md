# Custom symbol properties

In the introduction to this chapter, we mentioned [custom symbols](/en/book/advanced/custom_symbols). These are the symbols with the quotes created directly in the terminal at the user's command or programmatically.

Custom symbols can be used, for example, to create a synthetic instrument based on a formula that includes other Market Watch symbols. This is available to the user directly in the [terminal interface](https://www.metatrader5.com/en/terminal/help/trading_advanced/custom_instruments).

An MQL program can implement more complex scenarios in MQL5, such as merging different instruments for different periods, generating series according to a given random distribution, or receiving data (quotes, bars, or ticks) from external sources.

In order to be able to distinguish a standard symbol from a custom symbol in algorithms, MQL5 provides the SYMBOL_CUSTOM property, which is a logical sign that a symbol is custom.

If the symbol has a formula, it is available through the SYMBOL_FORMULA string property. In formulas, as you know, you can use the names of other symbols, as well as mathematical functions and operators. Here are some examples:

- Synthetic symbol: "@ESU19"/EURCAD
- Calendar spread: "Si-9.13"-"Si-6.13"
- Euro index: 34.38805726 * pow(EURUSD,0.3155) * pow(EURGBP,0.3056) * pow(EURJPY,0.1891) * pow(EURCHF,0.1113) * pow(EURSEK,0.0785)

Specifying a formula is convenient for the user, but usually not used from MQL programs since they can calculate formulas directly in the code, with non-standard functions and with more control, in particular, on each tick and not on a timer 1 time per 100ms.

Let's check the work with properties in the script SymbolFilterCustom.mq5: it logs all custom symbols and their formulas (if any).

```
input bool UseMarketWatch = false;
   
void OnStart()
{
   SymbolFilter f;                // filter object
   string symbols[];              // array for symbol names
   string formulae[];             // array for formulas
   
 // apply filter and fill arrays
   f.let(SYMBOL_CUSTOM, true)
   .select(UseMarketWatch, SYMBOL_FORMULA, symbols, formulae);
   const int n = ArraySize(symbols);
   
   PrintFormat("===== %s custom symbols =====",
      (UseMarketWatch ? "Market Watch" : "All available"));
   PrintFormat("Total symbols: %d", n);
   
   for(int i = 0; i < n; ++i)
   {
      Print(symbols[i], " ", formulae[i]);
   }
}

```

Below is the result with the only custom character found.

```
===== All available custom symbols =====
Total symbols: 1
synthEURUSD SP500m/UK100

```
