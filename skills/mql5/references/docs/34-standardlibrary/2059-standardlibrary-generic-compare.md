# Compare

Compares the two values, whether one of them is "greater than, less than or equal to" the other one.

A version for comparing two bool values.

```
int Compare(
   const bool  x,         // the first value
   const bool  y          // the second value
   );

```

A version for comparing two char values.

```
int Compare(
   const char  x,         // the first value
   const char  y          // the second value
   );

```

A version for comparing two uchar values.

```
int Compare(
   const uchar  x,        // the first value
   const uchar  y         // the second value
   );

```

A version for comparing two short values.

```
int Compare(
   const short  x,        // the first value
   const short  y         // the second value
   );

```

A version for comparing two ushort values.

```
int Compare(
   const ushort  x,       // the first value
   const ushort  y        // the second value
   );

```

A version for comparing two color values.

```
int Compare(
   const color  x,        // the first value
   const color  y         // the second value
   );

```

A version for comparing two int values.

```
int Compare(
   const int  x,          // the first value
   const int  y           // the second value
   );

```

A version for comparing two uint values.

```
int Compare(
   const uint  x,         // the first value
   const uint  y          // the second value
   );

```

A version for comparing two datetime values.

```
int Compare(
   const datetime  x,     // the first value
   const datetime  y      // the second value
   );

```

A version for comparing two long values.

```
int Compare(
   const long  x,         // the first value
   const long  y          // the second value
   );

```

A version for comparing two ulong values.

```
int Compare(
   const ulong  x,        // the first value
   const ulong  y         // the second value
   );

```

A version for comparing two float values.

```
int Compare(
   const float  x,        // the first value
   const float  y         // the second value
   );

```

A version for comparing two double values.

```
int Compare(
   const double  x,       // the first value
   const double  y        // the second value
   );

```

A version for comparing two string values.

```
int Compare(
   const string  x,       // the first value
   const string  y        // the second value
   );

```

A version for comparing two values of other types.

```
template<typename T>
int Compare(
   T  x,                  // the first value
   T  y                   // the second value
   );

```

Parameters

x

[in]  The first value

y

[in]  The second value

Return Value

Returns a number that expresses the ratio of the two compared values:

- if the result is less than zero, x is less than y (x<y)
- if the result is equal to zero, x is equal to y (x=y)
- if the result is greater than zero, x is greater than y (x>y)

Note

If the T type is an object that implements the IComparable<T> interface, then the objects will be compared based on its Compare method. In all other cases, 0 is returned.
