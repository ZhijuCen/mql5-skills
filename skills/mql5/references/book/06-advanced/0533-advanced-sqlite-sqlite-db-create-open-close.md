# Creating, opening, and closing databases

The DatabaseOpen and DatabaseClose functions enable the creation and opening of databases.

int DatabaseOpen(const string filename, uint flags)

The function opens or creates a database in a file named filename. The parameter can contain not only the name but also the path with subfolders relative to MQL5/Files (of a specific terminal instance or in a shared folder, see flags below). The extension can be omitted, which adds ".sqlite" to the default name.

If NULL or an empty string "" is specified in the filename parameter, then the database is created in a temporary file, which will be automatically deleted after the database is closed.

If the string ":memory:" is specified in the filename parameter, the database will be created in memory. Such a temporary base will be automatically deleted after closing.

The flags parameter contains a combination of flags that describe additional conditions for creating or opening a database from the ENUM_DATABASE_OPEN_FLAGS enumeration.

| Identifier | Description |
| --- | --- |
| DATABASE_OPEN_READONLY | Open for reading only |
| DATABASE_OPEN_READWRITE | Open for reading and writing |
| DATABASE_OPEN_CREATE | Create a file on disk if it doesn't exist |
| DATABASE_OPEN_MEMORY | Create an in-memory database |
| DATABASE_OPEN_COMMON | The file is located in the shared folder of all terminals |

If none of the DATABASE_OPEN_READONLY or DATABASE_OPEN_READWRITE flags are specified in the flags parameter, the DATABASE_OPEN_READWRITE flag will be used.

On success, the function returns a handle to the database, which is then used as a parameter for other functions to access it. Otherwise, INVALID_HANDLE is returned, and the error code can be found in _LastError.

void DatabaseClose(int database)

The DatabaseClose function closes the database by its handle, which was previously received from the DatabaseOpen function.

After calling DatabaseClose, all query handles that we will learn to create for an open base in the following sections are automatically removed and invalidated.

The function does not return anything. However, if an incorrect handle is passed to it, it will set _LastError to ERR_DATABASE_INVALID_HANDLE.

Let's start developing an object-oriented wrapper for databases in a file DBSQLite.mqh.

The DBSQlite class will ensure the creation, opening, and closing of databases. We will extend it later.

```
class DBSQLite
{
protected:
   const string path;
   const int handle;
   const uint flags;
   
public:
   DBSQLite(const string file, const uint opts =
      DATABASE_OPEN_CREATE | DATABASE_OPEN_READWRITE):
      path(file), flags(opts), handle(DatabaseOpen(file, opts))
   {
   }
   
   ~DBSQLite(void)
   {
      if(handle != INVALID_HANDLE)
      {
         DatabaseClose(handle);
      }
   }
   
   int getHandle() const
   {
      return handle;
   }
   
   bool isOpen() const
   {
      return handle != INVALID_HANDLE;
   }
};

```

Note that the database is automatically created or opened when the object is created, and closed when the object is destroyed.

Using this class, let's write a simple script DBinit.mq5, which will create or open the specified database.

```
input string Database = "MQL5Book/DB/Example1";
   
void OnStart()
{
   DBSQLite db(Database);                   // create or open the base in the constructor
   PRTF(db.getHandle());                    // 65537 / ok
   PRTF(FileIsExist(Database + ".sqlite")); // true / ok
} // the base is closed in the destructor

```

After the first run, with default settings, we should get a new file MQL5/Files/MQL5Book/DB/Example1.sqlite. This is confirmed in the code by checking for the existence of the file. On subsequent runs with the same name, the script simply opens the database and logs the current descriptor (an integer number).
