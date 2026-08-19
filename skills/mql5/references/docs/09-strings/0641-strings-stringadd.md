# StringAdd

The function adds a substring to the end of a string.

```
bool  StringAdd(
   string&  string_var,        // string, to which we add
   string   add_substring      // string, which is added
   );

```

Parameters

string_var

[in][out]  String, to which another one is added.

add_substring

[in]  String that is added to the end of a  source string.

Return Value

In case of success returns true, otherwise false. In order to get an [error code](/en/docs/constants/errorswarnings/errorcodes), the [GetLastError()](/en/docs/check/getlasterror) function should be called.

Example:

```
void OnStart()
  {
   long length=1000000;
   string a="a",b="b",c;
//--- first method
   uint start=GetTickCount(),stop;
   long i;
   for(i=0;i<length;i++)
     {
      c=a+b;
     }
   stop=GetTickCount();
   Print("time for 'c = a + b' = ",(stop-start)," milliseconds, i = ",i);
 
//--- second method
   start=GetTickCount();
   for(i=0;i<length;i++)
     {
      StringAdd(a,b);
     }
   stop=GetTickCount();
   Print("time for 'StringAdd(a,b)' = ",(stop-start)," milliseconds, i = ",i);
 
//--- third method
   start=GetTickCount();
   a="a"; // re-initialize variable a
   for(i=0;i<length;i++)
     {
      StringConcatenate(c,a,b);
     }
   stop=GetTickCount();
   Print("time for 'StringConcatenate(c,a,b)' = ",(stop-start)," milliseconds, i = ",i);
  }

```

See also

[StringConcatenate](/en/docs/strings/stringconcatenate), [StringSplit](/en/docs/strings/stringsplit), [StringSubstr](/en/docs/strings/stringsubstr)
