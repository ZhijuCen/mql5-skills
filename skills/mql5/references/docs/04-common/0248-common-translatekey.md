# TranslateKey

Returns a Unicode character by a virtual key code considering the current input language and the status of control keys.

```
short  TranslateKey(
   int  key_code      // key code for receiving a Unicode character
   );

```

Parameters

key_code

[in]  Key code.

Return Value

Unicode character in case of a successful conversion. The function returns -1 in case of an error.

Note

The function uses [ToUnicodeEx](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-tounicodeex) to convert keys pressed by a user into Unicode characters.  An error may occur in case ToUnicodeEx is not triggered – for example, when trying to receive the SHIFT key character.

Example:

```
void OnChartEvent(const int id,const long& lparam,const double& dparam,const string& sparam)
  { 
   if(id==CHARTEVENT_KEYDOWN)
     {
      short sym=TranslateKey((int)lparam);
      //--- if the entered character is successfully converted to Unicode
      if(sym>0)
         Print(sym,"'",ShortToString(sym),"'");
      else
         Print("Error in TranslateKey for key=",lparam);
     }
  }

```

See also

[Client terminal events](/en/docs/runtime/event_fire), [OnChartEvent](/en/docs/event_handlers/onchartevent)
