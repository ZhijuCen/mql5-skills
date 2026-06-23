# Deleting and resetting prepared queries

Since prepared queries can be executed multiple times, in a loop for different parameter values, it is required to reset the query to the initial state at each iteration. This is done by the DatabaseReset function. But it does not make sense to call it if the prepared query is executed once.

bool DatabaseReset(int request)

The function resets the internal compiled query structures to the initial state, similarly to calling [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare). However, DatabaseReset does not recompile the query and is therefore very fast.

It is also important that the function does not reset already established data bindings in the query if any have been made. Thus, if necessary, you can change the value of only one or a small number of parameters. Then, after calling DatabaseReset, you can simply call DatabaseBind functions only for changed parameters.

At the time of writing the book, the MQL5 API did not provide a function to reset the data binding, an analog of the sqlite_clear_bindings function in the standard SQLite distribution.

In the request parameter, specify the valid handle of the query obtained earlier from DatabasePrepare. If you pass a handle of the query that was previously removed with DatabaseFinalize (see below), an error will be returned.

The function returns an indicator of success (true) or error (false).

The general principle of working with recurring queries is shown in the following pseudo-code. The DatabaseBind and DatabaseRead functions will be described in the following sections and will be "packed" into ORM classes.

```
struct Data                                       // structure example
{
   long count;
   double value;
   string comment;
};
Data data[];
...                                               // getting data array
int r =
     DatabasePrepare(db, "INSERT... (?, ?, ?)")); // compile query with parameters
for(int i = 0; i < ArraySize(data); ++i)          // data loop
{
   DatabaseBind(r, 0, data[i].count);             // make data binding to parameters
   DatabaseBind(r, 1, data[i].value);
   DatabaseBind(r, 2, data[i].comment);
   DatabaseRead(r);                               // execute request
   ...                                            // analyze or save results
   DatabaseReset(r);                              // initial state at each iteration
}
DatabaseFinalize(r);

```

After the prepared query is no longer needed, you should release the computer resources it occupies using DatabaseFinalize.

void DatabaseFinalize(int request)

The function deletes the query with the specified handle, created in [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare).

If an incorrect descriptor is passed, the function will record ERR_DATABASE_INVALID_HANDLE to _LastError.

When closing the database with [DatabaseClose](/en/book/advanced/sqlite/sqlite_db_create_open_close), all query handles created for it are automatically removed and invalidated.

Let's complement our ORM layer (DBSQLite.mqh) with a new class DBQuery to work with prepared queries. For now, it will only contain the initialization and deinitialization functionality inherent in the RAII concept, but we will expand it soon.

```
class DBQuery
{
protected:
   const string sql;  // query
   const int db;      // database handle (constructor argument)
   const int handle;  // prepared request handle
   
public:
   DBQuery(const int owner, const string s): db(owner), sql(s),
      handle(PRTF(DatabasePrepare(db, sql)))
   {
   }
   
   ~DBQuery()
   {
      DatabaseFinalize(handle);
   }
   
   bool isValid() const
   {
      return handle != INVALID_HANDLE;
   }
   
   virtual bool reset()
   {
      return DatabaseReset(handle);
   }
   ...
};

```

In the DBSQLite class, we initiate the preparation of the request in the prepare method by creating an instance of DBQuery. All query objects will be stored in the internal array queries in the form of autopointers, which allows the calling code not to follow their explicit deletion.

```
class DBSQLite
{
   ...
protected:
   AutoPtr<DBQuery> queries[];
public:
   DBQuery *prepare(const string sql)
   {
      return PUSH(queries, new DBQuery(handle, sql));
   }
   ...
};

```
