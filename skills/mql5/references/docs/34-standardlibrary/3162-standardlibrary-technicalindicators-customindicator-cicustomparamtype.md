# ParamType

Gets a type of the parameter.

```
ENUM_DATATYPE  ParamType(
   int  index      // index
   ) const

```

Parameters

index

[in]  Parameter index.

Return Value

Returns the data type of the specified parameter, used in indicator creation.

Note

If parameter index is invalid, it returns [WRONG_VALUE](/en/docs/constants/namedconstants/otherconstants).
