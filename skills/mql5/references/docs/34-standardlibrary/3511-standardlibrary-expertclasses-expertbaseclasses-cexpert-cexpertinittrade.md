# InitTrade

Initializes the trade object.

```
virtual bool  InitTrade(
   ulong            magic,       // identifier
   CExpertTrade*    trade=NULL   // pointer
   )

```

Parameters

magic

[in]  Expert Advisor ID (will be used in trade requests).

trade

[in]  Pointer to trade object.

Return Value

true - successful, otherwise - false.
