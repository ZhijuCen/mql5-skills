# String Type

The string type is used for storing text strings. A text string is a sequence of characters in the Unicode format with the final zero at the end of it. A string constant can be assigned to a string variable. A string constant is a sequence of Unicode characters enclosed in double quotes: "This is a string constant".

If you need to include a double quote (") into a string, the backslash character (\) must be put before it. Any special [character constants](/en/docs/basis/types/integer/symbolconstants) can be written in a string, if the backslash character (\) is typed before them.

Examples:

```
string svar="This is a character string";
string svar2=StringSubstr(svar,0,4);
Print("Copyright symbol\t\x00A9");
FileWrite(handle,"This string contains a new line symbols \n");
string MT5path="C:\\Program Files\\MetaTrader 5";

```

To make the source code readable, long constant strings can be split into parts without addition operation. During compilation, these parts will be combined into one long string:

```
//--- Declare a long constant string
   string HTML_head="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\""
                    " \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n"
                    "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
                    "<head>\n"
                    "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n"
                    "<title>Trade Operations Report</title>\n"
                    "</head>";
//--- Output the constant string into log
   Print(HTML_head);
  }

```

## 

## Built-in string type methods

Strings can be handled by [string functions](/en/docs/strings), conversion functions and built-in methods of string type provided in the table:

| String method | Analog | Description |
| --- | --- | --- |
| Constructor  string( const int len ) |  | Constructs a string of a specified |
| string []  length both for reading and writing. The index should be within BufferSize() |  | Provides access to the string element by a specified index |
| static string string. Init (const int len, const ushort character); | StringInit | Initializes a string using specified symbols with a specified size |
| void string. Fill (const ushort character); | StringFill | Fills in the string with a specified symbol |
| int string. Len (); | StringLen | Returns the number of characters in a string |
| int string. BufferSize (); | StringBufferLen | Returns the size of a buffer distributed for a string |
| bool string. SetLen (const int new_len); | StringSetLength | Sets a specified length (in characters) for a string |
| bool string. Reserve (const int buffer_len); | StringReserve | Reserves the buffer of a specified size for a string in memory |
| bool string. Add (const string substring); | StringAdd | Adds a specified substring to the end |
| int string. Concatenate (const scalar val1, const scalar val2...); | StringConcatenate | Forms a string consisting of passed parameters |
| array string. Split (const ushort separator, const bool long_separator); | StringSplit | Returns a string array by a specified separator |
| int string. Compare (const string str, const bool case_sensivity); | StringCompare | Compares with a specified string and returns 1 if the first string exceeds the second one; 0 - if the strings are equal; -1 (minus one) - if the first string is less than the second one |
| string string. Substr (const int start_pos, const int len); | StringSubstr | Retrieves a substring from a specified position |
| int string. Find (const string substr, const int pos); | StringFind | Returns an index of the position the necessary substring starts from |
| void string. ToLower (); | StringToLower | Converts all characters to lower case |
| void string. ToUpper (); | StringToUpper | Converts all characters to upper case |
| int string. TrimLeft (); | StringTrimLeft | Deletes spaces, as well as carriage movement and tabulation characters to the left |
| int string. TrimRight () | StringTrimRight | Deletes spaces, as well as carriage movement and tabulation characters to the right |
| void string. Double (const double var, const int digits=8); | DoubleToString | Converts a string to a  double  type number |
| void string. Enum (const enum value); | EnumToString | Converts the enumeration value of any type into a string |
| void string. Integer (const int value, const int str_len=0, const ushort fill=' '); | IntegerToString | Converts a string to a  long  type number |
| void string. CharArray (const uchar array[], const int start_pos=0, const int len=-1, const uint cp=CP_ACP); | CharArrayToString | Converts part of the  uchar  type array to a string |
| void string. ShortArray (const ushort array[], const int start_pos=0, const int len=-1); | ShortArrayToString | Copies part of the  ushort  type array to a string |
| void string. Time (const datetime dt,const int mode=TIME_DATE|TIME_MINUTES); | TimeToString | Converts  datetime  to the "yyyy.mm.dd hh:mi" format string. |
| void string. Format (const string format_str); | StringFormat | Formats the obtained parameters into a string |

See also

[Conversion Functions](/en/docs/convert), [String Functions](/en/docs/strings),  [FileOpen](/en/docs/files/fileopen), [FileReadString](/en/docs/files/filereadstring), [FileWriteString](/en/docs/files/filewritestring)
