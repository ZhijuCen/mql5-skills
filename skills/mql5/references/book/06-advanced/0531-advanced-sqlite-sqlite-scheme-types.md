# Structure of tables: data types and restrictions

When describing table fields, you need to specify data types for them, but the concept of a data type in SQLite is very different from MQL5.

MQL5 is a strongly typed language: each variable or structure field always retains the data type according to the declaration. SQL, on the other hand, is a loosely typed language: the types that we specify in the table description are nothing more than a recommendation. The program can write a value of an arbitrary type to any "cell" (a field in the record), and the "cell" will change its type, which, in particular, can be detected by the built-in MQL function [DatabaseColumnType](/en/book/advanced/sqlite/sqlite_columns).

Of course, in practice, most users tend to stick to "respect" column types.

The second significant difference in the SQL type mechanism is the presence of a large number of keywords that describe types, but all these words ultimately come down to five storage classes. Being a simplified version of SQL, SQLite in most cases does not distinguish between keywords of the same group (for example, in the description of a string with a VARCHAR(80) length limit, this limit is not controlled, and the description is equivalent to the TEXT storage class), so it is more logical to describe the type by the group name. Specific types are left only for compatibility with other DBMS (but this is not important for us).

The following table lists the MQL5 types and their corresponding "affinities" (which mean generalizing features of SQL types).

| MQL5 types | Generic SQL types |
| --- | --- |
| NULL (not a type in MQL5) | NULL (no value) |
| bool, char, short, int, long, uchar, ushort, 
 uint, ulong, datetime, color, enum | INTEGER |
| float, double | REAL |
| (real number of fixed precision,  
 no analog in MQL5) | NUMERIC |
| string | TEXT |
| (arbitrary "raw" data,  
 analog of uchar[] array or others) | BLOB (binary large object), NONE |

When writing a value to the SQL database, it determines its type according to several rules:

- The absence of quotes, decimal point, or exponent give INTEGER
- The presence of a decimal point and an exponent means REAL
- framing of single or double quotes signals the TEXT type
- a NULL value without quotes corresponds to the NULL class
- literals (constants) with binary data are written as a hexadecimal string prefixed with 'x'

Special SQL function typeof allows you to check the type of a value. For example, the following query can be run in the MetaEditor.

```
SELECT typeof(100), typeof(10.0), typeof('100'), typeof(x'1000'), typeof(NULL);

```

It will output to the results table:

```
integer        |        real        |        text        |        blob        |        null

```

You cannot check values for NULL by comparing '=' (because the result will also give NULL), you should use the special NOT NULL operator.

SQLite imposes some limits on stored data: some of them are difficult to achieve (and therefore we will omit them here), but others can be taken into account when designing a program. So, the maximum number of columns in the table is 2000, and the size of one row, BLOB, and in general one record cannot exceed one million bytes. The same value is chosen as the SQL query length limit.

As far as dates and times are concerned, SQL can in theory store them in three formats, but only the first one matches datetime in MQL5:

- INTEGER — the number of seconds since 1970.01.01 (also known as the "Unix epoch")
- REAL — the number of days (with fractions) from November 24, 4714 BC
- TEXT — date and time with accuracy to the millisecond in the format "YYYY-MM-DD HH:mm:SS.sss", optionally with the time zone, for which the suffix "[±]HH:mm" is added with an offset from UTC

A real date storage type (also called the Julian day, for which there is a built-in SQL function Julianday) is interesting in that it allows you to store time accurate to milliseconds. In theory, this can also be done as a 'YYYY-MM-DDTHH:mm:SS.sssZ' format string, but such storage is very uneconomical. The conversion of the "day" into the number of seconds with a fractional part, starting from the familiar date 1970.01.01 00:00:00, is made according to the formula: julianday('now') - 2440587.5) * 86400.0. 'Now' here denotes the current UTC time but can be changed to other values described in the SQLite documentation. The constant 2440587.5 is exactly equal to the number of "calendar" days for the specified "zero" date — the starting point of the "Unix epoch".

In addition to the type, each field can have one or more constraints, which are written with special keywords after the type. A constraint describes what values the field can take and even allows you to automate the completion according to the field's predefined purpose.

Let's consider the main constraints.

```
... DEFAULT expression

```

When adding a new record, if the field value is not specified, the system will automatically enter the value (constant) specified here or calculate the expression (function).

```
... CHECK ( boolean_expression )

```

When adding a new record, the system will check that the expression, which can contain field names as variables, is true. If the expression is false, the record will not be inserted and the system will return an error.

```
... UNIQUE

```

The system checks that all records in the table have different values for this field. Attempting to add an entry with a value that already exists will result in an error and the addition will not occur.

To track uniqueness, the system implicitly creates an index for the specified field.

```
... PRIMARY KEY

```

A field marked with this attribute is used by the system to identify records in a table and links to them from other tables (this is how relational relationships are formed, giving the name to relational databases in question like SQLite). Obviously, this feature also includes a unique index.

If the table does not have an INTEGER type field with the PRIMARY KEY attribute, the system automatically implicitly creates such a column named rowid. If your table has an integer field declared as a primary key, then it is also available under the alias rowid.

If a record with an omitted or NULL rowid is added to the table, SQLite will automatically assign it the next integer (64-bit, corresponding to long in MQL5), larger than the maximum rowid in the table by 1. The initial value is 1.

Usually the counter just increments by 1 each time, but if the number of records ever inserted into one table (and possibly then deleted) exceeds long, the counter will jump to the beginning and the system will try to find free numbers. But this is unlikely. For example, if you write ticks to a table at an average rate of 1 tick per millisecond, then the overflow will occur in 292 million years.

There can be only one primary key, but it can consist of several columns, which is done using a syntax other than constraints directly in the table description.

```
CREATE TABLE table_name (
  column_name type [ restrictions ]
  [, column_name type [ restrictions ] ...]
  , PRIMARY KEY ( column_name [, column_name ...] ) );

```

Let's get back to constraints.

```
... AUTOINCREMENT

```

This constraint can only be specified as a complement to the PRIMARY KEY, ensuring that identifiers are incremented all the time. This means that any previous IDs, even those used on deleted entries, will not be reselected. However, this mechanism is implemented in SQLite less efficiently than a simple PRIMARY KEY in terms of computing resources and therefore is not recommended for use.

```
... NOT NULL

```

This constraint prohibits adding a record to the table in which this field is not filled. By default, when there is no constraint, any non-unique field can be omitted from the added record and will be set to NULL.

```
... CURRENT_TIME
... CURRENT_DATE
... CURRENT_TIMESTAMP

```

These instructions allow you to automatically populate a field with the time (no date), date (no time), or full UTC time at the time the record was inserted (provided that the INSERT SQL statement does not explicitly write anything to this field, even NULL). SQLite does not know how to automatically detect the time of a record change in a similar way — for this purpose you will have to write a trigger (which is beyond the scope of the book).

Unfortunately, the CURRENT_TIMESTAMP group restrictions are implemented in SQLite with an omission: the timestamp is not applied if the field is NULL. This distinguishes SQLite from other SQL engines and from how SQLite itself handles NULLs in primary key fields. It turns out that for automatic labeling, you cannot write the entire object to the database, but you need to explicitly specify all the fields except for the field with the date and time. To solve the problem, we need an alternative option in which the SQL function STRFTIME('%s') is substituted in the compiled query for the corresponding columns.
