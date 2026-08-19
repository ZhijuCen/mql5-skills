# CPositionInfo

CPositionInfo is a class for easy access to the open position properties.

### Description

CPositionInfo class provides easy access to the open position properties.

### Declaration

```
   class CPositionInfo : public CObject

```

### Title

```
   #include <Trade\PositionInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CPositionInfo

```

### Class methods by groups

| Access to integer type properties |  |
| --- | --- |
| Time | Gets the time of position opening |
| TimeMsc | Receives the time of   position opening in milliseconds since 01.01.1970 |
| TimeUpdate | Receives  the time of position changing in seconds since 01.01.1970 |
| TimeUpdateMsc | Receives  the time of position changing in milliseconds since 01.01.1970 |
| PositionType | Gets the position type |
| TypeDescription | Gets the position type as a string |
| Magic | Gets the ID of expert, that opened the position |
| Identifier | Gets the ID of position |
| Access to double type properties |  |
| Volume | Gets the volume of position |
| PriceOpen | Gets the price of position opening |
| StopLoss | Gets the price of position's Stop Loss |
| TakeProfit | Gets the price of position's Take Profit |
| PriceCurrent | Gets the current price by position symbol |
| Commission | Gets the amount of commission by position |
| Swap | Gets the amount of swap by position |
| Profit | Gets the amount of current profit by position |
| Access to text properties |  |
| Symbol | Gets the name of position symbol |
| Comment | Gets the comment of the position |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of specified integer type property |
| InfoDouble | Gets the value of specified double type property |
| InfoString | Gets the value of specified string type property |
| Selection |  |
| Select | Selects the position |
| SelectByIndex | Selects the position by index |
| SelectByMagic | Selects a position with the specified symbol name and magic number |
| SelectByTicket | Selects the position by ticket |
| State |  |
| StoreState | Saves the position parameters |
| CheckState | Checks the current parameters against the saved parameters |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
