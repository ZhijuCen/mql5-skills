# StringToCharArray

Symbol-wise copies a string converted from Unicode to ANSI, to a selected place of array of uchar type. It returns the number of copied elements.

```
int  StringToCharArray(
   string  text_string,         // source string
   uchar&  array[],             // array
   int     start=0,             // starting position in the array
   int     count=-1             // number of symbols
   uint    codepage=CP_ACP      // code page
   );

```

Parameters

text_string

[in]  String to copy.

array[]

[out]  Array of uchar type.

start=0

[in]  Position from which copying starts. Default - 0.

count=-1

[in]  Number of array elements to copy. Defines length of a resulting string. Default value is -1, which means copying up to the array end, or till terminal 0. Terminal 0 will also be copied to the recipient array, in this case the size of a dynamic array can be increased if necessary to the size of the string. If the size of the dynamic array exceeds the length of the string, the size of the array will not be reduced.

codepage=CP_ACP

[in]  The value of the code page. For the most-used [code pages](/en/docs/constants/io_constants/codepageusage) provide appropriate constants.

Return Value

Number of copied elements.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- string to convert
   string text = "This is a test of the StringToCharArray() function";
 
//--- convert the input string into a uchar array in accordance with the set code page
   uchar char_array[];
   int   copied=StringToCharArray(text, char_array);
   PrintFormat("String length: %u\nNumber of characters copied (with terminal 0): %d\nArray of characters for the string '%s':",
               StringLen(text), copied, text);
//--- print the resulting array to the journal
   ArrayPrint(char_array, 0, " | ");
   /*
   result:
   String length: 50
   Number of characters copied (with terminal 0): 51
   Array of characters for the string 'This is a test of the StringToCharArray() function':
   [ 0]  84 | 104 | 105 | 115 |  32 | 105 | 115 |  32 |  97 |  32 | 116 | 101 | 115 | 116 |  32 | 111 | 102
   [17]  32 | 116 | 104 | 101 |  32 |  83 | 116 | 114 | 105 | 110 | 103 |  84 | 111 |  67 | 104 |  97 | 114
   [34]  65 | 114 | 114 |  97 | 121 |  40 |  41 |  32 | 102 | 117 | 110 |  99 | 116 | 105 | 111 | 110 |   0
   */
  }

```

See also

[CharArrayToString](/en/docs/convert/chararraytostring),[ ](/en/docs/convert/shortarraytostring)[StringToShortArray](/en/docs/convert/stringtoshortarray), [Use of a Codepage](/en/docs/constants/io_constants/codepageusage)
