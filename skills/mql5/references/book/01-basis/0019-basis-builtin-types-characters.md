# Character types

Character data types are intended for storing particular characters (letters), of which strings are formed (see [Strings](/en/book/basis/builtin_types/strings)). MQL5 has 4 character types: Two sized 1 byte (char, uchar) and two sized 2 bytes (short, ushort). Types prefixed with 'u' are unsigned.

In fact, character types are integer ones, since they store an integer code of a character from the relevant table: For char, it is the table of ASCII characters (codes 0-127); for uchar, it is extended ASCII (codes 0-255); and for short/ushort, it is the Unicode table (up to 65535 characters in the unsigned version). If it is of any interest to you, ASCII is the abbreviated American Standard Code for Information Interchange.

For MQL5 strings, 2-byte chars ushort are used. 1-byte uchar types are normally used to integrate with external programs when transferring the [arrays](/en/book/basis/arrays) of random data that are packed and unpacked in other types according to applied protocols, such as for connecting to a crypto platform.

Constants of characters are recorded as letters enclosed in single quotes. However, you can also use the integer notation (see [Integers](/en/book/basis/builtin_types/integer_numbers)) considered above. At the same time, the integer must be within the range of values for 1- or 2-byte format.

Additionally, we can use the notation of escape sequences. They use a backslash ('\') as the first character followed by one of the predefined control characters and/or a numerical code. MQL5 supports the following escape sequences:

- \n — new line
- \r — carriage return
- \t — tabulation
- \\ — backslash
- \" — double quote
- \' — single quote
- \X or \x — prefix to subsequently specify a numerical code in hexadecimal format
- \0 — prefix to subsequently specify a numerical code in octal format

Basic methods of using the constants of character types are given in script MQL5/Scripts/MQL5Book/p2/TypeChar.mq5.

```
void OnStart()
{
  char a1 = 'a';  // ok, a1 = 97, English letter 'a' code
  char a2 = 97;   // ok, a2 = 'a' as well
  char b = '£';   // warning: truncation of constant value, b = -93
  uchar c = '£';  // ok, c = 163, pound symbol code
  short d = '£';  // ok
  short z = '\0';    // ok, 0
  short t = '\t';    // ok, 9
  short s1 = '\x5c'; // ok, backslash code 92
  short s2 = '\\';   // ok, backslash as is, code 92 as well
  short s3 = '\0134';// ok, backslash code in octal form
}

```

Variables a1 and a2 get the value of character 'a' (English letter) in two different ways.

There is an attempt to record '£' in variable b, but its code 163 is beyond the range char (127); therefore it is "transformed" into the signed -93 (compiler gives a warning). The variables of types uchar (c) and short (d) that follow it perceive this code as normal.

Other variables are initialized using escape sequences.

Characters can be processed with the same operations as integers (see [Expressions](/en/book/basis/expressions)).
