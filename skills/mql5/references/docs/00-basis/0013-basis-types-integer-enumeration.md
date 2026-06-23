# Enumerations

Data of the enum type belong to a certain limited set of data. Defining the enumeration type:

```
enum name of enumerable type
  {
   list of values
  };

```

The list of values is a list of identifiers of named constants separated by commas.

Example:

```
enum months  // enumeration of named constants
   {
    January,
    February,
    March,
    April,
    May,
    June,
    July,
    August,
    September,
    October,
    November,
    December
   };

```

After the enumeration is declared, a new integer-valued 4-byte data type appears. Declaration of the new data type allows the compiler to strictly control types of passed parameters, because enumeration introduces new named constants. In the above example, the January named constant has the value of 0, February - 1, December - 11.

Rule: If a certain value is not assigned to a named constant that is a member of the enumeration, its new value will be formed automatically. If it is the first member of the enumeration, the 0 value will be assigned to it. For all subsequent members, values will be calculated based on the value of the previous members by adding one.

Example:

```
enum intervals  // Enumeration of named constants
   {
    month=1,     // Interval of one month
    two_months,  // Two months
    quarter,     // Three months - quarter
    halfyear=6,  // Half a year
    year=12,     // Year - 12 months
   };

```

### Notes

- Unlike C++, the size of the internal representation of the enumerated type in MQL5 is always equal to 4 bytes. That is, [sizeof](/en/docs/basis/operations/other#sizeof) (months) returns the value 4.
- Unlike C++, an anonymous enumeration can't be declared in MQL5. That is, a unique name must be always specified after the enum keyword.

See also

[Typecasting](/en/docs/basis/types/casting)
