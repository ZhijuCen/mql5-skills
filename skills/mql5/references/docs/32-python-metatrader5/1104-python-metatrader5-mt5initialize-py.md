# initialize

Establish a connection with the MetaTrader 5 terminal. There are three call options.

Call without parameters. The terminal for connection is found automatically.

```
initialize()

```

Call specifying the path to the MetaTrader 5 terminal we want to connect to.

```
initialize(
   path                      // path to the MetaTrader 5 terminal EXE file
   )

```

Call specifying the trading account path and parameters.

```
initialize(
   path,                     // path to the MetaTrader 5 terminal EXE file
   login=LOGIN,              // account number
   password="PASSWORD",      // password
   server="SERVER",          // server name as it is specified in the terminal
   timeout=TIMEOUT,          // timeout
   portable=False            // portable mode
   )

```

Parameters

path

[in]  Path to the metatrader.exe or metatrader64.exe file. Optional unnamed parameter. It is indicated first without a parameter name. If the path is not specified, the module attempts to find the executable file on its own.

login=LOGIN

[in]  Trading account number. Optional named parameter. If not specified, the last trading account is used.

password="PASSWORD"

[in]  Trading account password. Optional named parameter. If the password is not set, the password for a specified trading account saved in the terminal database is applied automatically.

server="SERVER"

[in]  Trade server name. Optional named parameter. If the server is not set, the server for a specified trading account saved in the terminal database is applied automatically.

timeout=TIMEOUT

[in]  Connection timeout in milliseconds. Optional named parameter. If not specified, the value of 60 000 (60 seconds) is applied.

portable=False

[in]  Flag of the terminal launch in [portable](https://www.metatrader5.com/en/terminal/help/start_advanced/start#portable) mode. Optional named parameter. If not specified, the value of False is used.

Return Value

Returns True in case of successful connection to the MetaTrader 5 terminal, otherwise - False.

Note

If required, the MetaTrader 5 terminal is launched to establish connection when executing the initialize() call.

Example:

```
import MetaTrader5 as mt5
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# display data on connection status, server name and trading account
print(mt5.terminal_info())
# display data on MetaTrader 5 version
print(mt5.version())
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

```

See also

[shutdown](/en/docs/python_metatrader5/mt5shutdown_py), [terminal_info](/en/docs/python_metatrader5/mt5terminalinfo_py), [version](/en/docs/python_metatrader5/mt5version_py)
