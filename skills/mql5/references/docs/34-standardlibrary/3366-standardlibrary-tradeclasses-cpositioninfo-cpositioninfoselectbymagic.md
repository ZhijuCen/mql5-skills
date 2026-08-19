# SelectByMagic

Select a position based on the name of a financial instrument and magic number to further work with.

```
bool  SelectByMagic(
   const string  symbol, // symbol name
   const ulong   magic   // magic number
   );

```

Parameters

symbol

[in]  Symbol name.

magic

[in]  Magic number of the position.

Return Value

true - successful, false - unable to select position.
