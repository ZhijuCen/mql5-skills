# DatabaseReadBind

Moves to the next record and reads data into the structure from it.

```
bool  DatabaseReadBind(
   int    request,           // the handle of a request created in DatabasePrepare
   void&  struct_object      // the reference to the structure for reading the record 
   );

```

Parameters

request

[in]  The handle of a request created in [DatabasePrepare()](/en/docs/database/databaseprepare).

struct_object

[out]  The reference to the structure the data from the current record is to be read to. The structure should only have numerical types and/or strings (arrays are not allowed) as members and cannot be a descendant.

Return Value

Return true if successful, otherwise false. To get the error code, use GetLastError(), the possible responses are:

- ERR_INVALID_PARAMETER (4003)               –  no table name specified (empty string or NULL);
- ERR_WRONG_STRING_PARAMETER (5040)  – error converting a request into a UTF-8 string;
- ERR_DATABASE_INTERNAL (5120)              – internal database error;
- ERR_DATABASE_INVALID_HANDLE (5121)    – invalid database handle;
- ERR_DATABASE_EXECUTE (5124)                –  request execution error;
- ERR_DATABASE_NO_MORE_DATA (5126)    – no table exists (not an error, normal completion).

Note

A number of fields in the struct_object structure should not exceed [DatabaseColumnsCount()](/en/docs/database/databasecolumnscount). If the number of fields in the struct_object structure is less than the number of fields in the record, the partial reading is performed. The remaining data can be explicitly obtained using the corresponding [DatabaseColumnText()](/en/docs/database/databasecolumntext), [DatabaseColumnInteger()](/en/docs/database/databasecolumninteger) and other functions.

Example:

```
struct Person
  {
   int               id;
   string            name;
   int               age;
   string            address;
   double            salary;
  };
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
   int db;
   string filename="company.sqlite";
//--- open
   db=DatabaseOpen(filename, DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE |DATABASE_OPEN_COMMON);
   if(db==INVALID_HANDLE)
     {
      Print("DB: ", filename, " open failed with code ", GetLastError());
      return;
     }
//--- if the table COMPANY exists then drop the table
   if(DatabaseTableExists(db, "COMPANY"))
     {
      //--- delete the table
      if(!DatabaseExecute(db, "DROP TABLE COMPANY"))
        {
         Print("Failed to drop table COMPANY with code ", GetLastError());
         DatabaseClose(db);
         return;
        }
     }
//--- create table
   if(!DatabaseExecute(db, "CREATE TABLE COMPANY("
                       "ID INT PRIMARY KEY     NOT NULL,"
                       "NAME           TEXT    NOT NULL,"
                       "AGE            INT     NOT NULL,"
                       "ADDRESS        CHAR(50),"
                       "SALARY         REAL );"))
     {
      Print("DB: ", filename, " create table failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
 
//--- insert data
   if(!DatabaseExecute(db, "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 25000.00 ); "
                       "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 ); "
                       "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 );"
                       "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 );"))
     {
      Print("DB: ", filename, " insert failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
 
//--- prepare the request
   int request=DatabasePrepare(db, "SELECT * FROM COMPANY WHERE SALARY>15000");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
//--- print records
   Person person;
   Print("Persons with salary > 15000:");
   for(int i=0; DatabaseReadBind(request, person); i++)
      Print(i, ":  ", person.id, " ", person.name, " ", person.age, " ", person.address, " ", person.salary);
//--- delete request after use
   DatabaseFinalize(request);
 
   Print("Some statistics:");
//--- prepare new request about total salary
   request=DatabasePrepare(db, "SELECT SUM(SALARY) FROM COMPANY");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      DatabaseClose(db);
      return;
     }
   while(DatabaseRead(request))
     {
      double total_salary;
      DatabaseColumnDouble(request, 0, total_salary);
      Print("Total salary=", total_salary);
     }
//--- delete request after use
   DatabaseFinalize(request);
 
//--- prepare new request about average salary
   request=DatabasePrepare(db, "SELECT AVG(SALARY) FROM COMPANY");
   if(request==INVALID_HANDLE)
     {
      Print("DB: ", filename, " request failed with code ", GetLastError());
      ResetLastError();
      DatabaseClose(db);
      return;
     }
   while(DatabaseRead(request))
     {
      double aver_salary;
      DatabaseColumnDouble(request, 0, aver_salary);
      Print("Average salary=", aver_salary);
     }
//--- delete request after use
   DatabaseFinalize(request);
 
//--- close database
   DatabaseClose(db);
  }
//+-------------------------------------------------------------------
/*
Output:
Persons with salary > 15000:
0:  1 Paul 32 California 25000.0
1:  3 Teddy 23 Norway 20000.0
2:  4 Mark 25 Rich-Mond  65000.0
Some statistics:
Total salary=125000.0
Average salary=31250.0
*/

```

See also

[DatabasePrepare](/en/docs/database/databaseprepare), [DatabaseRead](/en/docs/database/databaseread)
