# Data Types

Any program operates with data. Data can be of different types depending on their purposes. For example, integer data are used to access to array components. Price data belong to those of double precision with floating point. This is related to the fact that no special data type for price data is provided in MQL5.

Data of different types are processed with different rates. Integer data are processed at the fastest. To process the double precision data, a special co-processor is used. However, because of complexity of internal representation of data with floating point, they are processed slower than the integer ones.

String data are processed at the longest because of dynamic computer memory allocation/reallocation.

The basic data types are:

- integers ([char](/en/docs/basis/types/integer/integertypes), [short](/en/docs/basis/types/integer/integertypes), [int](/en/docs/basis/types/integer/integertypes), [long](/en/docs/basis/types/integer/integertypes), [uchar](/en/docs/basis/types/integer/integertypes), [ushort](/en/docs/basis/types/integer/integertypes), [uint](/en/docs/basis/types/integer/integertypes), [ulong](/en/docs/basis/types/integer/integertypes));
- logical ([bool](/en/docs/basis/types/integer/boolconst));
- [literals](/en/docs/basis/types/integer/symbolconstants) (ushort);
- strings ([string](/en/docs/basis/types/stringconst));
- floating-point numbers ([double](/en/docs/basis/types/double), [float](/en/docs/basis/types/double));
- color ([color](/en/docs/basis/types/integer/color));
- date and time ([datetime](/en/docs/basis/types/integer/datetime));
- enumerations ([enum](/en/docs/basis/types/integer/enumeration)).

Complex data types are:

- [structures](/en/docs/basis/types/classes);
- [classes](/en/docs/basis/types/classes#class).

In terms of [OOP](/en/docs/basis/oop) complex data types are called abstract data types.

The color and datetime types make sense only to facilitate visualization and input of parameters defined from outside - from the table of Expert Advisor or custom indicator properties (the [Inputs](/en/docs/basis/variables/inputvariables) tab). Data of color and datetime types are represented as integers. Integer types and floating-point types are called arithmetic (numeric) types.

Only implicit [type casting](/en/docs/basis/types/casting) is used in [expressions](/en/docs/basis/operations/operexpression), unless the explicit casting is specified.

See also

[Typecasting](/en/docs/basis/types/casting)
