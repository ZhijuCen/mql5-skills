# Connecting a Python script to the terminal and account

The initialize function establishes a connection with the MetaTrader 5 terminal and has 2 forms: short (without parameters) and full (with several optional parameters, the first of them is path and it is positional, and all the rest are named).

bool initialize()

bool initialize(path, account = <ACCOUNT>, password = <"PASSWORD">,  

   server = <"SERVER">, timeout = 60000, portable = False)

The path parameter sets the path to the terminal file (metatrader64.exe) (note that this is an unnamed parameter, unlike all the others, so if it is specified, it must come first in the list).

If the path is not specified, the module will try to find the executable file on its own (the developers do not disclose the exact algorithm). To eliminate ambiguities, use the second form of the function with parameters.

In the account parameter, you can specify the number of the trading account. If it is not specified, then the last trading account in the selected instance of the terminal will be used.

The password for the trading account is specified in the password parameter and can also be omitted: in this case, the password stored in the terminal database for the specified trading account is automatically substituted.

The server parameter is processed in a similar way with the trade server name (as it is specified in the terminal): if it is not specified, then the server saved in the terminal database for the specified trading account is automatically substituted.

The timeout parameter indicates the timeout in milliseconds that is given for the connection (if it is exceeded, an error will occur). The default value is 60000 (60 seconds).

The portable parameter contains a flag for launching the terminal in the portable mode (default is False).

The function returns True in case of successful connection to the MetaTrader 5 terminal and False otherwise.

If necessary, when making a call initialize, the MetaTrader 5 terminal can be launched.

For example, connection to a specific trading account is performed as follows.

```
import MetaTrader5 as mt5 
if not mt5.initialize(login = 562175752, server = "MetaQuotes-Demo", password = "abc"):
   print("initialize() failed, error code =", mt5.last_error()) 
   quit()
...

```

The login function also connects to the trading account with the specified parameters. But this implies that the connection with the terminal has already been established, that is, the function is usually used to change the account.

bool login(account, password = <"PASSWORD">, server = <"SERVER">, timeout = 60000)

The trading account number is provided in the account parameter. This is a required unnamed parameter, meaning it must come first in the list.

The password, server, and timeout parameters are identical to the relevant parameters of the initialize function.

The function returns True in case of successful connection to the trading account and False otherwise.

shutdown()

The shutdown function closes the previously established connection to the MetaTrader 5 terminal.

The example for the above functions will be provided in the [next section](/en/book/advanced/python/python_last_error).

When the connection is established, the script can find the version of the terminal.

tuple version()

The version function returns brief information about the version of the MetaTrader 5 terminal as a tuple of three values: version number, build number, and build date.

| Field type | Description |
| --- | --- |
| integer | MetaTrader 5 terminal version (current, 500) |
| integer | Build number (for example, 3456) |
| string | Build date (e.g. '25 Feb 2022') |

In case of an error, the function returns None, and the error code can be obtained using [last_error](/en/book/advanced/python/python_last_error).

More complete information about the terminal can be obtained using the [terminal_info](/en/book/advanced/python/python_terminal_info) function.
