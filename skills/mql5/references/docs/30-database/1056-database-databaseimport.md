# DatabaseImport

Imports data from a file into a table.

```
long  DatabaseImport(
   int           database,          // database handle received in DatabaseOpen
   const string  table,             // name of a table to insert data
   const string  filename,          // name of a file to import data
   uint          flags,             // combination of flags
   const string  separator,         // data separator 
   ulong         skip_rows,         // how many initial strings to skip 
   const string  skip_comments      // string of characters defining comments
   );

```

Parameters

database

[in]  Database handle received in [DatabaseOpen()](/en/docs/database/databaseopen).

table

[in]  Name of a table the data from a file is to be added to.

filename

[in]  CSV file or ZIP archive for reading data. The name may contain subdirectories and is set relative to the MQL5\Files folder.

flags

[in]  Combination of flags from the [ENUM_DATABASE_IMPORT_FLAGS](/en/docs/database/databaseimport#enum_database_import_flags) enumeration.

separator

[in]  Data separator in CSV file.

skip_rows

[in]  Number of initial strings to be skipped when reading data from the file.

skip_comments

[in]  String of characters for designating strings as comments. If any character from skip_comments is detected at the beginning of a string, such a string is considered a comment and is not imported.

Return Value

Return the number of imported strings or -1 in case of an error. To get the error code, use [GetLastError()](/en/docs/check/getlasterror), the possible responses are:

- ERR_INVALID_PARAMETER (4003)              –  no table name specified (empty string or NULL);
- ERR_DATABASE_INTERNAL (5120)              – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)   - invalid database handle.

Note

If there is no table named table, it is generated automatically. Names and field types in the created table are defined automatically based on the file data.

If there is no table named table, it is generated automatically. Names and field types in the created table are defined automatically based on the file data.

ENUM_DATABASE_IMPORT_FLAGS

| ID | Description |
| --- | --- |
| DATABASE_IMPORT_HEADER | The first line contains the names of the table fields |
| DATABASE_IMPORT_CRLF | CRLF (the default is LF) is considered a string break |
| DATABASE_IMPORT_APPEND | Add data to the end of an existing table |
| DATABASE_IMPORT_QUOTED_STRINGS | String values enclosed in double quotes |
| DATABASE_IMPORT_COMMON_FOLDER | The file is stored in the common folder of all client terminals \Terminal\Common\File. |

Example of reading the table from the file created by the code from the [DatabaseExport](/en/docs/database/databaseexport) example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
  string csv_filename;
//--- get the names of text files for downloading from the common folder of the client terminals
  string filenames[];
  if(FileSelectDialog("Select a CSV file to download a table", NULL,
                      "Text files (*.csv)|*.csv",
                      FSD_WRITE_FILE|FSD_COMMON_FOLDER, filenames, "data.csv")>0)
   {
    //--- display the name of each selected file
    if(ArraySize(filenames)==1)
      csv_filename=filenames[0];
    else
     {
      Print("Unknown error while selecting file. Error code ", GetLastError());
      return;
     }
   }
  else
   {
    Print("CSV file not selected");
    return;
   }
//--- create or open a database
  string db_filename="test.sqlite";
  int db=DatabaseOpen(db_filename, DATABASE_OPEN_READWRITE|DATABASE_OPEN_CREATE);
//--- check if the TEST table exists
  if(DatabaseTableExists(db, "TEST"))
   {
    //--- remove the TEST table
    if(!DatabaseExecute(db, "DROP TABLE IF EXISTS TEST"))
     {
      Print("Failed to drop the TEST table with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   }
  //--- import entries from the file to the TEST table
  long imported=DatabaseImport(db, "TEST", csv_filename, DATABASE_IMPORT_HEADER|DATABASE_IMPORT_COMMON_FOLDER|DATABASE_IMPORT_APPEND, ";", 0, NULL);
  if(imported>0)
   {
    Print(imported," lines imported in table TEST");
    DatabasePrint(db,"SELECT * FROM TEST",DATABASE_PRINT_NO_INDEX);
   }
  else
    {
     Print("DatabaseImport() failed. Error ",GetLastError());
    }
//--- close the database file and inform of that
  DatabaseClose(db);
  PrintFormat("Database: %s closed", db_filename);
 }

```

See also

[DatabaseOpen](/en/docs/database/databaseopen), [DatabasePrint](/en/docs/database/databaseprint)
