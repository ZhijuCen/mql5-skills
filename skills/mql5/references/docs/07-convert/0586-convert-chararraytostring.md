# CharArrayToString

It copies and converts part of array of uchar type into a returned string.

```
string  CharArrayToString(
   uchar  array[],              // array
   int    start=0,              // starting position in the array
   int    count=-1              // number of symbols
   uint    codepage=CP_ACP      // code page
   );

```

Parameters

array[]

[in]  Array of uchar type.

start=0

[in]  Position from which copying starts. by default 0 is used.

count=-1

[in]  Number of array elements for copying. Defines the length of a resulting string. Default value is -1, which means copying up to the array end, or till terminal 0.

codepage=CP_ACP

[in]  The value of the code page. There is a number of built-in constants for the most used [code pages](/en/docs/constants/io_constants/codepageusage).

Return Value

String.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create an array with symbol codes
   uchar array[]= { 84, 104, 105, 115,  32, 105, 115,  32,  97,  32,
                   116, 101, 115, 116,  32, 111, 102,  32, 116, 104,
                   101,  32,  67, 104,  97, 114,  65, 114, 114,  97,
                   121,  84, 111,  83, 116, 114, 105, 110, 103,  40,
                    41,  32, 102, 117, 110,  99, 116, 105, 111, 110
                  };
//--- print an array of codes converted into a string in the journal
   Print(CharArrayToString(array));
 
//--- create an array with symbol codes and terminal zero
   uchar array_z[]= { 84, 104, 105, 115,  32, 105, 115,  32,  97,  32,
                     116, 101, 115, 116,   0,  32, 111, 102,  32, 116,
                     104, 101,  32,  67, 104,  97, 114,  65, 114, 114,
                      97, 121,  84, 111,  83, 116, 114, 105, 110, 103,
                      40,  41,  32, 102, 117, 110,  99, 116, 105, 111, 110
                    };
//--- print the second array of codes with terminal zero in the journal
   PrintFormat("%s ...", CharArrayToString(array_z));
 
   /*
   result:
   This is a test of the CharArrayToString() function
   This is a test ...
   */
  }

```

See also

[StringToCharArray](/en/docs/convert/stringtochararray),[ ](/en/docs/constants/io_constants/codepageusage)[ShortArrayToString](/en/docs/convert/shortarraytostring), [Use of a Codepage](/en/docs/constants/io_constants/codepageusage)
