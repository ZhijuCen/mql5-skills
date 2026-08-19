# FormatRequestResult

Prepares the formatted string with results of the last request execution.

```
string  FormatRequestResult(
   string&                 str,         // string
   const MqlTradeRequest&  request,     // request
   const MqlTradeResult&   result       // result
   ) const

```

Parameters

str

[in]  Target string passed by reference.

request

[in]   A structure of [MqlTradeRequest](/en/docs/constants/structures/mqltraderequest) type with parameters of the last request.

result

[in]   A structure of [MqlTradeResult](/en/docs/constants/structures/mqltraderesult) type with results of the last request.

Return Value

None.
