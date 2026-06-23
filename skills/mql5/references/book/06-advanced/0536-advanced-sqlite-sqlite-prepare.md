# Preparing bound queries: DatabasePrepare

In many cases, parameters need to be embedded in SQL queries. Since the SQL query is "originally" a string that corresponds to a special syntax, it can be formed by a simple StringFormat call or by concatenation, adding parameter values in the right places. We have already used this technique in queries to create a table ("CREATE TABLE %s '%s' (%s);"), but here only part of the parameters contained data (the list of values was substituted for %s inside parentheses), and the rest represented an option and a table name. In this section, we will focus exclusively on substituting data into a query. Doing this in a native SQL way is important for several reasons.

First of all, the SQL query is only passed to the SQLite engine as a string, and there it is parsed into components, checked for correctness, and "compiled" in a certain way (of course, this is not an MQL5 compiler). The compiled query is then executed by the database. That is why we put the word "originally" in quotation marks.

When the same query needs to be executed with different parameters (for example, inserting many records into a table; we are slowly approaching this task), separately compiling and checking the query for each record is rather inefficient. It is more correct to compile the query once, and then execute it in bulk, simply substituting different values.

This compilation operation is called query preparation and is performed by the DatabasePrepare function.

Prepared queries have one more purpose: with their help, the SQLite engine returns the results of query execution to the MQL5 code (you will find more on this in the sections [Executing prepared queries](/en/book/advanced/sqlite/sqlite_read) and [Separate reading of query result record fields](/en/book/advanced/sqlite/sqlite_columns)).

The last, but not least, moment associated with parameterized queries is that they protect your program from potential hacker attacks called SQL injection. First of all, this is critical for databases of public sites, where information entered by users is recorded in the database by embedding it in SQL queries: if in this case a simple format substitution '%s' is used, the user will be able to enter some long string instead of the expected data with additional SQL commands, and it will become part of the original SQL query, distorting its meaning. But if the SQL query is compiled, it cannot be changed by the input data: it is always treated as data.

Although the MQL program is not a server program, it can still store information received from the user in the database.

int DatabasePrepare(int database, const string sql, ...)

The DatabasePrepare function creates a handle in the specified database for the query in the string sql. The database must be opened beforehand by the [DatabaseOpen](/en/book/advanced/sqlite/sqlite_db_create_open_close) function.

The query parameter locations are specified in the sql string using fragments '?1', '?2', '?3', and so on. The numbering means the parameter index used in the future when assigning an input value to it, in [DatabaseBind](/en/book/advanced/sqlite/sqlite_bind)[ functions](/en/book/advanced/sqlite/sqlite_bind). Numbers in the sql string are not required to go in order and can be repeated if the same parameter needs to be inserted in different places in the query.

Attention! Indexing in substituted fragments '?n' starts from 1, while in DatabaseBind functions it starts from 0. For example, the '?1' parameter in the query body will get the value when calling DatabaseBind at index 0, parameter '?2' at index 1, and so on. This constant offset of 1 is maintained even if there are gaps (whether it was accidental or intentional) in the numbering of the '?n' parameters.

If you plan to bind all the parameters strictly in order, you can use an abbreviated notation: in place of each parameter, simply indicate the symbol '?' without a number: in this case, the parameters are automatically numbered. Any parameter '?' without a number gets the number which is by 1 larger than the maximum of the parameters read to the left (with explicit numbers or calculated according to the same principle, and the very first one will get the number 1, that is, '?1').

Thus, the request

```
SELECT * FROM table WHERE risk > ?1 AND signal = ?2

```

is equivalent to:

```
SELECT * FROM table WHERE risk > ? AND signal = ?

```

If some of the parameters are constant or the query is being prepared for one-time execution in order to get a result, the parameter values can be passed to the DatabasePrepare function as a comma-separated list instead of an ellipsis (same as in Print or Comment).

Query parameters can only be used to set values in table columns (when writing, changing, or filtering conditions). Names of tables, columns, options, and SQL keywords cannot be passed through '?'/'?n' parameters.

The DatabasePrepare function itself does not fulfill the query. The handle returned from it must then be passed to [DatabaseRead](/en/book/advanced/sqlite/sqlite_read) or [DatabaseReadBind](/en/book/advanced/sqlite/sqlite_read) function calls. These functions execute the query and make the result available for reading (it can be one record or many). Of course, if there are parameter placeholders ('?' or '?n') in the query, and the values for them were not specified in DatabasePrepare, before executing the query, you need to bind the parameters and data using the appropriate [DatabaseBind](/en/book/advanced/sqlite/sqlite_bind)[ functions](/en/book/advanced/sqlite/sqlite_bind).

If a value is not assigned to a parameter, NULL is substituted for it during query execution.

In case of an error, the DatabasePrepare function will return INVALID_HANDLE.

An example of using DatabasePrepare will be introduced in the following sections, after exploring other features related to prepared queries.
