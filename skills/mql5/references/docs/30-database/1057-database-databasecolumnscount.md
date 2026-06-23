# DatabaseColumnsCount

Gets the number of fields in a request.

```
int  DatabaseColumnsCount(
   int  request      // request handle received in DatabasePrepare
   );

```

Parameters

request

[in]  Request handle received in [DatabasePrepare()](/en/docs/database/databaseprepare).

Return Value

Number of fields or -1 in case of an error. To get the error code, use GetLastError(), the possible responses are:

- ERR_DATABASE_INVALID_HANDLE (5121) - invalid request handle.

Note

There is no need to call the [DatabaseRead()](/en/docs/database/databaseread) function to get the number of fields of a request created in DatabasePrepare(). For the remaining DatabaseColumnXXX() functions, DatabaseRead() should be preliminarily called.

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseFinalize](/en/docs/database/databasefinalize), [DatabaseClose](/en/docs/database/databaseclose)
