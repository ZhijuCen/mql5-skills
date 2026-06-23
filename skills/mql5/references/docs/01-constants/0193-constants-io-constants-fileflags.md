# File Opening Flags

File opening flag values specify the file access mode. Flags are defined as follows:

| Identifier | Value | Description |
| --- | --- | --- |
| FILE_READ | 1 | File is opened for reading. Flag is used in  FileOpen() . When opening a file specification of FILE_WRITE and/or FILE_READ is required. |
| FILE_WRITE | 2 | File is opened for writing. Flag is used in  FileOpen() . When opening a file specification of FILE_WRITE and/or FILE_READ is required. |
| FILE_BIN | 4 | Binary read/write mode (without string to string conversion). Flag is used in  FileOpen() . |
| FILE_CSV | 8 | CSV file (all its elements are converted to strings of the appropriate type, Unicode or ANSI, and separated by separator). Flag is used in  FileOpen() . |
| FILE_TXT | 16 | Simple text file (the same as csv file, but without taking into account the separators). Flag is used in  FileOpen() . |
| FILE_ANSI | 32 | Strings of ANSI type (one byte symbols). Flag is used in  FileOpen() . |
| FILE_UNICODE | 64 | Strings of UNICODE type (two byte symbols). Flag is used in  FileOpen() . |
| FILE_SHARE_READ | 128 | Shared access for reading from several programs. Flag is used in  FileOpen() , but it does not replace the necessity to indicate FILE_WRITE and/or the FILE_READ flag when opening a file. |
| FILE_SHARE_WRITE | 256 | Shared access for writing from several programs. Flag is used in  FileOpen() , but it does not replace the necessity to indicate FILE_WRITE and/or the FILE_READ flag when opening a file. |
| FILE_REWRITE | 512 | Possibility for the file rewrite using functions  FileCopy()  and  FileMove() . The file should exist or should be opened for writing, otherwise the file will not be opened. |
| FILE_COMMON | 4096 | The file path in the common folder of all client terminals  \Terminal\Common\Files . Flag is used in  FileOpen() ,  FileCopy() ,  FileMove()  and in  FileIsExist()  functions. |

One or several flags can be specified when opening a file. This is a combination of flags. The combination of flags is written using the sign of logical OR (|), which is positioned between enumerated flags. For example, to open a file in CSV format for reading and writing at the same time, specify the combination FILE_READ|FILE_WRITE|FILE_CSV.

Example:

```
   int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_CSV);

```

There are some specific features of work when you specify read and write flags:

- If FILE_READ is specified, an attempt is made to open an existing file. If a file does not exist, file opening fails, a new file is not created.
- FILE_READ|FILE_WRITE – a new file is created if the file with the specified name does not exist.
- FILE_WRITE –  the file is created again with a zero size.

When opening a file, specification of FILE_WRITE and/or FILE_READ is required.

Flags that define the type of reading of an open file possess priority. The highest flag is FILE_CSV, then goes FILE_BIN, and FILE_TXT is of lowest priority. Thus, if several flags are specified at the same time, (FILE_TXT|FILE_CSV or FILE_TXT|FILE_BIN or FILE_BIN|FILE_CSV), the flag with the highest priority will be used.

Flags that define the type of encoding also have priority. FILE_UNICODE is of a higher priority than FILE_ANSI. So if you specify combination FILE_UNICODE|FILE_ANSI, flag FILE_UNICODE will be used.

If neither FILE_UNICODE nor FILE_ANSI is indicated, FILE_UNICODE is implied. If neither FILE_CSV, nor FILE_BIN, nor FILE_TXT is specified, FILE_CSV is implied.

If a file is opened for reading as a text file (FILE_TXT or FILE_CSV), and at the file beginning a special two-byte indication 0xff,0xfe is found, the encoding flag will be FILE_UNICODE, even if FILE_ANSI is specified.

See also

[File Functions](/en/docs/files)
