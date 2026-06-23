# Executing prepared queries: DatabaseRead/Bind

Prepared queries are executed using the DatabaseRead and DatabaseReadBind functions. The first function extracts the results from the database in such a way that later individual fields can be read from each record received in turn in response, and the second extracts each matching record in its entirety, in the form of a structure.

bool DatabaseRead(int request)

On the first call, after [Database Prepare](/en/book/advanced/sqlite/sqlite_prepare) or [DatabaseReset](/en/book/advanced/sqlite/sqlite_reset), the DatabaseRead function executes the query and sets the internal query result pointer to the first record retrieved (if the query expects records to be returned). The [DatabaseColumn](/en/book/advanced/sqlite/sqlite_columns)[ functions](/en/book/advanced/sqlite/sqlite_columns) enable the reading of the values of the record fields, i.e., the columns specified in the query.

On subsequent calls, the DatabaseRead function jumps to the next record in the query results until the end is reached.

The function returns true upon successful completion. The false value is used as an indicator of an error (for example, the database may be blocked or busy), as well as when the end of the results is normally reached, so you should analyze the code in _LastError. In particular, the value ERR_DATABASE_NO_MORE_DATA (5126) indicates that the results are finished.

Attention! If DatabaseRead is used to execute queries that don't return data, such as INSERT, UPDATE, etc., the function immediately returns false and sets the error code ERR_DATABASE_NO_MORE_DATA if the request was successful.

The usual pattern of using the function is illustrated by the following pseudo-code (DatabaseColumn functions for different types are presented in the [next section](/en/book/advanced/sqlite/sqlite_columns)).

```
int r = DatabasePrepare(db, "SELECT... WHERE...?",
   param));                            //compiling the query(optional with parameters)
while(DatabaseRead(r))                 // query execution (on the first iteration)
{                                      //    and loop through result records
   int count;
   DatabaseColumnInteger(r, 0, count); // read one field from the current record
   double number;
   DatabaseColumnDouble(r, 1, number); // read another field from the current record
   ...                                 // column types and numbers in record are determined by program
                                       // process the received values of count, number, etc.
}                                      // loop is interrupted when the end of the results is reached
DatabaseFinalize(r);

```

Note that since the query (reading conditional data) is actually executed only once (on the very first iteration), there is no need to call [DatabaseReset](/en/book/advanced/sqlite/sqlite_reset), as we did when recording changing data. However, if we want to run the query again and "walk" through the new results, calling DatabaseReset would be necessary.

bool DatabaseReadBind(int request, void &object)

The DatabaseReadBind function works in a similar way to DatabaseRead: the first call executes the SQL query and, in case of success (there is suitable data in the result), fills the object structure passed by reference with fields of the first record; subsequent calls continue moving the internal pointer through the records in the query results, filling the structure with the data of the next record.

The structure must have only numeric types and/or strings as members (arrays are not allowed), it cannot cannot inherit from or contain static members of object types.

The number of fields in the object structure should not exceed the number of columns in the query results; otherwise, we will get an error. The number of columns can be found dynamically using the [DatabaseColumnsCount](/en/book/advanced/sqlite/sqlite_columns) function, however, the caller usually needs to "know" in advance the expected data configuration according to the original request.

If the number of fields in the structure is less than the number of fields in the record, a partial read will be performed. The rest of the data can be obtained using the appropriate [DatabaseColumn ](/en/book/advanced/sqlite/sqlite_columns)[functions](/en/book/advanced/sqlite/sqlite_columns).

It is assumed that the field types of the structure match the data types in the result columns. Otherwise, an automatic implicit conversion will be performed, which can lead to unexpected consequences (for example, a string read into a numeric field will give 0).

In the simplest case, when we calculate a certain total value for the database records, for example, by calling an aggregate function like SUM(column), COUNT(column), or AVERAGE(column), the result of the query will be a single record with a single field.

```
SELECT SUM(swap) FROM trades;

```

Because reading the results is related to DatabaseColumn functions, we will defer the development of the example until the next section, where they are presented.
