# Transactions

SQLite supports transactions — logically related sets of actions that can be performed either entirely or not performed at all, which ensures the consistency of data in the database.

The concept of a transaction has a new meaning in the context of databases, different from what we used to describe in [trade transactions](/en/book/automation/experts/experts_transaction_type). A trade transaction means a separate operation on the entities of a trading account, including orders, deals, and positions.

Transactions provide 4 main characteristics of database changes:

- Atomic (indivisible) — upon successful completion of the transaction, all the changes included in it will get into the database, and in case of an error, nothing will get into it.
- Consistent — the current correct state of the base can only change to another correct state (intermediate, according to application logic, states are excluded).
- Isolated — changes in the transaction of the current connection are not visible until the end of this transaction in other connections to the same database and vice versa, changes from other connections are not visible in the current connection while there is an incomplete transaction.
- Durable — changes from a successful transaction are guaranteed to be stored in the database.

The terms for these characteristics — Atomic, Consistent, Isolated, and Durable — form the acronym ACID, well-known in database theory.

Even if the normal course of the program is interrupted due to a system failure, the database will retain its working state.

Most often, the use of transactions is illustrated by the example of a banking system, in which funds are transferred from the account of one client to the account of another. It should affect two records with customer balances: in one, the balance is reduced by the amount of the transfer, and in the other, it is increased. A situation where only one of these changes applies would upset the balance of bank accounts: depending on which operation failed, the transferred amount could disappear or, conversely, come from nowhere.

It is possible to give an example that is closer to trading practice but on the basis of the "opposite" principle. The fact is that the system for accounting for orders, deals, and positions in MetaTrader 5 is not transactional.

In particular, as we know from the chapter on [Creating Expert Advisors](/en/book/automation/experts), a triggered order (market or pending), missing from the list of active ones, may not immediately be displayed in the list of positions. Therefore, in order to analyze the actual result, it is necessary to implement in the MQL program the expectation of updating (actualization) the trading environment. If the accounting system was based on transactions, then the execution of an order, the registration of a transaction in history, and the appearance of a position would be enclosed in a transaction and coordinated with each other. The terminal developers have chosen a different approach: to return any modifications of the trading environment as quickly and asynchronously as possible, and their integrity must be monitored by an MQL program.

Any SQL command that changes the base (that is, in fact, everything except SELECT) will automatically be wrapped in a transaction if this was not done explicitly beforehand.

The MQL5 API provides 3 functions for managing transactions: DatabaseTransactionBegin, DatabaseTransactionCommit, and DatabaseTransactionRollback. All functions return true if successful or false in case of an error.

bool DatabaseTransactionBegin(int database)

The DatabaseTransactionBegin function starts executing a transaction in the database with the specified descriptor obtained from [DatabaseOpen](/en/book/advanced/sqlite/sqlite_db_create_open_close).

All subsequent changes made to the database are accumulated in the internal transaction cache and do not get into the database until the DatabaseTransactionCommit function is called.

Transactions in MQL5 cannot be nested: if a transaction has already been started, then re-calling DatabaseTransactionBegin will return an error flag and output a message to the log.

```
database error, cannot start a transaction within a transaction
DatabaseTransactionBegin(db)=false / DATABASE_ERROR(5601)

```

Respectively, you cannot try and complete the transaction multiple times.

bool DatabaseTransactionCommit(int database)

The function DatabaseTransactionCommit ends a transaction previously started in the database with the specified handle and applies all accumulated changes (saves them). If an MQL program starts a transaction but does not apply it before closing the database, all changes will be lost.

If necessary, the program can undo the transaction, and thus all changes since the beginning of the transaction.

bool DatabaseTransactionRollback(int database)

The DatabaseTransactionRollback function performs a "rollback" of all actions included in the previously started transaction for the database with the database handle.

Let's complete the DBSQLite class methods for working with transactions, taking into account the restriction on their nesting, which we will calculate in the transaction variable. If it is 0, the begin method starts a transaction by calling DatabaseTransactionBegin. All subsequent attempts to start a transaction simply increase the counter. In the commit method, we decrement the counter, and when it reaches 0 we call DatabaseTransactionCommit.

```
class DBSQLite
{
protected:
   int transaction;
   ...
public:
   bool begin()
   {
      if(transaction > 0)   // already in transaction
      {
         transaction++;     // keep track of the nesting level
         return true; 
      }
      return (bool)(transaction = PRTF(DatabaseTransactionBegin(handle)));
   }
   
   bool commit()
   {
      if(transaction > 0)
      {
         if(--transaction == 0) // outermost transaction
            return PRTF(DatabaseTransactionCommit(handle));
      }
      return false;
   }
   bool rollback()
   {
      if(transaction > 0)
      {
         if(--transaction == 0)
            return PRTF(DatabaseTransactionRollback(handle));
      }
      return false;
   }
};

```

Also, let's create the DBTransaction class, which will allow describing objects inside blocks (for example, functions) that ensure the automatic start of a transaction with its subsequent application (or cancellation) when the program exits the block.

```
class DBTransaction
{
   DBSQLite *db;
   const bool autocommit;
public:
   DBTransaction(DBSQLite &owner, const bool c = false): db(&owner), autocommit(c)
   {
      if(CheckPointer(db) != POINTER_INVALID)
      {
         db.begin();
      }
   }
   
   ~DBTransaction()
   {
      if(CheckPointer(db) != POINTER_INVALID)
      {
         autocommit ? db.commit() : db.rollback();
      }
   }
   
   bool commit()
   {
      if(CheckPointer(db) != POINTER_INVALID)
      {
         const bool done = db.commit();
         db = NULL;
         return done;
      }
      return false;
   }
};

```

The policy of using such objects eliminates the need to process various options for exiting a block (function).

```
void DataFunction(DBSQLite &db)
{
   DBTransaction tr(db);
   DBQuery *query = db.prepare("UPDATE..."); // batch changes
   ... // base modification
   if(... /* error1 */) return;             // automatic rollback
   ... // base modification
   if(... /* error2 */) return;             // automatic rollback
   tr.commit();
}

```

For an object to automatically apply changes at any stage, pass true in the second parameter of its constructor.

```
void DataFunction(DBSQLite &db)
{
   DBTransaction tr(db, true);
   DBQuery *query = db.prepare("UPDATE...");  // batch changes
   ... // base modification
   if(... /* condition1 */) return;           // automatic commit
   ... // base modification
   if(... /* condition2 */) return;           // automatic commit
   ...
}                                             // automatic commit

```

You can describe the DBTransaction object inside the loop and then, at each iteration, a separate transaction will start and close.

A demonstration of transactions will be given in the section [An example of searching for a trading strategy using SQLite](/en/book/advanced/sqlite/sqlite_example_ts).
