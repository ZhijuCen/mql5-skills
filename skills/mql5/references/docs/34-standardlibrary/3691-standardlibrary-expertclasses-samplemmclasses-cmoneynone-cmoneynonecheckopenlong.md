# CheckOpenLong

Gets trade volume for a long position.

```
virtual double  CheckOpenLong(
   double  price,     // price
   double  sl         // Stop Loss price
   )

```

Parameters

price

[in]  Estimated open price.

sl

[in]  Estimated Stop Loss price.

Return Value

Trade volume for a long position.

Note

The function always returns the minimal lot size.
