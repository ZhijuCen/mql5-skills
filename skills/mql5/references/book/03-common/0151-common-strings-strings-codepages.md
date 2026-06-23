# Working with symbols and code pages

Since strings are made up of characters, it is sometimes necessary or simply more convenient to manipulate individual characters or groups of characters in a string at the level of their integer codes. For example, you need to read or replace characters one at a time or convert them into arrays of integer codes for transmission over communication protocols or into third-party programming interfaces of [dynamic libraries](/en/book/advanced/libraries/libraries_dll) DLL. In all such cases, passing strings as text can be accompanied by various difficulties:

- ensuring the correct encoding (of which there are a great many, and the choice of a specific one depends on the operating system locale, program settings, the configuration of the servers with which communication is carried out, and much more)
- conversion of national language characters from the local text encoding to Unicode and vice versa
- allocation and deallocation of memory in a unified way

The use of arrays with integer codes (while such use actually produces a binary rather than a textual representation of the string) simplifies these problems.

The MQL5 API provides a set of functions to operate on individual characters or their groups, taking into account encoding features.

Strings in MQL5 contain characters in two-byte Unicode encoding. This provides universal support for the entire variety of national alphabets in a single (but very large) character table. Two bytes allow the encoding of 65535 elements.

The default character type is ushort. However, if necessary, the string can be converted to a sequence of single-byte uchar characters in a specific language encoding. This conversion may be accompanied by the loss of some information (in particular, letters that are not in the localized character table may "lose" umlauts or even "turn" into some kind of substitute character: depending on the context, it can be displayed differently, but usually as ' ?' or a square character).

To avoid problems with texts that may contain arbitrary characters, it is recommended that you always use Unicode. An exception can be made if some external services or programs that should be integrated with your MQL program do not support Unicode, or if the text is intended from the beginning to store a limited set of characters (for example, only numbers and Latin letters).

When converting to/from single-byte characters, the MQL5 API uses the ANSI encoding by default, depending on the current Windows settings. However, the developer can specify a different code table (see further functions CharArrayToString, StringToCharArray).

Examples of using the functions described below are given in the StringSymbols.mq5 file.

bool StringSetCharacter(string &variable, int position, ushort character)

The function changes the character at position to the character value in the passed variable string. The number must be between 0 and the string length ([StringLen](/en/book/common/strings/strings_init)) minus 1.

If the character to be written is 0, it specifies a new line ending (acts as a terminal zero), i.e. the length of the line becomes equal to position. The size of the buffer allocated for the line does not change.

If the position parameter is equal to the length of the string and the character being written is not equal to 0, then the character is added to the string and its length is increased by 1. This is equivalent to the expression: variable += ShortToString(character).

The function returns true upon successful completion, or false in case of error.

```
void OnStart()
{
   string numbers = "0123456789";
   PRT(numbers);
   PRT(StringSetCharacter(numbers, 7, 0));   // cut off at the 7th character
   PRT(numbers);                             // 0123456
   PRT(StringSetCharacter(numbers, StringLen(numbers), '*')); // add '*'
   PRT(numbers);                             // 0123456*
   ...
}

```

ushort StringGetCharacter(string value, int position)

The function returns the code of the character located at the specified position in the string. The position number must be between 0 and the string length ([StringLen](/en/book/common/strings/strings_init)) minus 1. In case of an error, the function will return 0.

The function is equivalent to writing using the operator '[]': value[position].

```
   string numbers = "0123456789";
   PRT(StringGetCharacter(numbers, 5));      // 53 = code '5'
   PRT(numbers[5]);                          // 53 - is the same 

```

string CharToString(uchar code)

The function converts the ANSI code of a character to a single-character string. Depending on the set Windows code page, the upper half of the codes (greater than 127) can generate different letters (the character style is different, while the code remains the same). For example, the symbol with the code 0xB8 (184 in decimal) denotes a cedilla (lower hook) in Western European languages, while in the Russian language the letter 'ё' is located here. Here's another example:

```
   PRT(CharToString(0xA9));   // "©"
  PRT(CharToString(0xE6));   // "æ", "ж", or another character
                             // depending on your Windows locale

```

string ShortToString(ushort code)

The function converts the Unicode code of a character to a single-character string. For the code parameter, you can use a literal or an integer. For example, the Greek capital letter "sigma" (the sign of the sum in mathematical formulas) can be specified as 0x3A3 or 'Σ'.

```
   PRT(ShortToString(0x3A3)); // "Σ"
   PRT(ShortToString('Σ'));   // "Σ"

```

int StringToShortArray(const string text, ushort &array[], int start = 0, int count = -1)

The function converts a string to a sequence of ushort character codes that are copied to the specified location in the array: starting from the element numbered start (0 by default, that is, the beginning of the array) and in the amount of count.

Please note: the start parameter refers to the position in the array, not in the string. If you want to convert part of a string, you must first extract it using the [StringSubstr](/en/book/common/strings/strings_find_replace_split) function.

