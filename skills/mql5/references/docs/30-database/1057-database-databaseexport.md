# DatabaseExport

Exports a table or an SQL request execution result to a CSV file. The file is created in the UTF-8 encoding.

```
long  DatabaseExport(
   int           database,           // database handle received in DatabaseOpen
   const string  table_or_sql,       // a table name or an SQL request
   const string  filename,           // a name of a CSV file for data export
   uint          flags,              // combination of flags
   const string  separator           // data separator in the CSV file
   );

```

Parameters

database

[in]  Database handle received in [DatabaseOpen()](/en/docs/database/databaseopen).

table_or_sql

[in]   A name of a table or a text of an SQL request whose results are to be exported to a specified file.

filename

[in]  A file name for data export. The path is set relative to the MQL5\Files folder.

flags

[in]  Combination of flags from the [ENUM_DATABASE_EXPORT_FLAGS](/en/docs/database/databaseexport) enumeration.

separator

[in]  Data separator. If NULL is specified, the '\t' tabulation character is used as a separator.  An empty string "" is considered a valid separator but the obtained CSV file cannot be read as a table – it is considered as a set of strings.

Return Value

Return the number of exported entries or a negative value in case of an error. To get the error code, use [GetLastError()](/en/docs/check/getlasterror), the possible responses are:

- ERR_INTERNAL_ERROR (4001)                       – critical runtime error;
- ERR_INVALID_PARAMETER (4003)                  – path to the database file contains an empty string, or an incompatible combination of flags is set;
- ERR_NOT_ENOUGH_MEMORY (4004)              - insufficient memory;
- ERR_FUNCTION_NOT_ALLOWED(4014)           – specified pipe is not allowed;
- ERR_PROGRAM_STOPPED(4022)                    – operation canceled (MQL program stopped);
- ERR_WRONG_FILENAME (5002)                     - invalid file name;
- ERR_TOO_LONG_FILENAME (5003)                 - absolute path to the file exceeds the maximum length;
- ERR_CANNOT_OPEN_FILE(5004)                    – unable to open the file for writing;
- ERR_FILE_WRITEERROR(5026)                      – unable to write to the file;
- ERR_DATABASE_INTERNAL (5120)                 – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)      - invalid database handle;
- ERR_DATABASE_QUERY_PREPARE(5125)        – request generation error;
- ERR_DATABASE_QUERY_NOT_READONLY       – read-only request is allowed.

Note

If request results are exported, the SQL request should begin with "SELECT" or "select". In other words, the SQL request cannot alter the database status, otherwise DatabaseExport() fails with an error.

Database string values may contain the conversion character ('\r' or '\r\n' ), as well as the value separator character set in the separator parameter. In this case, be sure to use the DATABASE_EXPORT_QUOTED_STRINGS flag in the 'flags' parameter. If this flag is present, all displayed strings are enclosed in double quotes. If a string contains a double quote, it is replaced by two double quotes.

ENUM_DATABASE_EXPORT_FLAGS

| ID | Description |
| --- | --- |
| DATABASE_EXPORT_HEADER | Display field names in the first string |
| DATABASE_EXPORT_INDEX | Display string indices |
| DATABASE_EXPORT_NO_BOM | Do not insert BOM mark at the beginning of the file (BOM is inserted by default) |
| DATABASE_EXPORT_CRLF | Use CRLF for string break (the default is LF) |
| DATABASE_EXPORT_APPEND | Add data to the end of an existing file (by default, the file is overwritten). If the file does not exist, it will be created. |
| DATABASE_EXPORT_QUOTED_STRINGS | Display string values in double quotes. |
| DATABASE_EXPORT_COMMON_FOLDER | A CSV file is created in the common folder of all client terminals \Terminal\Common\File. |

Example:

