# File Properties

The [FileGetInteger()](/en/docs/files/filegetinteger) function is used for obtaining file properties. The identifier of the required property from the ENUM_FILE_PROPERTY_INTEGER enumeration is passed to it during call.

ENUM_FILE_PROPERTY_INTEGER

| ID | ID description |
| --- | --- |
| FILE_EXISTS | Check the existence |
| FILE_CREATE_DATE | Date of creation |
| FILE_MODIFY_DATE | Date of the last modification |
| FILE_ACCESS_DATE | Date of the last access to the file |
| FILE_SIZE | File size in bytes |
| FILE_POSITION | Position of a pointer in the file |
| FILE_END | Get the end of file sign |
| FILE_LINE_END | Get the end of line sign |
| FILE_IS_COMMON | The file is opened in a shared folder of all terminals (see  FILE_COMMON ) |
| FILE_IS_TEXT | The file is opened as a text file (see  FILE_TXT ) |
| FILE_IS_BINARY | The file is opened as a binary file (see  FILE_BIN ) |
| FILE_IS_CSV | The file is opened as CSV (see  FILE_CSV ) |
| FILE_IS_ANSI | The file is opened as ANSI (see  FILE_ANSI ) |
| FILE_IS_READABLE | The opened file is readable (see  FILE_READ ) |
| FILE_IS_WRITABLE | The opened file is writable (see  FILE_WRITE ) |

The [FileGetInteger()](/en/docs/files/filegetinteger) function has two different options of call. In the first option, for getting properties of a file, its handle is specified, which is obtained while opening the file using the [FileOpen()](/en/docs/files/fileopen) function. This option allows getting all properties of a file.

The second option of the [FileGetInteger()](/en/docs/files/filegetinteger) function returns values of file properties by the file name. Using this option, only the following general properties can be obtained:

- FILE_EXISTS – existence of a file with a specified name
- FILE_CREATE_DATE – date of creation of the file with the specified name
- FILE_MODIFY_DATE – date of modification of the file with the specified name

- FILE_ACCESS_DATE – date of the last access to the file with the specified name

- FILE_SIZE – size of the file with the specified name

When trying to get properties other than specified above, the second option of FileGetInteger() call will return an error.
