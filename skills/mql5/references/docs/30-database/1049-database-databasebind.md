# DatabaseBind

Sets a parameter value in a request.

```
bool  DatabaseBind(
   int  request,      // the handle of a request created in DatabasePrepare
   int  index,        // the parameter index in the request
   T    value         // the value of a simple type parameter
   );

```

Parameters

request

[in]  The handle of a request created in [DatabasePrepare()](/en/docs/database/databaseprepare).

index

[in]  The parameter index in the request a value should be set for. The numbering starts with zero.

value

[in]  The value to be set. Extended types: bool, char, uchar, short, ushart, int, uint, color, datetime, long, ulong, float, double, string.

Return Value

Returns true if successful, otherwise - false. To get the error code, use GetLastError(), the possible responses are:

- ERR_INVALID_PARAMETER (4003)             – unsupported type;
- ERR_DATABASE_INVALID_HANDLE (5121)  - invalid database handle;
- ERR_DATABASE_NOT_READY (5128)         - cannot use the function to make a request at the moment. The request is being executed or already complete. [DatabaseReset()](/en/docs/database/databasereset) should be called.

Note

The function is used in case an SQL request contains "?" or "?N" parameterizable values where N means the parameter index (starting from one). At the same time, parameters indexing in DatabaseBind() starts from zero.

For example:

```
     INSERT INTO table VALUES (?,?,?)
     SELECT * FROM table WHERE id=?

```

The function may be called immediately after a parametrized request is created in [DatabasePrepare()](/en/docs/database/databaseprepare) or after the request is reset using [DatabaseReset()](/en/docs/database/databasereset).

Use this function together with [DatabaseReset()](/en/docs/database/databasereset) to execute the request as many times as needed with different parameter values.

The function is designed to work with simple type parameters. If a parameter should be checked against an array, use the [DatabaseBindArray()](/en/docs/database/databasebindarray) function.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   MqlTick ticks[];
//--- remember the start time before receiving the ticks
   uint start=GetTickCount();
//--- request the tick history per day
   ulong to=TimeCurrent()*1000;
   ulong from=to-PeriodSeconds(PERIOD_D1)*1000;
   if(CopyTicksRange(_Symbol, ticks, COPY_TICKS_ALL, from, to)==-1)
     {
      PrintFormat("%s: CopyTicksRange(%s - %s) failed, error=%d",
                  _Symbol, TimeToString(datetime(from/1000)), TimeToString(datetime(to/1000)), _LastError);
      return;
     }
   else
     {
      //--- how many ticks were received and how much time it took to receive them
      PrintFormat("%s: CopyTicksRange received %d ticks in %d ms (from %s to %s)",
                  _Symbol, ArraySize(ticks), GetTickCount()-start,
                  TimeToString(datetime(from/1000)), TimeToString(datetime(to/1000)));
     }
 
//--- set the file name for storing the database
   string filename=_Symbol+" "+TimeToString(datetime(from/1000))+" - "+TimeToString(datetime(to/1000))+".sqlite";
   StringReplace(filename, ":", "."); // ":" character is not allowed in file names
//--- open/create the database in the common terminal folder
   int db=DatabaseOpen(filename, DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE | DATABASE_OPEN_COMMON);
   if(db==INVALID_HANDLE)
     {
      Print("Database: ", filename, " open failed with code ", GetLastError());
      return;
     }
   else
      Print("Database: ", filename, " opened successfully");
 
//--- create the TICKS table
   if(!DatabaseExecute(db, "CREATE TABLE TICKS("
                       "SYMBOL             CHAR(10),"
                       "TIME               INT NOT NULL,"
                       "BID                REAL,"
                       "ASK                REAL,"
                       "LAST               REAL,"
                       "VOLUME             INT,"
                       "TIME_MSC           INT,"
                       "VOLUME_REAL        REAL);"))
     {
      Print("DB: ", filename, " create table TICKS failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
//--- display the list of all fields in the TICKS table
   if(DatabasePrint(db, "PRAGMA TABLE_INFO(TICKS)", 0)<0)
     {
      PrintFormat("DatabasePrint(\"PRAGMA TABLE_INFO(TICKS)\") failed, error code=%d at line %d", GetLastError(), __LINE__);
      DatabaseClose(db);
      return;
     }
//--- create a parametrized request to add ticks to the TICKS table
   string sql="INSERT INTO TICKS (SYMBOL,TIME,BID,ASK,LAST,VOLUME,TIME_MSC,VOLUME_REAL)"
              " VALUES (?1,?2,?3,?4,?5,?6,?7,?8)"; // request parameters
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
//--- remember the start time before adding ticks to the TICKS table
   start=GetTickCount();
   DatabaseTransactionBegin(db);
   int total=ArraySize(ticks);
   bool request_error=false;
   for(int i=0; i<total; i++)
     {
      //--- set the values of the remaining parameters before adding the entry
      ResetLastError();
      if(!DatabaseBind(request, 1, ticks[i].time))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      //--- if the previous DatabaseBind() call was successful, set the next parameter       
      if(!request_error && !DatabaseBind(request, 2, ticks[i].bid))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      if(!request_error && !DatabaseBind(request, 3, ticks[i].ask))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      if(!request_error && !DatabaseBind(request, 4, ticks[i].last))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      if(!request_error && !DatabaseBind(request, 5, ticks[i].volume))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      if(!request_error && !DatabaseBind(request, 6, ticks[i].time_msc))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
         request_error=true;
         break;
        }
      if(!request_error && !DatabaseBind(request, 7, ticks[i].volume_real))
        {
         PrintFormat("DatabaseBind() failed with code=%d", GetLastError());
         PrintFormat("Tick #%d line=%d", i+1, __LINE__);
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
     } //--- done going through all the ticks
 
//--- transactions status
   if(request_error)
     {
      PrintFormat("Table TICKS: failed to add %d ticks ", ArraySize(ticks));
      DatabaseTransactionRollback(db);
      DatabaseClose(db);
      return;
     }
   else
     {
      DatabaseTransactionCommit(db);
      PrintFormat("Table TICKS: added %d ticks in %d ms",
                  ArraySize(ticks), GetTickCount()-start);
     }
 
//--- close the database file and inform of that
   DatabaseClose(db);
   PrintFormat("Database: %s created and closed", filename);
  }
/*
 Result:
  EURUSD: CopyTicksRange received 268061 ticks in 47 ms (from 2020.03.18 12:40 to 2020.03.19 12:40)
  Database: EURUSD 2020.03.18 12.40 - 2020.03.19 12.40.sqlite opened successfully
  #| cid name        type     notnull dflt_value pk
  -+-----------------------------------------------
  1|   0 SYMBOL      CHAR(10)       0             0 
  2|   1 TIME        INT            1             0 
  3|   2 BID         REAL           0             0 
  4|   3 ASK         REAL           0             0 
  5|   4 LAST        REAL           0             0 
  6|   5 VOLUME      INT            0             0 
  7|   6 TIME_MSC    INT            0             0 
  8|   7 VOLUME_REAL REAL           0             0 
  Table TICKS: added 268061 ticks in 797 ms
  Database: EURUSD 2020.03.18 12.40 - 2020.03.19 12.40.sqlite created and closed
  OnCalculateCorrelation=0.87 2020.03.19 13:00:  EURUSD vs GBPUSD  PERIOD_M30 
*/

```

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseReset](/en/docs/database/databasereset), [DatabaseRead](/en/docs/database/databaseread), [DatabaseBindArray](/en/docs/database/databasebindarray)
