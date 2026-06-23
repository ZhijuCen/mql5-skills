# Selecting an encoding for text mode

For written text files, the encoding should be chosen based on the characteristics of the text or adjusted to the requirements of external programs for which the generated files are intended. If there are no external requirements, you can follow the rule to always use ANSI for plain texts with numbers, English letters and punctuation (a table of 128 such international characters is given in the section [String comparison](/en/book/common/strings/strings_comparison)). When working with various languages or special characters, use UTF-8 or Unicode, i.e. respectively:

```
int u8 = FileOpen("utf8.txt", FILE_WRITE | FILE_TXT | FILE_ANSI, 0, CP_UTF8);
int u0 = FileOpen("unicode.txt", FILE_WRITE | FILE_TXT | FILE_UNICODE);

```

For example, these settings are useful for saving the names of financial instruments to a file, since they sometimes use special characters that denote currencies or trading modes.

Reading your own files should not be a problem, because it is enough to specify the same encoding settings when reading as you did when writing. However, text files can come from different sources. Their encoding may be unknown, or subject to change without prior notice. Therefore, here comes the question of what to do if some of the files can be supplied as single-byte strings (ANSI), some as two-byte strings (Unicode), and some as UTF-8 encoding.

Encoding can be selected via the [input parameters](/en/book/basis/variables/input_variables) of the program. However, this is effective only for one file, and if you have to open many different files, their encodings may not match. Therefore, it is desirable to instruct the system to make the correct model choice on the fly (from file to file).

MQL5 does not allow 100% automatic detection and application of correct encodings, however, there is one most universal mode for reading a variety of text files. To do this, you need to set the following input parameters of the FileOpen function:

```
int h = FileOpen(filename, FILE_READ | FILE_TXT | FILE_ANSI, 0, CP_UTF8);

```

There are several factors at work.

First, the UTF-8 encoding transparently skips the mentioned 128 characters in any ANSI encoding (i.e. they are transmitted "one to one").

Second, it is the most popular for Internet protocols.

Third, MQL5 has an additional built-in analysis for text formatting in two-byte Unicode, which allows you to automatically switch the file operation mode to FILE_UNICODE, if necessary, regardless of the specified parameters. The fact is that files in Unicode format are usually preceded by a special pair of identifiers: 0xFFFE, or vice versa, 0xFEFF. This sequence is called the Byte Order Mark (BOM). It is needed because, as we know, bytes can be stored inside numbers in a different order on different platforms (this was discussed in the section [Endianness control in integers](/en/book/common/maths/maths_byte_swap)).

The FILE_UNICODE format uses a 2-byte integer (code) per character, so byte order becomes important, unlike other encodings. The Windows byte order BOM is 0xFFFE. If the MQL5 core finds this label at the beginning of a text file, its reading will automatically switch to Unicode mode.

Let's see how the different mode settings work with text files of different encodings. For this, we will use the FileText.mq5 script and several text files with the same content, but in different encodings (the size in bytes is indicated in brackets):

- ansi1252.txt (50): European encoding 1252 (it will be displayed in full without distortion in Windows with the European language)
- unicode1.txt (102): two-byte Unicode, at the beginning is the inherent Windows BOM 0xFFFE
- unicode2.txt (100): two-byte Unicode without BOM (in general, BOM is optional)
- unicode3.txt (102): two-byte Unicode, at the beginning there is BOM inherent to Unix, 0xFEFF
- utf8.txt (54): UTF-8 encoding

In the OnStart function, we will read these files in loops with different settings of FileOpen. Please note that by using FileHandle (reviewed in the [previous section](/en/book/common/files/files_handles)) we don't have to worry about closing files: everything happens automatically within each iteration.

```
void OnStart()
{
   Print("=====> UTF-8");
   for(int i = 0; i < ArraySize(texts); ++i)
   {
      FileHandle fh(FileOpen(texts[i], FILE_READ | FILE_TXT | FILE_ANSI, 0, CP_UTF8));
      Print(texts[i], " -> ", FileReadString(~fh));
   }
   
   Print("=====> Unicode");
   for(int i = 0; i < ArraySize(texts); ++i)
   {
      FileHandle fh(FileOpen(texts[i], FILE_READ | FILE_TXT | FILE_UNICODE));
      Print(texts[i], " -> ", FileReadString(~fh));
   }
   
   Print("=====> ANSI/1252");
   for(int i = 0; i < ArraySize(texts); ++i)
   {
      FileHandle fh(FileOpen(texts[i], FILE_READ | FILE_TXT | FILE_ANSI, 0, 1252));
      Print(texts[i], " -> ", FileReadString(~fh));
   }
}

```

The FileReadString function reads a string from a file. We'll cover it in the section on [writing and reading variables](/en/book/common/files/files_txt_atomic).

Here is an example log with the script execution results:

```
=====> UTF-8
MQL5Book/ansi1252.txt -> This is a text with special characters: ?? / ? / ?
MQL5Book/unicode1.txt -> This is a text with special characters: ±Σ / £ / ¥
MQL5Book/unicode2.txt -> T
MQL5Book/unicode3.txt -> ??
MQL5Book/utf8.txt -> This is a text with special characters: ±Σ / £ / ¥
=====> Unicode
MQL5Book/ansi1252.txt -> 桔獩椠⁳⁡整瑸眠瑩⁨灳捥慩⁬档牡捡整獲㾱⼠ꌠ⼠ꔠ
MQL5Book/unicode1.txt -> This is a text with special characters: ±Σ / £ / ¥
MQL5Book/unicode2.txt -> This is a text with special characters: ±Σ / £ / ¥
MQL5Book/unicode3.txt -> 吀栀椀猀 椀猀 愀 琀攀砀琀 眀椀琀栀 猀瀀攀挀椀愀氀 挀栀愀爀愀挀琀攀爀猀㨀 넀
MQL5Book/utf8.txt -> 桔獩椠⁳⁡整瑸眠瑩⁨灳捥慩⁬档牡捡整獲뇂ꏎ⼠술₣ ꗂ
=====> ANSI/1252
MQL5Book/ansi1252.txt -> This is a text with special characters: ±? / £ / ¥
MQL5Book/unicode1.txt -> This is a text with special characters: ±Σ / £ / ¥
MQL5Book/unicode2.txt -> T
MQL5Book/unicode3.txt -> þÿ
MQL5Book/utf8.txt -> This is a text with special characters: Â±Î£ / Â£ / Â¥

```

The unicode1.txt file is always read correctly because it has BOM 0xFFFE, and the system ignores the settings in the source code. However, if the label is missing or is big-endian, this auto-detection does not work. Also, when setting FILE_UNICODE, we lose the ability to read single-byte texts and UTF-8.

As a result, the aforementioned combination of FILE_ANSI and CP_UTF8 should be considered more resistant to variations in formatting. Selecting a specific national code page is only recommended when required explicitly.

Despite the significant help provided for the programmer from the API when working with files in text mode, we can, if necessary, avoid the FILE_TXT or FILE_CSV mode, and open a text file in binary mode FILE_BINARY. This will shift all the complexity of parsing text and determining the encoding onto the shoulders of the programmer, but it will allow them to support other non-standard formats. But the main point here is that text can be read from and written to a file opened in binary mode. However, the opposite, in the general case, is impossible. A binary file with arbitrary data (which means, it does not contain strings exclusively) opened in text mode will most likely be interpreted as text "gibberish". If you need to write binary data to a text file, first use the [CryptEncode](/en/book/advanced/crypt/crypt_encode) function and CRYPT_BASE64 encoding.
