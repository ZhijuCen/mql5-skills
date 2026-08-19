# StringTrimRight

The function cuts line feed characters, spaces and tabs in the right part of the string after the last meaningful symbol. The string is modified at place.

```
int  StringTrimRight(
   string&  string_var      // string to cut
   );

```

Parameters

string_var

[in][out]  String that will be cut from the right.

Return Value

Returns the number of cut symbols.

Example:

```
void OnStart()
  {
//--- define the source string with six spaces on the right
   string text="All spaces on the right will be removed from this string      ";
//--- Display the source string in the log
   PrintFormat("Source line:\n'%s'", text);
//--- remove all spaces on the right and display the number of removed characters and the resulting string in the log
   int num=StringTrimRight(text);
   PrintFormat("The StringTrimRight() function removed %d chars from the right side. Now the line looks like this:\n'%s'", num, text);
   
   /*
   Result
   Source line:
   'All spaces on the right will be removed from this string      '
   The StringTrimRight() function removed 6 chars from the right side. Now the line looks like this:
   'All spaces on the right will be removed from this string'
   */
  }

```

See also

[StringTrimLeft](/en/docs/strings/stringtrimleft), [StringToLower](/en/docs/strings/stringtolower), [StringToUpper](/en/docs/strings/stringtoupper)
