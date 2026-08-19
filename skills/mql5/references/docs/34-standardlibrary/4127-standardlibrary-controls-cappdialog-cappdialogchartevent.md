# ChartEvent

Virtual handler of the control events.

```
virtual bool  ChartEvent(
   const int      id,         // ID
   const long&    lparam,     // parameter
   const double&  dparam,     // parameter
   const string&  sparam      // parameter
   )

```

Parameters

id

[in]  Event ID.

lparam

[in]  Event parameter of [long](/en/docs/basis/types/integer/integertypes#long) type passed by reference.

dparam

[in]  Event parameter of [double](/en/docs/basis/types/double) type passed by reference.

sparam

[in]  Event parameter of [string](/en/docs/basis/types/stringconst) type passed by reference.

Return Value

true - event processed, otherwise - false.
