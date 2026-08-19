# login

Connect to a trading account using specified parameters.

```
login(
   login,                    // account number
   password="PASSWORD",      // password
   server="SERVER",          // server name as it is specified in the terminal
   timeout=TIMEOUT           // timeout
   )

```

Parameters

login

[in]  Trading account number. Required unnamed parameter.

password

[in]  Trading account password. Optional named parameter. If the password is not set, the password saved in the terminal database is applied automatically.

server

[in]  Trade server name. Optional named parameter. If no server is set, the last used server is applied automatically.

timeout=TIMEOUT

[in]  Connection timeout in milliseconds. Optional named parameter. If not specified, the value of 60 000 (60 seconds) is applied. If the connection is not established within the specified time, the call is forcibly terminated and the exception is generated.

Return Value

True in case of a successful connection to the trade account, otherwise – False.

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
 
# display data on MetaTrader 5 version
print(mt5.version())
# connect to the trade account without specifying a password and a server
account=17221085
authorized=mt5.login(account)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(account))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
 
# now connect to another trading account specifying the password
account=25115284
authorized=mt5.login(account, password="gqrtz0lbdm")
if authorized:
    # display trading account data 'as is'
    print(mt5.account_info())
    # display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
[500, 2367, '23 Mar 2020']
 
connected to account #17221085
 
connected to account #25115284
AccountInfo(login=25115284, trade_mode=0, leverage=100, limit_orders=200, margin_so_mode=0, ...
account properties:
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
   balance=99588.33
   credit=0.0
   profit=-45.23
   equity=99543.1
   margin=54.37
   margin_free=99488.73
   margin_level=183084.6054809638
   margin_so_call=50.0
   margin_so_so=30.0
   margin_initial=0.0
   margin_maintenance=0.0
   assets=0.0
   liabilities=0.0
   commission_blocked=0.0
   name=James Smith
   server=MetaQuotes-Demo
   currency=USD
   company=MetaQuotes Software Corp.

```

See also

[initialize](/en/docs/python_metatrader5/mt5initialize_py), [shutdown](/en/docs/python_metatrader5/mt5shutdown_py)
