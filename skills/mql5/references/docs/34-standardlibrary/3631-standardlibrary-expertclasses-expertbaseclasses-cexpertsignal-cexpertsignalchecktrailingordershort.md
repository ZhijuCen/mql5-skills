# CheckTrailingOrderShort

Checks conditions to modify parameters of Sell Pending order.

```
virtual bool  CheckTrailingOrderShort(
   COrderInfo*    order,          // order
   double&        price           // price
   )

```

Parameters

order

[in]  Pointer to [COrderInfo](/en/docs/standardlibrary/tradeclasses/corderinfo) class object.

price

[in][out]  Variable for Stop Loss price.

Return Value

true - condition is satisfied, otherwise - false.
