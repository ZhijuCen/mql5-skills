# SQL Basics

All tasks performed in SQLite assume the presence of a working database (one or more), so creating and opening a database (similar to a file) are mandatory framework operations that establish the necessary programming environment. There is no facility for programmatic deletion of the database in SQLite as it is assumed that you can simply delete the database file from disk.

The actions available in the context of an open base can be conditionally divided into the following main groups:

- Creating and deleting tables, as well as modifying their schemas, i.e., column descriptions, including the identification of types, names, and restrictions
- Creating (adding), reading, editing, and deleting records in tables; these operations are often denoted by the common abbreviation CRUD (Create, Read, Update, Delete)
- Building queries to select records from one or a combination of several tables according to complex conditions
- Optimizing algorithms by building indexes on selected columns, using views (view), wrapping batch actions in transactions, declaring event processing triggers, and other advanced tools

In SQL databases, all of these actions are performed using reserved SQL commands (or statements). Due to the specifics of integration with MQL5, some of the actions are performed by built-in MQL5 functions. For example, opening, applying, or canceling a transaction is performed by the trinity of [DatabaseTransaction](/en/book/advanced/sqlite/sqlite_transactions)[ functions](/en/book/advanced/sqlite/sqlite_transactions), although the SQL standard (and the public implementation of SQLite) has corresponding SQL commands (BEGIN TRANSACTION, COMMIT, and ROLLBACK).

Most SQL commands are also available in MQL programs: they are passed to the SQLite executing engine as string parameters of the [DatabaseExecute](/en/book/advanced/sqlite/sqlite_simple_queries) or [DatabasePrepare](/en/book/advanced/sqlite/sqlite_prepare) functions. The difference between these two options lies in several nuances.

DatabasePrepare allows you to prepare a query for its subsequent mass cyclic execution with different parameter values at each iteration (the parameters themselves, that is, their names in the query, are the same). In addition, these prepared queries provide a mechanism to read the results using [DatabaseRead](/en/book/advanced/sqlite/sqlite_read) and [DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read). So, you can use them for operations with a set of selected records.

In contrast, the DatabaseExecute function executes the passed single query unilaterally: the command goes inside the SQLite engine, performs some actions on the data, but returns nothing. This is commonly used for table creation or batch modification of data.

In the future, we will often have to operate with several basic concepts. Let's introduce them:

Table — a structured set of data, consisting of rows and columns. Each row is a separate data record with fields (properties) described using the name and type of the corresponding columns. All database tables are physically stored in the database file and are available for reading and writing (if rights were not restricted when opening the database).

View — a kind of virtual table calculated by the SQLite engine based on a given SQL query, other tables, or views. Views are read-only. Unlike any tables (including temporary ones that SQL allows you to create in memory for the duration of a program session), views are dynamically recalculated each time they are accessed.

Index — a service data structure (the balanced tree, B-tree) for quick search of records by the values of predefined fields (properties) or their combinations.

Trigger — a subroutine of one or more SQL statements assigned to be automatically run in response to events (before or after) adding, changing, or deleting a record in a particular table.

Here is a short list of the most popular SQL statements and the actions they perform:

- CREATE — creates a database object (table, view, index, trigger);
- ALTER — changes an object (table);
- DROP — deletes an object (table, view, index, trigger);
- SELECT — selects records or calculates values that satisfy the given conditions;
- INSERT — adds new data (one or a set of records);
- UPDATE — changes existing records;
- DELETE — deletes records from the table;

The list only shows the keywords that start the corresponding SQL language construct. A more detailed syntax will be shown below. Their practical application will be shown in the following examples.

Each statement can span multiple lines (linefeed characters and extra spaces are ignored). If necessary, you can send several commands to SQLite at once. In this case, after each command, you should use the command termination character ';' (semicolon).

The text in commands is analyzed by the system regardless of case, but in SQL it is customary to write keywords in capital letters.

When creating a table, we must specify its name, as well as a list of columns in parentheses, separated by commas. Each column is given a name, a type, and optionally a constraint. The simplest form:

```
CREATE TABLE table_name
  ( column_name type [ constraints ] [, column_name type [ constraints ...] ...]);

```

We will see the restrictions in SQL in the [next section](/en/book/advanced/sqlite/sqlite_scheme_types). In the meantime, let's have a look at a clear example (with different types and options):

```
CREATE TABLE IF NOT EXISTS example_table
   (id INTEGER PRIMARY KEY,
    name TEXT,
    timestamp INTEGER DEFAULT CURRENT_STAMP,
    income REAL,
    data BLOB);

```

The syntax for creating an index is:

```
CREATE [ UNIQUE ] INDEX index_name
  ON table_name( column_name [, column_name ...]);

```

Existing indexes are automatically used in queries with filter conditions on the corresponding columns. Without indexes, the process is slower.

Deleting a table (along with the data, if something has been written to it) is quite simple:

```
DROP TABLE table_name;

```

You can insert data into a table like this:

```
INSERT INTO table_name [ ( column_name [, column_name ...] ) ]
  VALUES( value [, value ...]);

```

The first list in parentheses includes the column names and is optional (see explanation below). It must match the second list with values for them. For example,

```
INSERT INTO example_table (name, income) VALUES ('Morning Flat Breakout', 1000);

```

Note that string literals are enclosed in single quotes in SQL.

