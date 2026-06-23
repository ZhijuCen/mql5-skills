# Data Type Identifiers

When creating an indicator handle using the [IndicatorCreate()](/en/docs/series/indicatorcreate) function, an array of [MqlParam](/en/docs/constants/structures/mqlparam) type must be specified as the last parameter. Accordingly, the MqlParam structure, describing indicator, contains a special field type. This field contains information about the data type ([real](/en/docs/basis/types/double), [integer](/en/docs/basis/types/integer) or [string](/en/docs/basis/types/stringconst) type) that are passed by a particular element of the array. The value of this field of the MqlParam structure may be one of ENUM_DATATYPE values.

ENUM_DATATYPE

| Identifier | Data type |
| --- | --- |
| TYPE_BOOL | bool |
| TYPE_CHAR | char |
| TYPE_UCHAR | uchar |
| TYPE_SHORT | short |
| TYPE_USHORT | ushort |
| TYPE_COLOR | color |
| TYPE_INT | int |
| TYPE_UINT | uint |
| TYPE_DATETIME | datetime |
| TYPE_LONG | long |
| TYPE_ULONG | ulong |
| TYPE_FLOAT | float |
| TYPE_DOUBLE | double |
| TYPE_STRING | string |

Each element of the array describes the corresponding input parameter of a created [technical indicator](/en/docs/indicators), so the type and order of elements in the array must be strictly maintained in accordance with the description.
