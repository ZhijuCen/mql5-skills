# DatabaseFinalize

Removes a request created in [DatabasePrepare(](/en/docs/database/databaseprepare)).

```
void  DatabaseFinalize(
   int  request      // request handle received in DatabasePrepare
   );

```

Parameters

request

[in]  Request handle received in DatabasePrepare().

Return Value

None.

Note

If the handle is invalid, the function sets the ERR_DATABASE_INVALID_HANDLE error. You can check the error using GetLastError().

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseExecute](/en/docs/database/databaseexecute)
