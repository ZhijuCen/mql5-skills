# DatabaseColumnType

Gets a field type by index.

```
ENUM_DATABASE_FIELD_TYPE  DatabaseColumnType(
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

Return the field type from the [ENUM_DATABASE_FIELD_TYPE](/en/docs/database/databasecolumntype#enum_database_field_type) enumeration. To get the error code, use GetLastError(), the possible responses are:

- ERR_DATABASE_INVALID_HANDLE (5121) – invalid request handle;
- ERR_DATABASE_NO_MORE_DATA (5126)  –  'column' index exceeds DatabaseColumnsCount() -1.

Note

The value can be obtained only if at least one [DatabaseRead()](/en/docs/database/databaseread) call has been preliminarily made for 'request'.

ENUM_DATABASE_FIELD_TYPE

| ID | Description |
| --- | --- |
| DATABASE_FIELD_TYPE_INVALID | Error getting type, the error code can be obtained using int GetLastError() |
| DATABASE_FIELD_TYPE_INTEGER | Integer type |
| DATABASE_FIELD_TYPE_FLOAT | Real type |
| DATABASE_FIELD_TYPE_TEXT | String type |
| DATABASE_FIELD_TYPE_BLOB | Binary type |
| DATABASE_FIELD_TYPE_NULL | Special NULL type |

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseColumnsCount](/en/docs/database/databasecolumnscount), [DatabaseColumnName](/en/docs/database/databasecolumnname)
