# symbols_get

Get all financial instruments from the MetaTrader 5 terminal.

```
symbols_get(
   group="GROUP"      // symbol selection filter 
)

```

group="GROUP"

[in]  The filter for arranging a group of necessary symbols. Optional parameter. If the group is specified, the function returns only symbols meeting a specified criteria.

Return Value

Return symbols in the form of a tuple. Return None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

The group parameter allows sorting out symbols by name. '*' can be used at the beginning and the end of a string.

The group parameter can be used as a named or an unnamed one. Both options work the same way. The named option (group="GROUP") makes the code easier to read.

The group parameter may contain several comma separated conditions. A condition can be set as a mask using '*'. The logical negation symbol '!' can be used for an exclusion. All conditions are applied sequentially, which means conditions of including to a group should be specified first followed by an exclusion condition. For example, group="*, !EUR" means that all symbols should be selected first and the ones containing "EUR" in their names should be excluded afterwards.

Unlike [symbol_info()](/en/docs/python_metatrader5/mt5symbolinfo_py), the symbols_get() function returns data on all requested symbols within a single call.

Example:

```
import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# get all symbols
symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))
count=0
# display the first five ones
for s in symbols:
    count+=1
    print("{}. {}".format(count,s.name))
    if count==5: break
print()
 
# get symbols containing RU in their names
ru_symbols=mt5.symbols_get("*RU*")
print('len(*RU*): ', len(ru_symbols))
for s in ru_symbols:
    print(s.name)
print()
 
# get symbols whose names do not contain USD, EUR, JPY and GBP
group_symbols=mt5.symbols_get(group="*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(group_symbols))
for s in group_symbols:
    print(s.name,":",s)
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
Symbols:  84
1. EURUSD
2. GBPUSD
3. USDCHF
4. USDJPY
5. USDCNH
 
len(*RU*):  8
EURUSD
USDRUB
USDRUR
EURRUR
EURRUB
FORTS.RUB.M5
EURUSD_T20
EURUSD4
 
len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):  13
AUDCAD : SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session...
AUDCHF : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
AUDNZD : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
CADCHF : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
NZDCAD : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
NZDCHF : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
NZDSGD : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
CADMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
CHFMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
NZDMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi...
FORTS.RTS.M5 : SymbolInfo(custom=True, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, ...
FORTS.RUB.M5 : SymbolInfo(custom=True, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, ...
FOREX.CHF.M5 : SymbolInfo(custom=True, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, ...

```

See also

[symbols_total](/en/docs/python_metatrader5/mt5symbolstotal_py), [symbol_select](/en/docs/python_metatrader5/mt5symbolselect_py), [symbol_info](/en/docs/python_metatrader5/mt5symbolinfo_py)
