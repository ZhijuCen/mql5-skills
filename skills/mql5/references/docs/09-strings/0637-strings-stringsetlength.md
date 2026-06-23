# StringSetLength

Sets a specified length (in characters) for a string.

```
bool  StringSetLength(
   string&    string_var,      // string
   uint       new_length       // new string length
   );

```

Parameters

string_var

[in][out]  String, for which a new length in characters should be set.

new_capacity

[in]  Required string length in characters. If new_length is less than the current size, the excessive characters are discarded.

Return Value

In case of successful execution, returns true, otherwise - false. To receive an [error](/en/docs/constants/errorswarnings/errorcodes) code, the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Note

TheStringSetLength() function does not change the size of the buffer allocated for a string.

Example:

```
void OnStart()
  {
//--- define the string
   string text="123456789012345";
   
//--- display a string and its length in the log
   PrintFormat("Before StringSetLength() the string '%s' has a size of %d characters", text, StringLen(text));
   
//--- reduce the string size to 10 characters
   StringSetLength(text, 10);
   
//--- display a string, changed due to StringSetLength() operation, and its new length to the log
   PrintFormat("After StringSetLength() the string is now '%s', and has a size of %d characters", text, StringLen(text));
   
   /*
   Result
   Before StringSetLength() the string '123456789012345' has a size of 15 characters
   After StringSetLength() the string is now '1234567890', and has a size of 10 characters
   */
  }

```

See also

[StringLen](/en/docs/strings/stringlen), [StringBufferLen](/en/docs/strings/stringbufferlen), [StringReserve](/en/docs/strings/stringreserve) [StringInit](/en/docs/strings/stringinit), [StringSetCharacter](/en/docs/strings/stringsetcharacter)
