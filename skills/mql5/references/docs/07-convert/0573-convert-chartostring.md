# CharToString

Converting a symbol code into a one-character string.

```
string  CharToString(
   uchar  char_code      // numeric code of symbol
   );

```

Parameters

char_code

[in]  Code of ANSI symbol.

Return Value

String with a ANSI symbol.

Example:

```
string ExtStrArray[224];
 
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- in the loop from the symbol code 32 (space) to 255(UCHAR_MAX),
//--- fill the array with symbol codes converted to a string in accordance with the current code page
   for(int i=32; i<=UCHAR_MAX; i++)
      ExtStrArray[i-32]=CharToString((uchar)i);
 
//--- print the header and the symbol table in the journal
   Print("Table of symbols:");
   ArrayPrint(ExtStrArray,_Digits," | ");
   /*
   result:
   Table of symbols:
   [  0] " " | "!" | """ | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
   [ 25] "9" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q"
   [ 50] "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
   [ 75] "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" | "" | "Ђ" | "Ѓ" | "‚" | "ѓ"
   [100] "„" | "…" | "†" | "‡" | "€" | "‰" | "Љ" | "‹" | "Њ" | "Ќ" | "Ћ" | "Џ" | "ђ" | "‘" | "’" | "“" | "”" | "•" | "–" | "—" | "˜" | "™" | "љ" | "›" | "њ"
   [125] "ќ" | "ћ" | "џ" | " " | "Ў" | "ў" | "Ј" | "¤" | "Ґ" | "¦" | "§" | "Ё" | "©" | "Є" | "«" | "¬" | "­" | "®" | "Ї" | "°" | "±" | "І" | "і" | "ґ" | "µ"
   [150] "¶" | "·" | "ё" | "№" | "є" | "»" | "ј" | "Ѕ" | "ѕ" | "ї" | "А" | "Б" | "В" | "Г" | "Д" | "Е" | "Ж" | "З" | "И" | "Й" | "К" | "Л" | "М" | "Н" | "О"
   [175] "П" | "Р" | "С" | "Т" | "У" | "Ф" | "Х" | "Ц" | "Ч" | "Ш" | "Щ" | "Ъ" | "Ы" | "Ь" | "Э" | "Ю" | "Я" | "а" | "б" | "в" | "г" | "д" | "е" | "ж" | "з"
   [200] "и" | "й" | "к" | "л" | "м" | "н" | "о" | "п" | "р" | "с" | "т" | "у" | "ф" | "х" | "ц" | "ч" | "ш" | "щ" | "ъ" | "ы" | "ь" | "э" | "ю" | "я"
   */
  }

```

See also

[StringToCharArray](/en/docs/convert/stringtochararray), [ShortToString](/en/docs/convert/shorttostring), [StringGetCharacter](/en/docs/strings/stringgetcharacter)
