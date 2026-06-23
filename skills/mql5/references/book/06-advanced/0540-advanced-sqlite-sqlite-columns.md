# Reading fields separately: DatabaseColumn Functions

As a result of query execution by the DatabaseRead or DatabaseReadBind functions, the program gets the opportunity to scroll through the records selected according to the specified conditions. At each iteration, in the internal structures of the SQLite engine, one specific record is allocated, the fields (columns) of which are available through the group of DatabaseColumn functions.

int DatabaseColumnsCount(int request)

Based on the query descriptor, the function returns the number of fields (columns) in the query results. In case of an error, it returns -1.

You can find out the number of fields in the query created in [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare) even before calling the [DatabaseRead](/en/book/advanced/sqlite/sqlite_read) function. For other DatabaseColumn functions, you should initially call DatabaseRead (at least once).

Using the original number of a field in the query results, the program can find the field name (DatabaseColumnName), type (DatabaseColumnType), size (DatabaseColumnSize), and the value of the corresponding type (each type has its function).

bool DatabaseColumnName(int request, int column, string &name)

The function fills the string parameter passed by reference (name) with the name of the column specified by number (column) in the query results (request).

Field numbering starts from 0 and cannot exceed the value of DatabaseColumnsCount() - 1. This applies not only to this function but also to all other functions of the section.

The function returns true if successful or false in case of an error.

ENUM_DATABASE_FIELD_TYPE DatabaseColumnType(int request, int column)

The DatabaseColumnType function returns the type of the value in the specified column in the current record of the query results. The possible types are collected in the ENUM_DATABASE_FIELD_TYPE enumeration.

| Identifier | Description |
| --- | --- |
| DATABASE_FIELD_TYPE_INVALID | Error getting type, error code in  _LastError |
| DATABASE_FIELD_TYPE_INTEGER | Integer number |
| DATABASE_FIELD_TYPE_FLOAT | Real number |
| DATABASE_FIELD_TYPE_TEXT | String |
| DATABASE_FIELD_TYPE_BLOB | Binary data |
| DATABASE_FIELD_TYPE_NULL | Void (special type NULL) |

More details about SQL types and their correspondence to MQL5 types were described in the section [Structure (schema) of tables: data types and restrictions](/en/book/advanced/sqlite/sqlite_scheme_types).

int DatabaseColumnSize(int request, int column)

The function returns the size of the value in bytes for the field with the column index in the current record of results of the request query. For example, integer values can be represented by a different number of bytes (we know this from MQL5 types, in particular, short/int/long).

The next group of functions allows you to get the value of a particular type from the corresponding field of the record. To read values from the next record, you need to call DatabaseRead again.

bool DatabaseColumnText(int request, int column, string &value)

bool DatabaseColumnInteger(int request, int column, int &value)

bool DatabaseColumnLong(int request, int column, long &value)

bool DatabaseColumnDouble(int request, int column, double &value)

bool DatabaseColumnBlob(int request, int column, void &data[])

All functions return true on success and put the field value in the receiving variable value. The only special case is the function DatabaseColumnBlob, which passes an array of an arbitrary simple type or simple structures as an output variable. By specifying the uchar[] array as the most versatile option, you can read the byte representation of any value (including binary files marked with the DATABASE_FIELD_TYPE_BLOB type).

The SQLite engine does not check that for a column a function corresponding to its type is called. If the types are inadvertently or intentionally different, the system will automatically implicitly convert the field value to the type of the receiving variable.

Now, after getting familiar with the majority of Database functions, we can complete the development of a set of SQL classes in the DBSQLite.mqh file and proceed to practical examples.
