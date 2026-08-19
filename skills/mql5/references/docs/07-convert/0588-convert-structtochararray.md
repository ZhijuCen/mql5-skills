# StructToCharArray

Copy [POD structure](/en/docs/basis/types/classes#simple_structure) to uchar type array.

```
bool  StructToCharArray(
   const void&  struct_object,     // structure
   uchar&       char_array[],      // array
   uint         start_pos=0        // starting position in the array
   );

```

Parameters

struct_object

[in]  Reference to any type of [POD structure](/en/docs/basis/types/classes#simple_structure)  (containing only simple data types).

char_array[]

[in]  [uchar](/en/docs/basis/types/integer/integertypes) type array.

start_pos=0

[in]  Position in the array, starting from which the copied data are added.

Return Value

Returns true if successful, otherwise false.

Note

When copying, the dynamic array automatically expands ([ArrayResize](/en/docs/array/arrayresize)) if there is not enough space. If the array cannot be expanded up to the required value, the function returns an error.

Example:

```
uchar    ExtCharArray[];
MqlRates ExtRates[1];
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- copy the data of one current bar into the MqlRates structure
   if(CopyRates(Symbol(), PERIOD_CURRENT, 0, 1, ExtRates)!=1)
     {
      Print("CopyRates() failed. Error code: ", GetLastError());
      return;
     }
 
//--- print the data received in the MqlRates structure in the journal
   Print("Data in the structure immediately after receiving it:");
   MqlRatesPrint(ExtRates[0]);
 
//--- copy the structure to the uchar type array
   ResetLastError();
   if(!StructToCharArray(ExtRates[0], ExtCharArray))
     {
      Print("StructToCharArray() failed. Error code: ", GetLastError());
      return;
     }
 
//--- clear the structure
   ZeroMemory(ExtRates[0]);
//--- print the data in the structure after clearing
   Print("\nData in the structure after ZeroMemory():");
   MqlRatesPrint(ExtRates[0]);
 
//--- now copy the data from the uchar array to the MqlRates structure
   if(!CharArrayToStruct(ExtRates[0], ExtCharArray))
     {
      Print("CharArrayToStruct() failed. Error code: ", GetLastError());
      return;
     }
//--- print the data in the MqlRates structure after copying it from the uchar array
   Print("\nData in the MqlRates structure after copying it from a uchar array:");
   MqlRatesPrint(ExtRates[0]);
 
   /*
   result:
 
   Data in the structure immediately after receiving it:
   MqlRates data:
    Time = 2024.02.21 07:00;
    Open = 1.08143;
    High = 1.08158;
    Low = 1.08122;
    Close = 1.08137;
    Tick volume = 1341;
    Spread = 4;
    Real volume = 0
 
   Data in the structure after ZeroMemory():
   MqlRates data:
    Time = 0;
    Open = 0.00000;
    High = 0.00000;
    Low = 0.00000;
    Close = 0.00000;
    Tick volume = 0;
    Spread = 0;
    Real volume = 0
 
   Data in the MqlRates structure after copying it from a uchar array:
   MqlRates data:
    Time = 2024.02.21 07:00;
    Open = 1.08143;
    High = 1.08158;
    Low = 1.08122;
    Close = 1.08137;
    Tick volume = 1341;
    Spread = 4;
    Real volume = 0
   */
  }
//+------------------------------------------------------------------+
//| Print the fields of the MqlRates structure in the journal        |
//+------------------------------------------------------------------+
void MqlRatesPrint(MqlRates &rates)
  {
//--- create the output string
   string text=StringFormat(" Time = %s;\n"
                            " Open = %.*f;\n"
                            " High = %.*f;\n"
                            " Low = %.*f;\n"
                            " Close = %.*f;\n"
                            " Tick volume = %I64u;\n"
                            " Spread = %d;\n"
                            " Real volume = %I64u",
                            TimeToString(rates.time),
                            _Digits, rates.open,
                            _Digits, rates.high,
                            _Digits, rates.low,
                            _Digits, rates.close,
                            rates.tick_volume,
                            rates.spread,
                            rates.real_volume);
//--- print the header and the output string in the journal
   Print("MqlRates data:\n", text);
  }

```

See also

[StringToCharArray](/en/docs/convert/stringtochararray),[ ](/en/docs/constants/io_constants/codepageusage)[ShortArrayToString](/en/docs/convert/shortarraytostring),[CharArrayToStruct](/en/docs/convert/chararraytostruct), [Use of a Codepage](/en/docs/constants/io_constants/codepageusage), [FileWriteStruct](/en/docs/files/filewritestruct), [Unions (union)](/en/docs/basis/types/classes#union), [MathSwap](/en/docs/math/mathswap)
