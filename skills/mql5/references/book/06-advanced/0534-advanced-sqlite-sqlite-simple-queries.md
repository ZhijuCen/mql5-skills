# Executing queries without MQL5 data binding

Some SQL queries are commands that you just need to send to the engine as is. They require neither variable input nor results. For example, if our MQL program needs to create a table, index, or view with a certain structure and name in the database, we can write it as a constant string with the "CREATE ..." statement. In addition, it is convenient to use such queries for batch processing of records or their combination (merging, calculating aggregated indicators, and same-type modifications). That is, with one query, you can convert the entire table data or fill other tables based on it. These results can be analyzed in the subsequent queries.

In all these cases, it is only important to obtain confirmation of the success of the action. Requests of this type are performed using the DatabaseExecute function.

bool DatabaseExecute(int database, const string sql)

The function executes a query in the database specified by the database descriptor. The request itself is sent as a ready string sql.

The function returns an indicator of success (true) or error (false).

For example, we can complement our DBSQLite class with this method (the descriptor is already inside the object).

```
class DBSQLite
{
   ...
   bool execute(const string sql)
   {
      return DatabaseExecute(handle, sql);
   }
};

```

Then the script that creates a new table (and, if necessary, beforehand, the database itself) may look like this (DBcreateTable.mq5).

```
input string Database = "MQL5Book/DB/Example1";
input string Table = "table1";
   
void OnStart()
{
   DBSQLite db(Database);
   if(db.isOpen())
   {
      PRTF(db.execute(StringFormat("CREATE TABLE %s (msg text)", Table))); // true
   }
}

```

After executing the script, try to open the specified database in MetaEditor and make sure that it contains an empty table with a single "msg" text field. But it can also be done programmatically (see the [next section](/en/book/advanced/sqlite/sqlite_table_exists)).

If we run the script a second time with the same parameters, we will get an error (albeit a non-critical one, without forcing the program to close).

```
database error, table table1 already exists
db.execute(StringFormat(CREATE TABLE %s (msg text),Table))=false / DATABASE_ERROR(5601)

```

This is because you can't re-create an existing table. But SQL allows you to suppress this error and create a table only if it hasn't existed yet, otherwise do almost nothing and return a success indicator. To do this, just add "IF NOT EXISTS" in front of the name in the query.

```
   db.execute(StringFormat("CREATE TABLE IF NOT EXISTS %s (msg text)", Table));

```

In practice, tables are required to store information about objects in the application area, such as quotes, deals, and trading signals. Therefore, it is desirable to automate the creation of tables based on the description of objects in MQL5. As we will see below, SQLite functions provide the ability to bind query results to MQL5 structures (but not classes). In this regard, within the framework of the ORM wrapper, we will develop a mechanism for generating the SQL query "CREATE TABLE" according to the struct description of the specific type in MQL5.

This requires registering the names and types of structure fields in some way in the general list at the time of compilation, and then, already at the program execution stage, SQL queries can be generated from this list.

Several categories of MQL5 entities are parsed at the compilation stage, which can be used to identify types and names:

- [macros](/en/book/basis/preprocessor/preprocessor_define_functional)
- [inheritance](/en/book/oop/classes_and_interfaces/classes_inheritance)
- [templates](/en/book/oop/templates)

First of all, it should be recalled that the collected field descriptions are related to the context of a particular structure and should not be mixed, because the program may contain many different structures with potentially matching names and types. In other words, it is desirable to accumulate information in separate lists for each type of structure. A template type is ideal for this, the template parameter of which (S) will be the application structure. Let's call the template DBEntity.

```
template<typename S>
struct DBEntity
{
   static string prototype[][3]; // 0 - type, 1 - name, 2 - constraints
   ...
};
   
template<typename T>
static string DBEntity::prototype[][3];

```

Inside the template, there is a multidimensional array prototype, in which we will write the description of the fields. To intercept the type and name of the applied field, you will need to declare another template structure, DBField, inside DBEntity: this time its parameter T is the type of the field itself. In the constructor, we have information about this type (typename(T)), and we also get the name of the field (and optionally, the constraint) as parameters.

