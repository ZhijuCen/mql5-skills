# StringFind

Search for a substring in a string.

```
int  StringFind(
   string  string_value,        // string in which search is made
   string  match_substring,     // what is searched
   int     start_pos=0          // from what position search starts
   );

```

Parameters

string_value

[in]  String, in which search is made.

match_substring

[in]  Searched substring.

start_pos=0

[in]  Position in the string from which search is started.

Return Value

Returns position number in a string, from which the searched substring starts, or -1, if the substring is not found.

Example:

```
#define   RESERVE    100
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the symbol base currency and the profit currency
   string symbol_currency_base  =SymbolInfoString(Symbol(), SYMBOL_CURRENCY_BASE);
   string symbol_currency_profit=SymbolInfoString(Symbol(), SYMBOL_CURRENCY_PROFIT);
   PrintFormat("Symbol Currency Base: %s\nSymbol Currency Profit: %s", symbol_currency_base, symbol_currency_profit);
   
//--- in the loop through all symbols available on the server
   int total=SymbolsTotal(false), pos=-1;
   for(int i=0; i<total; i++)
     {
      //--- get the name of the next symbol
      string name=SymbolName(i, false);
      
      //--- look for a substring in the symbol name with the name of the base currency and
      //--- if a substring is found, display the symbol name, its index in the currency list and the name of the searched currency in the log
      pos = StringFind(name, symbol_currency_base);
      if(pos >= 0)
         PrintFormat("The '%s' symbol at index %u in the list contains the '%s' currency. Substring position in the symbol name: %d", name, i, symbol_currency_base, pos);
         
      //--- look for a substring in the symbol name with the name of the quoted currency and
      //--- if a substring is found, display the symbol name, its index in the currency list and the name of the searched currency in the log
      pos = StringFind(name, symbol_currency_profit);
      if(pos >= 0)
         PrintFormat("The '%s' symbol at index %u in the list contains the '%s' currency. Substring position in the symbol name: %d", name, i, symbol_currency_profit, pos);
     }
      
   /*
   Result
   StringFind (EURUSD,D1)   Symbol Currency Base: EUR
   StringFind (EURUSD,D1)   Symbol Currency Profit: USD
   The 'EURUSD' symbol at index 0 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURUSD' symbol at index 0 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'GBPUSD' symbol at index 1 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'USDCHF' symbol at index 2 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDJPY' symbol at index 3 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDCNH' symbol at index 4 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDRUB' symbol at index 5 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'AUDUSD' symbol at index 6 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'NZDUSD' symbol at index 7 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'USDCAD' symbol at index 8 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDSEK' symbol at index 9 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDHKD' symbol at index 10 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDSGD' symbol at index 11 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDNOK' symbol at index 12 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDDKK' symbol at index 13 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDTRY' symbol at index 14 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDZAR' symbol at index 15 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDCZK' symbol at index 16 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDHUF' symbol at index 17 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDPLN' symbol at index 18 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDRUR' symbol at index 19 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'EURAUD' symbol at index 27 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURCAD' symbol at index 28 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURCHF' symbol at index 29 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURCZK' symbol at index 30 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURDKK' symbol at index 31 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURGBP' symbol at index 32 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURHKD' symbol at index 33 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURHUF' symbol at index 34 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURJPY' symbol at index 35 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURNOK' symbol at index 36 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURNZD' symbol at index 37 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURPLN' symbol at index 38 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURRUR' symbol at index 39 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURRUB' symbol at index 40 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURSEK' symbol at index 41 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURTRY' symbol at index 42 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURZAR' symbol at index 43 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'XAUUSD' symbol at index 47 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'XAUEUR' symbol at index 48 in the list contains the 'EUR' currency. Substring position in the symbol name: 3
   The 'XAGUSD' symbol at index 50 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'XAGEUR' symbol at index 51 in the list contains the 'EUR' currency. Substring position in the symbol name: 3
   The 'USDCRE' symbol at index 53 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'XPDUSD' symbol at index 65 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'XPTUSD' symbol at index 66 in the list contains the 'USD' currency. Substring position in the symbol name: 3
   The 'USDGEL' symbol at index 67 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDMXN' symbol at index 68 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'EURMXN' symbol at index 69 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'USDCOP' symbol at index 75 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDARS' symbol at index 76 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDCLP' symbol at index 77 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'EURSGD' symbol at index 89 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'USDILS' symbol at index 95 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDTHB' symbol at index 122 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'USDRMB' symbol at index 123 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   The 'EURILS' symbol at index 126 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'EURCNH' symbol at index 137 in the list contains the 'EUR' currency. Substring position in the symbol name: 0
   The 'USDBRL' symbol at index 139 in the list contains the 'USD' currency. Substring position in the symbol name: 0
   */
  }

```

See also

[StringSubstr](/en/docs/strings/stringsubstr), [StringGetCharacter](/en/docs/strings/stringgetcharacter), [StringLen](/en/docs/strings/stringlen), [StringLen](/en/docs/strings/stringlen)
