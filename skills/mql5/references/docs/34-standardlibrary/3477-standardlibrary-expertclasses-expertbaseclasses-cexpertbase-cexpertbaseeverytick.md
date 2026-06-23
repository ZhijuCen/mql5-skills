# EveryTick

Sets the "Every tick" flag.

```
void  EveryTick(
   bool    value         // flag
   )

```

Parameters

value

[in]  New value of a flag.

Return Value

None.

Note

If the flag is set, each price (tick) change at a working symbol is processed.

If the flag is not set, the processing method is called only at a new bar on the working timeframe and symbol.
