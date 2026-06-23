# Using a Codepage in String Conversion Operations

When converting [string](/en/docs/basis/types/stringconst) variables into arrays of [char type](/en/docs/basis/types/integer/integertypes#char) and back, the encoding that by default corresponds to the current ANSI of Windows operating system (CP_ACP) is used in MQL5. If you want to specify a different type of encoding, it can be set as additional parameter for the [CharArrayToString()](/en/docs/convert/chararraytostring), [StringToCharArray()](/en/docs/convert/stringtochararray) and [FileOpen()](/en/docs/files/fileopen) functions.

The table lists the built-in constants for some of the most popular code pages. Not mentioned code pages can be specified by a code corresponding to the page.

Built-in Constants of Codepages

| Constant | Value | Description |
| --- | --- | --- |
| CP_ACP | 0 | The current Windows ANSI code page. |
| CP_OEMCP | 1 | The current system OEM code page. |
| CP_MACCP | 2 | The current system Macintosh code page. 
 Note:  This value is mostly used in earlier created program codes and is of no use now, since modern Macintosh computers use Unicode for encoding. |
| CP_THREAD_ACP | 3 | The Windows ANSI code page for the current thread. |
| CP_SYMBOL | 42 | Symbol code page |
| CP_UTF7 | 65000 | UTF-7 code page. |
| CP_UTF8 | 65001 | UTF-8 code page. |

See also

[Client Terminal Properties](/en/docs/constants/environment_state/terminalstatus#enum_terminal_info_integer)
