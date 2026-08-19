# StringSubstr

Extracts a substring from a text string starting from the specified position.

```
string  StringSubstr(
   string  string_value,     // string
   int     start_pos,        // position to start with
   int     length=-1         // length of extracted string
   );

```

Parameters

string_value

[in]  String to extract a substring from.

start_pos

[in]  Initial position of a substring. Can be from 0 to [StringLen](/en/docs/strings/stringlen)(text) -1.

length=-1

[in] Length of an extracted substring. If the parameter value is equal to -1 or parameter isn't set, the substring will be extracted from the indicated position till the string end.

Return Value

Copy of a extracted substring, if possible. Otherwise returns an empty string.

Example:

```
void OnStart()
  {
//--- get the name of the current symbol
   string name = Symbol();
   
//--- get the base and quoted symbol currencies
   string base   = StringSubstr(name, 0, 3);
   string quoted = StringSubstr(name, 3, 3);
   
//--- display the obtained symbol currencies in the log
   PrintFormat("Symbol: %s. Currency base: %s, currency quoted: %s", name, base, quoted);
  
   /*
   Result
   Symbol: EURUSD. Currency base: EUR, currency quoted: USD
   */
  }

```

See also

[StringSplit](/en/docs/strings/stringsplit), [StringFind](/en/docs/strings/stringfind), [StringGetCharacter](/en/docs/strings/stringgetcharacter)
