# ShortArrayToString

It copies part of array into a returned string.

```
string  ShortArrayToString(
   ushort  array[],      // array
   int     start=0,      // starting position in the array
   int     count=-1      // number of symbols
   );

```

Parameters

array[]

[in]  Array of ushort type (analog of wchar_t type).

start=0

[in] Position, from which copying starts, Default - 0.

count=-1

[in]  Number of array elements to copy. Defines the length of a resulting string. Default value is -1, which means copying up to the array end, or till terminal 0.

Return Value

String.

Example:

```
#define ROW_SIZE 16
 
ushort ExtShortArray[]={0x2190,0x2191,0x2192,0x2193,0x2194,0x2195,0x2196,0x2197,0x2198,0x2199,0x219A,0x219B,0x219C,0x219D,0x219E,0x219F,
                        0x21A0,0x21A1,0x21A2,0x21A3,0x21A4,0x21A5,0x21A6,0x21A7,0x21A8,0x21A9,0x21AA,0x21AB,0x21AC,0x21AD,0x21AE,0x21AF,
                        0x21B0,0x21B1,0x21B2,0x21B3,0x21B4,0x21B5,0x21B6,0x21B7,0x21B8,0x21B9,0x21BA,0x21BB,0x21BC,0x21BD,0x21BE,0x21BF,
                        0x21C0,0x21C1,0x21C2,0x21C3,0x21C4,0x21C5,0x21C6,0x21C7,0x21C8,0x21C9,0x21CA,0x21CB,0x21CC,0x21CD,0x21CE,0x21CF,
                        0x21D0,0x21D1,0x21D2,0x21D3,0x21D4,0x21D5,0x21D6,0x21D7,0x21D8,0x21D9,0x21DA,0x21DB,0x21DC,0x21DD,0x21DE,0x21DF,
                        0x21E0,0x21E1,0x21E2,0x21E3,0x21E4,0x21E5,0x21E6,0x21E7,0x21E8,0x21E9,0x21EA,0x21EB,0x21EC,0x21ED,0x21EE,0x21EF,
                        0x21F0,0x21F1,0x21F2,0x21F3,0x21F4,0x21F5,0x21F6,0x21F7,0x21F8,0x21F9,0x21FA,0x21FB,0x21FC,0x21FD,0x21FE,0x21FF};
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- calculate the number of strings in the symbol table of 7x16
   int total=(int)ExtShortArray.Size()/ROW_SIZE;
//--- in a loop by the table rows, display 7 sets of arrows, 16 pieces in each row in Unicode characters, to the journal row by row
   for(int i=0; i<total; i++)
     {
      int row=i*ROW_SIZE;
      PrintFormat("Arrow set %u: %s",i+1,ShortArrayToString(ExtShortArray,row,ROW_SIZE));
     }
   /*
   result:
   Arrow set 1: ←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟
   Arrow set 2: ↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯
   Arrow set 3: ↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿
   Arrow set 4: ⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏
   Arrow set 5: ⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟
   Arrow set 6: ⇠⇡⇢⇣⇤⇥⇦⇧⇨⇩⇪⇫⇬⇭⇮⇯
   Arrow set 7: ⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿
   */
  }

```

See also

[StringToShortArray](/en/docs/convert/stringtoshortarray), [CharArrayToString](/en/docs/convert/chararraytostring), [Use of a Codepage](/en/docs/constants/io_constants/codepageusage)
