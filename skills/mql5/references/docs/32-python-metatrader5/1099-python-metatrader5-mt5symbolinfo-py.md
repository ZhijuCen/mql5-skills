# symbol_info

Get data on the specified financial instrument.

```
symbol_info(
   symbol      // financial instrument name
)

```

symbol

[in]  Financial instrument name. Required unnamed parameter.

Return Value

Return info in the form of a named tuple structure (namedtuple). Return None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

The function returns all data that can be obtained using [SymbolInfoInteger](/en/docs/marketinformation/symbolinfointeger), [SymbolInfoDouble](/en/docs/marketinformation/symbolinfodouble) and [SymbolInfoString](/en/docs/marketinformation/symbolinfostring) in one call.

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
 
# attempt to enable the display of the EURJPY symbol in MarketWatch
selected=mt5.symbol_select("EURJPY",True)
if not selected:
    print("Failed to select EURJPY")
    mt5.shutdown()
    quit()
 
# display EURJPY symbol properties
symbol_info=mt5.symbol_info("EURJPY")
if symbol_info!=None:
    # display the terminal data 'as is'    
    print(symbol_info)
    print("EURJPY: spread =",symbol_info.spread,"  digits =",symbol_info.digits)
    # display symbol properties as a list
    print("Show symbol_info(\"EURJPY\")._asdict():")
    symbol_info_dict = mt5.symbol_info("EURJPY")._asdict()
    for prop in symbol_info_dict:
        print("  {}={}".format(prop, symbol_info_dict[prop]))
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
SymbolInfo(custom=False, chart_mode=0, select=True, visible=True, session_deals=0, session_buy_orders=0, session_sell_orders=0, ...
EURJPY: spread = 17   digits = 3
Show symbol_info()._asdict():
  custom=False
  chart_mode=0
  select=True
  visible=True
  session_deals=0
  session_buy_orders=0
  session_sell_orders=0
  volume=0
  volumehigh=0
  volumelow=0
  time=1585069682
  digits=3
  spread=17
  spread_float=True
  ticks_bookdepth=10
  trade_calc_mode=0
  trade_mode=4
  start_time=0
  expiration_time=0
  trade_stops_level=0
  trade_freeze_level=0
  trade_exemode=1
  swap_mode=1
  swap_rollover3days=3
  margin_hedged_use_leg=False
  expiration_mode=7
  filling_mode=1
  order_mode=127
  order_gtc_mode=0
  option_mode=0
  option_right=0
  bid=120.024
  bidhigh=120.506
  bidlow=118.798
  ask=120.041
  askhigh=120.526
  asklow=118.828
  last=0.0
  lasthigh=0.0
  lastlow=0.0
  volume_real=0.0
  volumehigh_real=0.0
  volumelow_real=0.0
  option_strike=0.0
  point=0.001
  trade_tick_value=0.8977708350166538
  trade_tick_value_profit=0.8977708350166538
  trade_tick_value_loss=0.8978272580355541
  trade_tick_size=0.001
  trade_contract_size=100000.0
  trade_accrued_interest=0.0
  trade_face_value=0.0
  trade_liquidity_rate=0.0
  volume_min=0.01
  volume_max=500.0
  volume_step=0.01
  volume_limit=0.0
  swap_long=-0.2
  swap_short=-1.2
  margin_initial=0.0
  margin_maintenance=0.0
  session_volume=0.0
  session_turnover=0.0
  session_interest=0.0
  session_buy_orders_volume=0.0
  session_sell_orders_volume=0.0
  session_open=0.0
  session_close=0.0
  session_aw=0.0
  session_price_settlement=0.0
  session_price_limit_min=0.0
  session_price_limit_max=0.0
  margin_hedged=100000.0
  price_change=0.0
  price_volatility=0.0
  price_theoretical=0.0
  price_greeks_delta=0.0
  price_greeks_theta=0.0
  price_greeks_gamma=0.0
  price_greeks_vega=0.0
  price_greeks_rho=0.0
  price_greeks_omega=0.0
  price_sensitivity=0.0
  basis=
  category=
  currency_base=EUR
  currency_profit=JPY
  currency_margin=EUR
  bank=
  description=Euro vs Japanese Yen
  exchange=
  formula=
  isin=
  name=EURJPY
  page=http://www.google.com/finance?q=EURJPY
  path=Forex\EURJPY

```

See also

[account_info](/en/docs/python_metatrader5/mt5accountinfo_py), [terminal_info](/en/docs/python_metatrader5/mt5terminalinfo_py)
