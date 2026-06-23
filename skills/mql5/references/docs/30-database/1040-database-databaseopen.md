# DatabaseOpen

Opens or creates a database in a specified file.

```
int  DatabaseOpen(
   string  filename,      // file name
   uint    flags          // combination of flags
   );

```

Parameters

filename

[in]  File name relative to the "MQL5\Files" folder.

flags

[in]  Combination of flags from the [ENUM_DATABASE_OPEN_FLAGS](/en/docs/database/databaseopen#enum_database_open_flags) enumeration.

Return Value

If executed successfully, the function returns the database handle, which is then used to access the database. Otherwise, it returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). To get the error code, use GetLastError(), the possible responses are:

- ERR_INTERNAL_ERROR (4001)                       – critical runtime error;
- ERR_WRONG_INTERNAL_PARAMETER (4002)  - internal error, while accessing the "MQL5\Files" folder;
- ERR_INVALID_PARAMETER (4003)                  – path to the database file contains an empty string, or an incompatible combination of flags is set;
- ERR_NOT_ENOUGH_MEMORY (4004)              - insufficient memory;
- ERR_WRONG_FILENAME (5002)                     - wrong database file name;
- ERR_TOO_LONG_FILENAME (5003)                 - absolute path to the database file exceeds the maximum length;
- ERR_DATABASE_TOO_MANY_OBJECTS (5122) - exceeded the maximum acceptable number of Database objects;
- ERR_DATABASE_CONNECT (5123)                  - database connection error;

- ERR_DATABASE_MISUSE (5621)                      - incorrect use of the SQLite library.

Note

If the filename parameter features NULL or the empty string "", a temporary file is created on the disk. It is automatically deleted after closing the database connection.

If the filename parameter features ":memory:", the database is created in the memory and is automatically deleted after the connection to it is closed.

If the flags parameter features none of the DATABASE_OPEN_READONLY or DATABASE_OPEN_READWRITE flags, the DATABASE_OPEN_READWRITE flag is used.

If the file extension is not specified, ".sqlite" is used.

ENUM_DATABASE_OPEN_FLAGS

| ID | Description |
| --- | --- |
| DATABASE_OPEN_READONLY | Read only |
| DATABASE_OPEN_READWRITE | Open for reading and writing |
| DATABASE_OPEN_CREATE | Create the file on a disk if necessary |
| DATABASE_OPEN_MEMORY | Create a database in RAM |
| DATABASE_OPEN_COMMON | The file is in the common folder of all terminals |

See also

[DatabaseClose](/en/docs/database/databaseclose)
