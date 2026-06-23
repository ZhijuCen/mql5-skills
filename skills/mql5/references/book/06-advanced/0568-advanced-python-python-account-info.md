# Getting information about a trading account

The account_info function obtains full information about the current trading account.

namedtuple account_info()

The function returns information as a structure of named tuples (namedtuple). In case of an error, the result is None.

Using this function, you can use one call to get all the information that is provided by [AccountInfoInteger](/en/book/automation/account/account_info_overview), [AccountInfoDouble](/en/book/automation/account/account_info_overview), and [AccountInfoString](/en/book/automation/account/account_info_overview) in MQL5, with all variants of supported properties. The names of the fields in the tuple correspond to the names of the enumeration elements without the "ACCOUNT_" prefix, reduced to lowercase.

The following script MQL5/Scripts/MQL5Book/Python/accountinfo.py is included with the book.

```
import MetaTrader5 as mt5
  
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize(): 
   print("initialize() failed, error code =", mt5.last_error())
   quit()
   
account_info = mt5.account_info()
if account_info != None:
   # display trading account data as is
   print(account_info) 
   # display data about the trading account in the form of a dictionary
   print("Show account_info()._asdict():")
   account_info_dict = mt5.account_info()._asdict()
   for prop in account_info_dict:
      print("  {}={}".format(prop, account_info_dict[prop]))
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown()

```

The result should be something like this.

```
AccountInfo(login=25115284, trade_mode=0, leverage=100, limit_orders=200, margin_so_mode=0, ... 
Show account_info()._asdict(): 
  login=25115284 
  trade_mode=0 
  leverage=100 
  limit_orders=200 
  margin_so_mode=0 
  trade_allowed=True 
  trade_expert=True 
  margin_mode=2 
  currency_digits=2 
  fifo_close=False 
  balance=99511.4 
  credit=0.0 
  profit=41.82 
  equity=99553.22 
  margin=98.18 
  margin_free=99455.04 
  margin_level=101398.67590140559 
  margin_so_call=50.0 
  margin_so_so=30.0 
  margin_initial=0.0 
  margin_maintenance=0.0 
  assets=0.0 
  liabilities=0.0 
  commission_blocked=0.0 
  name=MetaQuotes Dev Demo 
  server=MetaQuotes-Demo 
  currency=USD 
  company=MetaQuotes Software Corp. 

```