```
input int InpRates=100;
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
 {
  MqlRates rates[];
//--- remember the start time before receiving bars
  ulong start=GetMicrosecondCount();
//--- request the last 100 bars on H1
  if(CopyRates(Symbol(), PERIOD_H1, 1, InpRates, rates)<InpRates)
   {
    Print("CopyRates() failed,, Error ", GetLastError());
    return;
   }
  else
   {
    //--- how many bars were received and how much time it took to receive them
    PrintFormat("%s: CopyRates received %d bars in %d ms ",
                _Symbol, ArraySize(rates), (GetMicrosecondCount()-start)/1000);
   }
//--- set the file name for storing the database
  string filename=_Symbol+"_"+EnumToString(PERIOD_H1)+"_"+TimeToString(TimeCurrent())+".sqlite";
  StringReplace(filename, ":", "-"); // ":" character is not allowed in file names
//--- open/create the database in the common terminal folder
  int db=DatabaseOpen(filename, DATABASE_OPEN_READWRITE|DATABASE_OPEN_CREATE|DATABASE_OPEN_COMMON);
  if(db==INVALID_HANDLE)
   {
    Print("Database: ", filename, " open failed with code ", GetLastError());
    return;
   }
  else
    Print("Database: ", filename, " opened successfully");
 
//--- check if the RATES table exists
  if(DatabaseTableExists(db, "RATES"))
   {
    //--- remove the RATES table
    if(!DatabaseExecute(db, "DROP TABLE IF EXISTS RATES"))
     {
      Print("Failed to drop the RATES table with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   }
//--- create the RATES table
  if(!DatabaseExecute(db, "CREATE TABLE RATES("
                      "SYMBOL             CHAR(10),"
                      "TIME               INT NOT NULL,"
                      "OPEN               REAL,"
                      "HIGH               REAL,"
                      "LOW                REAL,"
                      "CLOSE              REAL,"
                      "TICK_VOLUME        INT,"
                      "SPREAD             INT,"
                      "REAL_VOLUME        INT);"))
   {
    Print("DB: ", filename, " create table RATES with code ", GetLastError());
    DatabaseClose(db);
    return;
   }
//--- display the list of all fields in the RATES table
  if(DatabasePrint(db, "PRAGMA TABLE_INFO(RATES)", 0)<0)
   {
    PrintFormat("DatabasePrint(\"PRAGMA TABLE_INFO(RATES)\") failed, error code=%d at line %d", GetLastError(), __LINE__);
    DatabaseClose(db);
    return;
   }
//--- create a parametrized request to add bars to the RATES table
  string sql="INSERT INTO RATES (SYMBOL,TIME,OPEN,HIGH,LOW,CLOSE,TICK_VOLUME,SPREAD,REAL_VOLUME)"
             " VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9)"; // request parameters
  int request=DatabasePrepare(db, sql);
  if(request==INVALID_HANDLE)
   {
    PrintFormat("DatabasePrepare() failed with code=%d", GetLastError());
    Print("SQL request: ", sql);
    DatabaseClose(db);
    return;
   }
//--- set the value of the first request parameter
  DatabaseBind(request, 0, _Symbol);
//--- remember the start time before adding bars to the RATES table
  start=GetMicrosecondCount();
  DatabaseTransactionBegin(db);
  int total=ArraySize(rates);
  bool request_error=false;
  for(int i=0; i<total; i++)
   {
    //--- set the values of the remaining parameters before adding the entry
    ResetLastError();
    if(!DatabaseBind(request, 1, rates[i].time))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    //--- if the previous DatabaseBind() call was successful, set the next parameter
    if(!request_error && !DatabaseBind(request, 2, rates[i].open))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 3, rates[i].high))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 4, rates[i].low))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 5, rates[i].close))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 6, rates[i].tick_volume))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 7, rates[i].spread))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
    if(!request_error && !DatabaseBind(request, 8, rates[i].real_volume))
     {
      PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
      PrintFormat("Bar #%d line=%d", i+1, __LINE__);
      request_error=true;
      break;
     }
 
    //--- execute a request for inserting the entry and check for an error
    if(!request_error && !DatabaseRead(request) && (GetLastError()!=ERR_DATABASE_NO_MORE_DATA))
     {
      PrintFormat("DatabaseRead() failed with code=%d", GetLastError());
      DatabaseFinalize(request);
      request_error=true;
      break;
     }
    //--- reset the request before the next parameter update
    if(!request_error && !DatabaseReset(request))
     {
      PrintFormat("DatabaseReset() failed with code=%d", GetLastError());
      DatabaseFinalize(request);
      request_error=true;
      break;
     }
   } //--- done going through all the bars
 
//--- transactions status
  if(request_error)
   {
    PrintFormat("Table RATES: failed to add %d bars ", ArraySize(rates));
    DatabaseTransactionRollback(db);
    DatabaseClose(db);
    return;
   }
  else
   {
    DatabaseTransactionCommit(db);
    PrintFormat("Table RATES: added %d bars in %d ms",
                ArraySize(rates), (GetMicrosecondCount()-start)/1000);
   }
//--- save the RATES table to a CSV file
  string csv_filename=Symbol()+".csv";
  long saved=DatabaseExport(db, "SELECT * FROM RATES", csv_filename, DATABASE_EXPORT_HEADER|DATABASE_EXPORT_INDEX|DATABASE_EXPORT_COMMON_FOLDER, ";");
  if(saved>0)
    Print("Table RATES saved in ", Symbol(), ".csv");
  else
    Print("DatabaseExport() failed. Error ", GetLastError());
//--- close the database file and inform of that
  DatabaseClose(db);
  PrintFormat("Database: %s created and closed", filename);

```

See also

[DatabasePrint](/en/docs/database/databaseprint), [DatabaseImport](/en/docs/database/databaseimport)
