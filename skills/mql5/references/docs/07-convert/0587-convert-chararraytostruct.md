# CharArrayToStruct

Copy uchar type array to [POD structure](/en/docs/basis/types/classes#simple_structure).

```
bool  CharArrayToStruct(
   void&         struct_object,    // structure
   const uchar&  char_array[],     // array
   uint          start_pos=0       // starting position in the array
   );

```

Parameters

struct_object

[in]  Reference to any type of [POD structure](/en/docs/basis/types/classes#simple_structure) (containing only simple data types).

char_array[]

[in]  [uchar](/en/docs/basis/types/integer/integertypes) type array.

start_pos=0

[in]  Position in the array, data copying starts from.

Return Value

Returns true if successful, otherwise false.

Example:

```
#define DATA_TOTAL 4
 
MqlRates ExtDataRates[DATA_TOTAL];
uchar    ExtCharArray[];
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- copy the data of the last four bars into the uchar array
   ResetLastError();
   for(int i=0; i<DATA_TOTAL; i++)
     {
      if(!CopyRatesToCharArray(i, ExtCharArray))
         return;
     }
 
//--- copy all available data into the MqlRates structure array in a loop by the amount of data from the uchar array
   for(int i=0; i<DATA_TOTAL; i++)
     {
      ResetLastError();
      if(!CharArrayToStruct(ExtDataRates[i], ExtCharArray, sizeof(MqlRates)*i))
        {
         Print("CharArrayToStruct() failed. Error code: ", GetLastError());
         return;
        }
      //--- upon successful copying of data from the uchar array to the MqlRates structure,
      //--- print the data, copied into the structure, to the journal
      MqlRatesPrint(ExtDataRates[i]);
     }
 
   /*
   result:
   MqlRates data:
    Time = 2024.02.21 09:00;
    Open = 1.08116;
    High = 1.08141;
    Low = 1.08062;
    Close = 1.08124;
    Tick volume = 5344;
    Spread = 1;
    Real volume = 0
 
   MqlRates data:
    Time = 2024.02.21 08:00;
    Open = 1.08149;
    High = 1.08153;
    Low = 1.08073;
    Close = 1.08114;
    Tick volume = 3607;
    Spread = 2;
    Real volume = 0
 
   MqlRates data:
    Time = 2024.02.21 07:00;
    Open = 1.08143;
    High = 1.08165;
    Low = 1.08122;
    Close = 1.08150;
    Tick volume = 2083;
    Spread = 0;
    Real volume = 0
 
   MqlRates data:
    Time = 2024.02.21 06:00;
    Open = 1.08178;
    High = 1.08190;
    Low = 1.08132;
    Close = 1.08142;
    Tick volume = 1733;
    Spread = 0;
    Real volume = 0
   */
  }
//+------------------------------------------------------------------+
//| Copy bar data to the uchar array                                 |
//| by the specified index via the MqlRates structure                |
//+------------------------------------------------------------------+
bool CopyRatesToCharArray(const int index, uchar &data_array[])
  {
   MqlRates rates[1];
   uint     start=sizeof(MqlRates);
 
   ResetLastError();
   if(CopyRates(Symbol(), PERIOD_CURRENT, index, 1, rates)!=1)
     {
      Print("CopyRates() failed. Error code: ", GetLastError());
      return(false);
     }
   if(!StructToCharArray(rates[0], data_array, start*index))
     {
      Print("StructToCharArray() failed. Error code: ", GetLastError());
      return(false);
     }
 
   return(true);
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
   Print("MqlRates data:\n", text, "\n");
  }

```

See also

[StringToCharArray](/en/docs/convert/stringtochararray),[ ](/en/docs/constants/io_constants/codepageusage)[ShortArrayToString](/en/docs/convert/shortarraytostring), [StructToCharArray](/en/docs/convert/structtochararray),[ Use of a Codepage](/en/docs/constants/io_constants/codepageusage), [FileReadStruct](/en/docs/files/filereadstruct), [Unions (union)](/en/docs/basis/types/classes#union), [MathSwap](/en/docs/math/mathswap)
