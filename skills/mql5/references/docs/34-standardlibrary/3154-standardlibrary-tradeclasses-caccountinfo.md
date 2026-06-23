# CAccountInfo

CAccountInfo is a class for easy access to the currently opened trade account properties.

### Description

CAccountInfo class provides easy access to the currently opened trade account properties.

### Declaration

```
   class CAccountInfo : public CObject

```

### Title

```
   #include <Trade\AccountInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CAccountInfo

```

### Class methods by groups

| Access to integer type properties |  |
| --- | --- |
| Login | Gets the account number |
| TradeMode | Gets the trade mode |
| TradeModeDescription | Gets the trade mode as a string |
| Leverage | Gets the amount of given leverage |
| StopoutMode | Gets the mode of stop out setting |
| StopoutModeDescription | Gets the mode of stop out setting as a string |
| TradeAllowed | Gets the flag of trade allowance |
| TradeExpert | Gets the flag of automated trade allowance |
| LimitOrders | Gets the maximal number of allowed pending orders |
| MarginMode | Gets margin calculation mode |
| MarginModeDescription | Gets margin calculation mode as a string |
| Access to double type properties |  |
| Balance | Gets the balance of account |
| Credit | Gets the amount of given credit |
| Profit | Gets the amount of current profit on account |
| Equity | Gets the amount of current equity on account |
| Margin | Gets the amount of reserved margin |
| FreeMargin | Gets the amount of free margin |
| MarginLevel | Gets the level of margin |
| MarginCall | Gets the level of margin for deposit |
| MarginStopOut | Gets the level of margin for Stop Out |
| Access to text properties |  |
| Name | Gets the client name |
| Server | Gets the trade server name |
| Currency | Gets the deposit currency name |
| Company | Gets the company name that serves an account |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of specified integer type property |
| InfoDouble | Gets the value of specified double type property |
| InfoString | Gets the value of specified string type property |
| Additional methods |  |
| OrderProfitCheck | Gets the evaluated profit based on the parameters passed |
| MarginCheck | Gets the amount of margin required to execute trade operation |
| FreeMarginCheck | Gets the amount of free margin left after execution of trade operation |
| MaxLotCheck | Gets the maximal possible volume of trade operation |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