```
template<typename S>
struct DBEntity
{
   ...
   template<typename T>
   struct DBField
   {
      T f;
      DBField(const string name, const string constraints = "")
      {
         const int n = EXPAND(prototype);
         prototype[n][0] = typename(T);
         prototype[n][1] = name;
         prototype[n][2] = constraints;
      }
   };

```

The f field is not used but is needed because structures cannot be empty.

Let's say we have an application structure Data (DBmetaProgramming.mq5).

```
struct Data
{
   long id;
   string name;
   datetime timestamp;
   double income;
};

```

We can make its analog inherited from DBEntity<DataDB>, but with substituted fields based on DBField, identical to the original set.

```
struct DataDB: public DBEntity<DataDB>
{
   DB_FIELD(long, id);
   DB_FIELD(string, name);
   DB_FIELD(datetime, timestamp);
   DB_FIELD(double, income);
} proto;

```

By substituting the name of the structure into the parent template parameter, the structure provides the program with information about its own properties.

Pay attention to the one-time definition of the proto variable along with the structure declaration. This is necessary because, in templates, each specific parameterized type is compiled only if at least one object of this type is created in the source code. It is important for us that the creation of this proto-object occurs at the very beginning of the program launch, at the moment of initialization of global variables.

A macro is hidden under the DB_FIELD identifier:

```
#define DB_FIELD(T,N) struct T##_##N: DBField<T> { T##_##N() : DBField<T>(#N) { } } \
   _##T##_##N;

```

Here's how it expands for a single field:

```
   struct Type_Name: DBField<Type>
   {
      Type_Name() : DBField<Type>(Name) { }
   } _Type_Name;

```

Here the structure is not only defined but is also instantly created: in fact, it replaces the original field.

Since the DBField structure contains a single f variable of the desired type, dimensions and internal binary representation of Data and DataDB are identical. This can be easily verified by running the script DBmetaProgramming.mq5.

```
void OnStart()
{
   PRTF(sizeof(Data));
   PRTF(sizeof(DataDB));
   ArrayPrint(DataDB::prototype);
}

```

It outputs to the log:

```
DBEntity<Data>::DBField<long>::DBField<long>(const string,const string)
long id
DBEntity<Data>::DBField<string>::DBField<string>(const string,const string)
string name
DBEntity<Data>::DBField<datetime>::DBField<datetime>(const string,const string)
datetime timestamp
DBEntity<Data>::DBField<double>::DBField<double>(const string,const string)
double income
sizeof(Data)=36 / ok
sizeof(DataDB)=36 / ok
            [,0]        [,1]        [,2]
[0,] "long"      "id"        ""         
[1,] "string"    "name"      ""         
[2,] "datetime"  "timestamp" ""         
[3,] "double"    "income"    ""         

```

However, to access the fields, you would need to write something inconvenient: data._long_id.f, data._string_name.f, data._datetime_timestamp.f, data._double_income.f.

We will not do this, not only and not so much because of inconvenience, but because this way of constructing meta-structures is not compatible with the principles of data binding to SQL queries. In the following sections, we will explore database functions that allow you to get records of tables and results of SQL queries in MQL5 structures. However, it is allowed to use only simple structures without inheritance and static members of object types. Therefore, it is required to slightly change the principle of revealing meta-information.

We will have to leave the original types of structures unchanged and actually repeat the description for the database, making sure that there are no discrepancies (typos). This is not very convenient, but there is no other way at the moment.

We will transfer the declaration of instances DBEntity and DBField beyond application structures. In this case, the DB_FIELD macro will receive an additional parameter (S), in which it will be necessary to pass the type of the application structure (previously it was implicitly taken by declaring it inside the structure itself).

```
#define DB_FIELD(S,T,N) \
   struct S##_##T##_##N: DBEntity<S>::DBField<T> \
   { \
      S##_##T##_##N() : DBEntity<S>::DBField<T>(#N) {} \
   }; \
   const S##_##T##_##N _##S##_##T##_##N;

```

