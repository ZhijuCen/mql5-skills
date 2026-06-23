# DatabaseColumnSize

Gets a field size in bytes.

```
int  DatabaseColumnSize(
   int  request,     // request handle received in DatabasePrepare
   int  column       // field index in the request
   );

```

Parameters

request

[in]  Request handle received in [DatabasePrepare()](/en/docs/database/databaseprepare).

column

[in]  Field index in the request. Field numbering starts from zero and cannot exceed [DatabaseColumnsCount()](/en/docs/database/databasecolumnscount) - 1.

Return Value

If successful, the field size in bytes is returned, otherwise -1. To get the error code, use GetLastError(), the possible responses are:

- ERR_DATABASE_INVALID_HANDLE (5121) – invalid request handle;
- ERR_DATABASE_NO_MORE_DATA (5126)  – 'column' index exceeds DatabaseColumnsCount() -1.

Note

The value can be obtained only if at least one [DatabaseRead()](/en/docs/database/databaseread) call has been preliminarily made for 'request'.

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseColumnBlob](/en/docs/database/databasecolumnblob), [DatabaseColumnsCount](/en/docs/database/databasecolumnscount), [DatabaseColumnName](/en/docs/database/databasecolumnname), [DatabaseColumnType](/en/docs/database/databasecolumntype)
