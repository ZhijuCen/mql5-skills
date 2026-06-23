# StringSetCharacter

Returns copy of a string with a changed character in a specified position.

```
bool  StringSetCharacter(
   string&   string_var,       // string
   int       pos,              // position
   ushort    character         // character
   );

```

Parameters

string_var

[in][out]  String.

pos

[in]  Position of a character in a string. Can be from 0 to [StringLen](/en/docs/strings/stringlen)(text).

character

[in]  Symbol code Unicode.

Return Value

In case of success returns true, otherwise false. In order to get an [error code](/en/docs/constants/errorswarnings/errorcodes), the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

If pos is less than [string length](/en/docs/strings/stringlen) and the symbol code value = 0, the string is cut off (but the [buffer size](/en/docs/strings/stringbufferlen), distributed for the string remains unchanged). The string length becomes equal to pos.

If pos is equal to string length, the specified symbol is added at the string end, and the length is enlarged by one.

Example:

```
void OnStart()
  {
   string str="0123456789";
   Print("before: str = ",str,",StringBufferLen(str) = ",
         StringBufferLen(str),"  StringLen(str) = ",StringLen(str));
//--- add zero value in the middle
   StringSetCharacter(str,6,0);
   Print("after: str = ",str,",StringBufferLen(str) = ",
         StringBufferLen(str),"  StringLen(str) = ",StringLen(str));
//--- add symbol at the end
   int size=StringLen(str);
   StringSetCharacter(str,size,'+');
   Print("addition: str = ",str,",StringBufferLen(str) = ",
         StringBufferLen(str),"  StringLen(str) = ",StringLen(str));
  }
/* Result
   before: str = 0123456789 ,StringBufferLen(str) = 0   StringLen(str) = 10
   after:  str = 012345 ,StringBufferLen(str) = 16   StringLen(str) = 6
   addition: str = 012345+ ,StringBufferLen(str) = 16   StringLen(str) = 7
*/

```

See also

[StringBufferLen](/en/docs/strings/stringbufferlen), [StringLen](/en/docs/strings/stringlen), [StringFill](/en/docs/strings/stringfill), [StringInit](/en/docs/strings/stringinit), [CharToString](/en/docs/convert/chartostring), [ShortToString](/en/docs/convert/shorttostring), [CharArrayToString](/en/docs/convert/chararraytostring), [ShortArrayToString](/en/docs/convert/shortarraytostring)
