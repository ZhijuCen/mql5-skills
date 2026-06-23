# Identifying the account, client, server, and broker

Perhaps the most important properties of an account are its number and identification data: the name of the server and the broker's company, as well as the name of the client. All of these properties, except for the number, are string properties.

| Identifier | Description |
| --- | --- |
| ACCOUNT_LOGIN | Account number (long) |
| ACCOUNT_NAME | Client name |
| ACCOUNT_SERVER | Trade server name |
| ACCOUNT_COMPANY | Name of the company servicing the account |

Let's use the AccountMonitor class from the previous section to log these and many other properties that will be discussed in a moment. Let's create the corresponding object and call its properties in the script AccountInfo.mq5.

```
#include <MQL5Book/AccountMonitor.mqh>
   
void OnStart()
{
   AccountMonitor m;
   m.list2log<ENUM_ACCOUNT_INFO_INTEGER>();
   m.list2log<ENUM_ACCOUNT_INFO_DOUBLE>();
   m.list2log<ENUM_ACCOUNT_INFO_STRING>();
}

```

Here is an example of a possible result of the script.

```
ENUM_ACCOUNT_INFO_INTEGER Count=10
  0 ACCOUNT_LOGIN=30000003
  1 ACCOUNT_TRADE_MODE=ACCOUNT_TRADE_MODE_DEMO
  2 ACCOUNT_TRADE_ALLOWED=true
  3 ACCOUNT_TRADE_EXPERT=true
  4 ACCOUNT_LEVERAGE=100
  5 ACCOUNT_MARGIN_SO_MODE=ACCOUNT_STOPOUT_MODE_PERCENT
  6 ACCOUNT_LIMIT_ORDERS=200
  7 ACCOUNT_MARGIN_MODE=ACCOUNT_MARGIN_MODE_RETAIL_HEDGING
  8 ACCOUNT_CURRENCY_DIGITS=2
  9 ACCOUNT_FIFO_CLOSE=false
ENUM_ACCOUNT_INFO_DOUBLE Count=14
  0 ACCOUNT_BALANCE=10000.00
  1 ACCOUNT_CREDIT=0.00
  2 ACCOUNT_PROFIT=-78.76
  3 ACCOUNT_EQUITY=9921.24
  4 ACCOUNT_MARGIN=1000.00
  5 ACCOUNT_MARGIN_FREE=8921.24
  6 ACCOUNT_MARGIN_LEVEL=992.12
  7 ACCOUNT_MARGIN_SO_CALL=50.00
  8 ACCOUNT_MARGIN_SO_SO=30.00
  9 ACCOUNT_MARGIN_INITIAL=0.00
 10 ACCOUNT_MARGIN_MAINTENANCE=0.00
 11 ACCOUNT_ASSETS=0.00
 12 ACCOUNT_LIABILITIES=0.00
 13 ACCOUNT_COMMISSION_BLOCKED=0.00
ENUM_ACCOUNT_INFO_STRING Count=4
  0 ACCOUNT_NAME=Vincent Silver
  1 ACCOUNT_COMPANY=MetaQuotes Software Corp.
  2 ACCOUNT_SERVER=MetaQuotes-Demo
  3 ACCOUNT_CURRENCY=USD

```

Pay attention to the properties of this section (ACCOUNT_LOGIN, ACCOUNT_NAME, ACCOUNT_COMPANY, ACCOUNT_SERVER). In this case, the script was executed on the account of the demo server "MetaQuotes-Demo". Obviously, this should be a demo account, and this is indicated not only by the name of the server but also by another property, ACCOUNT_TRADE_MODE, which will be discussed in the next section.

Account identifiers are usually used to link MQL programs to a specific trading environment. An example of such an algorithm was presented in the [Services](/en/book/applications/script_service/services) section.
