# DatabaseColumnDouble

Gets the double type value from the current record.

```
bool  DatabaseColumnDouble(
   int      request,     // request handle received in DatabasePrepare
   int      column,      // field index in the request
   double&  value        // the reference to the variable for receiving the value
   );

```

Parameters

request

[in]  Request handle received in [DatabasePrepare()](/en/docs/database/databaseprepare).

column

[in]  Field index in the request. Field numbering starts from zero and cannot exceed [DatabaseColumnsCount()](/en/docs/database/databasecolumnscount) - 1.

value

[out]  Reference to the variable for writing the field value.

Return Value

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_DATABASE_INVALID_HANDLE (5121) – invalid request handle;
- ERR_DATABASE_NO_MORE_DATA (5126)  – 'column' index exceeds DatabaseColumnsCount() -1.

Note

The value can be obtained only if at least one [DatabaseRead()](/en/docs/database/databaseread) call has been preliminarily made for 'request'.

To read the value from the next record, call [DatabaseRead()](/en/docs/database/databaseread) preliminarily.

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseColumnsCount](/en/docs/database/databasecolumnscount), [DatabaseColumnType](/en/docs/database/databasecolumntype), [DatabaseColumnName](/en/docs/database/databasecolumnname)
