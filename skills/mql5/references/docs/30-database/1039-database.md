# Working with databases

The functions for working with databases apply the popular and easy-to-use [SQLite](https://www.sqlite.org/index.html) engine. The convenient feature of this engine is that the entire database is located in a single file on a user PC's hard disk.

The functions allow for convenient creation of tables, adding data to them, performing modifications and sampling using simple SQL requests:

- receiving trading history and quotes from any formats,
- saving optimization and test results,
- preparing and exchanging data with other analysis packages,
- storing MQL5 application settings and status.

Queries allow using [statistical](/en/docs/database#math) and [mathematical](/en/docs/database#stats) functions.

The functions for working with databases allow you to replace the most repetitive large data array handling operations with SQL requests, so that it is often possible to use the [DatabaseExecute](/en/docs/database/databaseexecute)/[DatabasePrepare](/en/docs/database/databaseprepare) calls instead of programming complex loops and comparisons. Use the [DatabaseReadBind](/en/docs/database/databasereadbind) function to conveniently obtain query results in a ready-made structure. The function allows reading all record fields at once within a single call.

To accelerate reading, writing and modification, a database can be opened/created in RAM with the DATABASE_OPEN_MEMORY flag, although such a database is available only to a specific application and is not shared. When working with databases located on the hard disk, bulk data inserts/changes should be wrapped in transactions using [DatabaseTransactionBegin](/en/docs/database/databasetransactionbegin)/DatabaseTransactionCommit/DatabaseTransactionRollback. This accelerates the process hundreds of times.

To start working with the functions, read the article [SQLite: Native handling of SQL databases in MQL5](https://www.mql5.com/en/articles/7463).

| Function | Action |
| --- | --- |
| DatabaseOpen | Opens or creates a database in a specified file |
| DatabaseClose | Closes a database |
| DatabaseImport | Imports data from a file into a table |
| DatabaseExport | Exports a table or an SQL request execution result to a CSV file |
| DatabasePrint | Prints a table or an SQL request execution result in the Experts journal |
| DatabaseTableExists | Checks the presence of the table in a database |
| DatabaseExecute | Executes a request to a specified database |
| DatabasePrepare | Creates a handle of a request, which can then be executed using DatabaseRead() |
| DatabaseReset | Resets a request, like after calling  DatabasePrepare() |
| DatabaseBind | Sets a parameter value in a request |
| DatabaseBindArray | Sets an array as a parameter value |
| DatabaseRead | Moves to the next entry as a result of a request |
| DatabaseReadBind | Moves to the next record and reads data into the structure from it |
| DatabaseFinalize | Removes a request created in DatabasePrepare() |
| DatabaseTransactionBegin | Starts transaction execution |
| DatabaseTransactionCommit | Completes transaction execution |
| DatabaseTransactionRollback | Rolls back transactions |
| DatabaseColumnsCount | Gets the number of fields in a request |
| DatabaseColumnName | Gets a field name by index |
| DatabaseColumnType | Gets a field type by index |
| DatabaseColumnSize | Gets a field size in bytes |
| DatabaseColumnText | Gets a field value as a string from the current record |
| DatabaseColumnInteger | Gets the int type value from the current record |
| DatabaseColumnLong | Gets the long type value from the current record |
| DatabaseColumnDouble | Gets the double type value from the current record |
| DatabaseColumnBlob | Gets a field value as an array from the current record |

Statistical functions:

- mode – [mode](https://en.wikipedia.org/wiki/Mode_(statistics))
- median – [median](https://en.wikipedia.org/wiki/Median) (50th percentile)
- percentile_25 – 25th [percentile](https://en.wikipedia.org/wiki/Quantile)
- percentile_75
- percentile_90
- percentile_95
- percentile_99
- stddev or stddev_samp — sample standard deviation
- stddev_pop — population standard deviation
- variance or var_samp — sample variance
- var_pop — population variance

Mathematical functions

- [acos(X)](https://sqlite.org/lang_mathfunc.html#acos) – arccosine in radians
- [acosh(X)](https://sqlite.org/lang_mathfunc.html#acosh) – hyperbolic arccosine
- [asin(X)](https://sqlite.org/lang_mathfunc.html#asin) – arcsine in radians
- [asinh(X)](https://sqlite.org/lang_mathfunc.html#asinh) – hyperbolic arcsine
- [atan(X)](https://sqlite.org/lang_mathfunc.html#atan) – arctangent in radians
- [atan2(X,Y)](https://sqlite.org/lang_mathfunc.html#atan2) – arctangent in radians of the X/Y ratio
- [atanh(X)](https://sqlite.org/lang_mathfunc.html#atanh) – hyperbolic arctangent
- [ceil(X)](https://sqlite.org/lang_mathfunc.html#ceil) – rounding up to an integer
- [ceiling(X)](https://sqlite.org/lang_mathfunc.html#ceil) – rounding up to an integer
- [cos(X)](https://sqlite.org/lang_mathfunc.html#cos) – angle cosine in radians
- [cosh(X)](https://sqlite.org/lang_mathfunc.html#cosh) – hyperbolic cosine
- [degrees(X)](https://sqlite.org/lang_mathfunc.html#degrees) – convert radians into the angle
- [exp(X)](https://sqlite.org/lang_mathfunc.html#exp) – exponent
- [floor(X)](https://sqlite.org/lang_mathfunc.html#floor) – rounding down to an integer
- [ln(X)](https://sqlite.org/lang_mathfunc.html#ln) – natural logarithm
- [log(B,X)](https://sqlite.org/lang_mathfunc.html#log) – logarithm to the indicated base
- [log(X)](https://sqlite.org/lang_mathfunc.html#log) – decimal logarithm
- [log10(X)](https://sqlite.org/lang_mathfunc.html#log) – decimal logarithm
- [log2(X)](https://sqlite.org/lang_mathfunc.html#log2) – logarithm to base 2
- [mod(X,Y)](https://sqlite.org/lang_mathfunc.html#mod) – remainder of division
- [pi()](https://sqlite.org/lang_mathfunc.html#pi) – approximate Pi
- [pow(X,Y)](https://sqlite.org/lang_mathfunc.html#pow) – power by the indicated base
- [power(X,Y)](https://sqlite.org/lang_mathfunc.html#pow) – power by the indicated base
- [radians(X)](https://sqlite.org/lang_mathfunc.html#radians) – convert the angle into radians
- [sin(X)](https://sqlite.org/lang_mathfunc.html#sin) – angle sine in radians
- [sinh(X)](https://sqlite.org/lang_mathfunc.html#sinh) – hyperbolic sine
- [sqrt(X)](https://sqlite.org/lang_mathfunc.html#sqrt) – square root
- [tan(X)](https://sqlite.org/lang_mathfunc.html#tan) – angle tangent in radians
- [tanh(X)](https://sqlite.org/lang_mathfunc.html#tanh) – hyperbolic tangent
- [trunc(X)](https://sqlite.org/lang_mathfunc.html#trunc) – truncate to an integer closest to 0

Example:

```
select
  count(*) as book_count,
  cast(avg(parent) as integer) as mean,
  cast(median(parent) as integer) as median,
  mode(parent) as mode,
  percentile_90(parent) as p90,
  percentile_95(parent) as p95,
  percentile_99(parent) as p99
from moz_bookmarks;

```
