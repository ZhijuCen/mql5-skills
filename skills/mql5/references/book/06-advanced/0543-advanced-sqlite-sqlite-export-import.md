# Import and export of database tables

MQL5 allows the export and import of individual database tables to/from CSV files. Export/import of the entire database, as a file with SQL commands, is not provided.

long DatabaseImport(int database, const string table, const string filename, uint flags,  

   const string separator, ulong skip_rows, const string comment_chars)

The DatabaseImport function imports data from the specified file into the table. The open database descriptor and the table name are given by the first two parameters.

If tables named table does not exist, it will be created automatically. The names and types of fields in the table will be recognized automatically based on the data contained in the file.

The imported file can be not only a ready-made CSV file but also a ZIP archive with a CSV file. The filename may contain a path. The file is searched relative to the MQL5/Files directory.

Valid flags that can be bitwise combined are described in the ENUM_DATABASE_IMPORT_FLAGS enumeration:

- DATABASE_IMPORT_HEADER — the first line contains the names of the table fields
- DATABASE_IMPORT_CRLF — for line breaks, the CRLF character sequence is used
- DATABASE_IMPORT_APPEND — add data to an existing table
- DATABASE_IMPORT_QUOTED_STRINGS — string values in double quotes
- DATABASE_IMPORT_COMMON_FOLDER — common folder of terminals

Parameter separator sets the delimiter character in the CSV file.

Parameter skip_rows skips the specified number of leading lines in the file.

Parameter comment_chars contains the characters used in the file as a comment flag. Lines starting with any of these characters will be considered comments and will not be imported.

The function returns the number of imported rows or -1 on error.

long DatabaseExport(int database, const string table_or_sql, const string filename, uint flags, const string separator)

The DatabaseExport function exports a table or the result of an SQL query to a CSV file. The database handle, as well as the table name or query text, are specified in the first two parameters.

If query results are exported, then the SQL query must begin with "SELECT" or "select". In other words, a SQL query cannot change the database state; otherwise, DatabaseExport will end with an error.

File filename name may contain a path inside the MQL5/Files directory of the current instance of the terminal or the shared folder of terminals, depending on the flags.

The flags parameter allows you to specify a combination of flags that controls the format and location of the file.

- DATABASE_EXPORT_HEADER — output a string with field names
- DATABASE_EXPORT_INDEX — display line numbers
- DATABASE_EXPORT_NO_BOM — do not insert a label [BOM](/en/book/common/files/files_txt_codepage) at the beginning of the file (BOM is inserted by default)
- DATABASE_EXPORT_CRLF — use CRLF to break a line (LF by default)
- DATABASE_EXPORT_APPEND — append data to the end of an existing file (by default, the file is overwritten), if the file does not exist, it will be created
- DATABASE_EXPORT_QUOTED_STRINGS — output string values in double quotes
- DATABASE_EXPORT_COMMON_FOLDER — CSV file will be created in the common folder of all terminals MetaQuotes/Terminal/Common/File

Parameter separator specifies the column separator character. If it is NULL, then the tab character '\t' will be used as a separator. The empty string "" is considered a valid delimiter, but the resulting CSV file cannot be read as a table and it will be a set of rows.

Text fields in the database can contain newlines ('\r' or '\r\n' ) as well as the delimiter character specified in the separator parameter. In this case, it is necessary to use the DATABASE_EXPORT_QUOTED_STRINGS flag in the flags parameter. If this flag is present, all output strings will be enclosed in double quotes, and if the string contains a double quote, it will be replaced by two double quotes.

The function returns the number of exported records or a negative value in case of an error.
