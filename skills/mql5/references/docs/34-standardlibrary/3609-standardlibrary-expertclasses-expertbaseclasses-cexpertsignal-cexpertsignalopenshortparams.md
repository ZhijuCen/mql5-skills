# OpenShortParams

Sets parameters to open a short position.

```
virtual bool  OpenShortParams(
   double&    price,          // price
   double&    sl,             // Stop Loss
   double&    tp,             // Take Profit
   datetime&  expiration      // expiration
   )

```

Parameters

price

[in][out]  Variable for price, passed by reference.

sl

[in][out]  Variable for Stop Loss price, passed by reference.

tp

[in][out]  Variable for Take Profit price, passed by reference.

expiration

[in][out]  Variable for expiration time, passed by reference (if necessary).

Return Value

true - successful, otherwise - false.
