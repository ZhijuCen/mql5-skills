# StringSplit

Gets substrings by a specified separator from the specified string, returns the number of substrings obtained.

```
int  StringSplit(
   const string   string_value,       // A string to search in
   const ushort   separator,          // A separator using which substrings will be searched
   string         & result[]          // An array passed by reference to get the found substrings
   );

```

Parameters

string_value

[in]  The string from which you need to get substrings. The string will not change.

pos

[in]  The code of the separator character. To get the code, you can use the [StringGetCharacter()](/en/docs/strings/stringgetcharacter) function.

result[]

[out]  An array of strings where the obtained substrings are located.

Return Value

The number of substrings in the result[] array. If the separator is not found in the passed string, only one source string will be placed in the array.

If string_value is empty or NULL, the function will return zero. In case of an error the function returns -1. To get the [error](/en/docs/constants/errorswarnings/errorcodes) code, call the [GetLastError()](/en/docs/check/getlasterror) function.

Example:

```
string to_split="_life_is_good_"; // A string to split into substrings
   string sep="_";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];               // An array to get strings
   //--- Get the separator code
   u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
   int k=StringSplit(to_split,u_sep,result);
   //--- Show a comment 
   PrintFormat("Strings obtained: %d. Used separator '%s' with the code %d",k,sep,u_sep);
   //--- Now output all obtained strings
   if(k>0)
     {
      for(int i=0;i<k;i++)
        {
         PrintFormat("result[%d]=\"%s\"",i,result[i]);
        }
     }

```

See also

[StringReplace()](/en/docs/strings/stringreplace), [StringSubstr()](/en/docs/strings/stringsubstr), [StringConcatenate()](/en/docs/strings/stringconcatenate)
