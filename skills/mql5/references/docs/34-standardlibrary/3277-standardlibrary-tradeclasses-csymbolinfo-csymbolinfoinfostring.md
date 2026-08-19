# InfoString

Gets the value of specified string type property.

```
bool  InfoString(
   ENUM_SYMBOL_INFO_STRING  prop_id,     // property ID
   string&                  var          // reference to variable
   ) const

```

Parameters

prop_id

[in]  ID of text property.

var

[out]  Reference to [string](/en/docs/basis/types/stringconst) type variable to place result.

Return Value

true – success, false – unable to get property value.

Note

The symbol should be selected by [Name](/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfoname) method.