If the count parameter is equal to -1 (or WHOLE_ARRAY), all characters up to the end of the string (including the terminal null) or characters in accordance with the size of the array, if it is a fixed size, are copied.

In the case of a dynamic array, it will be automatically increased in size if necessary. If the size of a dynamic array is greater than the length of the string, then the size of the array is not reduced.

To copy characters without a terminating null, you must explicitly call StringLen as the count argument. Otherwise, the length of the array will be by 1 more than the length of the string (and 0 in the last element).

The function returns the number of copied characters.

```
   ...
   ushort array1[], array2[]; // dynamic arrays 
   ushort text[5];            // fixed size array 
   string alphabet = "ABCDEАБВГД";
   // copy with the terminal '0'
   PRT(StringToShortArray(alphabet, array1)); // 11
   ArrayPrint(array1); // 65   66   67   68   69 1040 1041 1042 1043 1044    0
   // copy without the terminal '0'
   PRT(StringToShortArray(alphabet, array2, 0, StringLen(alphabet))); // 10
   ArrayPrint(array2); // 65   66   67   68   69 1040 1041 1042 1043 1044
   // copy to a fixed array 
   PRT(StringToShortArray(alphabet, text)); // 5
   ArrayPrint(text); // 65 66 67 68 69
   // copy beyond the previous limits of the array 
   // (elements [11-19] will be random)
   PRT(StringToShortArray(alphabet, array2, 20)); // 11
   ArrayPrint(array2);
   /*
   [ 0]    65    66    67    68    69  1040  1041  1042
         1043  1044     0     0     0     0     0 14245
   [16] 15102 37754 48617 54228    65    66    67    68
           69  1040  1041  1042  1043  1044     0
   */

```

Note that if the position for copying is beyond the size of the array, then the intermediate elements will be allocated but not initialized. As a result, they may contain random data (highlighted in yellow above).

string ShortArrayToString(const ushort &array[], int start = 0, int count = -1)

The function converts part of the array with character codes to a string. The range of array elements is set by parameters start and count, the starting position, and quantity, respectively. The parameter start must be between 0 and the number of elements in the array minus 1. If count is equal to -1 (or WHOLE_ARRAY) all elements up to the end of the array or up to the first null are copied.

Using the same example from StringSymbols.mq5, let's try to convert an array into the array2 string, which has a size of 30.

```
   ...
   string s = ShortArrayToString(array2, 0, 30);
   PRT(s); // "ABCDEАБВГД", additional random characters may appear here

```

Because in the array array2 the string "ABCDEABCD" was copied twice, and specifically, firstly to the very beginning, and the second time —at offset 20, the intermediate characters will be random and able to form a longer string than we did.

int StringToCharArray(const string text, uchar &array[], int start = 0, int count = -1, uint codepage = CP_ACP)

The function converts the text string into a sequence of single-byte characters that are copied to the specified location in the array: starting from the element numbered start (0 by default, that is, the beginning of the array) and in the amount of count. The copying process converts characters from Unicode to the selected code page codepage — by default, CP_ACP, which means the language of the Windows operating system (more on this below).

If the count parameter is equal to -1 (or WHOLE_ARRAY), all characters up to the end of the string (including the terminal null) or in accordance with the size of the array, if it is a fixed size, are copied.

In the case of a dynamic array, it will be automatically increased in size if necessary. If the size of a dynamic array is greater than the length of the string, then the size of the array is not reduced.

To copy characters without a terminating null, you must explicitly call [StringLen](/en/book/common/strings/strings_init) as an argument count.

The function returns the number of copied characters.

See the list of valid code pages for the parameter codepage in the documentation. Here are some of the widely used ANSI code pages:

| Language | Code |
| --- | --- |
| Central European Latin | 1250 |
| Cyrillic | 1251 |
| Western European Latin | 1252 |
| Greek | 1253 |
| Turkish | 1254 |
| Hebrew | 1255 |
| Arab | 1256 |
| Baltic | 1257 |

Thus, on computers with Western European languages, CP_ACP is 1252, and, for example, on computers with Russian, it is 1251.

During the conversion process, some characters may be converted with loss of information, since the Unicode table is much larger than ANSI (each ANSI code table has 256 characters).

In this regard, CP_UTF8 is of particular importance among all the CP_*** constants. It allows national characters to be properly preserved by variable-length encoding: the resulting array still stores bytes, but each national character can span multiple bytes, written in a special format. Because of this, the length of the array can be significantly larger than the length of the string. UTF-8 encoding is widely used on the Internet and in various software. Incidentally, UTF stands for Unicode Transformation Format, and there are other modifications, notably UTF-16 and UTF-32.

We will consider an example for StringToCharArray after we get acquainted with the "inverse" function CharArrayToString: their work must be demonstrated in conjunction.

string CharArrayToString(const uchar &array[], int start = 0, int count = -1, uint codepage = CP_ACP)

The function converts an array of bytes or part of it into a string. The array must contain characters in a specific encoding. The range of array elements is set by parameters start and count, the starting position, and quantity, respectively. The parameter start must be between 0 and the number of elements in the array. When count is equal to -1 (or WHOLE_ARRAY) all elements up to the end of the array or up to the first null are copied.

