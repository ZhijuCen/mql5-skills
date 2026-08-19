# ShortToString

It converts the symbol code (unicode) into one-symbol string and returns resulting string.

```
string  ShortToString(
   ushort  symbol_code      // symbol
   );

```

Parameters

symbol_code

[in]  Symbol code. Instead of a symbol code you can use literal string containing a symbol or a literal string with 2-byte hexadecimal code corresponding to the symbol from the Unicode table.

Return Value

String.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- print 18 characters in a loop, starting with the character with the Unicode number of U+23E9
   for(int i=0; i<18; i++)
     {
      ushort code=0x23E9+(ushort)i;
      PrintFormat("Unicode number U+%hX: %s",code,ShortToString(code));
     }
   /*
   result:
   Unicode number U+23E9: ⏩
   Unicode number U+23EA: ⏪
   Unicode number U+23EB: ⏫
   Unicode number U+23EC: ⏬
   Unicode number U+23ED: ⏭
   Unicode number U+23EE: ⏮
   Unicode number U+23EF: ⏯
   Unicode number U+23F0: ⏰
   Unicode number U+23F1: ⏱
   Unicode number U+23F2: ⏲
   Unicode number U+23F3: ⏳
   Unicode number U+23F4: ⏴
   Unicode number U+23F5: ⏵
   Unicode number U+23F6: ⏶
   Unicode number U+23F7: ⏷
   Unicode number U+23F8: ⏸
   Unicode number U+23F9: ⏹
   Unicode number U+23FA: ⏺
   */
  }

```

See also

[StringToCharArray](/en/docs/convert/stringtochararray), [CharToString](/en/docs/convert/chartostring), [StringGetCharacter](/en/docs/strings/stringgetcharacter)
