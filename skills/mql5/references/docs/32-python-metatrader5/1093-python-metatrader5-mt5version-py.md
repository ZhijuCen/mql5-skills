# version

Return the MetaTrader 5 terminal version.

```
version()

```

Return Value

Return the MetaTrader 5 terminal version, build and release date. Return None in case of an error. The info on the error can be obtained using [last_error()](/en/docs/python_metatrader5/mt5lasterror_py).

Note

The version() function returns the terminal version, build and release date as a tuple of three values:

| Type | Description | Sample value |
| --- | --- | --- |
| integer | MetaTrader 5 terminal version | 500 |
| integer | Build | 2007 |
| string | Build release date | '25 Feb 2019' |

Example:

```
import MetaTrader5 as mt5
import pandas as pd
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# display data on MetaTrader 5 version
print(mt5.version())
 
# display data on connection status, server name and trading account 'as is'
print(mt5.terminal_info())
print()
 
# get properties in the form of a dictionary
terminal_info_dict=mt5.terminal_info()._asdict()
# convert the dictionary into DataFrame and print
df=pd.DataFrame(list(terminal_info_dict.items()),columns=['property','value'])
print("terminal_info() as dataframe:")
print(df[:-1])
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
 
Result:
MetaTrader5 package author:  MetaQuotes Software Corp.
MetaTrader5 package version:  5.0.29
[500, 2367, '23 Mar 2020']
TerminalInfo(community_account=True, community_connection=True, connected=True, dlls_allowed=False, trade_allowed=False, ...
 
terminal_info() as dataframe:
                 property                         value
0       community_account                          True
1    community_connection                          True
2               connected                          True
3            dlls_allowed                         False
4           trade_allowed                         False
5       tradeapi_disabled                         False
6           email_enabled                         False
7             ftp_enabled                         False
8   notifications_enabled                         False
9                    mqid                         False
10                  build                          2367
11                maxbars                          5000
12               codepage                          1251
13              ping_last                         77881
14      community_balance                       707.107
15         retransmission                             0
16                company     MetaQuotes Software Corp.
17                   name                  MetaTrader 5
18               language                       Russian
19                   path  E:\ProgramFiles\MetaTrader 5
20              data_path  E:\ProgramFiles\MetaTrader 5
 

```

See also

[initialize](/en/docs/python_metatrader5/mt5initialize_py), [shutdown](/en/docs/python_metatrader5/mt5shutdown_py), [terminal_info](/en/docs/python_metatrader5/mt5terminalinfo_py)
