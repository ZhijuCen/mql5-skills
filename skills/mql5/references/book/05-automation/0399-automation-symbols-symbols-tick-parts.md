# Current market information (tick)

In the section [Getting the last tick of a symbol](/en/book/automation/symbols/symbols_tick), we have already seen the SymbolInfoTick function, which provides complete information about the last tick (price change event) in the form of the MqlTick structure. If necessary, the MQL program can request the values of prices and volumes corresponding to the fields of this structure separately. All of them are denoted by properties of different types that are part of the ENUM_SYMBOL_INFO_INTEGER and ENUM_SYMBOL_INFO_DOUBLE enumerations.

| Identifier | Description | Property type |
| --- | --- | --- |
| SYMBOL_TIME | Last quote time | datetime |
| SYMBOL_BID | Bid price; the best sell offer | double |
| SYMBOL_ASK | Ask price; the best buy offer | double |
| SYMBOL_LAST | Last; the price of the last deal | double |
| SYMBOL_VOLUME | The volume of the last deal | long |
| SYMBOL_TIME_MSC | The time of the last quote in milliseconds since 1970.01.01 | long |
| SYMBOL_VOLUME_REAL | The volume of the last deal with increased accuracy | double |

Note that the code for the two volume-related properties, SYMBOL_VOLUME and SYMBOL_VOLUME_REAL, is the same in both enumerations. This is the only case where the element IDs of different enumerations overlap. The thing is that they return essentially the same tick property, but with different representation accuracy.

Unlike a structure, properties do not provide an analog to the uint flags field, which tells what kind of changes in the market caused the tick generation. This field is only meaningful within a structure.

Let's try to request tick properties separately and compare them with the result of the SymbolInfoTick call. In a fast market, there is a possibility that the results will differ. A new tick (or even several ticks) may come between function calls.

```
void OnStart()
{
   PRTF(TimeToString(SymbolInfoInteger(_Symbol, SYMBOL_TIME), TIME_DATE | TIME_SECONDS));
   PRTF(SymbolInfoDouble(_Symbol, SYMBOL_BID));
   PRTF(SymbolInfoDouble(_Symbol, SYMBOL_ASK));
   PRTF(SymbolInfoDouble(_Symbol, SYMBOL_LAST));
   PRTF(SymbolInfoInteger(_Symbol, SYMBOL_VOLUME));
   PRTF(SymbolInfoInteger(_Symbol, SYMBOL_TIME_MSC));
   PRTF(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_REAL));
   
   MqlTick tick[1];
   SymbolInfoTick(_Symbol, tick[0]);
   ArrayPrint(tick);
}

```

It is easy to verify that in a particular case, the information coincided.

```
TimeToString(SymbolInfoInteger(_Symbol,SYMBOL_TIME),TIME_DATE|TIME_SECONDS)
   =2022.01.25 13:52:51 / ok
SymbolInfoDouble(_Symbol,SYMBOL_BID)=1838.44 / ok
SymbolInfoDouble(_Symbol,SYMBOL_ASK)=1838.49 / ok
SymbolInfoDouble(_Symbol,SYMBOL_LAST)=0.0 / ok
SymbolInfoInteger(_Symbol,SYMBOL_VOLUME)=0 / ok
SymbolInfoInteger(_Symbol,SYMBOL_TIME_MSC)=1643118771166 / ok
SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_REAL)=0.0 / ok
                 [time]   [bid]   [ask] [last] [volume]    [time_msc] [flags] [volume_real]
[0] 2022.01.25 13:52:51 1838.44 1838.49   0.00        0 1643118771166       6          0.00

```
