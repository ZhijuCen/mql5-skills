# IntegerToString

This function converts value of integer type into a string of a specified length and returns the obtained string.

```
string  IntegerToString(
   long    number,              // number
   int     str_len=0,           // length of result string
   ushort  fill_symbol=' '      // filler
   );

```

Parameters

number

[in]  Number for conversion.

str_len=0

[in]  String length. If the resulting string length is larger than the specified one, the string is not cut off. If it is smaller, filler symbols will be added to the left.

fill_symbol=' '

[in]  Filler symbol. By default it is a space.

Return Value

String.

Example:

```
#define DATA_TOTAL 1001
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- display rows with the index multiple of 100 in the loop by DATA_TOTAL
//--- the string displays the index value in the four-character format
//--- if the string length is less than 4 characters, then the value of the loop index
//--- in the string is preceded by leading zeros
   for(int i=0; i<DATA_TOTAL; i++)
     {
      if(i%100==0)
         Print("Converted index value: ",IntegerToString(i,4,'0'));
     }
   /*
   result:
   Converted index value: 0000
   Converted index value: 0100
   Converted index value: 0200
   Converted index value: 0300
   Converted index value: 0400
   Converted index value: 0500
   Converted index value: 0600
   Converted index value: 0700
   Converted index value: 0800
   Converted index value: 0900
   Converted index value: 1000
   */
  }

```

See also

[StringToInteger](/en/docs/convert/stringtointeger)
