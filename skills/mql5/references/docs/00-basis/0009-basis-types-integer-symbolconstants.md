# Character Constants

Characters as elements of a [string](/en/docs/basis/types/stringconst) in MQL5 are indexes in the Unicode character set. They are hexadecimal values that can be cast into integers, and that can be manipulated by integer [operations](/en/docs/basis/operations/mathoperation) like addition and subtraction.

Any single character in quotation marks or a hexadecimal ASCII code of a character as '\x10' is a character constant and is of [ushort](/en/docs/basis/types/integer/integertypes#ushort) type. For example, a record of '0' type is a numerical value 30, that corresponds to the index of zero in the table of characters.

Example:

```
void OnStart()
  {
//--- define character constants
   int symbol_0='0';
   int symbol_9=symbol_0+9; // get symbol '9'
//--- output values of constants 
   printf("In a decimal form: symbol_0 = %d,  symbol_9 = %d",symbol_0,symbol_9);
   printf("In a hexadecimal form: symbol_0 = 0x%x,  symbol_9 = 0x%x",symbol_0,symbol_9);
//--- enter constants into a string
   string test=""; 
   StringSetCharacter(test,0,symbol_0);
   StringSetCharacter(test,1,symbol_9);
//--- this is what they look like in a string
   Print(test);
  }

```

A backslash is a control character for a compiler when dealing with constant strings and character constants in a source text of a program. Some symbols, for example a single quote ('), double quotes ("), backslash (\) and control characters can be represented as a combination of symbols that start with a backslash (\), according to the below table:

| Character name | Mnemonic code or image | Record in MQL5 | Numeric value |
| --- | --- | --- | --- |
| new line (line feed) | LF | '\n' | 10 |
| horizontal tab | HT | '\t' | 9 |
| carriage return | CR | '\r' | 13 |
| backslash | \ | '\\' | 92 |
| single quote | ' | '\'' | 39 |
| double quote | " | '\"' | 34 |
| hexadecimal code | hhhh | '\xhhhh' | 1 to 4 hexadecimal characters |
| decimal code | d | '\d' | decimal number from 0 to 65535 |

If a backslash is followed by a character other than those described above, result is undefined.

Example

```
void OnStart()
  {
//--- declare character constants
   int a='A';
   int b='$';
   int c='©';      // code 0xA9
   int d='\xAE';   // code of the symbol ®
//--- output print constants
   Print(a,b,c,d);
//--- add a character to the string
   string test="";
   StringSetCharacter(test,0,a);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,b);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,c);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,d);
   Print(test);
//--- represent characters as a number
   int a1=65;
   int b1=36;
   int c1=169;
   int d1=174;
//--- add a character to the string
   StringSetCharacter(test,1,a1);
   Print(test);
//--- add a character to the string
   StringSetCharacter(test,1,b1);
   Print(test);
//--- add a character to the string
   StringSetCharacter(test,1,c1);
   Print(test);
//--- add a character to the string
   StringSetCharacter(test,1,d1);
   Print(test);
  }

```

As it was mentioned above, the value of a character constant (or variable) is an index in the table of characters. Index being an integer, it can be written in different ways.

```
void OnStart()
  {
//--- 
   int a=0xAE;     // the code of ® corresponds to the '\xAE' literal
   int b=0x24;     // the code of $ corresponds to the '\x24' literal
   int c=0xA9;     // the code of © corresponds to the '\xA9' literal
   int d=0x263A;   // the code of ☺ corresponds to the '\x263A' literal
//--- show values
   Print(a,b,c,d);
//--- add a character to the string
   string test="";
   StringSetCharacter(test,0,a);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,b);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,c);
   Print(test);
//--- replace a character in a string
   StringSetCharacter(test,0,d);
   Print(test);
//--- codes of suits
   int a1=0x2660;
   int b1=0x2661;
   int c1=0x2662;
   int d1=0x2663;
//--- add a character of spades
   StringSetCharacter(test,1,a1);
   Print(test);
//--- add a character of hearts
   StringSetCharacter(test,2,b1);
   Print(test);
//--- add a character of diamonds
   StringSetCharacter(test,3,c1);
   Print(test);
//--- add a character of clubs
   StringSetCharacter(test,4,d1);
   Print(test);
//--- Example of character literals in a string
   test="Queen\x2660Ace\x2662";
   printf("%s",test);
  }

```

The internal representation of a character literal is the [ushort](/en/docs/basis/types/integer/integertypes#ushort) type. Character constants can accept values from 0 to 65535.

See also

[StringSetCharacter()](/en/docs/strings/stringsetcharacter),  [StringGetCharacter()](/en/docs/strings/stringgetcharacter), [ShortToString()](/en/docs/convert/shorttostring), [ShortArrayToString()](/en/docs/convert/shortarraytostring), [StringToShortArray()](/en/docs/convert/stringtoshortarray)
