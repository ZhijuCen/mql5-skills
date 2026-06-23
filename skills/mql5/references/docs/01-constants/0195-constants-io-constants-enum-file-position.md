# Positioning Inside a File

Most of [file functions](/en/docs/files) are associated with data read/write operations. At the same time, using the [FileSeek()](/en/docs/files/fileseek) you can specify the position of a file pointer to a position inside the file, from which the next read or write operation will be performed. The ENUM_FILE_POSITION enumeration contains valid pointer positions, relative to which you can specify the shift in bytes for the next operation.

ENUM_FILE_POSITION

| Identifier | Description |
| --- | --- |
| SEEK_SET | File beginning |
| SEEK_CUR | Current position of a file pointer |
| SEEK_END | File end |

See also

[FileIsEnding](/en/docs/files/fileisending), [FileIsLineEnding](/en/docs/files/fileislineending)
