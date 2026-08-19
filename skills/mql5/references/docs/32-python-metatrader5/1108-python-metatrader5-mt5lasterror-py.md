# last_error

Return data on the last error.

```
last_error()

```

Return Value

Return the last error code and description as a tuple.

Note

last_error() allows obtaining an error code in case of a failed execution of a MetaTrader 5 library function. It is similar to [GetLastError()](/en/docs/check/getlasterror). However, it applies its own error codes. Possible values:

| Constant | Value | Description |
| --- | --- | --- |
| RES_S_OK | 1 | generic success |
| RES_E_FAIL | -1 | generic fail |
| RES_E_INVALID_PARAMS | -2 | invalid arguments/parameters |
| RES_E_NO_MEMORY | -3 | no memory condition |
| RES_E_NOT_FOUND | -4 | no history |
| RES_E_INVALID_VERSION | -5 | invalid version |
| RES_E_AUTH_FAILED | -6 | authorization failed |
| RES_E_UNSUPPORTED | -7 | unsupported method |
| RES_E_AUTO_TRADING_DISABLED | -8 | auto-trading disabled |
| RES_E_INTERNAL_FAIL | -10000 | internal IPC general error |
| RES_E_INTERNAL_FAIL_SEND | -10001 | internal IPC send failed |
| RES_E_INTERNAL_FAIL_RECEIVE | -10002 | internal IPC recv failed |
| RES_E_INTERNAL_FAIL_INIT | -10003 | internal IPC initialization fail |
| RES_E_INTERNAL_FAIL_CONNECT | -10003 | internal IPC no ipc |
| RES_E_INTERNAL_FAIL_TIMEOUT | -10005 | internal timeout |

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
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

```

See also

[version](/en/docs/python_metatrader5/mt5version_py), [GetLastError](/en/docs/check/getlasterror)
