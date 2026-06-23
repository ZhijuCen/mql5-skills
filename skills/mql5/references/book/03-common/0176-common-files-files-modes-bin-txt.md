# Information storage methods: text and binary

We have already seen in many previous sections that the same information can be represented in textual and binary forms. For example, numbers of int, long, and double formats, date and time (datetime) and colors (color) are stored in memory as a sequence of bytes of a certain length. This method is compact and is better for computer interpretation, but it is more convenient for a human to analyze information in a text form, although it takes longer. Therefore, we paid much attention to [converting numbers to strings and vice versa](/en/book/common/conversions/conversions_numbers), and to [functions for working with strings](/en/book/common/strings).

At the file level, the division into the binary and textual representation of data is also preserved. A binary file is designed to store data in the same internal representation that is used in memory. The text file contains a string representation.

Text files are commonly used for standard formats such as CSV (Comma Separated Values), JSON (JavaScript Object Notation), XML (Extensible Markup Language), HTML (HyperText Markup Language).

Binary files, of course, also have standard formats for many applications, in particular for images (PNG, GIF, JPG, BMP), sounds (WAV, MP3), or compressed archives (ZIP). However, the binary format initially assumes greater protection and low-level work with data, and therefore is more often used to solve internal problems, when only storage efficiency and data availability for a specific program are important. In other words, objects of any applied structures and classes can easily save and restore their state in a binary file, actually making a memory impression and not worrying about compatibility with any standard.

In theory, we could manually convert the data to strings when writing to a binary file and then convert it back from strings to numbers (or structures, or arrays) when reading the file. This would be similar to what the text file mode automatically provides but would require additional effort. The text file mode saves us from such a routine. Moreover, the MQL5 file subsystem implicitly performs several optional but important operations that are necessary when working with text.

First, the concept of text is based on some general rules of using delimiter characters. In particular, it is assumed that all texts consist of strings. This way it is more convenient to read and analyze them algorithmically. Therefore, there are special characters that separate one string from another.

Here we are faced with the first difficulties associated with the fact that different operating systems accept different combinations of these characters. In Windows, the line separator is the sequence of two characters '\r\n' (either as hexadecimal codes: 0xD 0xA, or as the name CRLF, which stands for Carriage Return and Line Feed). In Unix and Linux, the single character '\n' is the standard, but some versions and programs under MacOS may use the single character '\r'.

Although MetaTrader 5 runs under Windows, we have no guarantee that any resulting text file will not be saved with unusual separators. If we were to read it in binary mode and check for delimiters ourselves to form strings, these discrepancies would require specific handling. Here the text mode of file operation in MQL5 comes to the rescue: it automatically normalizes line breaks when reading and writing.

MQL5 might not fix line breaks for all cases. In particular, a single character '\r' will not be interpreted as '\r\n' when reading a text file, while a single '\n' is correctly interpreted as '\r\n'.

Secondly, strings can be stored in memory in multiple representations. By default, string (type [string](/en/book/basis/builtin_types/strings)) in MQL5 consists of two-byte [characters](/en/book/basis/builtin_types/characters). This provides support for the universal Unicode encoding, which is nice because it includes all national scripts. However, in many cases, such universality is not required (for example, when storing numbers or messages in English), in which case it is more efficient to use strings of single-byte characters in the ANSI encoding. The MQL5 API functions allow you to choose the preferred way of writing strings in text mode into files. But if we control writing in our MQL program, we can guarantee the validity and reliability of switching from Unicode to single-byte characters. In this case, when integrating with some external software or web service, the ANSI code page in its files can be any. In this regard, the following point arises.

Thirdly, due to the presence of many different languages, you need to be prepared for texts in various ANSI encodings. Without the correct interpretation of the encoding, the text can be written or read with distortions, or even become unreadable. We saw it in the section [Working with symbols and code pages](/en/book/common/strings/strings_codepages). This is why file functions already include means for correct character processing: it is enough to specify the desired or expected encoding in the parameters. The choice of encoding is described in more detail in a [separate section](/en/book/common/files/files_txt_codepage).

And finally, the text mode has built-in support for the well-known CSV format. Since trading often requires tabular data, CSV is well suited for this. In a text file in CSV mode, the MQL5 API functions process not only delimiters for wrapping lines of text but also an additional delimiter for the border of columns (fields in each row of the table). This is usually a tab character '\t', a comma ',' or a semicolon ';'. For example, here is what a CSV file with Forex news looks like ( a comma-separated fragment is shown):

```
Title,Country,Date,Time,Impact,Forecast,Previous
Bank Holiday,JPY,08-09-2021,12:00am,Holiday,,
CPI y/y,CNY,08-09-2021,1:30am,Low,0.8%,1.1%
PPI y/y,CNY,08-09-2021,1:30am,Low,8.6%,8.8%
Unemployment Rate,CHF,08-09-2021,5:45am,Low,3.0%,3.1%
German Trade Balance,EUR,08-09-2021,6:00am,Low,13.9B,12.6B
Sentix Investor Confidence,EUR,08-09-2021,8:30am,Low,29.2,29.8
JOLTS Job Openings,USD,08-09-2021,2:00pm,Medium,9.27M,9.21M
FOMC Member Bostic Speaks,USD,08-09-2021,2:00pm,Medium,,
FOMC Member Barkin Speaks,USD,08-09-2021,4:00pm,Medium,,
BRC Retail Sales Monitor y/y,GBP,08-09-2021,11:01pm,Low,4.9%,6.7%
Current Account,JPY,08-09-2021,11:50pm,Low,1.71T,1.87T

```

And here it is, for clarity, in the form of a table:

| Title | Country | Date | Time | Impact | Forecast | Previous |
| --- | --- | --- | --- | --- | --- | --- |
| Bank Holiday | JPY | 08-09-2021 | 12:00am | Holiday |  |  |
| CPI y/y | CNY | 08-09-2021 | 1:30am | Low | 0.8% | 1.1% |
| PPI y/y | CNY | 08-09-2021 | 1:30am | Low | 8.6% | 8.8% |
| Unemployment Rate | CHF | 08-09-2021 | 5:45am | Low | 3.0% | 3.1% |
| German Trade Balance | EUR | 08-09-2021 | 6:00am | Low | 13.9B | 12.6B |
| Sentix Investor Confidence | EUR | 08-09-2021 | 8:30am | Low | 29.2 | 29.8 |
| JOLTS Job Openings | USD | 08-09-2021 | 2:00pm | Medium | 9.27M | 9.21M |
| FOMC Member Bostic Speaks | USD | 08-09-2021 | 2:00pm | Medium |  |  |
| FOMC Member Barkin Speaks | USD | 08-09-2021 | 4:00pm | Medium |  |  |
| BRC Retail Sales Monitor y/y | GBP | 08-09-2021 | 11:01pm | Low | 4.9% | 6.7% |
| Current Account | JPY | 08-09-2021 | 11:50pm | Low | 1.71T | 1.87T |
