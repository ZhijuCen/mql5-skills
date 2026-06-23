# DatabaseReset

Resets a request, like after calling [DatabasePrepare()](/en/docs/database/databaseprepare).

```
int  DatabaseReset(
   int  request      // request handle received in DatabasePrepare
   );

```

Parameters

request

[in]  The handle of the request obtained in [DatabasePrepare()](/en/docs/database/databaseprepare).

Return Value

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_DATABASE_INVALID_HANDLE (5121) - invalid database handle;
- SQLite error codes starting with ERR_DATABASE_ERROR(5601).

Note

The DatabaseReset() function is intended for multiple execution of a request with different parameter values. For example, when adding data to the table in bulk using the INSERT command, a custom set of field values should be formed for each entry.

Unlike [DatabasePrepare()](/en/docs/database/databaseprepare), the DatabaseReset() call does not compile the string with SQL commands into a new request, therefore DatabaseReset() is executed much faster than DatabasePrepare().

DatabaseReset() is used together with the [DatabaseBind()](/en/docs/database/databasebind) functions and/or [DatabaseBindArray()](/en/docs/database/databasebindarray) if the request parameter values should be changed after executing [DatabaseRead()](/en/docs/database/databaseread). This means that before setting new values of the request parameters (before the block of DatabaseBind/DatabaseBindArray calls), DatabaseReset() should be called to reset it. The parametrized request itself should be created using [DatabasePrepare()](/en/docs/database/databaseprepare).

Just like DatabasePrepare(), DatabaseReset() does not make a database request. A direct request execution is performed when calling [DatabaseRead()](/en/docs/database/databaseread) or [DatabaseReadBind()](/en/docs/database/databasereadbind).

DatabaseReset() call does not lead to resetting parameter values in the request if they were set by calling DatabaseBind()/DatabaseBindArray(), i.e. the parameters retain their values. Thus, the value of only a single parameter can be changed. There is no need to set all request parameters anew after calling DatabaseReset().

A handle of a request removed using [DatabaseFinalize()](/en/docs/database/databasefinalize) cannot be passed to DatabaseReset(). This will result in an error.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- create or open a database
   string filename="symbols.sqlite";
   int db=DatabaseOpen(filename, DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE);
   if(db==INVALID_HANDLE)
     {
      Print("DB: ", filename, " open failed with code ", GetLastError());
      return;
     }
   else
      Print("Database: ", filename, " opened successfully");
//--- if the SYMBOLS table exists, delete it
   if(DatabaseTableExists(db, "SYMBOLS"))
     {
      //--- delete the table
      if(!DatabaseExecute(db, "DROP TABLE SYMBOLS"))
        {
         Print("Failed to drop table SYMBOLS with code ", GetLastError());
         DatabaseClose(db);
         return;
        }
     }
