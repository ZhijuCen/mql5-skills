# GetHashCode

Calculates the hash code value.

A version for working with the bool type.

```
int GetHashCode(
   const bool  value         // value
   );

```

A version for working with the char type.

```
int GetHashCode(
   const char  value         // value
   );

```

A version for working with the uchar type.

```
int GetHashCode(
   const uchar  value        // value
   );

```

A version for working with the short type.

```
int GetHashCode(
   const short  value        // value
   );

```

A version for working with the ushort type.

```
int GetHashCode(
   const ushort  value       // value
   );

```

A version for working with the color type.

```
int GetHashCode(
   const color  value        // value
   );

```

A version for working with the int type.

```
int GetHashCode(
   const int  value          // value
   );

```

A version for working with the uint type.

```
int GetHashCode(
   const uint  value         // value
   );

```

A version for working with the datetime type.

```
int GetHashCode(
   const datetime  value     // value
   );

```

A version for working with the long type.

```
int GetHashCode(
   const long  value         // value
   );

```

A version for working with the ulong type.

```
int GetHashCode(
   const ulong  value        // value
   );

```

A version for working with the float type.

```
int GetHashCode(
   const float  value        // value
   );

```

A version for working with the double type.

```
int GetHashCode(
   const double  value       // value
   );

```

A version for working with the string type.

```
int GetHashCode(
   const string  value       // value
   );

```

A version for working with other types.

```
template<typename T>
int GetHashCode(
   T  value                  // value
   );

```

Parameters

value

[in]  The value for which you want to get the hash code.

Return Value

Returns the hash code.

Note

If the T type is an object that implements the IEqualityComparable<T> interface, then the hash code will be obtained based on its HashCode method. In all other cases, the hash code will be calculated as the hash value of the value type name.
