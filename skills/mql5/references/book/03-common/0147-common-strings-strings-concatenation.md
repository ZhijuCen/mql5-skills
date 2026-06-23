# String concatenation

Concatenation of strings is probably the most common string operation. In MQL5, it can be done using the '+' or '+=' operators. The first operator concatenates two strings (the operands to the left and right of the '+') and creates a temporary concatenated string that can be assigned to a target variable or passed to another part of an expression (such as a function call). The second operator appends the string to the right of the operator '+=' to the string (variable) to the left of this operator.

In addition to this, the MQL5 API provides a couple of functions for composing strings from other strings or elements of other types.

Examples of using functions are given in the script StringAdd.mq5, which is considered after their description.

bool StringAdd(string &variable, const string addition)

The function appends the specified addition string to the end of a string variable variable. Whenever possible, the system uses the available buffer of the string variable (if its size is enough for the combined result) without re-allocating memory or copying strings.

The function is equivalent to the operator variable += addition. Time costs and memory consumption are about the same.

The function returns true in case of success and false in case of error.

int StringConcatenate(string &variable, void argument1, void argument2 [, void argumentI...])

The function converts two or more arguments of [built-in types](/en/book/basis/builtin_types) to a string representation and concatenates them in the variable string. The arguments are passed starting from the second parameter of the function. Arrays, structures, objects, pointers are not supported as arguments.

The number of arguments must be between 2 and 63.

String arguments are added to the resulting variable as is.

Arguments of type double are converted with maximum precision (up to 16 significant digits), and scientific notation with exponent can be chosen if it turns out to be more compact. Arguments of type float are displayed with 5 characters.

Values of type datetime are converted to a string with all date and time fields ("YYYY.MM.DD hh:mm:ss").

Enumerations, single-byte and double-byte characters are output as integers.

Values of type color are displayed as a trio of "R,G,B" components or a color name (if available in the list of standard web colors).

When converting type bool the strings "true" or "false" are used.

The function StringConcatenate returns the length of the resulting string.

StringConcatenate is designed to build a string from other sources (variables, expressions) other than the receiving variable. It is not recommended to use StringConcatenate to concatenate new chunks of data to the same row by calling StringConcatenate(variable, variable, ...). This function call is not optimized and is extremely slow compared to the operator '+' and StringAdd.

Functions StringAdd and StringConcatenate are tested in the StringAdd.mq5 script, which uses the PRTE macro and the helper function StrOut from the [previous section](/en/book/common/strings/strings_init).

```
void OnStart()
{
   string s = "message";
   StrOut(s);
   PRTE(StringAdd(s, "r"));
   StrOut(s);
   PRTE(StringConcatenate(s, M_PI * 100, " ", clrBlue, PRICE_CLOSE));
   StrOut(s);
}

```

As a result of its execution, the following lines are displayed in the log:

```
'message' [7] 0
StringAdd(s,r)=true
'messager' [8] 260
StringConcatenate(s,M_PI*100, ,clrBlue,PRICE_CLOSE)=true
'314.1592653589793 clrBlue1' [26] 260

```

The script also includes the header file StringBenchmark.mqh with the class benchmark. It provides a framework for derived classes implemented in the script to measure the performance of various string addition methods. In particular, they make sure that adding strings using the operator '+' and the function StringAdd are comparable. This material is left for independent study.

Additionally, the book comes with the script StringReserve.mq5: it makes a visual comparison of the speed of adding strings depending on the use or non-use of the buffer (StringReserve).
