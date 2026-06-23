# Error checking: last_error

The last_error function returns information about the last Python error.

int last_error()

Integer error codes differ from the codes that are allocated for MQL5 errors and returned by the standard [GetLastError](/en/book/common/environment/env_last_error) function. In the following table, the abbreviation IPC refers to the term "Inter-Process Communication".

| Constant | Meaning | Description |
| --- | --- | --- |
| RES_S_OK | 1 | Success |
| RES_E_FAIL | -1 | Common error |
| RES_E_INVALID_PARAMS | -2 | Invalid arguments/parameters |
| RES_E_NO_MEMORY | -3 | Memory allocation error |
| RES_E_NOT_FOUND | -4 | Requested history not found |
| RES_E_INVALID_VERSION | -5 | Version not supported |
| RES_E_AUTH_FAILED | -6 | Authorization error |
| RES_E_UNSUPPORTED | -7 | Method not supported |
| RES_E_AUTO_TRADING_DISABLED | -8 | Algo trading is disabled |
| RES_E_INTERNAL_FAIL | -10000 | General internal IPC error |
| RES_E_INTERNAL_FAIL_SEND | -10001 | Internal error sending IPC data |
| RES_E_INTERNAL_FAIL_RECEIVE | -10002 | Internal error sending IPC data |
| RES_E_INTERNAL_FAIL_INIT | -10003 | IPC internal initialization error |
| RES_E_INTERNAL_FAIL_CONNECT | -10003 | No IPC |
| RES_E_INTERNAL_FAIL_TIMEOUT | -10005 | IPC timeout |

In the following script (MQL5/Scripts/MQL5Book/Python/init.py), in the case of an error when connecting to the terminal, we display the error code and exit.

```
import MetaTrader5 as mt5
# show MetaTrader5 package version
print("MetaTrader5 package version: ", mt5.__version__)  #  5.0.37
   
# let's try to establish a connection or launch the MetaTrader 5 terminal
if not mt5.initialize():
   print("initialize() failed, error code =", mt5.last_error()) 
   quit()
... # the working part of the script will be here
# terminate the connection to the terminal
mt5.shutdown()

```