Let's see how the functions StringToCharArray and CharArrayToString work with different national characters with different code page settings. A test script StringCodepages.mq5 has been prepared for this.

Two lines will be used as the test subjects - in Russian and German:

```
void OnStart()
{
   Print("Locales");
   uchar bytes1[], bytes2[];
 
   string german = "straßenführung";
   string russian = "Russian text";
   ...

```

We will copy them into arrays bytes1 and bytes2 and then restore them to strings.

First, let's convert the German text using the European code page 1252.

```
   ...
   StringToCharArray(german, bytes1, 0, WHOLE_ARRAY, 1252);
   ArrayPrint(bytes1);
   // 115 116 114  97 223 101 110 102 252 104 114 117 110 103   0

```

On European copies of Windows, this is equivalent to a simpler function call with default parameters, because there CP_ACP = 1252:

```
   StringToCharArray(german, bytes1);

```

Then we restore the text from the array with the following call and make sure that everything matches the original:

```
   ...
   PRT(CharArrayToString(bytes1, 0, WHOLE_ARRAY, 1252));
   // CharArrayToString(bytes1,0,WHOLE_ARRAY,1252)='straßenführung'

```

Now let's try to convert the Russian text in the same European encoding (or you can call StringToCharArray(english, bytes2) in the Windows environment where CP_ACP is set to 1252 as the default code page):

```
   ...
   StringToCharArray(russian, bytes2, 0, WHOLE_ARRAY, 1252);
   ArrayPrint(bytes2);
   // 63 63 63 63 63 63 63 32 63 63 63 63 63  0

```

Here you can already see that there was a problem during the conversion because 1252 does not have Cyrillic. Restoring a string from an array clearly shows the essence:

```
   ...
   PRT(CharArrayToString(bytes2, 0, WHOLE_ARRAY, 1252));
   // CharArrayToString(bytes2,0,WHOLE_ARRAY,1252)='??????? ?????'

```

Let's repeat the experiment in a conditional Russian environment, i.e., we will convert both strings back and forth using the Cyrillic code page 1251.

```
   ...
   StringToCharArray(russian, bytes2, 0, WHOLE_ARRAY, 1251);
   // on Russian Windows, this call is equivalent to a simpler one
   // StringToCharArray(russian, bytes2);
   // because CP_ACP = 1251
   ArrayPrint(bytes2); // this time the character codes are meaningful
   // 208 243 241 241 234 232 233  32 210 229 234 241 242   0
   
   // restore the string and make sure it matches the original
   PRT(CharArrayToString(bytes2, 0, WHOLE_ARRAY, 1251));
   // CharArrayToString(bytes2,0,WHOLE_ARRAY,1251)='Русский Текст'
   
   // and for the German text...
   StringToCharArray(german, bytes1, 0, WHOLE_ARRAY, 1251);
   ArrayPrint(bytes1);
   // 115 116 114  97  63 101 110 102 117 104 114 117 110 103   0
   // if we compare this content of bytes1 with the previous version,
   // it's easy to see that a couple of characters are affected; here's what happened:
   // 115 116 114  97 223 101 110 102 252 104 114 117 110 103   0
   
   // restore the string to see the differences visually:
   PRT(CharArrayToString(bytes1, 0, WHOLE_ARRAY, 1251));
   // CharArrayToString(bytes1,0,WHOLE_ARRAY,1251)='stra?enfuhrung'
   // specific German characters were corrupted

```

Thus, the fragility of single-byte encodings is evident.

Finally, let's enable the CP_UTF8 encoding for both test strings. This part of the example will work stably regardless of Windows settings.

```
   ...
   StringToCharArray(german, bytes1, 0, WHOLE_ARRAY, CP_UTF8);
   ArrayPrint(bytes1);
   // 115 116 114  97 195 159 101 110 102 195 188 104 114 117 110 103   0
   PRT(CharArrayToString(bytes1, 0, WHOLE_ARRAY, CP_UTF8));
   // CharArrayToString(bytes1,0,WHOLE_ARRAY,CP_UTF8)='straßenführung'
   
   StringToCharArray(russian, bytes2, 0, WHOLE_ARRAY, CP_UTF8);
   ArrayPrint(bytes2);
   // 208 160 209 131 209 129 209 129 208 186 208 184 208 185
   //  32 208 162 208 181 208 186 209 129 209 130   0
   PRT(CharArrayToString(bytes2, 0, WHOLE_ARRAY, CP_UTF8));
   // CharArrayToString(bytes2,0,WHOLE_ARRAY,CP_UTF8)='Русский Текст'

```

Note that both of the UTF-8 encoded strings required larger arrays than ANSI ones. Moreover, the array with the Russian text has actually become 2 times longer, because all letters now occupy 2 bytes. Those who wish can find details in open sources on how exactly the UTF-8 encoding works. In the context of this book, it is important for us that the MQL5 API provides ready-made functions to work with.
