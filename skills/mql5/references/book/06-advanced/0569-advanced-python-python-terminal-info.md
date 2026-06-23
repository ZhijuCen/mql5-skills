# Getting information about the terminal

The terminal_info function allows you to get the status and parameters of the connected MetaTrader 5 terminal.

namedtuple terminal_info()

On success, the function returns the information as a structure of named tuples (namedtuple), and in case of an error, it returns None.

In one call of this function, you can get all the information that is provided by [TerminalInfoInteger](/en/book/common/environment/env_listing), [TerminalInfoDouble](/en/book/common/environment/env_listing), and [TerminalInfoDouble](/en/book/common/environment/env_listing) in MQL5, with all variants of supported properties. The names of the fields in the tuple correspond to the names of the enumeration elements without the "TERMINAL_" prefix, reduced to lowercase.

For example (see MQL5/Scripts/MQL5Book/Python/terminalinfo.py):

```
import MetaTrader5 as mt5
  
# let's establish a connection to the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error())
   quit() 
   
# display brief information about the MetaTrader 5 version
print(mt5.version()) 
# display full information about the settings and the state of the terminal
terminal_info = mt5.terminal_info()
if terminal_info != None: 
   # display terminal data as is
   print(terminal_info) 
   # display the data as a dictionary
   print("Show terminal_info()._asdict():")
   terminal_info_dict = mt5.terminal_info()._asdict()
   for prop in terminal_info_dict: 
      print("  {}={}".format(prop, terminal_info_dict[prop]))
   
# complete the connection to the MetaTrader 5 terminal
mt5.shutdown() 

```

We should be something like the following.

```
[500, 3428, '14 Sep 2022'] 
TerminalInfo(community_account=True, community_connection=True, connected=True,.... 
Show terminal_info()._asdict(): 
  community_account=True 
  community_connection=True 
  connected=True 
  dlls_allowed=False 
  trade_allowed=False 
  tradeapi_disabled=False 
  email_enabled=False 
  ftp_enabled=False 
  notifications_enabled=False 
  mqid=False 
  build=2366 
  maxbars=5000 
  codepage=1251 
  ping_last=77850 
  community_balance=707.10668201585 
  retransmission=0.0 
  company=MetaQuotes Software Corp. 
  name=MetaTrader 5 
  language=Russian 
  path=E:\ProgramFiles\MetaTrader 5 
  data_path=E:\ProgramFiles\MetaTrader 5 
  commondata_path=C:\Users\User\AppData\Roaming\MetaQuotes\Terminal\Common 

```
