# The Structure of Input Parameters of Indicators (MqlParam)

The MqlParam structure has been specially designed to provide [input parameters](/en/docs/basis/variables/inputvariables) when creating the handle of [a technical indicator](/en/docs/indicators) using the [IndicatorCreate()](/en/docs/series/indicatorcreate) function.

```
struct MqlParam
  {
   ENUM_DATATYPE     type;                    // type of the input parameter, value of ENUM_DATATYPE
   long              integer_value;           // field to store an integer type
   double            double_value;            // field to store a double type
   string            string_value;            // field to store a string type
  };

```

All input parameters of an indicator are transmitted in the form of an array of the MqlParam type, the type field of each element of this array specifies the type of data transmitted by the element. The indicator values must be first placed in the appropriate fields for each element (in integer_value, in double_value or string_value) depending on what value of [ENUM_DATATYPE](/en/docs/constants/indicatorconstants/enum_datatype) enumeration is specified in the type field.

If the IND_CUSTOM value is passed third as the indicator type to the [IndicatorCreate()](/en/docs/series/indicatorcreate) function, the first element of the array of input parameters must have the type field with the value of TYPE_STRING from the [ENUM_DATATYPE](/en/docs/constants/indicatorconstants/enum_datatype) enumeration, and the string_value field must contain the name of the [custom indicator](/en/docs/indicators/icustom).