Since table columns can have constraints, they will also need to be passed to the DBField constructor if necessary. For this purpose, let's add a couple of macros with the appropriate parameters (in theory, one column can have several restrictions, but usually no more than two).

```
#define DB_FIELD_C1(S,T,N,C1) \
   struct S##_##T##_##N: DBEntity<S>::DBField<T> \
   {
      S##_##T##_##N() : DBEntity<S>::DBField<T>(#N, C1) {} \
   }; \
   const S##_##T##_##N _##S##_##T##_##N;
   
#define DB_FIELD_C2(S,T,N,C1,C2) \
   struct S##_##T##_##N: DBEntity<S>::DBField<T> \
   { \
      S##_##T##_##N() : DBEntity<S>::DBField<T>(#N, C1 + " " + C2) {} \
   }; \
   const S##_##T##_##N _##S##_##T##_##N;

```

All three macros, as well as further developments, are added to the header file DBSQLite.mqh.

It is important to note that this "self-made" binding of objects to a table is required only for entering data into the database because reading data from a table into an object is implemented in MQL5 using the [DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read) function.

Let's also improve the implementation of DBField. MQL5 types do not exactly correspond to SQL storage classes, and therefore it is necessary to perform a conversion when filling the prototype[n][0] element. This is done by the static method affinity.

```
   template<typename T>
   struct DBField
   {
      T f;
      DBField(const string name, const string constraints = "")
      {
         const int n = EXPAND(prototype);
         prototype[n][0] = affinity(typename(T));
         ...
      }
      
      static string affinity(const string type)
      {
         const static string ints[] =
         {
            "bool", "char", "short", "int", "long",
            "uchar", "ushort", "uint", "ulong", "datetime",
            "color", "enum"
         };
         for(int i = 0; i < ArraySize(ints); ++i)
         {
            if(type == ints[i]) return DB_TYPE::INTEGER;
         }
         
         if(type == "float" || type == "double") return DB_TYPE::REAL;
         if(type == "string") return DB_TYPE::TEXT;
         return DB_TYPE::BLOB;
      }
   };

```

The text constants of SQL generic types used here are placed in a separate namespace: they may be needed in different places in MQL programs at some point, and it is necessary to ensure that there are no name conflicts.

```
namespace DB_TYPE
{
   const string INTEGER = "INTEGER";
   const string REAL = "REAL";
   const string TEXT = "TEXT";
   const string BLOB = "BLOB";
   const string NONE = "NONE";
   const string _NULL = "NULL";
}

```

Presets of possible restrictions are also described in their group for convenience (as a hint).

```
namespace DB_CONSTRAINT
{
   const string PRIMARY_KEY = "PRIMARY KEY";
   const string UNIQUE = "UNIQUE";
   const string NOT_NULL = "NOT NULL";
   const string CHECK = "CHECK (%s)"; // requires an expression
   const string CURRENT_TIME = "CURRENT_TIME";
   const string CURRENT_DATE = "CURRENT_DATE";
   const string CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP";
   const string AUTOINCREMENT = "AUTOINCREMENT";
   const string DEFAULT = "DEFAULT (%s)"; // requires an expression (constants, functions)
}

```

Since some of the constraints require parameters (places for them are marked with the usual '%s' format modifier), let's add a check for their presence. Here is the final form of the DBField constructor.

```
   template<typename T>
   struct DBField
   {
      T f;
      DBField(const string name, const string constraints = "")
      {
         const int n = EXPAND(prototype);
         prototype[n][0] = affinity(typename(T));
         prototype[n][1] = name;
         if(StringLen(constraints) > 0       // avoiding error STRING_SMALL_LEN(5035)
            && StringFind(constraints, "%") >= 0)
         {
            Print("Constraint requires an expression (skipped): ", constraints);
         }
         else
         {
            prototype[n][2] = constraints;
         }
      }

```

Due to the fact that the combination of macros and auxiliary objects DBEntity<S> and DBField<T> populates an array of prototypes, inside the DBSQlite class, it becomes possible to implement the automatic generation of an SQL query to create a table of structures.

