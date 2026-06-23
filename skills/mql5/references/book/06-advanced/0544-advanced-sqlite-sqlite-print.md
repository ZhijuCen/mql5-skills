# Printing tables and SQL queries to logs

If necessary, an MQL program can output the contents of a table or the results of an SQL query to a log using the DatabasePrint function.

long DatabasePrint(int database, const string table_or_sql, uint flags)

The database handle is passed in the first parameter, followed by the table name or query text (table_or_sql). The SQL query must start with "SELECT" or "select", i.e. it must not change the state of the database. Otherwise, the DatabasePrint function will end with an error.

The flags parameter specifies a combination of flags that determine the formatting of the output.

- DATABASE_PRINT_NO_HEADER — do not display table column names (field names)
- DATABASE_PRINT_NO_INDEX — do not display line numbers
- DATABASE_PRINT_NO_FRAME — do not display a frame that separates the header and data
- DATABASE_PRINT_STRINGS_RIGHT — align strings to the right

If flags = 0, then columns and rows are displayed, the header and data are separated by a frame, and the rows are aligned to the left.

The function returns the number of displayed records or -1 in case of an error.

We will use the function in the next section.

Unfortunately, the function does not allow an output of [prepared queries](/en/book/advanced/sqlite/sqlite_prepare) with parameters. If there are parameters, they will need to be embedded in the query text at the MQL5 level.
