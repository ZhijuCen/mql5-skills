# StringLen

Returns the number of symbols in a string.

```
int  StringLen(
   string  string_value      // string
   );

```

Parameters

string_value

[in]  String to calculate length.

Return Value

Number of symbols in a string without the ending zero.

Example:

```
void OnStart()
  {
//--- define the test string
   string text="123456789012345";
//--- get the number of symbols in the string
   int str_len=StringLen(text);
//--- display the string and the number of symbols in it in the log
   PrintFormat("The StringLen() function returned the value of %d chars in string: '%s'", str_len, text);
   
   /*
   Result
   The StringLen() function returned the value of 15 chars in string: '123456789012345'
   */
  }

```

See also

[StringBufferLen](/en/docs/strings/stringbufferlen), [StringTrimLeft](/en/docs/strings/stringtrimleft), [StringTrimRight](/en/docs/strings/stringtrimright), [StringToCharArray](/en/docs/convert/stringtochararray), [StringToShortArray](/en/docs/convert/stringtoshortarray)
