# Buy

Opens a long position with specified parameters.

```
bool  Buy(
   double        volume,          // position volume
   const string  symbol=NULL,     // symbol
   double        price=0.0,       // execution price
   double        sl=0.0,          // stop loss price
   double        tp=0.0,          // take profit price
   const string  comment=""       // comment
   )

```

Parameters

volume

[in]  Requested position volume.

symbol=[NULL](/en/docs/basis/types/void)

[in]  Position symbol. If it is not specified, the current symbol will be used.

price=0.0

[in]  Price. If the price is not specified, the current market Ask price will be used.

sl=0.0

[in]  Stop Loss price.

tp=0.0

[in]  Take Profit price.

comment=""

[in]  Comment.

Return Value

true - successful check of the structures, otherwise - false.

Note

Successful completion of the Buy(...) method does not always mean successful execution of the trade operation. It is necessary to check the result of trade request (trade server [return code](/en/docs/constants/errorswarnings/enum_trade_return_codes)) using [ResultRetcode()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultretcode) and value returned by [ResultDeal()](/en/docs/standardlibrary/tradeclasses/ctrade/ctraderesultdeal).
