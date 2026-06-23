# Checking if a symbol exists

Instead of looking through the entire list of symbols, an MQL program can check for the presence of a particular symbol by its name. For this purpose, there is the SymbolExist function.

bool SymbolExist(const string name, bool &isCustom)

In the name parameter, you should pass the name of the desired symbol. The isCustom parameter passed by reference will be set by the function according to whether the specified symbol is standard (false) or custom (true).

The function returns false if the symbol is not found in either the standard or custom symbols.

A partial analog of this function is the [SYMBOL_EXIST](/en/book/automation/symbols/symbols_state) property query.

Let's analyze the simple script SymbolExists.mq5 to test this feature. In its parameter, the user can specify the name, which is then passed to SymbolExist, and the result is logged. If an empty string is input, the working symbol of the current chart will be checked. By default, the parameter is set to "XYZ", which presumably does not match any of the available symbols.

```
#property script_show_inputs
   
input string SymbolToCheck = "XYZ";
   
void OnStart()
{
   const string _SymbolToCheck = SymbolToCheck == "" ? _Symbol : SymbolToCheck;
   bool custom = false;
   PrintFormat("Symbol '%s' is %s", _SymbolToCheck,
      (SymbolExist(_SymbolToCheck, custom) ? (custom ? "custom" : "standard") : "missing"));
}

```

When the script is run two times, first with the default value and then with an empty line on the EURUSD chart, we will get the following entries in the log.

```
Symbol 'XYZ' is missing
Symbol 'EURUSD' is standard

```

If you already have custom symbols or create a new one with a simple calculation formula, you can make sure the custom variable is populated. For example, if you open the Symbols window in the terminal and press the Create symbol button, you can enter "SP500/FTSE100" (index names may differ for your broker) in the Synthetic tool formula field and "GBPUSD.INDEX" in the field with the Symbol name. A click on OK will create a custom instrument for which you can open a chart, and our script should display the following on it:

```
Symbol 'GBPUSD.INDEX' is custom

```

When setting up your own symbol, do not forget to set not only the formula but also sufficiently "small" values for the point size and the price change step (tick). Otherwise, the series of synthetic quotes may turn out to be "stepped", or even degenerate into a straight line.