If the column names are omitted from the INSERT statement, the VALUES keyword is assumed to be followed by the values for all the columns in the table, and in the exact order in which they are described in the table.

There are also more complex forms of the operator, allowing, in particular, the insertion of records from other tables or query results.

Selecting records by condition, with an optional limitation of the list of returned fields (columns), is performed by the SELECT command.

```
SELECT column_name [, column_name ...] FROM table_name [WHERE condition ];

```

If you want to return every matching record in its entirety (all columns), use the star notation:

```
SELECT *FROM table_name [WHERE condition ];

```

When the condition is not present, the system returns all records in the table.

As a condition, you can substitute a logical expression that includes column names and various comparison operators, as well as built-in SQL functions and the results of a nested SELECT query (such queries are written in parentheses). Comparison operators include:

- Logical AND
- Logical OR
- IN for a value from the list
- NOT IN  for a value outside the list
- BETWEEN  for a value in the range
- LIKE — similar in spelling to a pattern with special wildcard characters ('%', '_')
- EXISTS — check for non-emptiness of the results of the nested query

For example, a selection of record names with an income of at least 1000 and no older than one year (preliminarily rounded to the nearest month):

```
SELECT name FROM example_table
  WHERE income >= 1000 AND timestamp > datetime('now', 'start of month', '-1 year');

```

Additionally, the selection can be sorted in ascending or descending order (ORDER BY), grouped by characteristics (GROUP BY), and filtered by groups (HAVING). We can also limit the number of records in it (LIMIT, OFFSET). For each group, you can return the value of any aggregate function, in particular, COUNT, SUM, MIN, MAX, and AVG, calculated on all group records.

```
SELECT [ DISTINCT ] column_name [, column_name...](i) FROM table_name
  [ WHERE condition ]
  [ORDER BY column_name [ ASC | DESC ]
     [ LIMIT quantity OFFSET start_offset ] ]
  [ GROUP BY column_name ⌠ HAVING condition ] ];

```

The optional keyword DISTINCT allows you to remove duplicates (if they are found in the results according to the current selection criteria). It only makes sense in the absence of grouping.

LIMIT will only give reproducible results if sorting is present.

If necessary, the SELECT selection can be made not from one table but from several, combining them according to the required combination of fields. The keyword JOIN is used for this.

```
SELECT [...] FROM table name_1
  [ INNER | OUTER | CROSS ] JOIN table_name_2
  ON boolean_condition

```

or

```
SELECT [...] FROM table name_1
  [ INNER | OUTER | CROSS ] JOIN table_name_2
  USING ( common_column_name [, common_column_name ...] )

```

SQLite supports three kinds of JOINs: INNER JOIN, OUTER JOIN, and CROSS JOIN. The book provides a general idea of them from examples, while you can further explore the details on your own.

For example, using JOIN, you can build all combinations of records from one table with records from another table or compare deals from the deals table (let's call it "deals") with deals from the same table according to the principle of matching position identifiers, but in such a way that the direction of deals (entry to the market/exit from the market) was the opposite, resulting in a virtual table of trades.

```
SELECT // list the columns of the results table with aliases (after 'as')
  d1.time as time_in, d1.position_id as position, d1.type as type, // table d1
   d1.volume as volume, d1.symbol as symbol, d1.price as price_in,
  d2.time as time_out, d2.price as price_out,                      // table d2
   d2.swap as swap, d2.profit as profit,
  d1.commission + d2.commission as commission                      // combination
  FROM deals d1 INNER JOIN deals d2      // d1 and d2 - aliases of one table "deals"
  ON d1.position_id = d2.position_id     // merge condition by position
  WHERE d1.entry = 0 AND d2.entry = 1    // selection condition "entry/exit"

```

This is an SQL query from the MQL5 help, where JOIN examples are available in descriptions of the DatabaseExecute and DatabasePrepare functions.

The fundamental property of SELECT is that it always returns results to the calling program, unlike other queries such as CREATE, INSERT, etc. However, starting from SQLite 3.35, INSERT, UPDATE, and DELETE statements also have the ability to return values, if necessary, using the additional RETURNING keyword. For example,

```
INSERT INTO example_table (name, income) VALUES ('Morning Flat Breakout', 1000)
   RETURNING id;

```

In any case, query results in MQL5 are accessed through [DatabaseColumn](/en/book/advanced/sqlite/sqlite_columns)[ functions](/en/book/advanced/sqlite/sqlite_columns), [DatabaseRead](/en/book/advanced/sqlite/sqlite_read), and [DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read).

In addition, SELECT allows you to evaluate the results of expressions and return them as they are or combine them with results from tables. Expressions can include most of the operators we are familiar with from [MQL5 expressions](/en/book/basis/expressions), as well as built-in SQL functions. See the SQLite documentation for a complete list. For example, here's how you can find the current build version of SQLite in your terminal and editor instance, which can be important for finding out which options are available.

```
SELECT sqlite_version();

```

Here the entire expression consists of a single call of the sqlite_version function. Similar to selecting multiple columns from a table, you can evaluate multiple expressions separated by commas.

Several popular [statistical](https://www.mql5.com/en/docs/database#stats) and [mathematical](https://www.mql5.com/en/docs/database#math) functions are also available.

Records should be edited with an UPDATE statement.

```
UPDATE table_name SET column_name = value [, column_name = value ...] 
  WHERE condition;

```

The syntax for the deletion command is as follows:

```
DELETE FROM table_name WHERE condition;

```
