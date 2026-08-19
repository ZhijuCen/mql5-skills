# DatabaseRead

Moves to the next entry as a result of a request.

```
bool  DatabaseRead(
   int  request      // request handle received in DatabasePrepare
   );

```

Parameters

request

[in]  Request handle received in [DatabasePrepare()](/en/docs/database/databaseprepare).

Return Value

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_INVALID_PARAMETER (4003)               –  no table name specified (empty string or NULL);
- ERR_WRONG_STRING_PARAMETER (5040)  – error converting a request into a UTF-8 string;
- ERR_DATABASE_INTERNAL (5120)              – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)    – invalid database handle;
- ERR_DATABASE_EXECUTE (5124)                –  request execution error;
- ERR_DATABASE_NO_MORE_DATA (5126)    – no table exists (not an error, normal completion).

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseReadBind](/en/docs/database/databasereadbind)