The createTable method is templated with an application structure type and contains a query stub ("CREATE TABLE %s %s (%s);"). The first argument for it is the optional instruction "IF NOT EXISTS". The second parameter is the name of the table, which by default is taken as the type of the template parameter typename(S), but it can be replaced with something else if necessary using the input parameter name (if it is not NULL). Finally, the third argument in brackets is the list of table columns: it is formed by the helper method columns based on the array DBEntity <S>::prototype.

```
class DBSQLite
{
   ...
   template<typename S>
   bool createTable(const string name = NULL,
      const bool not_exist = false, const string table_constraints = "") const
   {
      const static string query = "CREATE TABLE %s %s (%s);";
      const string fields = columns<S>(table_constraints);
      if(fields == NULL)
      {
         Print("Structure '", typename(S), "' with table fields is not initialized");
         SetUserError(4);
         return false;
      }
      // attempt to create an already existing table will give an error,
      // if not using IF NOT EXISTS
      const string sql = StringFormat(query,
         (not_exist ? "IF NOT EXISTS" : ""),
         StringLen(name) ? name : typename(S), fields);
      PRTF(sql);
      return DatabaseExecute(handle, sql);
   }
      
   template<typename S>
   string columns(const string table_constraints = "") const
   {
      static const string continuation = ",\n";
      string result = "";
      const int n = ArrayRange(DBEntity<S>::prototype, 0);
      if(!n) return NULL;
      for(int i = 0; i < n; ++i)
      {
         result += StringFormat("%s%s %s %s",
            i > 0 ? continuation : "",
            DBEntity<S>::prototype[i][1], DBEntity<S>::prototype[i][0],
            DBEntity<S>::prototype[i][2]);
      }
      if(StringLen(table_constraints))
      {
         result += continuation + table_constraints;
      }
      return result;
   }
};

```

For each column, the description consists of a name, a type, and an optional constraint. Additionally, it is possible to pass a general constraint on the table (table_constraints).

Before sending the generated SQL query to the DatabaseExecute function, the createTable method produces a debug output of the query text to the log (all such output in the ORM classes can be centrally disabled by replacing the PRTF macro).

Now everything is ready to write a test script DBcreateTableFromStruct.mq5, which, by structure declaration, would create the corresponding table in SQLite. In the input parameter, we set only the name of the database, and the program will choose the name of the table itself according to the type of structure.

```
#include <MQL5Book/DBSQLite.mqh>
   
input string Database = "MQL5Book/DB/Example1";
   
struct Struct
{
   long id;
   string name;
   double income;
   datetime time;
};
   
DB_FIELD_C1(Struct, long, id, DB_CONSTRAINT::PRIMARY_KEY);
DB_FIELD(Struct, string, name);
DB_FIELD(Struct, double, income);
DB_FIELD(Struct, string, time);

```

In the main OnStart function, we create a table by calling createTable with default settings. If we do not want to receive an error sign when we try to create it next time, we need to pass true as the first parameter (db.createTable<Struct> (true)).

```
void OnStart()
{
   DBSQLite db(Database);
   if(db.isOpen())
   {
      PRTF(db.createTable<Struct>());
      PRTF(db.hasTable(typename(Struct)));
   }
}

```

The hasTable method checks for the presence of a table in the database by the table name. We will consider the implementation of this method in the [next section](/en/book/advanced/sqlite/sqlite_table_exists). Now, let's run the script. After the first run, the table is successfully created and you can see the SQL query in the log (it is displayed with line breaks, as we formed it in the code).

```
sql=CREATE TABLE  Struct (id INTEGER PRIMARY KEY,
name TEXT ,
income REAL ,
time TEXT ); / ok
db.createTable<Struct>()=true / ok
db.hasTable(typename(Struct))=true / ok

```

The second run will return an error from the DatabaseExecute call, because this table already exists, which is additionally indicated by the hasTable result.

```
sql=CREATE TABLE  Struct (id INTEGER PRIMARY KEY,
name TEXT ,
income REAL ,
time TEXT ); / ok
database error, table Struct already exists
db.createTable<Struct>()=false / DATABASE_ERROR(5601)
db.hasTable(typename(Struct))=true / ok

```
