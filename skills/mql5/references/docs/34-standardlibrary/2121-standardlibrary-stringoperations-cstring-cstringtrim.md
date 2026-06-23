# Trim

Removes all characters within a set (as well as ' ','\t','\r','\n') at both ends of a string from this string.

```
int  Trim(
   const string  targets      // set
   )

```

Parameters

targets

[in]  Set of characters to remove.

Return Value

Number of removed characters.

Example:

```
//--- example for CString::Trim
#include <Strings\String.mqh> 
//--- 
void OnStart() 
  { 
   CString str;
   //--- 
   str.Assign("   \t\tABCD\r\n");
   printf("Source string '%s'",str.Str());
   //---
   str.Trim("DA-DA-DA");
   printf("Result string '%s'",str.Str());
  } 

```
