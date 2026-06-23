# Getting information about financial instruments

The group of functions of the MetaTrader5 package provides information about financial instruments.

The symbol_info function returns information about one financial instrument as a named tuple structure.

namedtuple symbol_info(symbol)

The name of the desired financial instrument is specified in the symbol parameter.

One call provides all the information that can be obtained using three MQL5 functions [SymbolInfoInteger](/en/book/automation/symbols/symbols_info), [SymbolInfoDouble](/en/book/automation/symbols/symbols_info), and [SymbolInfoString](/en/book/automation/symbols/symbols_info) with all properties. The names of the fields in the named tuple are the same as the names of the enumeration elements used in the specified functions but without the "SYMBOL_" prefix and in lowercase.

In case of an error, the function returns None.

Attention! To ensure successful function execution, the requested symbol must be selected in Market Watch. This can be done from Python by calling symbol_select (see further).

Example (MQL5/Scripts/MQL5Book/Python/eurjpy.py):

```
import MetaTrader5 as mt5
   
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error())
   quit()
   
# make sure EURJPY is present in the Market Watch, or abort the algorithm
selected = mt5.symbol_select("EURJPY", True)
if not selected:
   print("Failed to select EURJPY")
   mt5.shutdown()
   quit()
   
# display the properties of the EURJPY symbol
symbol_info = mt5.symbol_info("EURJPY")
if symbol_info != None:
   # display the data as is (as a tuple)
   print(symbol_info)
   # output a couple of specific properties
   print("EURJPY: spread =", symbol_info.spread, ", digits =", symbol_info.digits)
   # output symbol properties as a dictionary
   print("Show symbol_info(\"EURJPY\")._asdict():")
   symbol_info_dict = mt5.symbol_info("EURJPY")._asdict()
   for prop in symbol_info_dict:
      print("  {}={}".format(prop, symbol_info_dict[prop]))
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

Result:

```
SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session_sell_orders=0, ... 
EURJPY: spread = 17, digits = 3 
Show symbol_info()._asdict(): 
  custom=False 
  chart_mode=0 
  select=True 
  visible=True 
  ...
  time=1585069682 
  digits=3 
  spread=17 
  spread_float=True 
  ticks_bookdepth=10 
  trade_calc_mode=0 
  trade_mode=4 
  ...
  trade_exemode=1 
  swap_mode=1 
  swap_rollover3days=3 
  margin_hedged_use_leg=False 
  expiration_mode=7 
  filling_mode=1 
  order_mode=127 
  order_gtc_mode=0 
  ...
  bid=120.024 
  ask=120.041 
  last=0.0 
  ...
  point=0.001 
  trade_tick_value=0.8977708350166538 
  trade_tick_value_profit=0.8977708350166538 
  trade_tick_value_loss=0.8978272580355541 
  trade_tick_size=0.001 
  trade_contract_size=100000.0 
  ...
  volume_min=0.01 
  volume_max=500.0 
  volume_step=0.01 
  volume_limit=0.0 
  swap_long=-0.2 
  swap_short=-1.2 
  margin_initial=0.0 
  margin_maintenance=0.0 
  margin_hedged=100000.0 
  ...
  currency_base=EUR 
  currency_profit=JPY 
  currency_margin=EUR 
  ...

```

bool symbol_select(symbol, enable = None)

The symbol_select function adds the specified symbol to Market Watch or removes it. The symbol is specified in the first parameter. The second parameter is passed as True or False, which means showing or hiding the symbol, respectively.

If the second optional unnamed parameter is omitted, then by Python's type casting rules, bool(none) is equivalent to False.

The function is an analog of [SymbolSelect](/en/book/automation/symbols/symbols_select).

int symbols_total()

The symbols_total function returns the number of all instruments in the MetaTrader 5 terminal, taking into account custom symbols and those not currently shown in the Market Watch window. This is the analog of the function [SymbolsTotal(false)](/en/book/automation/symbols/symbols_list).

Next symbols_get function returns an array of tuples with information about all instruments or favorite instruments with names matching the specified filter in the optional named parameter group.

tuple[] symbols_get(group = "PATTERN")

Each element in the array tuple is a named tuple with a full set of symbol properties (we saw a similar tuple above in the context of the description of the symbol_info function).

Since there is only one parameter, its name can be omitted when calling the function.

In case of an error, the function will return a special value of None.

The group parameter allows you to select symbols by name, optionally using the substitution (wildcard) character '*' at the beginning and/or end of the searched string. '*' means 0 or any number of characters. Thus, you can organize a search for a substring that occurs in the name with an arbitrary number of other characters before or after the specified fragment. For example, "EUR*" means symbols that start with "EUR" and have any name extension (or just "EUR"). The "*EUR*" filter will return symbols with the names containing the "EUR" substring anywhere.

Also, the group parameter may contain multiple conditions separated by commas. Each condition can be specified as a mask using '*'. To exclude symbols, you can use the logical negation sign '!'. In this case, all conditions are applied sequentially, i.e., first you need to specify the inclusion conditions, and then the exclusion conditions. For example, group="*, !*EUR*" means that we need to select all symbols first and then exclude those that contain "EUR" in the name (anywhere).

For example, to display information about cross-currency rates, except for the 4 major Forex currencies, you can run the following query:

```
crosses = mt5.symbols_get(group = "*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(crosses)) # the size of the resulting array - the number of crosses
for s in crosses: 
   print(s.name, ":", s) 

```

An example of the result:

```
len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):  10 
AUDCAD : SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session... 
AUDCHF : SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session... 
AUDNZD : SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session... 
CADCHF : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
NZDCAD : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
NZDCHF : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
NZDSGD : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
CADMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
CHFMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 
NZDMXN : SymbolInfo(custom=False, chart_mode=0, select=False, visible=False, session_deals=0, session_buy_orders=0, sessi... 

```

The symbol_info_tick function can be used to get the last tick for the specified financial instrument.

tuple symbol_info_tick(symbol)

The only mandatory parameter specifies the name of the financial instrument.

The information is returned as a tuple with the same fields as in the MqlTick structure. The function is an analog of [SymbolInfoTick](/en/book/automation/symbols/symbols_tick).

None is returned if an error occurs.

For the function to work properly, the symbol must be enabled in Market Watch. Let's demonstrate it in the script MQL5/Scripts/MQL5Book/Python/gbpusdtick.py.

```
import MetaTrader5 as mt5
   
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error())
   quit()
   
# try to include the GBPUSD symbol in the Market Watch
selected=mt5.symbol_select("GBPUSD", True)
if not selected:
   print("Failed to select GBPUSD")
   mt5.shutdown()
   quit()
   
# display the last tick of the GBPUSD symbol as a tuple
lasttick = mt5.symbol_info_tick("GBPUSD")
print(lasttick)
# display the values of the tick fields in the form of a dictionary
print("Show symbol_info_tick(\"GBPUSD\")._asdict():")
symbol_info_tick_dict = lasttick._asdict()
for prop in symbol_info_tick_dict:
   print("  {}={}".format(prop, symbol_info_tick_dict[prop]))
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

The result should be as follows:

```
Tick(time=1585070338, bid=1.17264, ask=1.17279, last=0.0, volume=0, time_msc=1585070338728, flags=2, volume_real=0.0) 
Show symbol_info_tick._asdict(): 
  time=1585070338 
  bid=1.17264 
  ask=1.17279 
  last=0.0 
  volume=0 
  time_msc=1585070338728 
  flags=2 
  volume_real=0.0

```
