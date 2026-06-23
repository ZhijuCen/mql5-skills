# Principles of database operations in MQL5

Databases store information in the form of tables. Getting, modifying, and adding new data to them is done using queries in the SQL language. We will describe its specifics in the following sections. In the meantime, let's use the DatabaseRead.mq5 script, which has nothing to do with trading, and see how to create a simple database and get information from it. All functions mentioned here will be described in detail later. Now it is important to imagine the general principles.

Creating and closing a database using built-in [DatabaseOpen/DatabaseClose](/en/book/advanced/sqlite/sqlite_db_create_open_close) functions are similar to working with files as we also create a descriptor for the database, check it, and close it at the end.

```
void OnStart()
{
   string filename = "company.sqlite";
   // create or open a database
   int db = DatabaseOpen(filename, DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE);
   if(db == INVALID_HANDLE)
   {
      Print("DB: ", filename, " open failed with code ", _LastError);
      return;
   }
   ...// further work with the database
   // close the database
   DatabaseClose(db);
}

```

After opening the database, we will make sure that there is no table in it under the name we need. If the table already exists, then when trying to insert the same data into it as in our example, an error will occur, so we use the [DatabaseTableExists](/en/book/advanced/sqlite/sqlite_table_exists) function.

Deleting and creating a table is done using queries that are sent to the database with two calls to the [DatabaseExecute](/en/book/advanced/sqlite/sqlite_simple_queries) function and accompanied by error checking.

```
   ...
   // if the table COMPANY exists, then delete it
   if(DatabaseTableExists(db, "COMPANY"))
   {
      if(!DatabaseExecute(db, "DROP TABLE COMPANY"))
      {
         Print("Failed to drop table COMPANY with code ", _LastError);
         DatabaseClose(db);
         return;
      }
   }
   // creating table COMPANY 
   if(!DatabaseExecute(db, "CREATE TABLE COMPANY("
     "ID      INT     PRIMARY KEY NOT NULL,"
     "NAME    TEXT    NOT NULL,"
     "AGE     INT     NOT NULL,"
     "ADDRESS CHAR(50),"
     "SALARY  REAL );"))
   {
      Print("DB: ", filename, " create table failed with code ", _LastError);
      DatabaseClose(db);
      return;
   }
   ...

```

Let's explain the essence of SQL queries. In the COMPANY table, we have only 5 fields: record ID, name, age, address, and salary. Here the ID field is a key, that is, a unique index. Indexes allow each record to be uniquely identified and can be used across tables to link them together. This is similar to how the position ID links all trades and orders that belong to a particular position.

Now you need to fill the table with data, this is done using the "INSERT" query:

```
   // insert data into table
   if(!DatabaseExecute(db,
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1,'Paul',32,'California',25000.00); "
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2,'Allen',25,'Texas',15000.00); "
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3,'Teddy',23,'Norway',20000.00);"
      "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4,'Mark',25,'Rich-Mond',65000.00);"))
   {
      Print("DB: ", filename, " insert failed with code ", _LastError);
      DatabaseClose(db);
      return;
   }
   ...

```

Here, 4 records are added to the table COMPANY, for each record there is a list of fields, and values that will be written to these fields are indicated. Records are inserted by separate "INSERT..." queries, which are combined into one line, through a special delimiter character ';', but we could insert each record into the table with a separate DatabaseExecute call.

Since at the end of the script the database will be saved to the "company.sqlite" file, the next time it is run, we would try to write the same data to the COMPANY table with the same ID. This would lead to an error, which is why we previously deleted the table so that we would start from scratch every time the script was run.

Now we get all records from the COMPANY table with the field SALARY > 15000. This is done using the [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare) function, which "compiles" the request text and returns its handle for later use in the [DatabaseRead](/en/book/advanced/sqlite/sqlite_read) or [DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read) functions.

```
   // prepare a request with a descriptor
   int request = DatabasePrepare(db, "SELECT * FROM COMPANY WHERE SALARY>15000");
   if(request == INVALID_HANDLE)
   {
      Print("DB: ", filename, " request failed with code ", _LastError);
      DatabaseClose(db);
      return;
   }
   ...

```

After the request has been successfully created, we need to get the results of its execution. This can be done using the DatabaseRead function, which on the first call will execute the query and jump to the first record in the results. On each subsequent call, it will read the next record until it reaches the end. In this case, it will return false, which means "there are no more records".

```
   // printing all records with salary over 15000
   int id, age;
   string name, address;
   double salary;
   Print("Persons with salary > 15000:");
   for(int i = 0; DatabaseRead(request); i++)
   {
      // read the values of each field from the received record by its number
      if(DatabaseColumnInteger(request, 0, id) && DatabaseColumnText(request, 1, name) &&
         DatabaseColumnInteger(request, 2, age) && DatabaseColumnText(request, 3, address) &&
         DatabaseColumnDouble(request, 4, salary))
         Print(i, ":  ", id, " ", name, " ", age, " ", address, " ", salary);
      else
      {
         Print(i, ": DatabaseRead() failed with code ", _LastError);
         DatabaseFinalize(request);
         DatabaseClose(db);
         return;
      }
   }
   // deleting handle after use
   DatabaseFinalize(request);

```

The result of execution will be:

```
Persons with salary > 15000:
0:  1 Paul 32 California 25000.0
1:  3 Teddy 23 Norway 20000.0
2:  4 Mark 25 Rich-Mond  65000.0

```

The DatabaseRead function allows you to go through all the records from the query result and then get complete information about each column in the resulting table via DatabaseColumn functions. These functions are designed to work universally with the results of any query but the cost is a redundant code.

If the structure of the query results is known in advance, it is better to use the DatabaseReadBind function, which allows you to read the entire record at once into a structure. We can remake the previous example in this way and present it under a new name DatabaseReadBind.mq5. Let's first declare the Person structure:

```
struct Person
{
   int    id;
   string name;
   int    age;
   string address;
   double salary;
};

```

Then we will subtract each record from the query results with DatabaseReadBind(request, person) in a loop as long as the function returns true:

```
   Person person;
   Print("Persons with salary > 15000:");
   for(int i = 0; DatabaseReadBind(request, person); i++)
      Print(i, ":  ", person.id, " ", person.name, " ", person.age,
         " ", person.address, " ", person.salary);
   DatabaseFinalize(request);

```

Thus, we immediately get the values of all fields from the current record and we do not need to read them separately.

This introductory example was taken from the article [SQLite: native work with SQL databases in MQL5](https://www.mql5.com/en/articles/7463), where, in addition to it, several options for the application of the database for traders are considered. Specifically, you can find there restoring the history of positions from trades, analyzing a trading report in terms of strategies, working symbols, or the most preferred trading hours, as well as techniques for working with optimization results.

Some basic knowledge of SQL may be required to master this material, so we will cover it briefly in the following sections.
