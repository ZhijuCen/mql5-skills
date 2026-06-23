# InitMoney

Initializes the money management object.

```
virtual bool  InitMoney(
   CExpertMoney*     money=NULL,        // pointer
   )

```

Parameters

money

[in]  Pointer to [CExpertMoney](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertmoney) class object (or its descendant).

Return Value

true - successful, otherwise - false.

Note

If money is NULL, the [CExpertMoney](/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertmoney) class will be used for initialization (it uses the minimum lot).
