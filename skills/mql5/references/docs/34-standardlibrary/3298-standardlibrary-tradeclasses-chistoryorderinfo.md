# CHistoryOrderInfo

CHistoryOrderInfo is a class for easy access to the history order properties.

### Description

CHistoryOrderInfo class provides easy access to the history order properties.

### Declaration

```
   class CHistoryOrderInfo : public CObject

```

### Title

```
   #include <Trade\HistoryOrderInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CHistoryOrderInfo

```

### Class methods by groups

| Access to integer type properties |  |
| --- | --- |
| TimeSetup | Gets the time of order placement |
| TimeSetupMsc | Receives the time of placing an order  in milliseconds since 01.01.1970 |
| OrderType | Gets the order type |
| OrderTypeDescription | Gets the order type as a string |
| State | Gets the order state |
| StateDescription | Gets the order state as a string |
| TimeExpiration | Gets the time of order expiration |
| TimeDone | Gets the time of order execution or cancellation |
| TimeDoneMsc | Receives order execution or cancellation time  in milliseconds since 01.01.1970 |
| TypeFilling | Gets the type of order execution by remainder |
| TypeFillingDescription | Gets the type of order execution by remainder as a string |
| TypeTime | Gets the type of order at the time of the expiration |
| TypeTimeDescription | Gets the order type by expiration time as a string |
| Magic | Gets the ID of expert that placed the order |
| PositionId | Gets the ID of position |
| Access to double type properties |  |
| VolumeInitial | Gets the initial volume of order |
| VolumeCurrent | Gets the unfilled volume of order |
| PriceOpen | Gets the order price |
| StopLoss | Gets the order's Stop Loss |
| TakeProfit | Gets the order's Take Profit |
| PriceCurrent | Gets the current price by order symbol |
| PriceStopLimit | Gets the price of a Limit order |
| Access to text properties |  |
| Symbol | Gets the order symbol |
| Comment | Gets the order comment |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of specified integer type property |
| InfoDouble | Gets the value of specified double type property |
| InfoString | Gets value of specified string type property |
| Selection |  |
| Ticket | Gets the ticket/selects the order |
| SelectByIndex | Selects the order by index |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
