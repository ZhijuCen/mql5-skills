# OnEvent

Chart event handler.

```
virtual bool  OnEvent(
   const int      id,         // ID
   const long&    lparam,     // event parameter
   const double&  dparam,     // event parameter
   const string&  sparam      // event parameter
   )

```

Parameters

id

[in]  Event ID.

lparam

[in]  Event parameter of [long](/en/docs/basis/types/integer/integertypes#long) type, passed by reference.

dparam

[in]  Event parameter of [double](/en/docs/basis/types/double) type, passed by reference.

sparam

[in]  Event parameter of [string](/en/docs/basis/types/stringconst) type, passed by reference.

Return Value

true - event has been processed, otherwise - false.
