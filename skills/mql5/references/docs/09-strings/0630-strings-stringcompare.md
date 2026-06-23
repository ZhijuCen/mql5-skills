# StringCompare

The function compares two strings and returns the comparison result in form of an integer.

```
int  StringCompare(
   const string&  string1,                 // the first string in the comparison
   const string&  string2,                 // the second string in the comparison
   bool           case_sensitive=true      // case sensitivity mode selection for the comparison
   );

```

Parameters

string1

[in]  The first string.

string2

[in]  The second string.

case_sensitive=true

[in]  Case sensitivity mode selection. If it is true, then "A">"a". If it is false, then "A"="a". By default the value is equal to true.

Return Value

- -1 (minus one), if string1<string2
- 0 (zero), if string1=string2
- 1 (one), if string1>string2

Note

The strings are compared symbol by symbol, the symbols are compared in the alphabetic order in accordance with the current code page.

Example:

```
void OnStart()
  {
//--- what is larger - apple or home?
   string s1="Apple";
   string s2="home";
 
//--- compare case sensitive 
   int result1=StringCompare(s1,s2);
   if(result1>0) PrintFormat("Case sensitive comparison: %s > %s",s1,s2);
   else
     {
      if(result1<0)PrintFormat("Case sensitive comparison: %s < %s",s1,s2);
      else PrintFormat("Case sensitive comparison: %s = %s",s1,s2);
     }
 
//--- compare case-insensitive
   int result2=StringCompare(s1,s2,false);
   if(result2>0) PrintFormat("Case insensitive comparison: %s > %s",s1,s2);
   else
     {
      if(result2<0)PrintFormat("Case insensitive comparison: %s < %s",s1,s2);
      else PrintFormat("Case insensitive comparison: %s = %s",s1,s2);
     }
/* Result
     Case-sensitive comparison: Apple < home
     Case insensitive comparison: Apple < home
*/
  }

```

See also

[String Type](/en/docs/basis/types/stringconst), [CharToString()](/en/docs/convert/chartostring), [ShortToString()](/en/docs/convert/shorttostring), [StringToCharArray()](/en/docs/convert/stringtochararray), [StringToShortArray()](/en/docs/convert/stringtoshortarray), [StringGetCharacter()](/en/docs/strings/stringgetcharacter), [Use of a Codepage](/en/docs/constants/io_constants/codepageusage)
