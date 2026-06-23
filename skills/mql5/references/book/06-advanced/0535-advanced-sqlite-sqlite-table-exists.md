# Checking if a table exists in the database

The built-in DatabaseTableExists function allows you to check the existence of a table by its name.

bool DatabaseTableExists(int database, const string table)

The database descriptor and the table name are specified in the parameters. The result of the function call is true if the table exists.

Let's extend the DBSQLite class by adding the hasTable method.

```
class DBSQLite
{
   ...
   bool hasTable(const string table) const
   {
      return DatabaseTableExists(handle, table);
   }

```

The script DBcreateTable.mq5 will check if the table has appeared.

```
void OnStart()
{
   DBSQLite db(Database);
   if(db.isOpen())
   {
      PRTF(db.execute(StringFormat("CREATE TABLE %s (msg text)", Table)));
      PRTF(db.hasTable(Table));
   }
}

```

Again, don't worry about potentially getting an error when trying to recreate. This does not affect the existence of the table in any way.

```
database error, table table1 already exists
db.execute(StringFormat(CREATE TABLE %s (msg text),Table))=false / DATABASE_ERROR(5601)
db.hasTable(Table)=true / ok

```

Since we are writing a generic helper class DBSQLite, we will provide a mechanism for deleting tables in it. SQL has the DROP command for this purpose.

```
class DBSQLite
{
   ...
   bool deleteTable(const string name) const
   {
      const static string query = "DROP TABLE '%s';";
      if(!DatabaseTableExists(handle, name)) return true;
      if(!DatabaseExecute(handle, StringFormat(query, name))) return false;
      return !DatabaseTableExists(handle, name)
         && ResetLastErrorOnCondition(_LastError == DATABASE_NO_MORE_DATA);
   }
   
   static bool ResetLastErrorOnCondition(const bool cond)
   {
      if(cond)
      {
         ResetLastError();
         return true;
      }
      return false;
   }

```

Before executing the query, we check for the existence of the table and immediately exit if it does not exist.

After executing the query, we additionally check whether the table has been deleted by calling DatabaseTableExists again. Since the absence of a table will be flagged with the DATABASE_NO_MORE_DATA error code, which is the expected result for this method, we clear the error code with ResetLastErrorOnCondition.

It can be more efficient to use the capabilities of SQL to exclude an attempt to delete a non-existent table: just add the phrase "IF EXISTS" to the query. Therefore, the final version of the method deleteTable is simplified:

```
   bool deleteTable(const string name) const
   {
      const static string query = "DROP TABLE IF EXISTS '%s';";
      return DatabaseExecute(handle, StringFormat(query, name));
   }

```

You can try to write a test script for deleting the table, but be careful not to delete a working table by mistake. Tables are deleted immediately with all data, without confirmation and without the possibility of recovery. For important projects, keep database backups.
