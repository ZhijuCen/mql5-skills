# Binding data to query parameters: DatabaseBind/Array

After the SQL query has been compiled by the [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare) function, you can use the received query handle to bind data to the query parameters, which is what the DatabaseBind and DatabaseBindArray functions are for. Both functions can be called not only immediately after creating a query in DatabasePrepare but also after resetting the request to its initial state with [DatabaseReset](/en/book/advanced/sqlite/sqlite_reset) (if the request is executed many times in a loop).

The data binding step is not always required because prepared queries may not have parameters. As a rule, this situation occurs when a query returns data from SQL to MQL5, and therefore a query descriptor is required: how to read query results by their handles is described in the sections on [DatabaseRead/DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read) and [DatabaseColumn](/en/book/advanced/sqlite/sqlite_columns)[-functions](/en/book/advanced/sqlite/sqlite_columns).

bool DatabaseBind(int request, int index, T value)

The DatabaseBind function sets the value of the index parameter for the query with the request handle. By default, numbering starts from 0 if the parameters in the query are marked with substituted symbols '?' (without a number). However, parameters can be specified in the query string and with a number (?1, '?5', ?21): in this case, the actual indexes to be passed to the function must be 1 less than the corresponding number in the string. This is because the numbering in the query string starts from 1.

For example, the following query requires one parameter (index 0):

```
int r = DatabasePrepare(db, "SELECT * FROM table WHERE id=?");
DatabaseBind(r, 0, 1234);

```

If the "... id=?10" substitution were used in the query string, it would be necessary to call DatabaseBind with index 9.

The value in the DatabaseBind prototype can be of any [simple type](/en/book/common/conversions/conversions_structs) or string. If a parameter needs to map composite type data (structures) or arbitrary binary data that can be represented as an array of bytes, use the DatabaseBindArray function.

The function returns true if successful. Otherwise, it returns false.

bool DatabaseBindArray(int request, int index, T &array[])

The DatabaseBindArray function sets the value of the index parameter as an array of a simple type or of simple structures (including strings) for the query with the request handle. This function allows you to write [BLOB](/en/book/advanced/sqlite/sqlite_scheme_types) and NULL (the absence of a value that is considered a separate type in SQL and is not equal to 0) to the database.

Now let's go back to the DBQuery class in the DBSQLite.mqh file and add data binding support.

```
class DBQuery
{
   ...
public:
   template<typename T>
   bool bind(const int index, const T value)
   {
      return PRTF(DatabaseBind(handle, index, value));
   }
   template<typename T>
   bool bindBlob(const int index, const T &value[])
   {
      return PRTF(DatabaseBindArray(handle, index, value));
   }
   
   bool bindNull(const int index)
   {
      static const uchar null[] = {};
      return bindBlob(index, null);
   }
   ...
};

```

BLOB is suitable for transferring any file to the database unchanged, for example, if you first read it into a byte array using the [FileLoad](/en/book/common/files/files_save_load) function.

The need to explicitly bind a null value is not so obvious. When inserting new records into the database, the calling program usually passes only the fields known to it, and all the missing ones (if they are not marked with the NOT NULL constraint or do not have a different DEFAULT value in the table description) will be automatically left equal to NULL by the engine. However, when using the ORM approach, it is convenient to write the entire object to the database, including the field with a unique primary key (PRIMARY KEY). The new object does not yet have this identifier, since the database itself adds it when the object is first written, so it is important to bind this field in the new object to the NULL value.
