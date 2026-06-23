# Numbers to strings and vice versa

Numbers to strings and back, strings to numbers, can be converted using the [explicit type casting](/en/book/basis/conversion/conversion_explicit) operator. For example, for types double and string, it might look like this:

```
double number = (double)text;
string text = (string)number;

```

Strings can be converted to other numeric types, such as float, long, int, etc.

Note that casting to a real type (float) provides fewer significant digits, which in some applications may be considered an advantage as it gives a more compact and easier-to-read representation.

Strictly speaking, this type casting is not mandatory, since even if there is no explicit cast operator, the compiler will produce type casting implicitly. However, you will receive a compiler warning in this case, and thus it is recommended to always make type castings explicit.

The MQL5 API provides some other useful functions, which are described below. The descriptions are followed by a general example.

double StringToDouble(string text)

The StringToDouble function converts a string to a double number.

It is a complete analog of type casting to (double). Its practical purpose is actually limited to preserving backward compatibility with legacy source codes. The preferred method is type casting, as it is more compact and is implemented within the syntax of the language.

According to the conversion process, a string should contain a sequence of characters that meet the rules for writing literals of numeric types (both [float](/en/book/basis/builtin_types/float_numbers) and [integer](/en/book/basis/builtin_types/integer_numbers)). In particular, a string may begin with a '+' or '-' sign, followed by a digit, and may continue further as a sequence of digits.

Real numbers can contain a single dot character '.' separating the fractional part and an optional exponent in the following format: character 'e' or 'E' followed by a sequence of digits for the degree (it can also be preceded by a '+' or '-').

For integers, hexadecimal notation is supported, i.e., the "0x" prefix can be followed not only by decimal digits but also by 'A', 'B', 'C', 'D', 'E', 'F' (in any position).

When any non-expected character (such as a letter, punctuation mark, second period, or intermediate space) is encountered in the string, the conversion ends. In this case, if there were allowed characters before this position, they are interpreted as a number, and if not, the result will be 0.

Initial empty characters (spaces, tabs, newlines) are skipped and do not affect the conversion. If they are followed by numbers and other characters that meet the rules, the number will be received correctly.

The following table provides some examples of valid conversions with explanations.

| string | double | Result |
| --- | --- | --- |
| "123.45" | 123.45 | One decimal point |
| "\t   123" | 123.0 | Whitespace characters at the beginning are ignored |
| "-12345" | -12345.0 | A signed number |
| "123e-5" | 0.00123 | Scientific notation with exponent |
| "0x12345" | 74565.0 | Hexadecimal notation |

The following table shows examples of incorrect conversions.

| string | double | Result |
| --- | --- | --- |
| "x12345" | 0.0 | Starts with an unresolved character (letter) |
| "123x45" | 123.0 | The letter after 123 breaks conversion |
| "   12 3" | 12.0 | The space after 12 breaks the conversion |
| "123.4.5" | 123.4 | The second decimal point after 123.4 breaks the conversion |
| "1,234.50" | 1.0 | The comma after 1 breaks conversion |
| "-+12345" | 0.0 | Too many signs (two) |

string DoubleToString(double number, int digits = 8)

The DoubleToString function converts a number to a string with the specified precision (number of digits from -16 to 16).

It does a job similar to casting a number to (string) but allows you to choose, using the second parameter, the number precision in the resulting string.

The operator (string) applied to double, displays 16 significant digits (total, including mantissa and fractional part). The full equivalent of this cannot be achieved with a function.

If the digits parameter is greater than or equal to 0, it indicates the number of decimal places. In this case, the number of characters before the decimal mark is determined by the number itself (how large it is), and if the total number of characters in the mantissa and that indicated in digits turns out to be greater than 16, then the least significant digits will contain "garbage" (due to how the [real numbers](/en/book/basis/builtin_types/float_numbers) are stored). 16 characters represent the average maximum precision for type double, i.e., setting digits to 16 (maximum) will only provide an accurate representation of values less than 10.

If the digits parameter is less than 0, it specifies the number of significant digits, and this number will be output in scientific format with an exponent. In terms of precision (but not recording format), setting digits=-16 in the function generates a result close to casting (string).

The function, as a rule, is used for uniform formatting of data sets (including right-alignment of a column of a certain table), in which values have the same decimal precision (for example, the number of decimal places in the financial instrument price or a lot size).

Please note that errors may occur during mathematical calculations, causing the result to be not a valid number although it has the type double (or float). For example, a variable might contain the result of calculating the square root of a negative number.  

   

Such values are called "Not a Number" (NaN) and are displayed when cast to (string) as a short hint of error type, for example, -nan(ind) (ind - undefined), nan(inf) (inf - infinity). When using the DoubleToString function, you will get a large number that makes no sense.  

   

It is especially important that all subsequent calculations with NaN will also give NaN. To check such values, there is the [MathIsValidNumber](/en/book/common/maths/maths_nan) function.

long StringToInteger(string text)

The function converts a string to a number of type long. Note that the result type is definitely long, and not int (despite the name) and not ulong.

An alternative way is to typecast using the operator (long). Moreover, any other integer type of your choice can be used for the cast:(int), (uint), (ulong), etc.

The conversion rules are similar to the type double, but exclude the dot character and the exponent from the allowed characters.

string IntegerToString(long number, int length = 0, ushort filling = ' ')

Function IntegerToString converts an integer of type long to a string of the specified length. If the number representation takes less than one character, it is left-padded with a character filling (with a space by default). Otherwise, the number is displayed in its entirety, without restriction. Calling a function with default parameters is equivalent to casting to (string).

Of course, smaller integer types (for example, int, short) will be processed by the function without problems.

Examples of using all the above functions are given in the script ConversionNumbers.mq5.

```
void OnStart()
{
   const string text = "123.4567890123456789";
   const string message = "-123e-5 buckazoid";
   const double number = 123.4567890123456789;
   const double exponent = 1.234567890123456789e-5;
   
   // type casting
   Print((double)text);    // 123.4567890123457
   Print((double)message); // -0.00123
   Print((string)number);  // 123.4567890123457
   Print((string)exponent);// 1.234567890123457e-05
   Print((long)text);      // 123
   Print((long)message);   // -123
   
   // converting with functions
   Print(StringToDouble(text)); // 123.4567890123457
   Print(StringToDouble(message)); // -0.00123
   
   // by default, 8 decimal digits
   Print(DoubleToString(number)); // 123.45678901
   
   // custom precision
   Print(DoubleToString(number, 5));  // 123.45679
   Print(DoubleToString(number, -5)); // 1.23457e+02
   Print(DoubleToString(number, -16));// 1.2345678901234568e+02
   Print(DoubleToString(number, 16)); // 123.4567890123456807
   // last 2 digits are not accurate!
   Print(MathSqrt(-1.0));                 // -nan(ind)
   Print(DoubleToString(MathSqrt(-1.0))); // 9223372129088496176.54775808
   
   Print(StringToInteger(text));      // 123
   Print(StringToInteger(message));   // -123
   
   Print(IntegerToString(INT_MAX));         // '2147483647'
   Print(IntegerToString(INT_MAX, 5));      // '2147483647'
   Print(IntegerToString(INT_MAX, 16));     // '      2147483647'
   Print(IntegerToString(INT_MAX, 16, '0'));// '0000002147483647'
}

```
