# StringFill

It fills out a selected string by specified symbols.

```
bool  StringFill(
   string&   string_var,       // string to fill
   ushort    character         // symbol that will fill the string
   );

```

Parameters

string_var

[in][out]  String, that will be filled out by the selected symbol.

character

[in]  Symbol, by which the string will be filled out.

Return Value

In case of success returns true, otherwise - false. To get the [error code](/en/docs/constants/errorswarnings/errorcodes) call [GetLastError()](/en/docs/check/getlasterror).

Note

Filling out a string at place means that symbols are inserted directly to the string without transitional operations of new string creation or copying. This allows to save the operation time.

Example:

```
void OnStart()
  {
   string str;
   StringInit(str,20,'_');
   Print("str = ",str);
   StringFill(str,0);
   Print("str = ",str,": StringBufferLen(str) = ", StringBufferLen(str));
  }
// Result
//   str = ____________________
//   str =  : StringBufferLen(str) = 20
//

```

See also

[StringBufferLen](/en/docs/strings/stringbufferlen), [StringLen](/en/docs/strings/stringlen), [StringInit](/en/docs/strings/stringinit)
