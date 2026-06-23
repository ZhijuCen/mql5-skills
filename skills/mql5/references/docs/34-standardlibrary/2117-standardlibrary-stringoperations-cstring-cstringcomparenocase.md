# CompareNoCase

Performs a case insensitive string comparison.

```
int  CompareNoCase(
   const string  str      // string
   ) const;

```

Parameters

str

[in]  String to compare.

Return Value

0 - strings are equal, -1 - a class string is lower than a string to compare, 1 - a class string is greater than a string to compare.

# CompareNoCase

Compares a string (case insensitive) to a CString class instance string.

```
int  CompareNoCase(
   CString*  str      // pointer
   ) const;

```

Parameters

str

[in]  Pointer to CString class instance to compare.

Return Value

0 - if strings are equal, -1 - a class string is lower than a string to compare, 1 - a class string is greater than a string to compare.
