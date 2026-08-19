# DatabaseTransactionRollback

Rolls back transactions.

```
bool  DatabaseTransactionRollback(
   int  database      // database handle received in DatabaseOpen
   );

```

Parameters

database

[in]  Database handle received in [DatabaseOpen()](/en/docs/database/databaseopen).

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_INTERNAL_ERROR (4001)                    –  critical runtime error;
- ERR_INVALID_PARAMETER (4003)               –  sql parameter contains an empty string;
- ERR_NOT_ENOUGH_MEMORY (4004)           –  insufficient memory;
- ERR_WRONG_STRING_PARAMETER (5040)  – error converting a request into a UTF-8 string;
- ERR_DATABASE_INTERNAL (5120)              – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)    – invalid database handle;
- ERR_DATABASE_EXECUTE (5124)                –  request execution error.

Note

DatabaseTransactionRollback() call cancels all transactions executed after calling the DatabaseTransactionBegin() function. The DatabaseTransactionRollback() function is necessary for rolling back changes in a database in case errors occur when executing a transaction.

See also

[DatabaseExecute](/en/docs/database/databaseexecute),[ DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseTransactionBegin](/en/docs/database/databasetransactionbegin), [DatabaseTransactionCommit](/en/docs/database/databasetransactioncommit)
