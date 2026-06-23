# DatabaseClose

Closes a database.

```
void  DatabaseClose(
   int  database      // database handle received in DatabaseOpen
   );

```

Parameters

database

[in]  Database handle received in [DatabaseOpen()](/en/docs/database/databaseopen).

Return Value

None.

Note

After calling DatabaseClose, all [handles of requests ](/en/docs/database/databaseprepare) to the database are automatically removed and become invalid.

If the handle is invalid, the function sets the ERR_DATABASE_INVALID_HANDLE error. You can check the error using GetLastError().

See also

[DatabaseOpen](/en/docs/database/databaseopen), [DatabasePrepare](/en/docs/database/databaseprepare)