//--- create the SYMBOLS table
   if(!DatabaseExecute(db, "CREATE TABLE SYMBOLS("
                       "NAME           TEXT    NOT NULL,"
                       "DESCRIPTION    TEXT            ,"
                       "PATH           TEXT            ,"
                       "SPREAD         INT             ,"
                       "POINT          REAL    NOT NULL,"
                       "DIGITS         INT     NOT NULL,"
                       "JSON           BLOB );"))
     {
      Print("DB: ", filename, " create table failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
//--- display the list of all fields in the SYMBOLS table
   if(DatabasePrint(db, "PRAGMA TABLE_INFO(SYMBOLS)", 0)<0)
     {
      PrintFormat("DatabasePrint(\"PRAGMA TABLE_INFO(SYMBOLS)\") failed, error code=%d at line %d", GetLastError(), __LINE__);
      DatabaseClose(db);
      return;
     }
 
//--- create a parametrized request to add symbols to the SYMBOLS table
   string sql="INSERT INTO SYMBOLS (NAME,DESCRIPTION,PATH,SPREAD,POINT,DIGITS,JSON)"
              " VALUES (?1,?2,?3,?4,?5,?6,?7);"; // request parameters
   int request=DatabasePrepare(db, sql);
   if(request==INVALID_HANDLE)
     {
      PrintFormat("DatabasePrepare() failed with code=%d", GetLastError());
      Print("SQL request: ", sql);
      DatabaseClose(db);
      return;
     }
 
//--- go through all the symbols and add them to the SYMBOLS table
   int symbols=SymbolsTotal(false);
   bool request_error=false;
   DatabaseTransactionBegin(db);   
   for(int i=0; i<symbols; i++)
     {
      //--- set the values of the parameters before adding a symbol
      ResetLastError();
      string symbol=SymbolName(i, false);
      if(!DatabaseBind(request, 0, symbol))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      //--- if the previous DatabaseBind() call was successful, set the next parameter
      if(!DatabaseBind(request, 1, SymbolInfoString(symbol, SYMBOL_DESCRIPTION)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      if(!DatabaseBind(request, 2, SymbolInfoString(symbol, SYMBOL_PATH)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      if(!DatabaseBind(request, 3, SymbolInfoInteger(symbol, SYMBOL_SPREAD)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      if(!DatabaseBind(request, 4, SymbolInfoDouble(symbol, SYMBOL_POINT)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      if(!DatabaseBind(request, 5, SymbolInfoInteger(symbol, SYMBOL_DIGITS)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
      if(!DatabaseBind(request, 6, GetSymBolAsJson(symbol)))
        {
         PrintFormat("DatabaseBind() failed at line %d with code=%d", __LINE__, GetLastError());
         request_error=true;
         break;
        }
 
      //--- execute a request for inserting the entry and check for an error
      if(!DatabaseRead(request)&&(GetLastError()!=ERR_DATABASE_NO_MORE_DATA))
        {
         PrintFormat("DatabaseRead() failed with code=%d", GetLastError());
         DatabaseFinalize(request);
         request_error=true;
         break;
        }
      else
         PrintFormat("%d: added %s", i+1, symbol);
      //--- reset the request before the next parameter update
      if(!DatabaseReset(request))
        {
         PrintFormat("DatabaseReset() failed with code=%d", GetLastError());
         DatabaseFinalize(request);
         request_error=true;
         break;
        }
     } //--- done going through all the symbols
 
//--- transactions status
   if(request_error)
     {
      PrintFormat("Table SYMBOLS: failed to add %d symbols", symbols);
      DatabaseTransactionRollback(db);
      DatabaseClose(db);
      return;
     }
   else
     {
      DatabaseTransactionCommit(db);
      PrintFormat("Table SYMBOLS: added %d symbols",symbols);
     }
 
//--- save the SYMBOLS table to a CSV file
   string csv_filename="symbols.csv";
   if(DatabaseExport(db, "SELECT * FROM SYMBOLS", csv_filename,
                     DATABASE_EXPORT_HEADER|DATABASE_EXPORT_INDEX|DATABASE_EXPORT_QUOTED_STRINGS, ";"))
      Print("Database: table SYMBOLS saved in ", csv_filename);
   else
      Print("Database: DatabaseExport(\"SELECT * FROM SYMBOLS\") failed with code", GetLastError());
 
//--- close the database file and inform of that
   DatabaseClose(db);
   PrintFormat("Database: %s created and closed", filename);
  }
//+------------------------------------------------------------------+
//| Return a symbol specification as JSON                            |
//+------------------------------------------------------------------+
string GetSymBolAsJson(string symbol)
  {
//--- indents
   string indent1=Indent(1);
   string indent2=Indent(2);
   string indent3=Indent(3);
//---
   int digits=(int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   string json="{"+
               "\n"+indent1+"\"ConfigSymbols\":["+
               "\n"+indent2+"{"+
               "\n"+indent3+"\"Symbol\":\""+symbol+"\","+
               "\n"+indent3+"\"Path\":\""+SymbolInfoString(symbol, SYMBOL_PATH)+"\","+
               "\n"+indent3+"\"CurrencyBase\":\""+SymbolInfoString(symbol, SYMBOL_CURRENCY_BASE)+"\","+
               "\n"+indent3+"\"CurrencyProfit\":\""+SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT)+"\","+
               "\n"+indent3+"\"CurrencyMargin\":\""+SymbolInfoString(symbol, SYMBOL_CURRENCY_MARGIN)+"\","+
               "\n"+indent3+"\"ColorBackground\":\""+ColorToString((color)SymbolInfoInteger(symbol, SYMBOL_BACKGROUND_COLOR))+"\","+
               "\n"+indent3+"\"Digits\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_DIGITS))+"\","+
               "\n"+indent3+"\"Point\":\""+DoubleToString(SymbolInfoDouble(symbol, SYMBOL_POINT), digits)+"\","+
               "\n"+indent3+"\"TickBookDepth\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TICKS_BOOKDEPTH))+"\","+
               "\n"+indent3+"\"ChartMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_CHART_MODE))+"\","+
               "\n"+indent3+"\"TradeMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_EXEMODE))+"\","+
               "\n"+indent3+"\"TradeCalcMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE))+"\","+
               "\n"+indent3+"\"OrderMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_ORDER_MODE))+"\","+
               "\n"+indent3+"\"CalculationMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE))+"\","+
               "\n"+indent3+"\"ExecutionMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_EXEMODE))+"\","+
               "\n"+indent3+"\"ExpirationMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_EXPIRATION_MODE))+"\","+
               "\n"+indent3+"\"FillFlags\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_FILLING_MODE))+"\","+
               "\n"+indent3+"\"ExpirFlags\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_EXPIRATION_MODE))+"\","+
               "\n"+indent3+"\"Spread\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SPREAD))+"\","+
               "\n"+indent3+"\"TickValue\":\""+StringFormat("%G", (SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)))+"\","+
               "\n"+indent3+"\"TickSize\":\""+StringFormat("%G", (SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)))+"\","+
               "\n"+indent3+"\"ContractSize\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE)))+"\","+
               "\n"+indent3+"\"StopsLevel\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL))+"\","+
               "\n"+indent3+"\"VolumeMin\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)))+"\","+
               "\n"+indent3+"\"VolumeMax\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)))+"\","+
               "\n"+indent3+"\"VolumeStep\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)))+"\","+
               "\n"+indent3+"\"VolumeLimit\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)))+"\","+
               "\n"+indent3+"\"SwapMode\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SWAP_MODE))+"\","+
               "\n"+indent3+"\"SwapLong\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_SWAP_LONG)))+"\","+
               "\n"+indent3+"\"SwapShort\":\""+StringFormat("%G",(SymbolInfoDouble(symbol, SYMBOL_SWAP_SHORT)))+"\","+
               "\n"+indent3+"\"Swap3Day\":\""+IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SWAP_ROLLOVER3DAYS))+"\""+
               "\n"+indent2+"}"+
               "\n"+indent1+"]"+
               "\n}";
   return(json);
  }
//+------------------------------------------------------------------+
//| Form an indent made of spaces                                    |
//+------------------------------------------------------------------+
string Indent(const int number, const int characters=3)
  {
   int length=number*characters;
   string indent=NULL;
   StringInit(indent, length, ' ');
   return indent;
  }
/*
 Result:
  Database: symbols.sqlite opened successfully
  #| cid name        type notnull dflt_value pk
  -+-------------------------------------------
  1|   0 NAME        TEXT       1             0 
  2|   1 DESCRIPTION TEXT       0             0 
  3|   2 PATH        TEXT       0             0 
  4|   3 SPREAD      INT        0             0 
  5|   4 POINT       REAL       1             0 
  6|   5 DIGITS      INT        1             0 
  7|   6 JSON        BLOB       0             0 
  1: added EURUSD
  2: added GBPUSD
  3: added USDCHF
  ...
  82: added USDCOP
  83: added USDARS
  84: added USDCLP
  Table SYMBOLS: added 84 symbols
  Database: table SYMBOLS saved in symbols.csv
  Database: symbols.sqlite created and closed
*/
 

```

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseBind](/en/docs/database/databasebind), [DatabaseBindArray](/en/docs/database/databasebindarray), [DatabaseFinalize](/en/docs/database/databasefinalize)
