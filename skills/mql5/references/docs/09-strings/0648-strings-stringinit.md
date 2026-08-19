# StringInit

Initializes a string by specified symbols and provides the specified string size.

```
bool  StringInit(
   string&   string_var,       // string to initialize
   int       new_len=0,        // required string length after initialization
   ushort    character=0       // symbol, by which the string will be filled
   );

```

Parameters

string_var

[in][out]  String that should be initialized and deinitialized.

new_len=0

[in]  String length after initialization. If length=0, it deinitializes the string, i.e. the string buffer is cleared and the buffer address is zeroed.

character=0

[in]  Symbol to fill the string.

Return Value

In case of success returns true, otherwise - false. To get the [error code](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

If  character=0 and the length new_len>0, the buffer of the string of indicated length will be distributed and filled by zeroes. The string length will be equal to zero, because the whole buffer is filled out by string terminators.

Example:

```
void OnStart()
  {
//---
   string str;
   StringInit(str,200,0);
   Print("str = ",str,": StringBufferLen(str) = ",
         StringBufferLen(str),"  StringLen(str) = ",StringLen(str));
  }
/*  Result
str = : StringBufferLen(str) = 200   StringLen(str) = 0
*/

```

See also

[StringBufferLen](/en/docs/strings/stringbufferlen), [StringLen](/en/docs/strings/stringlen)
