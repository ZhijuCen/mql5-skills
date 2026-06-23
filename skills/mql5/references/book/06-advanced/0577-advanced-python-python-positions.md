# Getting the number and list of open positions

The positions_total function returns the number of open positions.

int positions_total()

The function is an analog of [PositionsTotal](/en/book/automation/experts/experts_position_list).

To get detailed information about each position, use the positions_get function which has multiple options. All variants return an array of named tuples TradePosition with keys corresponding to position properties (see elements of [ENUM_POSITION_PROPERTY_enumerations](/en/book/automation/experts/experts_position_properties), without the "POSITION_" prefix, in lowercase). In case of an error, the result is None.

namedtuple[] positions_get()

namedtuple[] positions_get(symbol = <"SYMBOL">)

namedtuple[] positions_get(group = <"PATTERN">)

namedtuple[] positions_get(ticket = <TICKET>)

The function without parameters returns all open positions.

The function with the symbol parameter allows the selection of positions for the specified symbol.

The function with the group parameter provides filtering by search mask with wildcards '*' (any characters are replaced) and logical negation of the condition '!'. For details see the section [Getting information about financial instruments](/en/book/advanced/python/python_symbols).

A version with the ticket parameters selects a position with a specific ticket (POSITION_TICKET property).

The positions_get function can be used to get all positions and their properties in one call, which makes it similar to a bunch of [PositionsTotal](/en/book/automation/experts/experts_position_list), [PositionSelect](/en/book/automation/experts/experts_position_list), and [PositionGet](/en/book/automation/experts/experts_positionget_funcs)[ functions](/en/book/automation/experts/experts_positionget_funcs).

In the script MQL5/Scripts/MQL5Book/Python/positionsget.py, we request positions for a specific symbol and search mask.

```
import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # how many columns to show
pd.set_option('display.width', 1500)      # max. table width to display
   
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error())
   quit()
   
# get open positions on USDCHF
positions = mt5.positions_get(symbol = "USDCHF")
if positions == None: 
   print("No positions on USDCHF, error code={}".format(mt5.last_error()))
elif len(positions) > 0:
   print("Total positions on USDCHF =", len(positions))
 # display all open positions
   for position in positions:
      print(position)
   
# get a list of positions on symbols whose names contain "*USD*"
usd_positions = mt5.positions_get(group = "*USD*") 
if usd_positions == None:
    print("No positions with group=\"*USD*\", error code={}".format(mt5.last_error())) 
elif len(usd_positions) > 0: 
   print("positions_get(group=\"*USD*\") = {}".format(len(usd_positions)))
   # display the positions as a table using pandas.DataFrame
   df=pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
   df['time'] = pd.to_datetime(df['time'], unit='s')
   df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'],
   axis=1, inplace=True)
   print(df)
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

Here's what the result might be:

```
Total positions on USDCHF = 1
TradePosition(ticket=1468454363, time=1664217233, time_msc=1664217233239, time_update=1664217233,
   time_update_msc=1664217233239, type=1, magic=0, identifier=1468454363, reason=0, volume=0.01, price_open=0.99145,
   sl=0.0, tp=0.0, price_current=0.9853, swap=-0.01, profit=6.24, symbol='USDCHF', comment='', external_id='')
positions_get(group="*USD*") = 2
       ticket                time  type  ...  identifier  volume  price_open  ... _current  swap  profit  symbol comment
0  1468454363 2022-09-26 18:33:53     1  ...  1468454363    0.01     0.99145  ...  0.98530 -0.01    6.24  USDCHF        
1  1468475849 2022-09-26 18:44:00     0  ...  1468475849    0.01     1.06740  ...  1.08113  0.00   13.73  GBPUSD        
 

```
