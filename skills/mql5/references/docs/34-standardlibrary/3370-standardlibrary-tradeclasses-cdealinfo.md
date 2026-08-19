# CDealInfo

CDealInfo is a class for easy access to the deal properties.

### Description

CDealInfo class provides access to the deal properties.

### Declaration

```
   class CDealInfo : public CObject

```

### Title

```
   #include <Trade\DealInfo.mqh>

```

```
Inheritance hierarchy
   CObject
       CDealInfo

```

### Class methods by groups

| Access to integer type properties |  |
| --- | --- |
| Order | Gets the order by which the deal is executed |
| Time | Gets the time of deal execution |
| TimeMsc | Receives the time  of a deal execution in milliseconds since 01.01.1970 |
| DealType | Gets the deal type |
| TypeDescription | Gets the deal type as a string |
| Entry | Gets the deal direction |
| EntryDescription | Gets the deal direction as a string |
| Magic | Gets the ID of expert, that executed the deal |
| PositionId | Gets the ID of position, in which the deal was involved |
| Access to double type properties |  |
| Volume | Gets the volume of deal |
| Price | Gets the deal price |
| Commision | Gets the amount of commission of the deal |
| Swap | Gets the amount of swap when position is closed |
| Profit | Gets the financial result of deal |
| Access to text properties |  |
| Symbol | Gets the name of deal symbol |
| Comment | Gets the deal comment |
| Access to MQL5 API functions |  |
| InfoInteger | Gets the value of specified integer type property |
| InfoDouble | Gets the value of specified double type property |
| InfoString | Gets value of specified string type property |
| Selection |  |
| Ticket | Gets ticket/selects the deal |
| SelectByIndex | Selects the deal by index |

```
Methods inherited from class CObject
Prev, Prev, Next, Next, Save, Load, Type, Compare

```
